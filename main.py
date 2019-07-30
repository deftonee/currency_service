from aiohttp import web

from app import create_application


app = create_application()
web.run_app(app, host='0.0.0.0', port=8080)

