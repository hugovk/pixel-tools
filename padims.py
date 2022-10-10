#!/usr/bin/env python
"""
Pad images of different sizes so all end up the same size
with the same colour borders.
"""
from __future__ import annotations

import argparse
import glob
import os
import sys

from PIL import Image

import fileutils

# Optional, http://stackoverflow.com/a/1557906/724176
try:
    import timing

    assert timing  # silence warnings
except ImportError:
    pass


def sanity_check(files):
    num_files = len(files)
    print("Number of input images:", num_files)
    if num_files < 2:
        sys.exit("Not enough input images")


def pad_images(files):
    # Find max width and height
    max_width, max_height = 0, 0
    for f in files:
        width, height = Image.open(f).size
        if width > max_width:
            max_width = width
        if height > max_height:
            max_height = height

    print("Max width:\t", max_width)
    print("Max height:\t", max_height)

    fileutils.create_dir(args.outdir)
    for f in files:
        # Create a new blank image
        inew = Image.new("RGB", (max_width, max_height), args.bgcolour)
        img = Image.open(f)
        width, height = img.size
        # Calculate offsets
        if args.halign == "centre":
            left = int((max_width - width) / 2)
        elif args.halign == "left":
            left = 0
        elif args.halign == "right":
            left = max_width - width
        right = left + width

        if args.valign == "centre":
            upper = int((max_height - height) / 2)
        elif args.halign == "top":
            upper = 0
        elif args.halign == "bottom":
            upper = max_height - height
        lower = upper + height

        bbox = (left, upper, right, lower)

        inew.paste(img, bbox)
        outfile = os.path.join(args.outdir, f)
        print("Saving to", outfile)
        inew.save(outfile, quality=95)

        # sys.stdout.write('\rProcessing file ' + str(i))
    # sys.stdout.write('\r\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Pad images of different sizes so all end up "
        "the same size with the same colour borders.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-i", "--inspec", default="*.jpg", help="Input file spec")
    parser.add_argument("-o", "--outdir", default="out", help="Output directory")
    parser.add_argument("-bg", "--bgcolour", default="black", help="Background colour")
    parser.add_argument(
        "-ha",
        "--halign",
        default="centre",
        choices=("centre", "left", "right"),
        help="Horizontal alignment",
    )
    parser.add_argument(
        "-va",
        "--valign",
        default="centre",
        choices=("centre", "top", "bottom"),
        help="Vertical alignment",
    )
    args = parser.parse_args()
    print(args)

    files = glob.glob(args.inspec)
    sanity_check(files)
    pad_images(files)

# End of file
