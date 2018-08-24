from color.lab import LabColor
from color.rgb import RgbColor
from matrix import MatrixIterator


class Image:
    """Represents an image of pixels, each of one has its own RGB value.

    Public attributes:
    - width: Image width in pixels
    - height: Image height in pixels

    Public methods:
    - red: Returns red color value on (x, y). The value is between 0 and 255.
    - red_double: Returns red color value on (x, y). The value is between 0 and 0.1.
    - green: Returns green color value on (x, y). The value is between 0 and 255.
    - green_double: Returns green color value on (x, y). The value is between 0 and 0.1.
    - blue: Returns blue color value on (x, y). The value is between 0 and 255.
    - blue_double: Returns blue color value on (x, y). The value is between 0 and 0.1.
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.alphas = []
        self.reds = []
        self.greens = []
        self.blues = []
        self.coordinates = Coordinates(self)

        for _ in range(width):
            self.alphas.append([0] * height)
            self.reds.append([0] * height)
            self.greens.append([0] * height)
            self.blues.append([0] * height)

    @property
    def size(self):
        return self.width * self.height

    def has_alpha_channel(self):
        return any(any(value > 0 for value in column) for column in self.alphas)

    def get_alpha(self, x, y, result_type=int):
        if result_type not in [int, float]:
            raise ValueError('Return type must be one of: int, float')

        alpha = self.alphas[x][y]
        return alpha if result_type is int else alpha / 255

    def get_red(self, x, y, result_type=int):
        """Get red value of pixel on given coordinates.

        :param x:
            x coordinate
        :param y:
            y coordinate
        :return:
            Red value (between 0 and 255) of the pixel
        """
        if result_type not in [int, float]:
            raise ValueError('Return type must be one of: int, float')

        red = self.reds[x][y]
        return red if result_type is int else red / 255

    def get_green(self, x, y, result_type=int):
        if result_type not in [int, float]:
            raise ValueError('Return type must be one of: int, float')

        green = self.greens[x][y]
        return green if result_type is int else green / 255

    def get_blue(self, x, y, result_type=int):
        if result_type not in [int, float]:
            raise ValueError('Return type must be one of: int, float')

        blue = self.blues[x][y]
        return blue if result_type is int else blue / 255

    def get_argb(self, x, y):
        argb = self.alphas[x][y]
        argb <<= 8
        argb += self.reds[x][y]
        argb <<= 8
        argb += self.greens[x][y]
        argb <<= 8
        argb += self.blues[x][y]
        return argb

    def get_color(self, x, y):
        return RgbColor(self.reds[x][y], self.greens[x][y], self.blues[x][y])

    def get_luminance(self, x, y):
        lab = LabColor.from_rgb(self.reds[x][y], self.greens[x][y], self.blues[x][y])
        return lab.l

    def set_red(self, x, y, value):
        """
        Set red color on given coordinates. Red can be supplied either as
        int between 0 and 255, or float value between 0.0 and 1.0

        :param x:
        :param y:
        :param value:
        """
        self.reds[x][y] = value if type(value) is int else int(value * 255)

    def set_green(self, x, y, value):
        self.greens[x][y] = value if type(value) is int else int(value * 255)

    def set_blue(self, x, y, value):
        self.blues[x][y] = value if type(value) is int else int(value * 255)

    def set_rgb(self, x, y, value):
        self.reds[x][y] = (value >> 16) & 0xff
        self.greens[x][y] = (value >> 8) & 0xff
        self.blues[x][y] = value & 0xff

    def is_grayscale(self):
        return all(self.reds[x][y] == self.greens[x][y] == self.blues[x][y] for x, y in self)

    def __str__(self):
        return 'Image {} x {} px'.format(self.width, self.height)

    def __iter__(self):
        return PixelIterator(self)


class PixelIterator:

    def __init__(self, image):
        self.image = image
        self.max_x = image.width - 1
        self.max_y = image.height - 1
        self.x = 0
        self.y = 0

    def __next__(self):
        x = self.x
        y = self.y

        if y > self.max_y:
            raise StopIteration

        if x >= self.max_x:
            self.x = 0
            self.y += 1
        else:
            self.x += 1

        return self.image.get_argb(x, y)


class Coordinates:

    def __init__(self, image):
        self.image = image

    def __iter__(self):
        return MatrixIterator(self.image)
