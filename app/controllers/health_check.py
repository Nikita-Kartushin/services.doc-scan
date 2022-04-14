from aiohttp import web

__all__ = ['HealthCheckController']


class HealthCheckController:
    """
    Контроллер для проверки работоспособности сервиса
    livenessProve Kubernetes
    """

    @classmethod
    async def get(cls, request: web.Request):
        return {}
