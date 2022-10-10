#!/usr/bin/env python
"""
Wrapper around ImageMagick to annotate images
"""
from __future__ import annotations

import argparse
import os

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Wrapper around ImageMagick to annotate images.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("infile", help="Input file")
    parser.add_argument("text", help="Text to annotate")
    parser.add_argument(
        "-o", "--outfile", help="Output filename (default: infile-annotated.jpg"
    )
    parser.add_argument(
        "-g",
        "--gravity",
        default="South",
        choices=(
            "center",
            "east",
            "northeast",
            "north",
            "northwest",
            "southeast",
            "south",
            "southwest",
            "west",
        ),
        help="Placement of text",
    )
    parser.add_argument("-c", "--colour", default="black", help="Text colour")
    parser.add_argument("-p", "--pointsize", default="19", help="Text point size")
    parser.add_argument(
        "-x", "--no_box", action="store_true", help="Text with no background box"
    )
    parser.add_argument("--geometry", default="+3+3", help="Geometry argument (offset)")
    parser.add_argument(
        "--background", default="#cdc9c980", help="Box background colour"
    )
    # parser.add_argument(
    #     "-s", "--show", action="store_true", help="Show detected image with box"
    # )

    args = parser.parse_args()
    if not args.outfile:
        args.outfile = args.infile + "-annotated.jpg"
    print(args)

    if args.no_box:
        cmd = (
            'convert "'
            + args.infile
            + '" -quality 100 -fill '
            + args.colour
            + " -gravity "
            + args.gravity
            + " -pointsize "
            + str(args.pointsize)
            + ' -annotate 0 "'
            + args.text
            + '" "'
            + args.outfile
            + '"'
        )
    else:
        cmd = (
            'convert -background "'
            + args.background
            + '" -fill '
            + args.colour
            + " -pointsize "
            + str(args.pointsize)
            + " -geometry "
            + args.geometry
            + ' label:"'
            + args.text
            + '" miff:- | composite -gravity '
            + args.gravity
            + " -geometry "
            + args.geometry
            + '  - "'
            + args.infile
            + '" "'
            + args.outfile
            + '"'
        )

    print(cmd)
    os.system(cmd)

# End of file
