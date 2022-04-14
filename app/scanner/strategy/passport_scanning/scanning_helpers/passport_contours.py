import cv2
import numpy as np


class PassportContours:
    """
    Класс предназначен для обнаружения участков изображения, в которых есть текст
    """

    @classmethod
    def get_text_contours_main_page(cls, image_with_filters, image):
        """
        @var EXPANSION_X: Предназначен для изменения координаты x контура
        @var EXPANSION_Y: Предназначен для изменения координаты y контура
        @var EXPANSION_HEIGHT: Предназначен для изменения высоты контура
        @var EXPANSION_WIDTH: Предназначен для изменения ширины контура

        @var MIN_CONTOURS_WIDTH: Минимальная ширина контура
        @var MIN_CONTOURS_HEIGHT: минимальная высота контура

        @var X_TO_WIDTH_RATIO_MAX: Коэфициент, показывающий максимальное отношение значения x к ширине
        @var Y_TO_HEIGHT__RATIO_MIN: Коэфициент, показывающий минимальное отношение значения y к ширине
        @var Y_TO_HEIGHT__RATIO_MAX: Коэфициент, показывающий максимальное отношение значения y к ширине
        @var HEIGHT_TO_WIDTH_RATIO_MAX: Коэфициент, показывающий максимальное отношение высоты к ширине

        @var CONTOUR_ROTATION_RATIO: Коэфициент, показывающий максимальное отклонение поворота
        """
        EXPANSION_X = 30
        EXPANSION_Y = 10
        EXPANSION_HEIGHT = 15
        EXPANSION_WIDTH = 80

        MIN_CONTOURS_WIDTH = 8
        MIN_CONTOURS_HEIGHT = 8

        X_TO_WIDTH_RATIO_MAX = 0.9
        Y_TO_HEIGHT__RATIO_MIN = 0.1
        Y_TO_HEIGHT__RATIO_MAX = 0.85
        HEIGHT_TO_WIDTH_RATIO_MAX = 0.4

        CONTOUR_ROTATION_RATIO = 0.4

        _CONTOURS_MAIN_PAGE_ = []

        contours, hierarchy = cls._get_contours(image_with_filters)
        mask = np.zeros(image_with_filters.shape, dtype=np.uint8)

        for idx in range(len(contours)):
            x, y, w, h = cv2.boundingRect(contours[idx])
            mask[y:y + h, x:x + w] = 0

            cv2.drawContours(mask, contours, idx, (255, 255, 255), -1)

            r = float(cv2.countNonZero(mask[y:y + h, x:x + w])) / (w * h)
            height, width = image.shape[:2]

            condition = r > CONTOUR_ROTATION_RATIO
            condition &= w > MIN_CONTOURS_WIDTH
            condition &= h > MIN_CONTOURS_HEIGHT
            condition &= h < w * HEIGHT_TO_WIDTH_RATIO_MAX
            condition &= y > height * Y_TO_HEIGHT__RATIO_MIN
            condition &= y < height * Y_TO_HEIGHT__RATIO_MAX
            condition &= x < width * X_TO_WIDTH_RATIO_MAX

            x -= EXPANSION_X
            y -= EXPANSION_Y
            w += EXPANSION_WIDTH
            h += EXPANSION_HEIGHT

            if condition:
                _pt1 = (x, y)
                _pt2 = (x + w - 1, y + h - 1)
                _color = (0, 255, 0)

                cv2.rectangle(
                    img=image,
                    pt1=_pt1,
                    pt2=_pt2,
                    color=_color,
                    thickness=2
                )

                _CONTOURS_MAIN_PAGE_.append((x, y, w, h))

        _CONTOURS_MAIN_PAGE_ = sorted(
            _CONTOURS_MAIN_PAGE_,
            key=lambda _y: _CONTOURS_MAIN_PAGE_[1]
        )
        _CONTOURS_MAIN_PAGE_.reverse()

        return _CONTOURS_MAIN_PAGE_

    @classmethod
    def get_text_contours_serial_number(cls, image_with_filters, image):
        """
        @var EXPANSION_X: Предназначен для изменения координаты x контура
        @var EXPANSION_Y: Предназначен для изменения координаты y контура
        @var EXPANSION_HEIGHT: Предназначен для изменения высоты контура
        @var EXPANSION_WIDTH: Предназначен для изменения ширины контура

        @var MIN_CONTOURS_WIDTH: Минимальная ширина контура
        @var MIN_CONTOURS_HEIGHT: минимальная высота контура

        @var X_TO_WIDTH_RATIO_MAX: Коэфициент, показывающий максимальное отношение значения x к ширине
        """
        EXPANSION_X = 15
        EXPANSION_Y = 10
        EXPANSION_HEIGHT = 15
        EXPANSION_WIDTH = 25

        MIN_CONTOURS_WIDTH = 8
        MIN_CONTOURS_HEIGHT = 8

        Y_TO_HEIGHT__RATIO_MAX = 0.1
        X_TO_WIDTH_RATIO_MAX = 0.5

        _CONTOURS_SERIAL_NUMBER_ = []

        contours, hierarchy = cls._get_contours(image_with_filters)
        mask = np.zeros(image_with_filters.shape, dtype=np.uint8)

        for idx in range(len(contours)):
            x, y, w, h = cv2.boundingRect(contours[idx])
            mask[y:y + h, x:x + w] = 0

            cv2.drawContours(mask, contours, idx, (255, 255, 255), -1)

            height, width = image.shape[:2]

            condition = x - EXPANSION_X > 0
            condition &= y - EXPANSION_Y > 0
            condition &= w > MIN_CONTOURS_WIDTH
            condition &= h > MIN_CONTOURS_HEIGHT
            condition &= x < width * X_TO_WIDTH_RATIO_MAX
            condition &= y < height * Y_TO_HEIGHT__RATIO_MAX

            x -= EXPANSION_X
            y -= EXPANSION_Y
            h += EXPANSION_HEIGHT
            w += EXPANSION_WIDTH

            if condition:
                _pt1 = (x, y)
                _pt2 = (x + w - 1, y + h - 1)
                _color = (0, 255, 0)

                cv2.rectangle(
                    img=image,
                    pt1=_pt1,
                    pt2=_pt2,
                    color=_color,
                    thickness=2
                )

                _CONTOURS_SERIAL_NUMBER_.append((x, y, w, h))

        return _CONTOURS_SERIAL_NUMBER_

    @staticmethod
    def _get_contours(image: np.array):
        return cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
