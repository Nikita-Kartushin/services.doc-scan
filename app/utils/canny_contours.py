import cv2
import imutils
import numpy as np


class CannyContours:
    """
    Класс реализует получение контура объекта на изображении
        с помощью фильра Кэнии.
    """
    params = None

    @classmethod
    def get_canny_contours(cls, image: np.array, **params) -> np.array:
        cls.params = params

        _gray_image = cls._convert_to_gray(image)
        _contours = cls._execute_canny_algorithm(_gray_image)

        # Аппроксимируем контур
        _canny_contour = None
        for _contour in _contours:

            _peri = cv2.arcLength(
                curve=_contour,
                closed=True
            )
            _approx = cv2.approxPolyDP(
                closed=True,
                curve=_contour,
                epsilon=cls.params.get('epsilon') * _peri
            )

            if len(_approx) == cls.params.get('count_vertex'):
                _canny_contour = _approx

        return _canny_contour

    @classmethod
    def _convert_to_gray(cls, _image: np.array):
        _gray = cv2.cvtColor(_image, cv2.COLOR_BGR2GRAY)
        _gray = cv2.GaussianBlur(
            src=_gray,
            sigmaX=cls.params.get('gaussian_sigmaX'),
            ksize=cls.params.get('gaussian_kernel_size')
        )
        return _gray

    @classmethod
    def _execute_canny_algorithm(cls, _image: np.array):
        _edged = cv2.Canny(
            image=_image,
            threshold1=cls.params.get('canny_threshold_1'),
            threshold2=cls.params.get('canny_threshold_2')
        )

        _kernel = cv2.getStructuringElement(
            shape=cv2.MORPH_RECT,
            ksize=cls.params.get('morph_close_kernel_size')
        )
        _closed = cv2.morphologyEx(_edged, cv2.MORPH_CLOSE, _kernel)

        _contours = cv2.findContours(
            image=_closed.copy(),
            mode=cv2.RETR_EXTERNAL,
            method=cv2.CHAIN_APPROX_SIMPLE
        )
        _contours = imutils.grab_contours(_contours)

        return _contours
