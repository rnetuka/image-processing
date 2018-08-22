from image import Image


class BmpFormat:

    def __init__(self, image):
        self.image = image
        self.dib_header = DibHeader.from_image(image)

    @property
    def bmp_header(self):
        header = BmpHeader()
        header.type = 'BM'
        header.offset = self.dib_header.size + BmpHeader.SIZE_BITS
        header.file_size = header.offset + self.dib_header.image_data_size
        return header

    @property
    def bitmap_data(self):
        rows = []
        for y in reversed(range(self.image.height)):
            rows.append([self.image.colors[x][y] for x in range(self.image.width)])
        return rows

    @staticmethod
    def bitmap_data_padding(width, pixel_dword_size):
        padding = b''
        for i in range(4):
            if ((width * pixel_dword_size) + i) % 4 == 0:
                break
            padding += b'\x00'
        return padding

    @staticmethod
    def from_bytes(bytes):
        bmp_header = BmpHeader.from_bytes(bytes[:BmpHeader.SIZE_BITS])
        bytes = bytes[BmpHeader.SIZE_BITS:]

        dib_header_size = int.from_bytes(bytes[:4], byteorder='little')
        dib_header = DibHeader.from_bytes(bytes[:dib_header_size])
        bytes = bytes[dib_header_size:]

        image = Image(dib_header.image_width, dib_header.image_height)
        image.has_alpha = dib_header.pixel_dword_size == 4

        x = 0
        y = image.height - 1

        pixel_count = image.width * image.height
        pixel_size = dib_header.pixel_dword_size

        i = 0

        for _ in range(pixel_count):
            pixel = int.from_bytes(bytes[i : i + pixel_size], byteorder='little')
            i += pixel_size

            a = pixel >> 24 & 0xff
            r = pixel >> 16 & 0xff
            g = pixel >> 8 & 0xff
            b = pixel & 0xff

            image.alphas[x][y] = a
            image.reds[x][y] = r
            image.greens[x][y] = g
            image.blues[x][y] = b

            x += 1

            if x >= image.width:
                x = 0
                y -= 1

        return image

    def __str__(self) -> str:
        string = "BMP image (Windows Bitmap)"
        if self.dib_header is not None:
            string += " {} * {} px".format(self.dib_header.image_width, self.dib_header.image_height)
        return string

    def __bytes__(self):
        b = bytearray()
        b += bytes(self.bmp_header)
        b += bytes(self.dib_header)

        for y in reversed(range(self.image.height)):
            for x in range(self.image.width):
                b += self.image.get_argb(x, y).to_bytes(self.dib_header.pixel_dword_size, byteorder='little')

            b += BmpFormat.bitmap_data_padding(self.image.width, self.dib_header.pixel_dword_size)

        return bytes(b)


class BmpHeader:

    SIZE_BITS = 14

    def __init__(self):
        self.type = 'BM'
        self.file_size = 0
        self.offset = 0

    @staticmethod
    def from_bytes(bytes: bytes):
        header = BmpHeader()
        header.type = bytes[0:2].decode()
        header.file_size = int.from_bytes(bytes[2:6], byteorder='little')
        header.offset = int.from_bytes(bytes[10:], byteorder='little')
        return header

    def __bytes__(self) -> bytes:
        return b'' + self.type.encode() + \
               self.file_size.to_bytes(4, byteorder='little') + \
               b'\x00\x00' + \
               b'\x00\x00' + \
               self.offset.to_bytes(4, byteorder='little')


class DibHeader:

    def __init__(self):
        self.size = 0
        self.image_width = 0
        self.image_height = 0
        self.planes = 0
        self.pixel_dword_size = 0
        self.compression = 0
        self.image_data_size = 0
        self.print_resolution_horizontal = 0
        self.print_resolution_vertical = 0
        self.colors_in_palette = 0
        self.important_colors = 0

    @staticmethod
    def from_image(image):
        header = DibHeader()
        header.size = 40
        header.image_width = image.width
        header.image_height = image.height
        header.planes = 1
        header.pixel_dword_size = 4 if image.has_alpha_channel() else 3
        header.compression = 0
        header.image_data_size = ((header.pixel_dword_size * image.width) + len(BmpFormat.bitmap_data_padding(image.width, header.pixel_dword_size))) * image.height
        header.print_resolution_horizontal = 2835
        header.print_resolution_vertical = 2835
        header.colors_in_palette = 0
        header.important_colors = 0
        return header

    @staticmethod
    def from_bytes(bytes):
        header = DibHeader()
        header.size = int.from_bytes(bytes[0:4], byteorder='little')
        header.image_width = int.from_bytes(bytes[4:8], byteorder='little')
        header.image_height = int.from_bytes(bytes[8:12], byteorder='little')
        header.planes = int.from_bytes(bytes[12:14], byteorder='little')
        header.pixel_dword_size = int.from_bytes(bytes[14:16], byteorder='little') // 8
        header.compression = int.from_bytes(bytes[16:20], byteorder='little')
        header.image_data_size = int.from_bytes(bytes[20:24], byteorder='little')
        header.print_resolution_horizontal = int.from_bytes(bytes[24:28], byteorder='little')
        header.print_resolution_vertical = int.from_bytes(bytes[28:32], byteorder='little')
        header.colors_in_palette = int.from_bytes(bytes[32:36], byteorder='little')
        header.important_colors = int.from_bytes(bytes[36:40], byteorder='little')
        return header

    def __bytes__(self) -> bytes:
        return b'' + \
            self.size.to_bytes(4, byteorder='little') + \
            self.image_width.to_bytes(4, byteorder='little') + \
            self.image_height.to_bytes(4, byteorder='little') + \
            self.planes.to_bytes(2, byteorder='little') + \
            (self.pixel_dword_size * 8).to_bytes(2, byteorder='little') + \
            self.compression.to_bytes(4, byteorder='little') + \
            self.image_data_size.to_bytes(4, byteorder='little') + \
            self.print_resolution_horizontal.to_bytes(4, byteorder='little') + \
            self.print_resolution_vertical.to_bytes(4, byteorder='little') + \
            self.colors_in_palette.to_bytes(4, byteorder='little') + \
            self.important_colors.to_bytes(4, byteorder='little')


def read(path):
    with open(path, 'rb') as file:
        return BmpFormat.from_bytes(file.read())


def write(image, path):
    with open(path, 'wb') as file:
        file.write(bytes(BmpFormat(image)))


if __name__ == '__main__':
    image = read('../test.bmp')
    write(image, '../test2.bmp')

    image2 = Image(2, 2)
    image2.set_blue(0, 0, 255)
    image2.set_green(1, 0, 255)
    image2.set_red(0, 1, 255)
    image2.set_rgb(1, 1, (255, 255, 255))
    write(image2, '../test3.bmp')

    # imageio.read('test.bmp').negative().gamma_correction(0.5).save_as('test.png')