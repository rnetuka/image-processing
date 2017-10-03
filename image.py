from color.rgb import RgbColor


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

        for _ in range(width):
            self.alphas.append([0] * height)
            self.reds.append([0] * height)
            self.greens.append([0] * height)
            self.blues.append([0] * height)

    @property
    def size(self):
        return self.width * self.height

    def has_alpha_channel(self):
        return any(value > 0 for value in self.alphas)

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

    def get_color(self, x, y, model='rgb'):
        if model == 'rgb':
            return RgbColor(self.reds[x][y], self.greens[x][y], self.blues[x][y])

        if model == 'xyz':
            return self.get_color(x, y, model='rgb').to_xyz()

        if model == 'lab':
            return self.get_color(x, y, model='rgb').to_lab()

    def get_luminance(self, x, y):
        lab = self.get_color(x, y, model='lab')
        return lab.l

    def adjust_luminance(self, x, y, value):
        lab = self.get_color(x, y, model='lab')
        lab.l = value
        self.set_color(x, y, lab)

    def adjust_luminance_values(self, function):
        for x, y in self:
            self.adjust_luminance(x, y, function(self.get_luminance(x, y)))

    def set_red(self, x, y, value):
        """
        Set red color on given coordinates. Red can be supplied either as
        int between 0 and 255, or float value between 0.0 and 1.0

        :param x:
        :param y:
        :param value:
        """
        self.reds[x][y] = value if type(value) is int else int(value * 255)

    def adjust_red(self, x, y, func, color_type=int):
        self.set_red(x, y, func(self.get_red(x, y, color_type)))

    def adjust_reds(self, func, color_type=int):
        for x, y in self:
            self.adjust_red(x, y, func, color_type)

    def set_green(self, x, y, value):
        self.greens[x][y] = value if type(value) is int else int(value * 255)

    def adjust_green(self, x, y, func, color_type=int):
        self.set_green(x, y, func(self.get_green(x, y, color_type)))

    def adjust_greens(self, func, color_type=int):
        for x, y in self:
            self.adjust_green(x, y, func, color_type)

    def set_blue(self, x, y, value):
        self.blues[x][y] = value if type(value) is int else int(value * 255)

    def adjust_blue(self, x, y, func, color_type=int):
        self.set_blue(x, y, func(self.get_blue(x, y, color_type)))

    def adjust_blues(self, func, color_type=int):
        for x, y in self:
            self.adjust_blue(x, y, func, color_type)

    def set_color(self, x, y, color):
        if type(color) is RgbColor:
            self.reds[x][y] = color.red
            self.greens[x][y] = color.green
            self.blues[x][y] = color.blue
        else:
            self.set_color(x, y, color.to_rgb())

    def adjust_color(self, x, y, func, color_model='rgb'):
        self.set_color(x, y, func(self.get_color(x, y, model=color_model)))

    def adjust_colors(self, func, color_model='rgb'):
        for x, y in self:
            self.adjust_color(x, y, func(self.get_color(x, y, model=color_model)))

    def is_grayscale(self):
        return all(self.reds[x][y] == self.greens[x][y] == self.blues[x][y] for x, y in self)

    def __str__(self):
        return 'Image {} x {} px'.format(self.width, self.height)

    def __iter__(self):
        return MatrixIterator(self)


class MatrixIterator:

    def __init__(self, image):
        self.__image = image
        self.__x = 0
        self.__y = 0

    def __next__(self):
        x = self.__x
        y = self.__y

        if y == self.__image.height:
            raise StopIteration

        if x >= self.__image.width - 1:
            self.__x = 0
            self.__y += 1
        else:
            self.__x += 1

        return x, y


class LuminanceMatrix:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.l = [[0] * height for _ in range(width)]
        self.a = [[0] * height for _ in range(width)]
        self.b = [[0] * height for _ in range(width)]

    def apply_to(self, image):
        for x, y in self:
            rgb = RgbColor.from_lab(self.l[x][y], self.a[x][y], self.b[x][y])
            image.reds[x][y] = rgb.red
            image.greens[x][y] = rgb.green
            image.blues[x][y] = rgb.blue

    def __iter__(self):
        return MatrixIterator(self)

    @staticmethod
    def from_image(image):
        from color.lab import LabColor

        matrix = LuminanceMatrix(image.width, image.height)
        for x, y in image:
            lab_color = LabColor.from_rgb(image.reds[x][y], image.greens[x][y], image.reds[x][y])
            matrix.l[x][y] = lab_color.l
            matrix.a[x][y] = lab_color.a
            matrix.b[x][y] = lab_color.b
        return matrix
