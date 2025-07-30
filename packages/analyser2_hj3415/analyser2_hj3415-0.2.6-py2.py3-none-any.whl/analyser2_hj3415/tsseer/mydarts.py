from typing import Literal
from darts import TimeSeries
from darts.dataprocessing.transformers import Scaler
from sklearn.preprocessing import StandardScaler
from darts.dataprocessing.transformers import MissingValuesFiller
import pandas as pd

from .utils import get_raw_data, timeseries_to_dataframe, redis_cached, judge_trend
from utils_hj3415 import setup_logger

mylogger = setup_logger(__name__,'INFO')


def prepare_data(df: pd.DataFrame) -> dict[str, TimeSeries | Scaler]:
    """
    주가-데이터 `DataFrame`을 **Darts** 시계열 객체로 전처리-패키징하는 함수
    -----------------------------------------------------------------------

    이 함수는 종가·거래량이 포함된 원본 `DataFrame`을 받아 다음 과정을 수행합니다.

    1. **컬럼 정리**
       - 다중 컬럼(OHLCV 등)이 있을 때 첫 번째 레벨만 유지합니다.
       - `Close`, `Volume` 두 컬럼만 남기고 결측 행을 제거합니다.

    2. **인덱스 정리**
       - 타임존 정보를 제거(`tz_localize(None)`)한 뒤,
         `DatetimeIndex`의 이름을 `"time"`으로 지정합니다.
       - 영업일 빈도(`'B'`)를 기준으로 빠진 날짜는 `fill_missing_dates=True` 옵션으로 자동 보간합니다.

    3. **`TimeSeries` 변환**
       - `target_series` : 종가(`Close`)를 단일 변수로 갖는 시계열
       - `volume_series` : 거래량(`Volume`)을 단일 변수로 갖는 시계열

    4. **결측값 보간**
       - 휴장일 등으로 인해 생긴 `NaN`은 **직전 값**으로 채웁니다.
         (`MissingValuesFiller().transform`)

    5. **스케일링 (0 ~ 1)**
       - `StandardScaler`를 래핑한 Darts `Scaler`를 사용해
         `target_series`와 `volume_series` 각각을 개별로 정규화합니다.
       - 변환 결과는 `target_scaled`, `volume_scaled`에 저장되며
         나중에 역-스케일링을 위해 `target_scaler`, `volume_scaler`도 함께 반환합니다.

    6. **디버그 로그**
       - 스케일된 시계열을 `mylogger.debug()`로 출력하여
         정상 변환 여부를 확인할 수 있습니다.

    반환값
    -------
    dict[str, TimeSeries | Scaler]
        - `'target_series'` : 원본 종가 시계열
        - `'volume_series'` : 원본 거래량 시계열
        - `'target_scaled'` : 정규화된 종가 시계열
        - `'volume_scaled'` : 정규화된 거래량 시계열
        - `'target_scaler'` : 종가 역-스케일링용 `Scaler` 객체
        - `'volume_scaler'` : 거래량 역-스케일링용 `Scaler` 객체
    """
    df.columns = df.columns.get_level_values(0)
    df.columns.name = None
    df = df[['Close', 'Volume']].dropna()
    df.index = df.index.tz_localize(None)  # 타임존 제거
    df.index.name = "time"  # darts는 index가 datetime이어야 함

    target_series = TimeSeries.from_dataframe(df, value_cols='Close', fill_missing_dates=True, freq='B')
    volume_series = TimeSeries.from_dataframe(df, value_cols='Volume', fill_missing_dates=True, freq='B')

    # 휴장일등으로 nan값을 가지는 데이터를 직전값으로 채운다.
    target_series = MissingValuesFiller().transform(target_series)
    volume_series = MissingValuesFiller().transform(volume_series)

    # 스케일링 (0~1)
    target_scaler = Scaler(StandardScaler())
    volume_scaler = Scaler(StandardScaler())

    target_scaled = target_scaler.fit_transform(target_series)
    volume_scaled = volume_scaler.fit_transform(volume_series)

    mylogger.debug(f"target_scaled : {target_scaled}")
    mylogger.debug(f"volume_scaled : {volume_scaled}")

    return {
        'target_series': target_series,
        'volume_series': volume_series,
        'target_scaled': target_scaled,
        'volume_scaled': volume_scaled,
        'target_scaler': target_scaler,
        'volume_scaler': volume_scaler,
    }


