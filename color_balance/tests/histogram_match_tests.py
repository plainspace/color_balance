'''
Copyright 2014 Planet Labs, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
import unittest

import numpy
import cv2

from color_balance import histogram_match as hm


class Tests(unittest.TestCase):
    def setUp(self):
        sequence_band = numpy.array(range(0,256), dtype=numpy.uint8)
        first_half_band = numpy.array(range(0,128)*2, dtype=numpy.uint8)
        second_half_band = numpy.array(range(128,256)*2, dtype=numpy.uint8)
        spread_band = numpy.array(range(0,256,32)*32, dtype=numpy.uint8)
        self.constant_band = numpy.ones(256, dtype=numpy.uint8)

        self.compressed_img = cv2.merge(
            [spread_band, first_half_band, second_half_band])

        self.sequence_img = cv2.merge([sequence_band]*3)
        self.constant_img = cv2.merge([self.constant_band]*3)

    def test_match_histogram(self):
        def luts_calculation(in_img, ref_img,
            in_mask=None, ref_mask=None):
            lut = numpy.ones(256, dtype=numpy.uint8)
            luts = [lut, 2*lut, 3*lut]
            return luts

        expected_img = cv2.merge(
            [self.constant_band,
             2*self.constant_band,
             3*self.constant_band])
        ret_img = hm.match_histogram(
            luts_calculation, self.sequence_img, self.constant_img)
        numpy.testing.assert_array_equal(ret_img, expected_img)

    def test_cdf_normalization_luts(self):
        sequence_to_compressed_luts = hm.cdf_normalization_luts(
            self.sequence_img,
            self.compressed_img)
        sequence_to_spread_lut = numpy.array(
            sorted(range(0, 256, 32) * 32),
            dtype=numpy.uint8)
        sequence_to_first_half_lut = numpy.array(
            sorted(range(0, 128) * 2),
            dtype=numpy.uint8)
        sequence_to_second_half_lut = numpy.array(
            sorted(range(128, 256) * 2),
            dtype=numpy.uint8)
        numpy.testing.assert_array_equal(sequence_to_compressed_luts,
            [sequence_to_spread_lut,
             sequence_to_first_half_lut,
             sequence_to_second_half_lut])

        compressed_to_sequence_luts = hm.cdf_normalization_luts(
            self.compressed_img,
            self.sequence_img)
        spread_to_sequence_lut = numpy.array(
            sorted(range(31, 256, 32) * 32),
            dtype=numpy.uint8)
        first_half_to_sequence_lut = numpy.array(
            range(1, 256, 2) + [255] * 128,
            dtype=numpy.uint8)
        second_half_to_sequence_lut = numpy.array(
            [0] * 128 + range(1, 256, 2),
            dtype=numpy.uint8)
        numpy.testing.assert_array_equal(compressed_to_sequence_luts,
            [spread_to_sequence_lut,
             first_half_to_sequence_lut,
             second_half_to_sequence_lut])

    def test_mean_std_luts(self):
        sequence_to_compressed_luts = hm.mean_std_luts(
            self.sequence_img,
            self.compressed_img)
        sequence_to_spread_lut = numpy.array(
            [0]*15 + range(0, 49) + range(48, 176) + range(175, 239),
            dtype=numpy.uint8)
        sequence_to_first_half_lut = numpy.array(
            [0] + sorted(range(0, 127) * 2) + [127],
            dtype=numpy.uint8)
        sequence_to_second_half_lut = numpy.array(
            [127] + sorted(range(128, 255) * 2) + [255],
            dtype=numpy.uint8)
        numpy.testing.assert_array_equal(sequence_to_compressed_luts,
            [sequence_to_spread_lut,
             sequence_to_first_half_lut,
             sequence_to_second_half_lut])

        compressed_to_sequence_luts = hm.mean_std_luts(
            self.compressed_img,
            self.sequence_img)
        spread_to_sequence_lut = numpy.array(
            range(14, 63) + range(64, 191) + range(192, 255) + [255] * 17,
            dtype=numpy.uint8)
        first_half_to_sequence_lut = numpy.array(
            range(0, 256, 2) + [255] * 128,
            dtype=numpy.uint8)
        second_half_to_sequence_lut = numpy.array(
            [0] * 128 + range(0, 256, 2),
            dtype=numpy.uint8)
        numpy.testing.assert_array_equal(compressed_to_sequence_luts,
            [spread_to_sequence_lut,
             first_half_to_sequence_lut,
             second_half_to_sequence_lut])


if __name__ == '__main__':
    unittest.main()
