import json
import time
import asyncio

from utils.cast import CastUtil
from aiohttp.web import Request, Response, middleware, json_response, HTTPOk


@middleware
async def prepare_response_middleware(request: Request, handler) -> Response:
    start = time.time()

    setattr(asyncio.Task.current_task(), 'request', request)
    response = await handler(request)

    end = time.time()

    execution_time = end - start
    request['execution_time'] = execution_time
    response = _prepare_response(response, execution_time)
    response.headers['user_id'] = str(request.get('user_id'))

    return response


def _prepare_response(response: Response, time_of_request: float, additional_headers: list = None) -> Response:
    """
    Method append time and execution time of request
    into meta if response is dictionary
    At last call method to extend custom headers with existing already

    :param response: web.Response
    :param time_of_request: float
    :param additional_headers: Any
    :return:
    """

    if isinstance(response, dict):
        if response.get('meta') is not None:
            response['meta']['execution_time'] = time_of_request
            response['meta']['time'] = time.time()

        response = json_response(response, dumps=lambda e: json.dumps(response, default=CastUtil.to_str))

    if isinstance(response, str):
        response = HTTPOk(body=response)

    response = _added_headers_to_response(response, additional_headers)

    return response


def _added_headers_to_response(response: Response, additional_headers: list = None) -> Response:
    """
    Method for setting headers in Response
    extend with custom headers in list additional_headers

    :param response: aiohttp.web.Response
    :param additional_headers: list
    :return:
    """

    headers = [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH'),
        ('Access-Control-Allow-Headers', 'Content-Type,'
                                         'Authorization,'
                                         'X-Requested-With'),
    ]

    for header in headers:
        response.headers.add(*header)

    if additional_headers and isinstance(additional_headers, list):
        headers.extend(additional_headers)

    return response
