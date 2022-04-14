import matplotlib.pyplot as plt
import numpy as np

from typing import List
from collections import namedtuple


OCRLocation = namedtuple("OCRLocation", ["bbox", "name"])


class PassportSegmenter:
    """
    Класс предназначен для сегментирования изображения
    """
    @classmethod
    def create_box_with_location(cls, image: np.array, contours: List):
        """
        Выделение участков изображения.
        Метод возвращает лист участков изображениий, полученных
            на основе contours.
        """
        locations = cls._create_location(contours)

        boxes = []
        for location in locations:
            (x, y, w, h) = location.bbox
            _image = image[y:y + h, x:x + w]
            boxes.append(_image)
        return boxes

    @classmethod
    def _create_location(cls, contours: List):
        """
        Метод возращает контуры в виде OCRLocation
        """
        _OCR_LOCATIONS_ = []

        for contour in contours:
            _OCR_LOCATIONS_.append(
                OCRLocation(contour, "")
            )

        return _OCR_LOCATIONS_
