from aiohttp import web
from controllers import HealthCheckController
from controllers import PassportScanningController


routes = [
    # PASSPORT
    web.get('/health-check', HealthCheckController.get),
    web.post('/scanning/passport/', PassportScanningController.post),
    # web.get('/contours/passport/', PassportScanningController.get_contours)
]

