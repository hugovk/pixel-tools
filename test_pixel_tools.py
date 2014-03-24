#!/usr/bin/env python
"""
Tests for pixel tools
"""
import argparse
import os
import sys
import tempfile
try:
    import unittest2 as unittest  # Python 2.6
except:
    import unittest

if os.name == "nt":
    OS_CMD = ""
else:
    OS_CMD = " ./"


def is_python_2_6():
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
        cmd = OS_CMD + cmd + \
            " -o " + self.outfile + " " + args
        print(cmd)
        os.system(cmd)

    def setUp(self):
        # Assumes some images in your temp directory...
        # self.inspec = os.path.join(tempfile.gettempdir(), "*.png")
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
        if is_python_2_6():
            unittest.main()
        else:
            unittest.main(failfast=True)

# End of file
