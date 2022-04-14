import cv2
import numpy as np
from matplotlib import pyplot as plt


class PassportFilters:
    """
    This class implements the functionality of applying filters to passport images
    """
    @classmethod
    def execute_filters_main_page(cls, image: np.array):
        _image_execute_filters = image

        # _image_execute_filters = cls.execute_sharpness(_image_execute_filters)
        _image_execute_filters = cls.bilateral_filter(_image_execute_filters)
        # _image_execute_filters = cls.execute_clahe(_image_execute_filters)
        _image_execute_filters = cls.otsu_thresholding(_image_execute_filters)

        _image_execute_filters = cv2.medianBlur(_image_execute_filters, 3)
        _image_execute_filters = (255 - _image_execute_filters)

        _image_execute_filters = cls.execute_closing(_image_execute_filters)
        _image_execute_filters = cls.execute_opening(_image_execute_filters)
        _image_execute_filters = cls.execute_closing(_image_execute_filters)

        return _image_execute_filters

    @classmethod
    def execute_filters_series_number(cls, image: np.array):
        _image_execute_filters = image
        _image_execute_filters = cls.bilateral_filter(_image_execute_filters)
        _image_execute_filters = cls.otsu_thresholding(_image_execute_filters)

        _image_execute_filters = (255 - _image_execute_filters)

        kernel = np.ones((5, 50), np.uint8)
        _image_execute_filters = cv2.morphologyEx(_image_execute_filters, cv2.MORPH_CLOSE, kernel=kernel)

        _image_execute_filters = cls.execute_closing(_image_execute_filters)

        return _image_execute_filters

    @classmethod
    def filtering_intermediate_values(cls, image: np.array) -> np.array:
        """
        Filter removes the remaining noise

        :param image:
        :return:
        """
        image[image > 50] = 255

        return image

    @classmethod
    def execute_sharpness(cls, image: np.array) -> np.array:
        """
        Filter for increasing sharpness

        :param image:
        :return:
        """

        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        return cv2.filter2D(image, -1, kernel=kernel)

    @classmethod
    def execute_closing(cls, image: np.array) -> np.array:
        """
        Filter closing small holes inside the foreground objects,
        or small black points on the object.

        description:
        https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html

        :return:
        """
        kernel = np.ones((5, 40), np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel=kernel)

    @classmethod
    def execute_opening(cls, image: np.array) -> np.array:
        """
        Filter for noise removal

        description:
        https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html

        :param image:
        :return:
        """
        kernel = np.ones((5, 1), np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel=kernel)

    @classmethod
    def execute_erosion(cls, image: np.array) -> np.array:
        """
         Filter for what that the thickness or size of the foreground object decreases
         or simply white region decreases in the image.
         It is useful for removing small white noises (as we have seen in colorspace chapter),
         detach two connected objects etc.

         description:
         https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html

        :param image:
        :return:
        """
        kernel = np.ones((1, 1), np.uint8)
        return cv2.erode(image, kernel=kernel, iterations=2)

    @classmethod
    def execute_equalizeHist(cls, image: np.array) -> np.array:
        """
        Histogram equalized image

        description:
        https://docs.opencv.org/3.1.0/d5/daf/tutorial_py_histogram_equalization.html

        """
        cv2.imwrite('test.png', np.hstack((image, cv2.equalizeHist(image))))
        return cv2.equalizeHist(image)

    @classmethod
    def execute_clahe(cls, image: np.array) -> np.array:
        """

        """
        clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(12, 12))
        _image = clahe.apply(image)

        return _image

    @classmethod
    def execute_adaptiveThreshold(cls, image: np.array):
        """

        """
        return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7, 4)

    @classmethod
    def otsu_thresholding(cls, image: np.array):
        """

        """
        blur = cv2.GaussianBlur(image, (1, 1), 0)
        th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_OTSU)[1]

        return th3

    @classmethod
    def bilateral_filter(cls, image: np.array):
        """

        """
        return cv2.bilateralFilter(image, 30, 27, 27)

    @classmethod
    def thresholding_filter(cls, image: np.array):
        """

        """
        return cv2.threshold(image, 0, 255, cv2.THRESH_TOZERO)[1]

    @classmethod
    def clear_highlights(cls, image: np.array):
        mask = cv2.threshold(image, 250, 255, cv2.THRESH_BINARY)[1]
        result = cv2.inpaint(image, mask, 21, cv2.INPAINT_TELEA)

        return result

    @classmethod
    def black_level(cls, image: np.array):
        in_gamma = np.array([1.0, 1.0, 1.0], dtype=np.float32)
        out_black = np.array([0, 0, 0], dtype=np.float32)
        in_black = np.array([150, 150, 150], dtype=np.float32)
        in_white = np.array([255, 255, 255], dtype=np.float32)
        out_white = np.array([255, 255, 255], dtype=np.float32)

        img = np.clip((image - in_black) / (in_white - in_black), 0, 255)
        img = (img ** (1 / in_gamma)) * (out_white - out_black) + out_black
        img = np.clip(img, 0, 255).astype(np.uint8)

        return img

