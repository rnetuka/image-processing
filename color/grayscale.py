import math

from matrix import Matrix


class GrayscaleMatrix(Matrix):

    def __init__(self, width, height, value_type=int):
        super().__init__(width, height)
        x = 0 if value_type is int else 0.0
        self.values = [[x] * height for _ in range(width)]
        self.value_type = value_type

    def apply_to(self, image):
        for x, y in image.coordinates:
            gray = self.values[x][y] if self.value_type is int else int(self.values[x][y] * 255)
            image.reds[x][y] = image.greens[x][y] = image.blues[x][y] = gray

    def luminance(self, x, y):
        return self.values[x][y] / 255 if self.value_type is int else self.values[x][y]

    def set_luminance(self, x, y, value):
        self.values[x][y] = int(value * 255) if self.value_type is int else value

    @staticmethod
    def from_image(image, value_type=int):
        matrix = GrayscaleMatrix(image.width, image.height, value_type)

        for x, y in image.coordinates:
            red = image.reds[x][y]
            green = image.greens[x][y]
            blue = image.blues[x][y]

            gray = gray_from_rgb(red, green, blue)
            matrix.values[x][y] = gray if value_type is int else gray / 255

        return matrix

    def __getitem__(self, x):
        return self.values[x]


def gray_from_rgb(red, green, blue):
    return math.floor(0.299 * red + 0.587 * green + 0.114 * blue)


if __name__ == '__main__':
    import sys
    from color.rgb import RgbColor

    color = RgbColor.from_string(sys.argv[1])
    gray = gray_from_rgb(color.red, color.green, color.blue)

    print(color(RgbColor(gray, gray, gray)))
