import os

from aiohttp import BasicAuth
from aiohttp.web_exceptions import HTTPUnauthorized
from aiohttp.web_middlewares import middleware


@middleware
async def auth_check(request, handler):
    if 'ADMIN_USER' not in os.environ or 'ADMIN_PASSWORD' not in os.environ:
        raise Exception('Admin login credentials not set')

    if 'Authorization' not in request.headers:
        raise HTTPUnauthorized()

    auth = BasicAuth.decode(request.headers['Authorization'])
    if (auth.login != os.environ['ADMIN_USER'] or
            auth.password != os.environ['ADMIN_PASSWORD']):
        raise HTTPUnauthorized()

    response = await handler(request)
    return response
