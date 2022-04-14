import cv2
import numpy as np

from numpy import asarray


class ImageUtils:
    @classmethod
    def bounding_rect(cls, _contour, _image: np.array):
        """
        Метод предназначен для выделения интересующей области
            исходя из найденных контуров
        """
        x, y, w, h = cv2.boundingRect(_contour)
        _bounding_rect = _image[y:y + h, x:x + w]

        return _bounding_rect

    @classmethod
    def get_np_array_of_image(cls, image) -> np.array:
        """
        Возвращает изображение в виде массива np.array
        """
        np_array_image = asarray(image)

        return np_array_image
