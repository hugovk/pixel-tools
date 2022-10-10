#!/usr/bin/env python
"""
Normalise input images.
"""
from __future__ import annotations

import glob
import os
import shutil

from PIL import Image, ImageOps


def mean(values):
    """Computes the arithmetic mean of a list of numbers.

    >>> print(mean([20, 30, 70]))
    40.0
    """
    return sum(values, 0.0) / len(values)


def mode(values):
    """Computes the mode of a list of numbers.

    >>> print(mode([1, 2, 2, 3, 70]))
    2
    """
    d = {}
    mode, freq = 0, 0
    for i in values:
        if i in d:
            d[i] += 1
        else:
            d[i] = 1

        if d[i] > freq:
            mode = i
            freq = d[i]

    # print("Found mode", mode, "frequency", freq)
    return mode


def remove_non_ascii(s):
    return "".join(i for i in s if ord(i) < 128)


def normalise_files(spec, files, normalise, temp_dir):
    if not normalise:
        normalise = "mode"
    widths, heights = [], []

    normalise_needed = False
    print("Checking sizes")
    for i, f in enumerate(files):
        print(f)
        try:
            width, height = Image.open(f).size
            # print(width, "x, height, height * 1.0/width, f)
            widths.append(width)
            heights.append(height)
            if (
                not normalise_needed
                and i > 0
                and (width != widths[0] or height != heights[0])
            ):
                normalise_needed = True
        except Exception as e:
            print("Ignoring problem file:", f)
            print(str(e))
            print(repr(e))
            # Add dummy data
            widths.append(0)
            heights.append(0)
            continue

    if not normalise_needed:
        print("Images all the same size. Normalising not needed.")
        return spec

    # Else we need to normalise
    if normalise == "mode":
        width = mode(widths)
        height = mode(heights)
        print("Mode:", width, "x", height)
        size = (width, height)
    elif normalise == "mean":
        width = int(mean(widths))
        height = int(mean(heights))
        print("Mean:", width, "x", height)
        size = (width, height)
    else:
        width, height = normalise.split(",")
        size = (int(width), int(height))

    if not os.path.isdir(temp_dir):
        os.mkdir(temp_dir)

    for i, f in enumerate(files):
        if widths[i] == 0 and heights[i] == 0:
            # Ignore problem file
            continue
        print(widths[i], "x", heights[i], f)
        progress = str(i) + "/" + str(len(files))

        if (widths[i], heights[i]) == size:
            print(progress, "Don't need to convert")
            shutil.copy2(f, temp_dir)
        else:
            print(progress, "Need to convert")
            filename = remove_non_ascii(os.path.split(f)[1])
            temp_file = os.path.join(temp_dir, filename)

            try:
                im = Image.open(f)
                # im = im.resize(size)
                im = ImageOps.fit(im, size, Image.ANTIALIAS)
                im.save(temp_file, quality=95)
            except Exception as e:
                print("Ignoring problem file:", filename)
                print(str(e))
                print(repr(e))
                continue

    # spec = os.path.split(spec)[1]
    # spec = os.path.join(temp_dir, spec)
    spec = os.path.join(temp_dir, "*")
    return spec


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Normalise images.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-i", "--inspec", default="*.jpg", help="Input file spec")
    parser.add_argument(
        "-o", "--outdir", default="temp_normalised", help="Output directory"
    )
    parser.add_argument(
        "-n",
        "--normalise",
        default="mode",
        help="If images are different sizes, normalise them first. "
        "[mode|mean|width,height]",
    )
    args = parser.parse_args()
    print(args)

    # If inspec is dir, append *.jpg
    inspec = args.inspec
    if os.path.isdir(inspec):
        inspec = os.path.join(inspec, "*.jpg")

    if not os.path.isdir(args.outdir):
        os.mkdir(args.outdir)

    files = glob.glob(args.inspec)
    print(len(files), "files found")
    inspec = normalise_files(args.inspec, files, args.normalise, args.outdir)
    print("Done. Normalised images:", inspec)

# End of file
