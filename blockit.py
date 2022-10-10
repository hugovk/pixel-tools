#!/usr/bin/env python
"""
Create an image from random blocks of other images.

Can do a grid of squares or rectangles, or vertical or horizontal stripes.
"""
from __future__ import annotations

import argparse
import random
import sys
from operator import itemgetter

from PIL import Image

import fileutils


def save_im(im):
    if args.show:
        print("Show image")
        im.show()
    if not args.outfile:
        args.outfile = (
            "blockit_b-"
            + str(args.blockwidth)
            + "x"
            + str(args.blockheight)
            + "_"
            + str(args.outwidth)
            + "x"
            + str(args.outheight)
            + ".jpg"
        )

    print("Save image to " + args.outfile)
    try:
        im.save(args.outfile)
    except OSError:
        print("Cannot save")


def get_rand_point(image_dimension, block_dimension):
    offset = image_dimension - block_dimension
    if offset <= 0:
        rand_point = 0
    else:
        rand_point = random.randrange(0, offset)
    return rand_point


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create image from blocks of other images. Requires PIL.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-i", "--inspec", default="2*.jpg", help="Input file spec")
    parser.add_argument(
        "-r", "--recursive", action="store_true", help="Recurse directories"
    )
    parser.add_argument(
        "-o", "--outfile", help="Output filename"  # default='blockit.jpg',
    )
    parser.add_argument(
        "-W",
        "--outwidth",
        metavar="pixels",
        type=int,
        default=640,
        help="Width of output image",
    )
    parser.add_argument(
        "-H",
        "--outheight",
        metavar="pixels",
        type=int,
        default=320,
        help="Height of output image",
    )
    parser.add_argument(
        "-b",
        "--blocksize",
        metavar="pixels",
        type=int,
        default=10,
        help="Size of square block",
    )
    parser.add_argument(
        "-bw",
        "--blockwidth",
        metavar="pixels",
        type=int,
        help="Width of block (instead of blocksize)",
    )
    parser.add_argument(
        "-bh",
        "--blockheight",
        metavar="pixels",
        type=int,
        help="Height of block (instead of blocksize)",
    )
    parser.add_argument(
        "-v",
        "--vertical",
        action="store_true",
        help="Vertical stripes (instead of blocksize/blockheight)",
    )
    parser.add_argument(
        "-z",
        "--horizontal",
        action="store_true",
        help="Horizontal stripes (instead of blocksize/blockwidth)",
    )
    parser.add_argument(
        "-s", "--show", action="store_true", help="Show image when done"
    )

    try:
        import timing  # optional

        assert timing  # silence warnings
    except ImportError:
        pass

    args = parser.parse_args()
    print(args)

    if not args.blockwidth:
        args.blockwidth = args.blocksize
    if not args.blockheight:
        args.blockheight = args.blocksize

    if args.vertical:
        args.blockheight = args.outheight
    elif args.horizontal:
        args.blockwidth = args.outwidth

    args.blockwidth = min(args.blockwidth, args.outwidth)
    args.blockheight = min(args.blockheight, args.outheight)

    files = fileutils.find_files(args.inspec, args.recursive)
    print(len(files), "files found")
    if len(files) == 0:
        sys.exit("No input files found")

    # Reduce width and height to fit full blocks
    args.outwidth = args.outwidth - divmod(args.outwidth, args.blockwidth)[1]
    args.outheight = args.outheight - divmod(args.outheight, args.blockheight)[1]

    number_of_blocks = int(
        args.outwidth * args.outheight / (args.blockwidth * args.blockheight)
    )

    print("Number of blocks required:", number_of_blocks)
    print("Picking", number_of_blocks, "random files")
    random_indices = []
    for block_number in range(0, number_of_blocks):
        rand_no = random.randrange(0, len(files))
        # print(rand_no)
        random_indices.append((rand_no, block_number))

    # Now sort by image index so we only need to load each image once
    print("Sort images")
    random_indices.sort(key=itemgetter(0))

    # Create new blank image
    new_image = Image.new("RGB", (args.outwidth, args.outheight))

    # Now open each image in turn and get the blocks
    open_index = -1
    open_im = ""
    done = 0
    width, height = 0, 0
    for index, block_number in random_indices:
        # print(open_index, index)

        if open_index != index:
            open_index = index
            sys.stdout.write(
                "\rBlocks done: "
                + str(done)
                + "/"
                + str(number_of_blocks)
                + ". Getting blocks from file "
                + str(index)
            )
            try:
                open_im = Image.open(files[open_index])
            except Exception:
                print("Problem with file", files[open_index])
                continue

        rand_x = get_rand_point(open_im.size[0], args.blockwidth)
        rand_y = get_rand_point(open_im.size[1], args.blockheight)
        crop_box = (rand_x, rand_y, rand_x + args.blockwidth, rand_y + args.blockheight)

        crop_im = open_im.crop(crop_box)
        height, width = divmod(block_number, args.outwidth / args.blockwidth)
        width *= args.blockwidth
        height *= args.blockheight
        new_image.paste(crop_im, (int(width), int(height)))
        width += args.blockwidth
        if (width + args.blockwidth) > args.outwidth:
            width = 0
            height += args.blockheight
        done += 1
    sys.stdout.write("\r\n")

    print("Done:", done, "/", number_of_blocks)
    # We have all the random blocks, save them
    save_im(new_image)

# End of file
