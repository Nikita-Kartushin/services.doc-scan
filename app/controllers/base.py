from aiohttp import web


__all__ = ['BaseController']


class BaseController:
    @classmethod
    async def get_contours(cls, request: web.Request):
        pass

    @classmethod
    async def post(cls, request: web.Request):
        pass
