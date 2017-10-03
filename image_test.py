import unittest

from unittest import TestCase
from image import Image


class ImageTest(TestCase):

    def setUp(self):
        self.image = Image(100, 80)
        self.image.set_red(0, 0, 255)
        self.image.set_green(0, 0, 153)
        self.image.set_blue(0, 0, 240)

    def test_get_red_int(self):
        red = self.image.red(0, 0)
        self.assertEqual(255, red)

    def test_get_red_float(self):
        red = self.image.red(0, 0, type=float)
        self.assertEqual(1.0, red)

    def test_get_green_int(self):
        green = self.image.green(0, 0)
        self.assertEqual(153, green)

    def test_get_green_float(self):
        green = self.image.green(0, 0, type=float)
        self.assertEqual(0.6, green)


if __name__ == '__main__':
    unittest.main()