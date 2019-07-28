import sqlalchemy as sa

from typing import Dict

from aiohttp.web_exceptions import HTTPBadRequest, HTTPInternalServerError
from datetime import datetime

from enums import CurrencyEnum
from models import Currency, Rate


PAGE_SIZE = 5


def fill_currencies(engine):
    conn = engine.connect()
    trans = conn.begin()
    for c in CurrencyEnum:
        query = sa.select((1, )).where(Currency.c.name == c.value)
        already_exists = conn.execute(query).scalar()
        if not already_exists:
            query = Currency.insert().values(name=c.value)
            conn.execute(query)
    trans.commit()


async def save_rates(engine, c, rows):
    conn = engine.connect()
    trans = conn.begin()

    query = sa.select((Currency.c.id, )).where(Currency.c.name == c.value)
    currency_id = conn.execute(query).scalar()
    if currency_id is None:
        raise HTTPInternalServerError(text=f'Currency "{c.value}" not found')
    for mts, _, close, _, _, volume in rows:
        query = Rate.insert().values(
            currency_id=currency_id,
            date=datetime.fromtimestamp(mts/1000),
            rate=close,
            volume=volume)
        conn.execute(query)

    trans.commit()


def param_to_int(params: Dict, name: str, default: int) -> int:
    try:
        result = int(params.get(name, default))
    except ValueError:
        raise HTTPBadRequest(text=f'Invalid param "{name}" value')
    else:
        if result < 0:
            raise HTTPBadRequest(text=f'Invalid param "{name}" value')
        return result


async def get_currencies(engine, **kwargs):
    conn = engine.connect()

    limit = param_to_int(kwargs, 'page_size', PAGE_SIZE)
    page = param_to_int(kwargs, 'page', 1)
    offset = limit * (page - 1)

    query = sa.select((Currency, )).limit(limit).offset(offset)
    currencies = conn.execute(query).fetchall()

    return currencies
