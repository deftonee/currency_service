import aiohttp

from aiohttp import web

from enums import CurrencyEnum
from helpers import save_rates, get_currencies, param_to_int


async def fetch(request):
    async with aiohttp.ClientSession() as session:
        for c, url in CurrencyEnum.urls().items():
            async with session.get(url, ssl=True) as response:
                rows = await response.json()
                await save_rates(request.app['db_engine'], c, rows)
    return web.Response(body='Success')


async def currencies(request):
    objs = await get_currencies(request.app['db_engine'], **request.query)
    return web.json_response([[o.id, o.name] for o in objs])


async def rates(request):
    rate_id = param_to_int(request.match_info, 'rate_id', 0)
    print(rate_id)
    return web.Response(body='Success')