def prepare_train_val_series(target_type: Literal['raw', 'scaled'], series_scaler: dict[str, TimeSeries | Scaler]) -> dict[str, TimeSeries | Scaler]:
    """
    Darts 시계열을 **학습·검증 세트**로 9 : 1 분할하는 도우미 함수
    -----------------------------------------------------------------

    Parameters
    ----------
    target_type : {'raw', 'scaled'}
        - `'raw'`   : 원본 종가(`target_series`)를 학습·검증에 사용
        - `'scaled'`: 정규화된 종가(`target_scaled`)를 사용
        *(두 경우 모두 거래량은 스케일된 값 `volume_scaled`를 covariate로 사용합니다.)*

    series_scaler : dict[str, TimeSeries | Scaler]
        `prepare_darts_data()`가 반환한 딕셔너리.
        내부에서 다음 키를 참조합니다.

        * `'target_series'`  : 원본 종가 시계열
        * `'target_scaled'`  : 스케일된 종가 시계열
        * `'volume_scaled'`  : 스케일된 거래량 시계열

    Returns
    -------
    dict[str, TimeSeries | Scaler]
        * `'target_train'` : (90 %) 학습용 종가 시계열
        * `'volume_train'` : (90 %) 학습용 거래량 covariate
        * `'target_val'`   : (10 %) 검증용 종가 시계열
        * `'volume_val'`   : (10 %) 검증용 거래량 covariate

    Notes
    -----
    * 각 시계열은 `TimeSeries.split_before(0.9)`를 사용해 **시간 순서**를 유지한 채 9 : 1로 분할합니다.
    * 스케일 여부는 `target_type`으로 제어하되, **거래량 covariate**는 항상 스케일된 데이터를 사용합니다.
    * 분할 결과의 길이와 일부 내용을 `mylogger.debug()`로 남겨
      데이터 누락·분할 오류를 쉽게 확인할 수 있습니다.

    Raises
    ------
    ValueError
        `target_type`이 `'raw'  / 'scaled'` 외의 값일 경우 예외를 발생시킵니다.
    """
    target_series = series_scaler.get('target_series')
    target_scaled = series_scaler.get('target_scaled')
    volume_scaled = series_scaler.get('volume_scaled')
    if target_type == 'raw':
        target_train, target_val = target_series.split_before(0.9)
        volume_train, volume_val = volume_scaled.split_before(0.9)
    elif target_type == 'scaled':
        target_train, target_val = target_scaled.split_before(0.9)
        volume_train, volume_val = volume_scaled.split_before(0.9)
    else:
        raise ValueError(f"'{target_type}' 오류")

    mylogger.debug(f"target_train / target_val: {len(target_train)} / {len(target_val)}")
    mylogger.debug(f"target_train: {target_train}")
    mylogger.debug(f"target_val: {target_val}")
    mylogger.debug(f"volume_train / volume_val: {len(volume_train)} / {len(volume_val)}")
    mylogger.debug(f"volume_train: {volume_train}")
    mylogger.debug(f"volume_val: {volume_val}")

    return {
        'target_train': target_train,
        'volume_train': volume_train,
        'target_val': target_val,
        'volume_val': volume_val,
    }


