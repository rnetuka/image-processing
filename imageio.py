import format.bmp as bmp


def read(path):
    if path.endswith('.bmp'):
        return bmp.read(path)


def write(image, path):
    if path.endswith('.bmp'):
        bmp.write(image, path)