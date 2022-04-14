from typing import List
from utils.text_box import TextBox


class PassportParser:
    """
    Класс предназначен для парсинга строки, полученной tesseract OCR,
    содержащий текст, который распознан на изображении.
    """
    @classmethod
    def parse_main_page(cls, data: List[TextBox], width, height) -> dict:
        full_name = cls._get_full_name(data, height, width)
        date_of_birth = cls._get_date_of_birth(data, height)
        date_of_issue = cls._get_date_of_issue(data, height)
        place_of_birth = cls._get_place_of_birth(data, height)
        name_issue_department = cls._get_name_issue_department(data, height)
        number_issue_department = cls._get_number_issue_department(data, height)

        passport_data = {
            'full_name': full_name,
            'date_of_birth': date_of_birth,
            'date_of_issue': date_of_issue,
            'place_of_birth': place_of_birth,
            'name_issue_department': name_issue_department,
            'number_issue_department': number_issue_department,
        }

        return passport_data

    @classmethod
    def parse_series_number(cls, data: List[TextBox]) -> str:
        series_number = ''
        for text_box in data:
            series_number = text_box.data

        return series_number

    @classmethod
    def _get_full_name(cls, data, height, width):
        Y_TO_HEIGHT_RATIO_MAX = 0.7
        Y_TO_HEIGHT_RATIO_MIN = 0.5
        DATA_TYPE = 'str'

        full_name = ''
        for text_box in data:
            is_true_condition = text_box.data_type == DATA_TYPE
            is_true_condition &= text_box.y < height * Y_TO_HEIGHT_RATIO_MAX
            is_true_condition &= text_box.y > height * Y_TO_HEIGHT_RATIO_MIN

            if is_true_condition:
                # Если мы задеваем контур с полом гражданина, то пропускаем этот контур
                if text_box.len_data <= 3 and text_box.y > height * 0.25 and text_box.x < width * 0.5:
                    continue

                full_name += text_box.data + ' '

        full_name.strip()
        return full_name

    @classmethod
    def _get_date_of_birth(cls, data, height):
        Y_TO_HEIGHT_RATIO_MIN = 0.5
        DATA_TYPE = 'numbers'
        LEN_DATA = 8

        date_of_birth = ''
        for text_box in data:
            is_true_condition = text_box.len_data == LEN_DATA
            is_true_condition &= text_box.data_type == DATA_TYPE
            is_true_condition &= text_box.y > height * Y_TO_HEIGHT_RATIO_MIN

            if is_true_condition:
                date_of_birth = text_box.data
                date_of_birth = date_of_birth[:2] + '.' + date_of_birth[2:]
                date_of_birth = date_of_birth[:5] + '.' + date_of_birth[5:]

        return date_of_birth

    @classmethod
    def _get_place_of_birth(cls, data, height):
        Y_TO_HEIGHT_RATIO_MIN = 0.7
        DATA_TYPE = 'str'
        MIN_WIDTH = 120

        _data = data.copy()
        _data.reverse()

        place_of_birth = ''
        for text_box in data:
            is_true_condition = text_box.width > MIN_WIDTH
            is_true_condition &= text_box.data_type == DATA_TYPE
            is_true_condition &= text_box.y > height * Y_TO_HEIGHT_RATIO_MIN

            if is_true_condition:
                place_of_birth += text_box.data + ' '

        place_of_birth.strip()
        return place_of_birth

    @classmethod
    def _get_date_of_issue(cls, data, height):
        Y_TO_HEIGHT_RATIO_MAX = 0.4
        DATA_TYPE = 'numbers'
        LEN_DATA = 8

        number_issue_department = ''
        for text_box in data:
            is_true_condition = text_box.len_data == LEN_DATA
            is_true_condition &= text_box.data_type == DATA_TYPE
            is_true_condition &= text_box.y < height * Y_TO_HEIGHT_RATIO_MAX

            if is_true_condition:
                number_issue_department = text_box.data
                number_issue_department = number_issue_department[:2] + '.' + number_issue_department[2:]
                number_issue_department = number_issue_department[:5] + '.' + number_issue_department[5:]

        return number_issue_department

    @classmethod
    def _get_name_issue_department(cls, data, height):
        Y_TO_HEIGHT_RATIO_MAX = 0.2
        DATA_TYPE = 'str'

        name_issue_department = ''
        for text_box in data:
            is_true_condition = text_box.data_type == DATA_TYPE
            is_true_condition &= text_box.y < height * Y_TO_HEIGHT_RATIO_MAX

            if is_true_condition:
                name_issue_department += text_box.data + ' '

        name_issue_department.strip()
        return name_issue_department

    @classmethod
    def _get_number_issue_department(cls, data, height):
        Y_TO_HEIGHT_RATIO_MAX = 0.4
        DATA_TYPE = 'numbers'
        LEN_DATA = 6

        number_issue_department = ''
        for text_box in data:
            is_true_condition = text_box.len_data == LEN_DATA
            is_true_condition &= text_box.data_type == DATA_TYPE
            is_true_condition &= text_box.y < height * Y_TO_HEIGHT_RATIO_MAX

            if is_true_condition:
                number_issue_department = text_box.data
                number_issue_department = number_issue_department[:3] + '-' + number_issue_department[3:]

        return number_issue_department
