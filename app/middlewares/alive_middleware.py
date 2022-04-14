from aiohttp.web import middleware, Request, HTTPOk


@middleware
async def alive_middleware(request: Request, handler):
    if request.method == 'OPTIONS':
        response = HTTPOk()

    else:
        response = await handler(request)

    return response
