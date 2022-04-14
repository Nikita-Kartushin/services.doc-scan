import cv2
import numpy as np

from typing import List
from utils.text_box import TextBox
from utils.converter import Converter
from utils.tesseract import TesseractOCR
from utils.image_utils import ImageUtils
from .scanning_helpers import PassportParser
from .scanning_helpers import PassportFilters
from .scanning_helpers import PassportContours
from utils.canny_contours import CannyContours
from utils.segmentator import PassportSegmenter
from scanner.strategy.base import BaseDocumentScanningStrategy


class ScanningPassportStrategy(BaseDocumentScanningStrategy):
    """
    Класс реализует стратегию сканирования паспорта.

    Он получает название файла, изображение в вижде np.array и контур документа.
        Если контур не был передан в запросе, то doc-scan сам попробует найти контур
    """
    def __init__(self, filename: str, image: np.array, contours):
        super().__init__(filename, image, contours)
        if self.contours is None:
            self.contours = CannyContours.get_canny_contours(
                self.image,
                epsilon=0.02,
                count_vertex=4,
                gaussian_sigmaX=0,
                canny_threshold_1=100,
                canny_threshold_2=250,
                gaussian_kernel_size=(5, 5),
                morph_close_kernel_size=(13, 13)
            )

    async def execute(self):
        """
        Метод делает предобработку изображения: вырезает замкнтутую
            контуром область, где находится документ, и делегирует задачи
            по распознованию сирии-номера и всего остального.

        Алгоритм распознования следующий:
        1 - Предобработка изображение, приведение его к формату BGR2GRAY
        2 - Применение фильтров в изображению в целях
                выделения текста и устранения шумов
        3 - Получение контуров, в которых, возможно, находятся паспортные данные
        4 - Выделение замкнутых контурами участков изображения
        5 - Распознование символов в выделенных участках
        6 - Парсинг данных

        :return: словарь с паспортными данными
        """
        bounding_rect = ImageUtils.bounding_rect(
            self.contours,
            self.image
        )
        _height, _width = bounding_rect.shape[:2]

        result_scanning_main_page = self._scan_main_pages(bounding_rect)
        result_scanning_series_number = self._scan_series_number(bounding_rect)

        parse_data_main_page = PassportParser.parse_main_page(
            data=result_scanning_main_page,
            width=_width,
            height=_height
        )

        parse_data_serial_number = PassportParser.parse_series_number(
            data=result_scanning_series_number
        )

        full_passport_data = parse_data_main_page
        full_passport_data['serial_number'] = parse_data_serial_number

        return full_passport_data

    def _scan_main_pages(self, image):
        """
        Метод возвращает распознанные данные с
            основной страницы паспорта
        """
        image_grayscale = Converter.jpg_convert_to_grayscale(self.filename, image)

        image_BRG2GRAY = cv2.cvtColor(
            image_grayscale,
            cv2.COLOR_BGR2GRAY
        )
        image_with_filters = PassportFilters.execute_filters_main_page(
            image_BRG2GRAY
        )
        contours = PassportContours.get_text_contours_main_page(
            image_with_filters,
            image_BRG2GRAY
        )
        images_text_box: List[np.array] = PassportSegmenter.create_box_with_location(
            image_grayscale,
            contours
        )
        tesseract_data = TesseractOCR.read_text_from_image(
            images_text_box,
            self.filename
        )
        text_boxes = self._get_text_boxes(
            contours,
            tesseract_data
        )

        return text_boxes

    def _scan_series_number(self, image):
        """
        Метод возвращает распознанные данные
            серии и номера паспорта
        """
        image_grayscale = Converter.jpg_convert_to_grayscale(self.filename, image)
        image_grayscale_rotate = cv2.rotate(image_grayscale, rotateCode=cv2.ROTATE_90_COUNTERCLOCKWISE
        )
        image_BRG2GRAY = cv2.cvtColor(
            image_grayscale_rotate,
            cv2.COLOR_BGR2GRAY
        )
        image_with_filters = PassportFilters.execute_filters_series_number(
            image_BRG2GRAY
        )
        contours = PassportContours.get_text_contours_serial_number(
            image_with_filters,
            image_BRG2GRAY
        )
        images_text_box: List[np.array] = PassportSegmenter.create_box_with_location(
            image_grayscale_rotate,
            contours
        )
        tesseract_data = TesseractOCR.read_text_from_image(
            images_text_box,
            self.filename
        )
        text_boxes = self._get_text_boxes(
            contours,
            tesseract_data
        )

        return text_boxes

    @staticmethod
    def _get_text_boxes(contours, tesseract_data):
        """
        Преобразует полученные из OCR данные к TextBox
            и возвращает их
        """
        text_boxes = []
        for contour, string in zip(contours, tesseract_data):
            text_box = TextBox()
            text_box.set_x(contour[0])
            text_box.set_y(contour[1])
            text_box.set_width(contour[2])
            text_box.set_height(contour[3])
            text_box.set_data(string)

            text_boxes.append(text_box)

        return text_boxes
