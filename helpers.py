import sqlalchemy as sa

from aiohttp.web_exceptions import HTTPBadRequest, HTTPInternalServerError
from datetime import datetime, timedelta, date
from sqlalchemy import func, and_
from sqlalchemy.engine import Engine, RowProxy
from typing import Dict, Optional, List, Any

from enums import CurrencyEnum
from models import Currency, Rate


DEFAULT_PAGE_SIZE = 5
DEFAULT_PAGE_NUM = 1
DAYS_TO_LOAD = 10
DAYS_FOR_AVG_VOLUME = 10


def fill_currencies(engine: Engine):
    """ Fill currencies table with CurrencyEnum values """
    conn = engine.connect()
    trans = conn.begin()
    for c in CurrencyEnum:
        query = sa.select((1, )).where(Currency.c.name == c.value)
        already_exists = conn.execute(query).scalar()
        if not already_exists:
            query = Currency.insert().values(name=c.value)
            conn.execute(query)
    trans.commit()


async def save_rates(engine: Engine, c: CurrencyEnum, rows: List[List[Any]]):
    """ Fill rates table on some currency with given rows values """
    conn = engine.connect()
    trans = conn.begin()

    border_date = date.today() - timedelta(days=DAYS_TO_LOAD - 1)
    query = sa.select((Currency.c.id, )).where(Currency.c.name == c.value)
    currency_id = conn.execute(query).scalar()
    if currency_id is None:
        raise HTTPInternalServerError(text=f'Currency "{c.value}" not found')
    for mts, _, close, _, _, volume in rows:
        rate_time = datetime.fromtimestamp(mts/1000)
        if rate_time.date() >= border_date:
            query = Rate.insert().values(
                currency_id=currency_id,
                date=rate_time,
                rate=close,
                volume=volume)
            conn.execute(query)

    trans.commit()


def param_to_positive_int(params: Dict, name: str, default: int) -> int:
    """
    Convert value from params dict to int
    Raise exception if it is negative or not a number
    """
    try:
        result = int(params.get(name, default))
    except ValueError:
        raise HTTPBadRequest(text=f'Invalid param "{name}" value')
    else:
        if result < 0:
            raise HTTPBadRequest(text=f'Invalid param "{name}" value')
        return result


async def get_currencies(engine: Engine, **kwargs) -> List[RowProxy]:
    """ Fetch paginated data from currencies table """
    conn = engine.connect()

    limit = param_to_positive_int(kwargs, 'page_size', DEFAULT_PAGE_SIZE)
    page = param_to_positive_int(kwargs, 'page', DEFAULT_PAGE_NUM)
    offset = limit * (page - 1)

    query = sa.select((Currency, )).limit(limit).offset(offset)
    currencies = conn.execute(query).fetchall()

    return currencies


async def get_last_rate(engine: Engine, currency_id: int) -> Optional[float]:
    """ Return last rate on given currency """
    conn = engine.connect()

    query = sa.select(
        (Rate.c.rate, )
    ).where(
        Rate.c.currency_id == currency_id
    ).order_by(
        Rate.c.date.desc()
    ).limit(1)

    rate = conn.execute(query).scalar()

    return rate


async def get_avg_volume(engine: Engine, currency_id: int) -> Optional[float]:
    """
    Return average volume for DAYS_FOR_AVG_VOLUME days on given currency
    """
    conn = engine.connect()

    border_date = date.today() - timedelta(days=DAYS_FOR_AVG_VOLUME - 1)

    query = sa.select(
        (func.avg(Rate.c.volume), )
    ).where(and_(
        Rate.c.date >= border_date,
        Rate.c.currency_id == currency_id
    ))

    volume = conn.execute(query).scalar()

    return volume
