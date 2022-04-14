import cv2
import numpy as np

from config import config
from matplotlib import pyplot as plt


class ImageAlignments:
    _MIN_MATCH_COUNT = 9
    _FLANN_INDEX_KDTREE = 0

    @classmethod
    def alignImages(cls, _image: np.array):
        """
        Some kind of magic ¯\_(ツ)_/¯

        Класс в текущей реализации не используется.

        Класс позволяет находить изображение по шаблону на изображении
            с помощью нахождения ключевых точек, то есть областей пикселей
            которые повторяются в двух изображениях.
        Затем класс преобразует изображения для его выделения с помощью cv2.warpPerspective().
        """

        _image_template = cv2.cvtColor(
            cv2.imread(config['passport_template'], cv2.IMREAD_COLOR),
            cv2.COLOR_BGR2GRAY
        )

        sift = cv2.SIFT_create()

        kp1, des1 = sift.detectAndCompute(_image_template, None)
        kp2, des2 = sift.detectAndCompute(_image, None)

        index_params = dict(algorithm=cls._FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)

        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1, des2, k=2)

        good = []
        img_reg = None

        for m, n in matches:
            if m.distance < 0.9 * n.distance:
                good.append(m)

        if len(good) >= cls._MIN_MATCH_COUNT:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

            matrix, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)

            height, width = _image_template.shape
            img_reg = cv2.warpPerspective(src=_image, M=matrix, dsize=(width, height))

            # Need for debugging
            # cls._debug(_image_template, _image, matrix, mask, kp1, kp2, good)

        else:
            print("Not enough matches are found - %d/%d" % (len(good), cls._MIN_MATCH_COUNT))

        return img_reg

    @classmethod
    def _debug(
            cls,
            _image_template: np.array,
            _image: np.array,
            _matrix,
            _mask,
            _kp1,
            _kp2,
            good
    ):
        """
        Метод позволяет посмотреть результат работы алгоритма поиска паспорта на изображении
        """
        matches_mask = _mask.ravel().tolist()

        h, w = _image_template.shape
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, _matrix)

        img2_debug = cv2.polylines(_image, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)

        draw_params = dict(matchColor=(0, 255, 0),
                           singlePointColor=None,
                           matchesMask=matches_mask,
                           flags=2)

        img3 = cv2.drawMatches(_image_template, _kp1, img2_debug, _kp2, good, None, **draw_params)

        plt.imshow(img3, 'gray'), plt.show()

