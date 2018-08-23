import math

from image import MatrixIterator


def gray_from_rgb(red, green, blue):
    return math.floor(0.299 * red + 0.587 * green + 0.114 * blue)


def convert_to_grayscale(image):
    matrix = GrayscaleMatrix.from_image(image)
    matrix.apply_to(image)


class GrayscaleMatrix:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.values = [[0] * height for _ in range(width)]

    def apply_to(self, image):
        for x, y in image.coordinates:
            image.reds[x][y] = image.greens[x][y] = image.blues[x][y] = self.values[x][y]

    def luminance(self, x, y):
        return self.values[x][y] / 255

    def set_luminance(self, x, y, value):
        self.values[x][y] = int(value * 255)

    @staticmethod
    def from_image(image):
        matrix = GrayscaleMatrix(image.width, image.height)

        for x, y in image.coordinates:
            red = image.reds[x][y]
            green = image.greens[x][y]
            blue = image.blues[x][y]

            matrix.values[x][y] = gray_from_rgb(red, green, blue)

        return matrix

    def __iter__(self):
        return MatrixIterator(self)


if __name__ == '__main__':
    import sys
    import imageio

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) == 3 else input_file

    image = imageio.read(input_file)
    convert_to_grayscale(image)
    imageio.write(image, output_file)
