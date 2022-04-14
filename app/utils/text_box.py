class TextBox:
    def __init__(self):
        self._x = None
        self._y = None
        self._width = None
        self._height = None

        self._len_data = None
        self._data_type = None

        self._data = None

    def set_x(self, x: int):
        if x >= 0:
            self._x = x
            return True
        else:
            return False

    def set_y(self, y: int):
        if y >= 0:
            self._y = y
            return True
        else:
            return False

    def set_data(self, data: str):
        filter_string = ''

        count_digits = 0
        for _char in data:
            if _char.isdigit():
                filter_string += _char
                count_digits += 1
            elif _char.isupper() or _char == ' ':
                filter_string += _char

        filter_string = filter_string.strip()

        self._data = filter_string
        self._len_data = len(filter_string)

        if filter_string.isupper() and count_digits < len(filter_string) * 0.5:
            self._data_type = 'str'
        elif filter_string.isdigit() or count_digits > len(filter_string) * 0.5:
            self._data_type = 'numbers'

    def set_height(self, height: int):
        self._height = height
        return True

    def set_width(self, width: int):
        self._width = width
        return True

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def data(self) -> str:
        return self._data

    @property
    def height(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width

    @property
    def len_data(self) -> int:
        return self._len_data

    @property
    def data_type(self) -> str:
        return self._data_type
