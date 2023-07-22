import logging
import argparse
import io
import sys
import asyncio
import csv
from typing import Tuple, Iterable
import getpass

import more_itertools
import degiroasync.api as dapi

from .helpers import run_concurrent
from .login import get_session_from_cache

LOGGER = logging.getLogger()


async def run_one(
        session: dapi.Session,
        exchange: str,
        symbol: str,
        period: dapi.PRICE.PERIOD
        ):
    """
    """
    try:
        products = await dapi.search_product(
                session,
                by_symbol=symbol,
                by_exchange=exchange,
                product_type_id=dapi.PRODUCT.TYPEID.STOCK,
                    )
        if len(products) > 1:
            raise AssertionError("More than one product for {}.{}".format(
                symbol,
                exchange))
        elif len(products) == 0:
            LOGGER.error(
                    "No product found for exchange {}, symbol {}. Ignore.".format(
                        exchange, symbol
                    )
            )
            # Abort this one
            return
        product = products[0]
        price_data: dapi.PriceSeriesTime = await dapi.get_price_data(
                session,
                product=product,
                resolution=dapi.PRICE.RESOLUTION.PT1D,
                period=period,
                data_type=dapi.PRICE.TYPE.OHLC
                )
    except Exception as exc:
        print(f"Error on symbol {exchange}.{symbol}: {exc}", file=sys.stderr)
        return exc

    writer = csv.writer(sys.stdout, delimiter=',')
    writer.writerows(
            (
                exchange,
                symbol,
                date,
                product.info.currency,
                *price,
            )

            for date, price in zip(price_data.date, price_data.price)
            )


def prepare_inputs(input_stream: Iterable[str]) -> Iterable[Tuple[str, str]]:
    """
    Filter & split inputs from input_stream. Ignore lines starting with #

    Example
    -------

        >>> inputs = ['EPA.AIR', 'EPA.BNP', ' #EPA.VIE']
        >>> list(prepare_inputs(inputs))
        [('EPA', 'AIR'), ('EPA', 'BNP')]

    """
    # filter-out lines starting with #
    inputs = (line.strip() for line in input_stream)
    inputs = filter(lambda l: len(l) > 0, inputs)
    inputs = filter(lambda l: l[0] != '#', inputs)
    inputs = more_itertools.unique_everseen(inputs)
    inputs = (line.split('.')[:2] for line in inputs)
    return inputs


async def run(
        session: dapi.Session, 
        *,
        symbols: Iterable[str],
        period: dapi.PRICE.PERIOD = dapi.PRICE.PERIOD.P1YEAR,
        max_workers: int = 5
        ):
    """
    Execute script: read symbols from standard input and output fetched price
    data on standard output.
    """
    inputs = prepare_inputs(symbols)
    inputs = ((session, *t, period) for t in inputs)
    #inputs = ((session, t) for t in inputs)

    queries = await run_concurrent(run_one, inputs, max_concurrents=max_workers)

    # ensure all queries completed before quitting
    return await asyncio.gather(*queries)


def run_cli():
    handler = logging.StreamHandler()

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Get history for provided symbols stocks. Symbols are read "
                    "from standard input, and expected in format "
                    "EXCHANGE.SYMBOL "
                    "with EXCHANGE being product exchange on DEGIRO platform. "
            )
    parser.add_argument(
            '-p', '--period',
            default='1y',
            dest='period',
            help="Period on which to request data. Must be one of: "
            "1d, 1m, 3m, 6m, 1y, 3y, 5y, 50y"
            )
    parser.add_argument(
            '-H',
            '--no-header-row',
            dest='no_headers',
            default=False,
            action='store_true',
            required=False,
            help="Do not print header line"
            )
    parser.add_argument(
            '--debug',
            default=False,
            action='store_true',
            dest='debug',
            help="Enable debug logging."
            )
    parser.add_argument(
            'symbols',
            nargs='*',
            default=[],
            help="Symbols should be in the form of EXCHANGE.PRODUCT_SYMBOL"
            )
    args = parser.parse_args()
    logging_level = logging.ERROR
    if args.debug:
        logging_level = logging.DEBUG
    handler.setLevel(logging_level)
    LOGGER.setLevel(logging_level)
    LOGGER.addHandler(handler)

    print_headers = not args.no_headers

    period = {
        '1d': dapi.PRICE.PERIOD.P1DAY,
        '1m': dapi.PRICE.PERIOD.P1MONTH,
        '3m': dapi.PRICE.PERIOD.P3MONTH,
        '6m': dapi.PRICE.PERIOD.P6MONTH,
        '1y': dapi.PRICE.PERIOD.P1YEAR,
        '3y': dapi.PRICE.PERIOD.P3YEAR,
        '5y': dapi.PRICE.PERIOD.P5YEAR,
        '50y': dapi.PRICE.PERIOD.P50YEAR
            }[args.period.lower()]

    session = get_session_from_cache()
    session.update_throttling(max_requests=7, period_seconds=1)

    symbols = sys.stdin
    if len(args.symbols) > 0:
        symbols = args.symbols

    if print_headers:
        writer = csv.writer(sys.stdout)
        writer.writerow((
            "exchange",
            "symbol",
            "date",
            "currency",
            "open",
            "high",
            "low",
            "close",
            ))
    asyncio.get_event_loop().run_until_complete(
            run(
                session,
                symbols=symbols,
                period=period,
                max_workers=5
                )
            )
