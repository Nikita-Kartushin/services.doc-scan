import cv2
import pytesseract
import numpy as np

from typing import List
from utils.converter import Converter


class TesseractOCR:
    LANG = 'rus'
    OCR_CONFIG = '--psm 7 --oem 3'

    @classmethod
    def read_text_from_image(cls, images: List[np.array], filename: str) -> list:
        """
        Класс реализует библиотеку tesseract для получения текста с изображения.
        """
        data = []
        for image in images:
            # image = cls._preprocessing_of_image(image)
            path_to_image = Converter.get_path_image(image, filename)

            pytesseract_result = pytesseract.image_to_string(
                path_to_image,
                lang=cls.LANG,
                config=cls.OCR_CONFIG
            )

            data.append(pytesseract_result)

        return data

    # @staticmethod
    # def _preprocessing_of_image(image: np.array):
    #     """
    #     Преобразование изображения в BGR2GRAY.
    #     Преобразования 'серых' пикселей в белые для удаления шума.
    #     """
    #     _image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #     _image[_image > 200] = 255
    #
    #     return _image
