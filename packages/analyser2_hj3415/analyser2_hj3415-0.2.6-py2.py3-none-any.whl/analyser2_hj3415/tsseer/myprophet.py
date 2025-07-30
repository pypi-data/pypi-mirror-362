from typing import Any

from prophet import Prophet
import pandas as pd
from sklearn.preprocessing import StandardScaler

from .utils import get_raw_data, redis_cached, judge_trend


from utils_hj3415 import setup_logger

mylogger = setup_logger(__name__,'INFO')


def prepare_data(df: pd.DataFrame) -> dict[str, pd.DataFrame | StandardScaler]:
    # ── (1) 기본 정리 ────────────────────────────────────
    df.columns = df.columns.get_level_values(0)
    df.index   = df.index.tz_localize(None)
    df = df[['Close', 'Volume']].dropna().reset_index()
    df.columns = ['ds', 'y', 'volume']          # Prophet 규격

    # ── (2) 스케일러 두 개 생성 ─────────────────────────
    volume_scaler = StandardScaler()
    y_scaler      = StandardScaler()

    df['volume_scaled'] = volume_scaler.fit_transform(df[['volume']])
    df['y_scaled']      = y_scaler.fit_transform(df[['y']])

    return {
        'prepared_df'   : df,              # y/raw, y_scaled, volume_scaled 모두 보존
        'volume_scaler' : volume_scaler,
        'y_scaler'      : y_scaler,
    }


def run_forecast(df_scaler_dict: dict[str, object], periods: int = 180) -> pd.DataFrame:
    """Prophet 학습 & periods 일 예측 → 역-스케일링해서 반환"""

    # ── 0. 필요한 객체 꺼내기 ───────────────────────────
    df:            pd.DataFrame   = df_scaler_dict['prepared_df'].copy()
    vol_scaler:    StandardScaler = df_scaler_dict['volume_scaler']
    y_scaler:      StandardScaler = df_scaler_dict['y_scaler']

    # ── 1. Prophet 학습용 DF 생성 (y_scaled만 사용) ────
    prophet_df = (
        df[['ds', 'y_scaled', 'volume_scaled']]
        .rename(columns={'y_scaled': 'y'})
    )

    model = Prophet()
    model.add_regressor('volume_scaled')
    model.fit(prophet_df)

    # ── 2. 미래 데이터프레임 생성 ───────────────────────
    future = model.make_future_dataframe(periods=periods)

    mean_vol = df['volume'].mean()
    future['volume_scaled'] = vol_scaler.transform([[mean_vol]] * len(future))

    # ── 3. 예측 + y 역-스케일링 ─────────────────────────
    pred_df = model.predict(future)

    cols_to_inverse = ['yhat', 'yhat_lower', 'yhat_upper']
    pred_df[cols_to_inverse] = y_scaler.inverse_transform(pred_df[cols_to_inverse])

    # (선택) 학습 구간의 실측 y도 복원해 두면 병합/시각화에 편리
    df['y'] = y_scaler.inverse_transform(df[['y_scaled']])
    # pred_df 와 df 를 나중에 merge 하면 실측·예측을 한 눈에 볼 수 있음

    return pred_df


def latest_anomaly_score(df: pd.DataFrame,
                         *,
                         y_col: str = 'actual',
                         lo_col: str = 'lower',
                         up_col: str = 'upper',
                         ndigits: int = 4,
                         eps: float = 1e-9         # width=0 보호용
                         ) -> float | None:
    """
    df 에서 가장 최근(마지막) 실측값이
    예측 구간을 얼마나 벗어났는지 상대적 점수로 돌려준다.

    • score = 0       → 구간 안 (정상)
    • score > 0       → 구간 밖 (이상)  ─ 벗어난 비율만큼 커짐
    • None            → 계산 불가(값이 없음·width=0 등)
    """
    # ① y·lo·up 모두 NaN이 아닌 행만 추림
    valid = df.dropna(subset=[y_col, lo_col, up_col])
    if valid.empty:
        return None

    # ② 가장 최근 행
    y, lo, up = valid.iloc[-1][[y_col, lo_col, up_col]]

    # ③ 새 점수 공식 ─ 구간 폭으로 정규화
    width   = max(up - lo, eps)          # 폭이 0이면 eps로 대체
    err_up  = max(y - up, 0)             # 위쪽 초과량
    err_low = max(lo - y, 0)             # 아래쪽 초과량
    score   = (err_up + err_low) / width

    return round(score, ndigits)


@redis_cached(prefix='prophet')
def prophet_forecast(ticker: str, refresh: bool = False, cache_only: bool = False) -> dict[str, Any]:
    """
    Pure 도메인 로직: (1)데이터 준비 → (2)예측 → (3)직렬화 dict 반환
    Redis 캐싱은 데코레이터가 담당.
    """
    df = get_raw_data(ticker)
    df_scaler_dict = prepare_data(df)
    past_and_forecast = run_forecast(df_scaler_dict)

    prepared_df: pd.DataFrame = df_scaler_dict['prepared_df']
    merged = (
        prepared_df[['ds', 'y']]
        .merge(
            past_and_forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']],
            on='ds', how='outer'
        )
        .sort_values('ds')
    )

    # ------------- (2) 추세 평가 -------------
    fcst_vals = merged.loc[merged['yhat'].notna(), 'yhat'].values
    trend = judge_trend(fcst_vals)  # "상승" | "하락" | "횡보" | 미정

    # 3-1) anomaly score 계산
    anomaly = latest_anomaly_score(merged, y_col='y', lo_col='yhat_lower', up_col='yhat_upper')

    return {
        'ds'      : merged['ds'].dt.strftime('%Y-%m-%d').tolist(),
        'actual'  : merged['y'].where(merged['y'].notna()).tolist(),
        'forecast': merged['yhat'].round(2).tolist(),
        'lower'   : merged['yhat_lower'].round(2).tolist(),
        'upper'   : merged['yhat_upper'].round(2).tolist(),
        'trend': trend,
        "anomaly_score": anomaly
    }


