from aiohttp.web_exceptions import HTTPBadRequest
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

from enums import CurrencyEnum
from models import Currency, Rate


PAGE_SIZE = 5


def fill_currencies(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    for c in CurrencyEnum:
        if not session.query(exists().where(Currency.name == c.value)).scalar():
            session.add(Currency(name=c.value))
    session.commit()


async def save_rates(engine, c, rows):
    Session = sessionmaker(bind=engine)
    session = Session()

    currency_id = session.query(Currency.id).filter(Currency.name == c.value)

    for mts, _, close, _, _, volume in rows:
        session.add(
            Rate(
                currency_id=currency_id,
                date=datetime.fromtimestamp(mts/1000),
                rate=close,
                volume=volume))

    session.commit()


def param_to_int(params, name, default):
    try:
        result = int(params.get(name, default))
    except ValueError:
        raise HTTPBadRequest()
    else:
        if result < 0:
            raise HTTPBadRequest()
        return result


async def get_currencies(engine, **kwargs):
    Session = sessionmaker(bind=engine)
    session = Session()

    limit = param_to_int(kwargs, 'page_size', PAGE_SIZE)
    page = param_to_int(kwargs, 'page', 1)
    offset = limit * (page - 1)

    currencies = session.query(Currency.name).limit(limit).offset(offset)

    return currencies
