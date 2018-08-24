from copy import deepcopy


class ConvolutionMask:

    def __init__(self, *rows):
        self.size = len(rows)
        self.values = [[0] * self.size for _ in range(self.size)]

        for y, row in enumerate(rows):
            for x, value in enumerate(row):
                self.values[x][y] = value

    def get_relative(self, dx, dy):
        return self.values[dx + self.size // 2][dy + self.size // 2]


def convolve(matrix, mask):
    result = deepcopy(matrix)

    offset = mask.size // 2

    for x in range(offset, matrix.width - offset):
        for y in range(offset, matrix.height - offset):
            g = 0

            for i in range(-offset, offset + 1):
                for j in range(-offset, offset + 1):
                    g += mask.get_relative(i, j) * (matrix[x - i][y - j])

            result[x][y] = g

    return result
