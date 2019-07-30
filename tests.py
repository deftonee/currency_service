from aiohttp import BasicAuth
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from app import create_application


class ServiceTestCase(AioHTTPTestCase):

    async def get_application(self):
        return create_application()

    @staticmethod
    def create_headers():
        return {
            'Authorization': BasicAuth(
                login='admin', password='12345'
            ).encode(),
        }

    @unittest_run_loop
    async def test_fetch(self):
        resp = await self.client.get(
            "/fetch", headers=self.create_headers())
        self.assertEqual(resp.status, 200)
        result = await resp.text()
        self.assertEqual(result, 'Success')

    @unittest_run_loop
    async def test_auth(self):
        resp = await self.client.get("/currencies")
        self.assertEqual(resp.status, 401)

    @unittest_run_loop
    async def test_currencies(self):
        resp = await self.client.get(
            "/currencies", headers=self.create_headers())
        self.assertEqual(resp.status, 200)
        result = await resp.json()
        self.assertEqual(len(result), 5)
        self.assertEqual(len(result[0]), 2)
        self.assertEqual(type(result[0][0]), int)
        self.assertEqual(type(result[0][1]), str)

    @unittest_run_loop
    async def test_rates(self):
        resp = await self.client.get(
            "/rates/1", headers=self.create_headers())
        self.assertEqual(resp.status, 200)
        result = await resp.json()
        self.assertEqual(len(result), 2)
        self.assertEqual(type(result[0]), float)
        self.assertEqual(type(result[1]), float)
