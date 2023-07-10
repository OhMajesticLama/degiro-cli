import sys
import asyncio
import logging
import argparse
import csv
from typing import Optional

import degiroasync.api as dapi

from .helpers import LOGGER
from .login import get_session_from_cache


async def run(
        session: dapi.Session, 
        *,
        search_txt: Optional[str],
        exchange_txt: Optional[str],
        country_txt: Optional[str],
        ):
    """
    Execute script: read symbols from standard input and output fetched price
    data on standard output.
    """
    exc_dict = session.exchange_dictionary
    products = await dapi.search_product(
        session=session,
        by_text=search_txt,
        by_exchange=exchange_txt,
        by_country=country_txt,
            )
    writer = csv.writer(sys.stdout)
    exc_dict: dapi.ExchangeDictionary = session.exchange_dictionary
    for product in products:
        exchange = exc_dict.exchange_by(id=product.info.exchange_id)
        writer.writerow((
                exchange.hiq_abbr,
                product.info.symbol,
                product.info.name,
                product.info.currency,
                product.info.isin,
                ))



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
            '-t',
            dest='search',
            default=None,
            required=False,
            help="Search for SEARCH_TXT and returns products."
            )
    parser.add_argument(
            '--exchange',
            dest='exchange',
            default=None,
            required=False,
            help="Search for products by exchange."
            )
    parser.add_argument(
            '--country',
            dest='country',
            default=None,
            required=False,
            help="Search products on exchange places in COUNTRY"
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
            '--list-countries',
            dest='list_countries',
            default=False,
            action='store_true',
            required=False,
            help="Print the available country codes on the platform."
            )
    parser.add_argument(
            '--debug',
            default=False,
            action='store_true',
            dest='debug',
            help="Enable debug logging."
            )
    args = parser.parse_args()
    
    print_headers = not args.no_headers
    search_txt = args.search
    exchange_txt = args.exchange
    country_txt = args.country

    logging_level = logging.ERROR
    if args.debug:
        logging_level = logging.DEBUG
    handler.setLevel(logging_level)
    LOGGER.setLevel(logging_level)
    LOGGER.addHandler(handler)

    session = get_session_from_cache()

    if args.list_countries:
        for country in sorted(
                session.exchange_dictionary.countries,
                key=lambda x: x.name):
            print(country.name)
        return 0

    if print_headers:
        writer = csv.writer(sys.stdout)
        writer.writerow((
            "exchange",
            "symbol",
            "name",
            "currency",
            "isin",
            ))
    asyncio.get_event_loop().run_until_complete(
            run(
                session,
                search_txt=search_txt,
                exchange_txt=exchange_txt,
                country_txt=country_txt,
                )
            )
