import os
import cv2
import numpy as np
from PIL import Image
from config import config
from matplotlib import pyplot as plt


class Converter:
    @classmethod
    def jpg_convert_to_grayscale(cls, filename: str, _image: np.array) -> np.array:
        """
        Функция конвертирует изображение в ЧБ формат .jpg

        :param _image:
        :param filename:
        :return:
        """

        path_to_image = os.path.join(
            config['path_tmp'],
            filename + '_jpg_convert_to_grayscale.jpg'
        )

        cv2.imwrite(path_to_image, _image)
        img = Image.open(path_to_image)

        # Save it in PNG format
        tmp_path = os.path.join(
            config['path_tmp'],
            filename + '_jpg_convert_to_grayscale.png'
        )
        img.save(tmp_path)

        # Open PNG image and convert in LA format
        # LA - 8-bit black-white pix with ALFA channel
        img = Image.open(tmp_path).convert('LA')
        img.save(tmp_path)

        # Open and save in JPG format
        im = plt.imread(tmp_path, cv2.IMREAD_GRAYSCALE)
        im_save = cv2.convertScaleAbs(im, alpha=255.0)

        path_to_grayscale_image = os.path.join(
            config['path_tmp'],
            filename + '_jpg_convert_to_grayscale.jpg'
        )

        cv2.imwrite(path_to_grayscale_image, im_save)
        return plt.imread(path_to_grayscale_image, cv2.IMREAD_GRAYSCALE)

    @classmethod
    def convert_image_to_png(cls, filename: str, _image: np.array):
        path_to_image = os.path.join(
            config['path_tmp'],
            filename + '_convert_image_to_png.jpg'
        )

        cv2.imwrite(path_to_image, _image)
        img = Image.open(path_to_image)

        # Save it in PNG format
        tmp_path = os.path.join(
            config['path_tmp'],
            filename + '_convert_image_to_png.png'
        )
        img.save(tmp_path)

        # Open PNG image and convert in LA format
        # LA - 8-bit black-white pix with ALFA channel
        img = Image.open(tmp_path).convert('LA')
        img.save(tmp_path)

        return plt.imread(tmp_path, 0)

    @classmethod
    def get_path_image(cls, _image: np.array, filename: str):
        """
        Сохраняет изображение в tmp/ директорию и возвращает путь к изображению
        """
        path = os.path.join(
            config['path_tmp'],
            filename + '_convert_24.jpg'
        )
        cv2.imwrite(path, _image)

        return path
