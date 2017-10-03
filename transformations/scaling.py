import math

from image import Image


def is_in_bounds(i, max_i):
    return 0 <= i < max_i


def neighbors(image, x, y):
    vectors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
    result = []
    for vector in vectors:
        new_x = x + vector[0]
        new_y = y + vector[1]
        if is_in_bounds(new_x, image.width()) and is_in_bounds(new_y, image.height()):
            result.append((new_x, new_y))
    return result


def resize(image, width, height):
    pass


def scale(image, delta=1.0):
    new_width = math.ceil(image.width() * delta)
    new_height = math.ceil(image.height() * delta)

    scaled = Image(new_width, new_height)

    if delta < 1.0:
        for x, y in image:
            pass
