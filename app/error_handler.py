import sentry_sdk
from config import config
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration


def configure_sentry():
    if config['env'] in ['test', 'prod']:
        sentry_sdk.init(
            dsn=config['sentry']['dsn'],
            server_name='doc_scan',
            environment=config['env'],
            integrations=[
                AioHttpIntegration(),
                SqlalchemyIntegration()
            ],
        )
