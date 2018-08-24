from operations.convolution import ConvolutionMask
from unittest import TestCase


class MaskTest(TestCase):

    def setUp(self):
        self.mask = ConvolutionMask((-2, -2, -2), (-1, 0, 1), (2, 2, 2))

    def test_getitem(self):
        self.assertEqual(0, self.mask[0][0])
        self.assertEqual(-1, self.mask[-1][0])
        self.assertEqual(2, self.mask[0][1])