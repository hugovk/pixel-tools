#!/usr/bin/env python
"""
Tests for pixel tools
"""
import argparse
import os
import sys
try:
    import unittest2 as unittest  # Python 2.6
except:
    import unittest

import imp
try:
    imp.find_module("coverage")
    COVERAGE_CMD = "coverage run --append --omit */PIL/* "
except ImportError:
    COVERAGE_CMD = ""

if os.name == "nt":
    OS_CMD = ""
else:
    OS_CMD = " ./"


def is_python_2_6():
    """Python 2.6 doesn't have failfast"""
    version = sys.version_info
    if version[0] == 2 and version[1] == 6:
        return True
    else:
        return False


class TestPixelTools(unittest.TestCase):

    def remove_file(self, file):
        if os.path.isfile(file):
            os.remove(file)

    def mkdir(self, dir):
        if not os.path.exists(dir):
            os.mkdir(dir)

    def run_cmd(self, cmd, args=""):
        cmd = COVERAGE_CMD + OS_CMD + cmd + \
            " -o " + self.outfile + " " + args
        print(cmd)
        os.system(cmd)

    def setUp(self):
        self.inspec = '"111*.jpg"'
        self.infile = "11132002246_2d43b85286_o.jpg"

    def helper_set_up(self, cmd):
        self.outfile = "out_" + cmd + ".jpg"
        self.remove_file(self.outfile)
        self.assertFalse(os.path.isfile(self.outfile))

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
        self.assertNotEqual(
            os.path.getsize(self.infile),
            os.path.getsize(self.outfile))

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
        args = " --quarter -i " + self.inspec
        self.helper_set_up(cmd)

        # Act
        self.run_cmd(cmd, args)

        # Assert
        self.assertTrue(os.path.isfile(self.outfile))

    def test_factors(self):
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Tests for pixel tools",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-1', '--single',
        help="Run a single test")
    parser.add_argument(
        '-m', '--matching',
        help="Run tests with this in the name")
    args = parser.parse_args()

    if args.single:
        suite = unittest.TestSuite()

        suite.addTest(TestPixelTools(args.single))
        unittest.TextTestRunner().run(suite)

    elif args.matching:
        suite = unittest.TestSuite()

        import inspect
        methods = inspect.getmembers(
            TestPixelTools, predicate=inspect.ismethod)

        tests = []
        for method, _ in methods:
            if method.startswith("test_") and args.matching in method:
                print(method)
                suite.addTest(TestPixelTools(method))

        unittest.TextTestRunner().run(suite)

    else:
        # if is_python_2_6():
        unittest.main()
        # else:
            # unittest.main(failfast=True)

# End of file