def latest_vs_first_bounds(df: pd.DataFrame,
                           *,
                           y_col: str = "actual",
                           lo_col: str = "lower",
                           up_col: str = "upper",
                           ndigits: int = 4,
                           eps: float = 1e-9) -> float | None:
    """
    • y :   가장 마지막(최근) 실측값
    • lo :  가장 처음(미래 예측의 첫 구간) 하단 값
    • up :  가장 처음(미래 예측의 첫 구간) 상단 값

    세 값이 모두 존재할 때만 점수를 돌려준다.
    ───────────────────────────────
    반환
      0        → 구간 안
      >0       → 구간 밖 (벗어난 비율만큼 커짐)
      None     → 셋 중 하나라도 값이 없으면 계산 불가
    """
    # ① 각 열에서 필요한 값만 뽑기
    y_series = df[y_col].dropna()   # 최근 actual
    lo_series = df[lo_col].dropna() # 첫 lower
    up_series = df[up_col].dropna() # 첫 upper

    if y_series.empty or lo_series.empty or up_series.empty:
        return None

    y  = y_series.iloc[-1]  # 가장 마지막 actual
    lo = lo_series.iloc[0]  # 가장 처음 lower
    up = up_series.iloc[0]  # 가장 처음 upper

    # ② 폭(width) 기준 정규화 점수
    width   = max(up - lo, eps)
    err_up  = max(y - up, 0)
    err_lo  = max(lo - y, 0)
    score   = (err_up + err_lo) / width

    return round(score, ndigits)


@redis_cached(prefix='nbeats')
def nbeats_forecast(ticker: str, refresh: bool = False, cache_only: bool = True) -> dict | None:
    # ─────────────────────────────
    # 1) 예측 수행 (기존 코드 그대로)
    # ─────────────────────────────
    df = get_raw_data(ticker)
    series_scaler = prepare_data(df)
    train_val_dict = prepare_train_val_series('scaled', series_scaler)

    from analyser2_hj3415.tsseer.models.nbeats import train_and_forecast
    ts_dict = train_and_forecast(series_scaler, train_val_dict)

    actual_ts = ts_dict['actual_ts']
    fcst_mean_ts = ts_dict['fcst_mean_ts']
    lower_ts = ts_dict['lower_ts']
    upper_ts = ts_dict['upper_ts']

    # ─────────────────────────────
    # 2) TimeSeries → DataFrame
    # ─────────────────────────────
    def _to_df(ts, name):
        df = ts.to_dataframe(copy=False)
        df.columns = [name]
        return df

    actual_df = _to_df(actual_ts, 'actual')
    fcst_df   = _to_df(fcst_mean_ts, 'forecast')
    lower_df  = _to_df(lower_ts, 'lower')
    upper_df  = _to_df(upper_ts, 'upper')

    merged = (
        actual_df
        .join([fcst_df, lower_df, upper_df], how="outer")
        .sort_index()
        .round(2)
        .where(lambda x: ~x.isna())  # NaN → None 직렬화 대비
    )

    # ─────────────────────────────
    # 3) 추세 판단 ⬅️ 여기만 새로 추가
    # ─────────────────────────────
    import numpy as np
    fcst_values = np.array([v for v in merged['forecast'].tolist() if v is not None])
    trend = judge_trend(fcst_values)  # 상승·하락·횡보 미정

    # 3-1) anomaly score 계산
    anomaly = latest_vs_first_bounds(merged, y_col='actual', lo_col='lower', up_col='upper')

    # ─────────────────────────────
    # 4) 직렬화-friendly dict 반환
    # ─────────────────────────────
    return {
        "ds": merged.index.strftime("%Y-%m-%d").tolist(),
        "actual": merged["actual"].tolist(),
        "forecast": merged["forecast"].tolist(),
        "lower": merged["lower"].tolist(),
        "upper": merged["upper"].tolist(),
        "trend": trend,
        "anomaly_score": anomaly
    }


# 신뢰구간을 나타낼수 없어서 mydarts의 prophet을 사용하지않고 직접 prophet을 설치해서 사용한다.
# 즉 이 함수를 사용하지 않는다.
def run_prophet_forecast(ticker: str):
    df = get_raw_data(ticker)
    series_scaler_dict = prepare_data(df)
    train_val_dict = prepare_train_val_series('raw', series_scaler_dict)

    from analyser2_hj3415.tsseer.models.prophet import train_and_forecast
    forecast_series = train_and_forecast(train_val_dict)

    return timeseries_to_dataframe(forecast_series)

