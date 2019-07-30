import os
import sqlalchemy as sa

from aiohttp import web

from helpers import fill_currencies
from middlewares import auth_check
from models import create_tables
from views import currencies, fetch, rates

db_engine = sa.create_engine(os.environ['DB_CONNECTION'])
create_tables(db_engine)
fill_currencies(db_engine)

app = web.Application(middlewares=(auth_check, ))
app.router.add_route('GET', '/fetch', fetch)
app.router.add_route('GET', '/currencies', currencies)
app.router.add_route('GET', r'/rates/{currency_id:\d+}', rates)

app['db_engine'] = db_engine
web.run_app(app, host='0.0.0.0', port=8080)

