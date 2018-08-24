from collections import defaultdict
from color.lab import LabMatrix


def luminance_histogram_from_matrix(matrix):
    histogram = defaultdict(int)
    for x, y in matrix:
        l = matrix.l[x][y]
        histogram[l] += 1
    return histogram


def equalize(image):
    matrix = LabMatrix.from_image(image)

    histogram = luminance_histogram_from_matrix(matrix)

    adjustments = {}

    for i, luminance in enumerate(sorted(histogram.keys())):
        relative_count = histogram[luminance] / image.size

        new_value = relative_count * 100

        if i > 0:
            previous_luminance = sorted(histogram.keys())[i - 1]
            new_value += adjustments[previous_luminance]
            new_value = min(new_value, 100.0)

        adjustments[luminance] = new_value

    for x, y in matrix:
        matrix.l[x][y] = adjustments[matrix.l[x][y]]

    matrix.apply_to(image)
