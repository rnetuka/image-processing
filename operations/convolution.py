import sys

from operations.monochrome import GrayscaleMatrix


def normalize(value, lowerBound, upperBound):
    return (value - lowerBound) / (upperBound - lowerBound)


def apply(matrix, mask):
    result = GrayscaleMatrix(matrix.width, matrix.height)

    offset = len(mask) // 2

    for x in range(offset, matrix.width - offset):
        for y in range(offset, matrix.height - offset):
            g = 0

            for i in range(-offset, offset):
                for j in range(-offset, offset):
                    g += mask[i][j] * matrix.luminance(x - i, y - j)

            result.set_luminance(x, y, g)

    return result


def apply_all(matrix, *masks):
    result = GrayscaleMatrix(matrix.width, matrix.height)

    for mask in masks:
        partial_result = apply(matrix, mask)

        for x, y in result:
            result.values[x][y] = abs(result.luminance(x, y)) + abs(partial_result.luminance(x, y))

    lowest = sys.maxsize
    highest = -1

    for x, y in result:
        g = result.luminance(x, y)

        if g > highest:
            highest = g

        if g < lowest:
            lowest = g

    for x, y in result:
        result.set_luminance(x, y, normalize(result.luminance(x, y), lowest, highest))

    return result
