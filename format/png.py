class PngFormat:

    def __init__(self, image):
        self.image = image

    @staticmethod
    def name():
        return 'Portable Network Graphics'

    @staticmethod
    def mime_type():
        return 'image/png'

    @staticmethod
    def extensions():
        return ['.png']

    @property
    def image_header(self) -> ImageHeader:
        ihdr = ImageHeader()
        ihdr.width = self.image.width
        ihdr.height = self.image.height

        if self.image.is_grayscale():
            ihdr.color_type = ImageHeader.COLOR_TYPE_GREYSCALE_WITH_ALPHA if self.image.has_alpha_channel() else ImageHeader.COLOR_TYPE_GREYSCALE
        else:
            ihdr.color_type = ImageHeader.COLOR_TYPE_TRUECOLOR_WITH_ALPHA if self.image.has_alpha_channel() else ImageHeader.COLOR_TYPE_TRUECOLOR

        ihdr.bit_depth = 0
        ihdr.compression_method = 0
        ihdr.filter_method = 0
        ihdr.interlace_method = 0
        return ihdr

    def __bytes__(self):
        b = b'\x89PNG\r\n\x1a\n'
        b += bytes(self.image_header)
        b += bytes(ImageData(self.image))
        b += bytes(ImageTrailer())
        return b


class ImageHeader:

    COLOR_TYPE_GREYSCALE = 0
    COLOR_TYPE_TRUECOLOR = 2
    COLOR_TYPE_INDEXED_COLOR = 3
    COLOR_TYPE_GREYSCALE_WITH_ALPHA = 4
    COLOR_TYPE_TRUECOLOR_WITH_ALPHA = 6

    def __init__(self):
        self.width = 0
        self.height = 0
        self._bit_depth = 0
        self._color_type = None
        self.compression_method = 0
        self.filter_method = 0
        self.interlace_method = 0

    @property
    def length(self) -> int:
        return 13

    @property
    def bit_depth(self) -> int:
        return self._bit_depth

    @bit_depth.setter
    def bit_depth(self, value: int):
        if value not in [1, 2, 4, 8, 16]:
            raise ValueError('Bit depth not allowed: {}. Allowed values are 1, 2, 4, 8, 16'.format(value))

        self._bit_depth = value

    @property
    def color_type(self):
        return self._color_type

    @color_type.setter
    def color_type(self, value: int):
        if value not in [0, 2, 3, 4, 6]:
            raise ValueError('Color type {} not allowed. Allowed values are: 0 (greyscale), 2 (truecolor), '
                             '3 (indexed color), 4 (greyscale with alpha) or 6 (truecolor with alpha)'.format(value))

        self._color_type = value

    @property
    def crc(self):
        return 0

    def __str__(self) -> str:
        return 'IHRD'

    def __bytes__(self):
        bytes = self.length.to_bytes(4, byteorder='big')
        bytes += str(self).encode('ascii')
        bytes += self.width.to_bytes(4, byteorder='big')
        bytes += self.height.to_bytes(4, byteorder='big')
        bytes += self.bit_depth.to_bytes(1, byteorder='big')
        bytes += self.color_type.to_bytes(1, byteorder='big')
        bytes += self.compression_method.to_bytes(1, byteorder='big')
        bytes += self.filter_method.to_bytes(1, byteorder='big')
        bytes += self.interlace_method.to_bytes(1, byteorder='big')
        bytes += self.crc.to_bytes(4, byteorder='big')
        return bytes


class Palette:

    def __init__(self):
        self.colors = []

    def add_entry(self, red, green, blue):
        self.colors.append((red, green, blue))

    @property
    def length(self) -> int:
        return len(self.colors)

    @property
    def crc(self) -> int:
        return 0

    @staticmethod
    def from_colors(colors: list):
        if not 0 <= len(colors) < 256:
            raise ValueError('At most 256 colors are allowed. Got {}.'.format(len(colors)))

        palette = Palette()
        palette.colors = colors
        return palette

    def __bytes__(self) -> bytes:
        if self.length == 0:
            raise 'Invalid PLTE. Must have between 1 and 256 entries. Currently has {}.'.format(self.length)

        bytes = self.length.to_bytes(4, byteorder='big')
        bytes += b'PLTE'
        for color in self.colors:
            bytes += color[0].to_bytes(1, byteorder='big')
            bytes += color[1].to_bytes(1, byteorder='big')
            bytes += color[2].to_bytes(1, byteorder='big')
        bytes += self.crc.to_bytes(4, byteorder='big')
        return bytes


class ImageData:

    def __init__(self, image):
        self.image = image

    @property
    def length(self):
        return 0

    def __str__(self):
        return 'IDAT'

    def __bytes__(self):
        bytes = b''
        bytes += str(self).encode('ascii')

        return bytes


class ImageTrailer:

    def __str__(self):
        return 'IEND'

    def __bytes__(self):
        return str(self).encode('ascii')