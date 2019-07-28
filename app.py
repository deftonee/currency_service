import os
import sqlalchemy as sa

from aiohttp import web

from helpers import fill_currencies
from models import create_tables
from views import currencies, fetch


db_engine = sa.create_engine(os.environ['DB_CONNECTION'])
create_tables(db_engine)
fill_currencies(db_engine)

app = web.Application()
app.router.add_route('GET', '/fetch', fetch)
app.router.add_route('GET', '/currencies', currencies)
app['db_engine'] = db_engine
web.run_app(app, host='0.0.0.0', port=8080)

