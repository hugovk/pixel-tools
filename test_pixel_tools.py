#!/usr/bin/env python
"""
Tests for pixel tools
"""
from __future__ import annotations

import argparse
import imp
import os
import sys
import unittest

import pytest

try:
    imp.find_module("coverage")
    COVERAGE_CMD = "coverage run --append --omit */site-packages/*,*pypy* "
except ImportError:
    COVERAGE_CMD = "python3 "


def remove_file(file):
    if os.path.isfile(file):
        os.remove(file)


def mkdir(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)


class TestPixelTools(unittest.TestCase):
    def run_cmd(self, cmd, args="", include_outfile=True):
        cmd = COVERAGE_CMD + cmd + " " + args
        if include_outfile:
            cmd += " -o " + self.outfile
        print(cmd)
        os.system(cmd)

    def setUp(self):
        self.inspec = '"111*.jpg"'
        self.infile = "11132002246_2d43b85286_o.jpg"

    def assert_deleted(self, filename):
        remove_file(filename)
        self.assertFalse(os.path.isfile(filename))

    def helper_set_up(self, cmd, extension="jpg"):
        self.outfile = f"out_{cmd}.{extension}"
        self.assert_deleted(self.outfile)

    @pytest.mark.skipif(sys.platform == "linux", reason="No Helvetica font")
    def test_annotate(self):
        """Just test with some options and check an output file is created"""
        # Arrange
        cmd = "annotate.py"
        args = "-c RED -p 200 " + self.infile + " " + '"A"'
        self.helper_set_up(cmd)

        # Act
        self.run_cmd(cmd, args)

        # Assert
        self.assertTrue(os.path.isfile(self.outfile))
        self.assertNotEqual(os.path.getsize(self.infile), os.path.getsize(self.outfile))

    def test_blockit(self):
        """Just test with some options and check an output file is created"""
        # Arrange
        cmd = "blockit.py"
        args = "-i " + self.inspec
        self.helper_set_up(cmd)

        # Act
        self.run_cmd(cmd, args)

        # Assert
        self.assertTrue(os.path.isfile(self.outfile))

    def test_colour_clock(self):
        """Just test with some options and check an output file is created"""
        # Arrange
        cmd = "colour_clock.py"
        args = self.inspec
        self.helper_set_up(cmd)

        # Act
        self.run_cmd(cmd, args)

        # Assert
        self.assertTrue(os.path.isfile(self.outfile))

    def test_contact_sheet(self):
        """Just test with some options and check an output file is created"""
        # Arrange
        cmd = "contact_sheet.py"
        args = " --quarter -i " + self.inspec + " --aspect_ratio 16,9"
        self.helper_set_up(cmd)

        # Act
        self.run_cmd(cmd, args)

        # Assert
        self.assertTrue(os.path.isfile(self.outfile))

    def test_deframify(self):
        """Just test with some options and check an output file is created"""
        # Arrange
        cmd = "deframify.py"
        args = " -i " + self.inspec

        self.outfile = "out-deframify.mp4"
        self.assert_deleted(self.outfile)

        # Act
        self.run_cmd(cmd, args)

        # Assert
        self.assertTrue(os.path.isfile(self.outfile))

    # def test_face_cropper(self):
    #     # Arrange
    #     """Just test with some options and check an output file is created"""
    #     # Arrange
    #     cmd = "face_cropper.py"
    #     outdir = "face_cropper"
    #     args = " -c haarcascade_frontalface_alt.xml -i " + self.inspec + \
    #        " -o " + outdir
    #     self.helper_set_up(cmd)
    #     outspec = os.path.join(outdir, self.inspec.strip('"'))
    #     import glob
    #
    #     # Act
    #     self.run_cmd(cmd, args, include_outfile=False)
    #
    #     # Assert
    #     outfiles = glob.glob(outspec)
    #     self.assertGreater(len(outfiles), 0)

    def test_factors_unit(self):
        # Arrange
        import factors

        # Act
        mid1 = factors.get_middleish_factor(1)
        mid4 = factors.get_middleish_factor(4)
        mid12 = factors.get_middleish_factor(12)
        mid100 = factors.get_middleish_factor(100)

        # Assert
        self.assertEqual(mid1, 1)
        self.assertEqual(mid4, 2)
        self.assertEqual(mid12, 3)
        self.assertEqual(mid100, 10)

    def test_image_packer(self):
        """Just test with some options and check an output file is created"""
        # Arrange
        cmd = "image_packer.py"
        args = " --largest_first -s 10000,10000 -i " + self.inspec
        self.helper_set_up(cmd)

        # Act
        self.run_cmd(cmd, args)

        # Assert
        self.assertTrue(os.path.isfile(self.outfile))

    def test_image_packer_tuple_arg(self):
        """Test tuple_arg works as expected"""
        # Arrange
        from image_packer import tuple_arg

        # Act
        out1 = tuple_arg("12, 34")
        out2 = tuple_arg("12,34")
        out3 = tuple_arg("12:34")
        out4 = tuple_arg("12x34")

        # Assert
        self.assertEqual(out1, (12, 34))
        self.assertEqual(out2, (12, 34))
        self.assertEqual(out3, (12, 34))
        self.assertEqual(out4, (12, 34))
        with self.assertRaises(argparse.ArgumentTypeError):
            tuple_arg("1234")

    def test_normalise_mean(self):
        """Just test with some options and check an output file is created"""
        # Arrange
        from normalise import mean

        # Act
        out = mean([1, 2, 3])

        # Assert
        self.assertEqual(out, 2)

    def test_og_image(self):
        """Check an output file is created"""
        # Arrange
        cmd = "og_image.py --logo tests/python-logo.png"
        self.helper_set_up("og-image", extension="png")

        # Act
        self.run_cmd(cmd, include_outfile=True)

        # Assert
        self.assertTrue(os.path.isfile(self.outfile))

    def test_padims(self):
        """Just test with some options and check an output file is created"""
        # Arrange
        cmd = "padims.py"
        outdir = "padims"
        args = " -i " + self.inspec + " -o " + outdir
        self.helper_set_up(cmd)
        import glob

        # Act
        self.run_cmd(cmd, args, include_outfile=False)

        # Assert
        inspec = self.inspec.strip('"')
        first_infile = glob.glob(inspec)[0]
        first_outfile = os.path.join(outdir, first_infile)
        self.assertTrue(os.path.isdir(outdir))
        self.assertTrue(os.path.isfile(first_outfile))

    def test_pixelator_units(self):
        # Arrange
        import pixelator

        # Act
        text = pixelator.encode_time()

        # Assert
        self.assertGreater(len(text), 0)

    def test_pixelator(self):
        """Just test with some options and check an output file is created"""
        # Arrange
        cmd = "pixelator.py"
        args = " -i " + self.inspec + " -b auto -n mode "
        self.helper_set_up(cmd)

        # Act
        self.run_cmd(cmd, args)

        # Assert
        self.assertTrue(os.path.isfile(self.outfile))

    def test_pixelator_random(self):
        """Just test with some options and check an output file is created"""
        # Arrange
        cmd = "pixelator.py"
        args = " -i " + self.inspec + " -b auto -n mode -e random"
        self.helper_set_up(cmd)

        # Act
        self.run_cmd(cmd, args)

        # Assert
        self.assertTrue(os.path.isfile(self.outfile))

    def test_slitscan(self):
        """Just test with some options and check an output file is created"""
        # Arrange
        cmd = "slitscan.py"
        self.helper_set_up(cmd)
        args = " -i " + self.inspec + " --supercombo "
        filelist = [
            "out-horizontal-eiriksmagick-greedy.jpg",
            "out-horizontal-fixed.jpg",
            "out-vertical-fixed-greedy.jpg",
            "out-horizontal-eiriksmagick.jpg",
            "out-vertical-eiriksmagick-greedy.jpg",
            "out-vertical-fixed.jpg",
            "out-horizontal-fixed-greedy.jpg",
            "out-vertical-eiriksmagick.jpg",
        ]
        for file in filelist:
            self.assert_deleted(file)

        # Act
        self.run_cmd(cmd, args)

        # Assert
        for file in filelist:
            self.assertTrue(os.path.isfile(file))
