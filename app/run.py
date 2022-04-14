from aiohttp import web
from routes import routes
from config import config
from logger import logger
from logs_manager import redirect_logs
from error_handler import configure_sentry
from middlewares import prepare_response_middleware, alive_middleware


@redirect_logs
def run():
    app = web.Application(middlewares=[prepare_response_middleware, alive_middleware])
    app.add_routes(routes)
    web.run_app(app, **config['server'])


async def create_wsgi_app(*args, **kwargs):
    # apply_args(sys_args=False, args=args, namespace=kwargs.get('namespace'))
    configure_sentry()
    app = web.Application(middlewares=[prepare_response_middleware, alive_middleware])
    app.add_routes(routes)
    return app


if __name__ == '__main__':
    run(logger)
