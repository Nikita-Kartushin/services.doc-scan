import abc
import numpy as np


class BaseDocumentScanningStrategy:
    def __init__(self, filename: str, image: np.array, contours):
        self.image = image
        self.contours = contours
        self.filename = filename

    @abc.abstractmethod
    async def execute(self):
        pass
