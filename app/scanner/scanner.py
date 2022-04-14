import os

from config import config
from logger import logger
from .strategy.strategies import DOCUMENT_SCANNING_STRATEGY
from .strategy.context_strategy import ScanningContextStrategy


class DocumentScanner:
    def __init__(self, data: dict, doc_type: str):
        self.data = data
        self.doc_type = doc_type

        self.image = self.data.get('image')
        self.filename = self.data.get('filename')
        self.contours = self.data.get('contours')

    async def execute_scanning(self) -> dict:
        logger.info(f'Start scanning {self.doc_type}')

        strategy = DOCUMENT_SCANNING_STRATEGY.get(self.doc_type)

        scanning_context_strategy = ScanningContextStrategy()
        scanning_context_strategy.setStrategy(strategy(self.filename, self.image, self.contours))

        try:
            scanning_results = await scanning_context_strategy.executeStrategy()
            logger.info("Document has been scanned")
            return scanning_results

        except Exception as e:
            logger.exception(e)
            self._clear_tmp()

        finally:
            self._clear_tmp()

    @staticmethod
    def _clear_tmp():
        files = os.listdir(config['path_tmp'])
        for file in files:
            os.remove(os.path.join(config["path_tmp"], file))
