#!/usr/bin/env python
"""
Python/PIL version of eirikmagick.sh with extra options
"""
from __future__ import annotations

import argparse
import glob
import os
import sys

from PIL import Image

# PIL jpeg saving: Maximum supported image dimension is 65500 pixels
MAX_DIMENSION = 65500


def sanity_check(files):
    num_files = len(files)
    print("Input images:\t", num_files)
    if num_files < 2:
        sys.exit("Not enough input images")


def make_image(files):
    if not args.outfile:
        args.outfile = "out-" + args.direction + "-" + args.mode
        if args.greedy:
            args.outfile += "-greedy"
        args.outfile += ".jpg"
    print("Outfile:", args.outfile)

    outfile = args.outfile
    # Assume all images are the same dimension
    in_width, in_height = Image.open(files[0]).size

    if args.direction == "vertical" or args.direction == "v":
        vertical = True
        horizontal = False
        number_of_slices = in_width
    elif args.direction == "horizontal" or args.direction == "h":
        vertical = False
        horizontal = True
        number_of_slices = in_height

    if args.greedy:
        number_of_slices = len(files)
    elif len(files) > number_of_slices:
        print(
            "WARNING: Too many input files. Only",
            number_of_slices,
            "will be used (picked proportionally).",
        )
        # files = files[:number_of_slices]
        chosen = []
        ratio = len(files) / float(number_of_slices)
        for i in range(0, number_of_slices):
            chosen.append(files[int(i * ratio)])  # pick proportionally
        files = chosen  # update original list

    print("In width:\t", in_width)
    print("In height:\t", in_height)

    if args.thickness:
        slice_thickness = args.thickness
    else:
        slice_thickness = int(number_of_slices / len(files))
    if slice_thickness == 0:
        slice_thickness = 1

    if vertical:
        print("Slice width:\t", slice_thickness)
        out_width = slice_thickness * len(files)
        out_height = in_height
        print("Out width:\t", out_width)
        upper = 0
        lower = in_height
    elif horizontal:
        print("Slice height:\t", slice_thickness)
        out_width = in_width
        out_height = slice_thickness * len(files)
        print("Out height:\t", out_height)
        left = 0
        right = in_width

    # Reset width and height for greedy eirkismagick;
    # don't want to go off the edge
    if args.mode == "eiriksmagick" and args.greedy:
        out_width = in_width
        out_height = in_height

    # print("Image size:", isize)
    if out_width > MAX_DIMENSION:
        sys.exit(
            "Output image is too wide: "
            + str(out_width)
            + " (Max: "
            + str(MAX_DIMENSION)
            + "). Tip: avoid --greedy or use a smaller --thickness."
        )
    if out_height > MAX_DIMENSION:
        sys.exit(
            "Output image is too high: "
            + str(out_height)
            + " (Max: "
            + str(MAX_DIMENSION)
            + "). Tip: avoid --greedy or use a smaller --thickness."
        )

    if args.mode == "fixed":
        if vertical:
            left = (in_width * args.fixedposition / 100) - (
                slice_thickness * args.fixedposition / 100
            )
            right = left + slice_thickness
        elif horizontal:
            upper = (in_height * args.fixedposition / 100) - (
                slice_thickness * args.fixedposition / 100
            )
            lower = upper + slice_thickness

    if args.mode == "all" and args.keepfree:
        loops = number_of_slices
        from psutil import virtual_memory  # for caching
    else:
        loops = 1

    img_cache = []
    cache_full = False
    for j in range(loops):
        print("Creating:\t" + str(j + 1) + "/" + str(loops))
        if args.mode == "all":
            if vertical:
                left = int(in_width * j / loops - slice_thickness / 2)
                right = left + slice_thickness
            elif horizontal:
                upper = int(in_height * j / loops - slice_thickness / 2)
                lower = upper + slice_thickness
            outfile = args.outfile + "-" + str(j).zfill(6) + ".jpg"

        if os.path.exists(outfile):
            print("File exists, skipping:", outfile)
            continue

        # Create the new image. The background doesn't have to be white
        white = (255, 255, 255)
        inew = Image.new("RGB", (out_width, out_height), white)

        if args.mode != "eiriksmagick":
            crop_bbox = (int(left), int(upper), int(right), int(lower))

        for i, filename in enumerate(files):
            sys.stdout.write("\rProcessing file " + str(i + 1) + "/" + str(len(files)))
            if vertical:
                left = i * slice_thickness
                right = left + slice_thickness
            elif horizontal:
                upper = i * slice_thickness
                lower = upper + slice_thickness
            paste_bbox = (int(left), int(upper), int(right), int(lower))
            if args.mode == "eiriksmagick":
                crop_bbox = paste_bbox
            # print(bbox)
            # try:
            # # Read in an image and resize appropriately

            # TODO when caching
            # 1. chop image, and only keep remainder in cache
            # 2. can then add more stuff to cache

            if (crop_bbox[2] > in_width) or (crop_bbox[3] > in_height):
                # Don't if crop_box is outside the image
                continue

            if args.mode == "all" and args.keepfree and not cache_full:
                free_megabytes = virtual_memory().free / (1024 * 1024)
                if free_megabytes < args.keepfree:
                    cache_full = True

            if len(img_cache) > i:
                # print("load from cache")
                img = img_cache[i].crop(crop_bbox)
            elif loops > 1 and not cache_full:
                # print("add to cache")
                img_cache.append(Image.open(filename))
                # img = img.crop(crop_bbox)
                img = img_cache[i].crop(crop_bbox)
            else:
                # print("don't use cache")
                img = Image.open(filename).crop(crop_bbox)

            # except:
            # break
            inew.paste(img, paste_bbox)
            # count += 1
        sys.stdout.write("\r\n")

        print("Saving to", outfile)
        inew.save(outfile, quality=95)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Slice input files into an output file. Requires PIL.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-i", "--inspec", default="*.jpg", help="Input file spec")
    parser.add_argument(
        "-v", "--reverse", action="store_true", help="Reverse list of input files"
    )
    parser.add_argument("-o", "--outfile", help="Output file name")
    parser.add_argument(
        "-m",
        "--mode",
        default="eiriksmagick",
        choices=("eiriksmagick", "fixed", "all"),
        help="How to slice images. 'fixed' takes slices from a fixed position "
        "in each image (e.g. the centre), 'eiriksmagick' takes a different "
        "slice from each, moving from left to right (or top to bottom). "
        "Both create a single image. 'all' makes lots of image, each with "
        "slices from the same place.",
    )
    parser.add_argument(
        "-p",
        "--fixedposition",
        type=int,
        default=50,
        help="When using `--mode fixed`, this is the percentage "
        "across the image to take slice.",
    )
    parser.add_argument(
        "-d",
        "--direction",
        default="vertical",
        choices=("vertical", "v", "horizontal", "h"),
        help="Direction to slitify",
    )
    parser.add_argument(
        "-t",
        "--thickness",
        type=int,
        help="Slit thickness in pixels. "
        "Default is to calculate based on number of input images.",
    )
    parser.add_argument(
        "-g",
        "--greedy",
        action="store_true",
        help="Use every input file even if more than the width or height",
    )
    parser.add_argument(
        "--supercombo",
        action="store_true",
        help="Do most of the combinations, apart from --mode all. "
        "Uses default filenames.",
    )
    parser.add_argument(
        "-kf",
        "--keepfree",
        type=int,
        help="Cache but keep this much MB free when initially filling cache.",
    )
    args = parser.parse_args()

    # Optional, http://stackoverflow.com/a/1557906/724176
    try:
        import timing

        assert timing  # silence warnings
    except ImportError:
        pass
    print(args)

    files = glob.glob(args.inspec)
    sanity_check(files)
    if args.reverse:
        files = files[::-1]
    if not args.supercombo:
        make_image(files)
    else:  # Super Combo!
        for args.mode in "eiriksmagick", "fixed":
            for args.direction in "horizontal", "vertical":
                for args.greedy in True, False:
                    args.outfile = None
                    make_image(files)

# End of file
