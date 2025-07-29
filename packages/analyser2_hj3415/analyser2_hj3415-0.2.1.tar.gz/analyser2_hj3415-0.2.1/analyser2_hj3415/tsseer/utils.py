from __future__ import annotations

import datetime
import time
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd

from darts import TimeSeries
from darts.dataprocessing.transformers import Scaler
from ..common.connection import get_redis_client


from utils_hj3415 import setup_logger

mylogger = setup_logger(__name__,'INFO')


def get_raw_data(ticker: str, max_retries: int = 3, delay_sec: int = 2) -> pd.DataFrame:
    """
    Yahoo Finance에서 특정 티커의 최근 4년간 주가 데이터를 가져옵니다.

    Args:
        ticker (str): 조회할 종목의 티커 (예: "005930.KQ").
        max_retries (int, optional): 최대 재시도 횟수. 기본값은 3.
        delay_sec (int, optional): 재시도 전 대기 시간 (초). 기본값은 2초.

    Returns:
        pd.DataFrame: 주가 데이터프레임. 실패 시 빈 DataFrame 반환.
    """
    today = datetime.datetime.today()
    four_years_ago = today - datetime.timedelta(days=365 * 4)

    for attempt in range(1, max_retries + 1):
        try:
            data = yf.download(
                tickers=ticker,
                start=four_years_ago.strftime('%Y-%m-%d'),
                # end=today.strftime('%Y-%m-%d')  # 생략 시 최신 날짜까지 자동 포함
            )

            if not data.empty:
                return data
            else:
                print(f"[{attempt}/{max_retries}] '{ticker}' 데이터가 비어 있습니다. {delay_sec}초 후 재시도합니다...")

        except Exception as e:
            print(f"[{attempt}/{max_retries}] '{ticker}' 다운로드 중 오류 발생: {e}. {delay_sec}초 후 재시도합니다...")

        time.sleep(delay_sec)

    mylogger.error(f"'{ticker}' 주가 데이터를 최대 {max_retries}회 시도했지만 실패했습니다.")
    return pd.DataFrame()


def timeseries_to_dataframe(forecast: TimeSeries) -> pd.DataFrame:
    forecast_df = forecast.to_dataframe()
    mylogger.debug(forecast_df)
    return forecast_df


def show_graph_nbeats(data: dict[str, list]) -> None:
    """
    JSON 직렬화가 가능한 dict( keys = ds, actual, forecast, lower, upper )를
    받아 matplotlib 그래프를 표시한다.

    Parameters
    ----------
    data   : dict
        {"ds": [...], "actual": [...], "forecast": [...], "lower": [...], "upper": [...]}
        * ds        : 날짜 문자열(YYYY-MM-DD)
        * actual    : 실제값. None → 결측
        * forecast  : 예측값(포인트). None → 결측
        * lower/upper : (선택) 예측구간 하한/상한. None → 결측
    """
    # ──────────────────────────────────────
    # ① dict → DataFrame
    # ──────────────────────────────────────
    df = pd.DataFrame(data)
    df["ds"] = pd.to_datetime(df["ds"])
    df.set_index("ds", inplace=True)

    # 숫자형 변환 (None → NaN)
    for col in ["actual", "forecast", "lower", "upper"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # ──────────────────────────────────────
    # ② plot
    # ──────────────────────────────────────
    fig, ax = plt.subplots(figsize=(14, 6))

    df["actual"].plot(ax=ax, label="Actual", lw=1.6)
    df["forecast"].plot(ax=ax, label="Forecast", lw=1.6, color="tab:orange")

    # 불확실성 구간이 있으면 음영으로 표시
    if {"lower", "upper"}.issubset(df.columns):
        ax.fill_between(
            df.index,
            df["lower"],
            df["upper"],
            color="tab:orange",
            alpha=0.5,
            label="90% interval",
        )

    ax.set_title("nbeats forecast")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.show()

def show_graph_prophet(series_scaler_dict: dict[str, TimeSeries | Scaler], forecast_series: TimeSeries) -> None:
    target_series = series_scaler_dict.get('target_series')

    target_series.plot(label='close')

    forecast_series.plot(label='predict')

    plt.axvline(target_series.end_time(), color="gray", ls="--", lw=1)  # 학습/검증 경계
    plt.legend()
    plt.title("prophet forecast")
    plt.show()

import json, os, redis, functools

def redis_cached(prefix: str | None = None, ttl_h: int | None = None):
    """Redis 캐싱 데코레이터

    Args:
        prefix     : Redis 키 prefix (기본 = 함수.__name__)
        ttl_h      : TTL(시간). 기본값: env `REDIS_EXPIRE_TIME_H` 또는 12
    """
    ttl_h = ttl_h or int(os.getenv("REDIS_EXPIRE_TIME_H", 12))
    prefix = prefix  # 나중에 wraps 안에서 참조
    key_maker = lambda a, k: str(a[0]).lower()

    def decorator(func):
        cache_prefix = prefix or func.__name__

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # ── NEW ─────────────────────────────
            refresh = kwargs.pop("refresh", False)  # ← 호출 시 refresh=True 로 강제 리셋
            # ────────────────────────────────────

            redis_cli = get_redis_client()
            cache_key = f"{cache_prefix}:{key_maker(args, kwargs)}"
            ttl = ttl_h * 60 * 60

            # 1) 캐시 조회 (refresh 가 False 일 때만)
            if not refresh:
                try:
                    if (raw := redis_cli.get(cache_key)):
                        mylogger.info(f"cache hit {cache_key}")
                        return json.loads(raw)
                except redis.RedisError as e:
                    mylogger.warning(f"Redis GET fail: {e}")

            # 2) 원본 함수 실행
            mylogger.info(f"{cache_key} → 계산 후 캐시{' 갱신' if refresh else ' 저장'}")
            result = func(*args, **kwargs)

            # 3) 캐시 저장/갱신
            try:
                redis_cli.setex(cache_key, ttl, json.dumps(result))
            except redis.RedisError as e:
                mylogger.warning(f"Redis SETEX fail: {e}")

            return result

        return wrapper
    return decorator