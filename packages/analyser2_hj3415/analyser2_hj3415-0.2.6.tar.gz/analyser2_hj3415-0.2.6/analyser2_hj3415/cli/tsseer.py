import argparse

from analyser2_hj3415.tsseer.mydarts import nbeats_forecast
from analyser2_hj3415.tsseer.myprophet import prophet_forecast

from utils_hj3415 import tools
from db2_hj3415.valuation import get_all_codes_sync

ENGINE_MAP = {
    'prophet': prophet_forecast,
    'nbeats': nbeats_forecast,
}

# 순서대로 달러인덱스, 원달러환율, 미국채3개월물, 원유, 금, 은, sp500, 코스피, 니케이225, 홍콩항셍
MI_TICKERS = ['DX-Y.NYB', 'KRW=X', '^IRX', 'CL=F', 'GC=F', 'SI=F', '^GSPC', '^KS11', '^N225', '^HSI' ]

def handle_cache_many_command(engine: str, targets: list[str]):
    valid_targets = [code for code in targets if tools.is_6digit(code)]
    if not valid_targets:
        print("유효한 종목 코드가 없습니다.")
        return

    for code in valid_targets:
        generator = ENGINE_MAP.get(engine)
        if not generator:
            raise ValueError(f"지원하지 않는 tsseer: {engine}")
        data = generator(code+'.KS', refresh=True)
        print(f'{code}: {data}')


def handle_cache_mi(engine: str):
    for ticker in MI_TICKERS:
        generator = ENGINE_MAP.get(engine)
        if not generator:
            raise ValueError(f"지원하지 않는 tsseer: {engine}")
        data = generator(ticker, refresh=True)
        print(f'{ticker}: {data}')


def handle_cache_command(engine: str, code: str):
    if not tools.is_6digit(code):
        print(f"잘못된 코드: {code}")
        return

    generator = ENGINE_MAP.get(engine)
    if not generator:
        raise ValueError(f"지원하지 않는 tsseer: {engine}")
    data = generator(code + '.KS', refresh=True)
    print(f'{code}: {data}')


def main():
    parser = argparse.ArgumentParser(description="Tsseer Commands")
    subparsers = parser.add_subparsers(dest='command', help='명령어')

    # cache 명령
    cache_parser = subparsers.add_parser('cache', help='레디스 캐시에 저장 실행')
    cache_parser.add_argument('engine', type=str, help="이름 : prophet, nbeats")
    cache_parser.add_argument('targets', nargs='*', help="종목코드 (예: 005930, 000660... and all)")

    args = parser.parse_args()

    if args.command == 'cache':
        engine = args.engine.lower()
        if len(args.targets) == 1 and args.targets[0].lower() == "all":
            handle_cache_many_command(engine, get_all_codes_sync())
            handle_cache_mi(engine)
        elif len(args.targets) == 1:
            handle_cache_command(engine, args.targets[0])
        else:
            handle_cache_many_command(engine, args.targets)

