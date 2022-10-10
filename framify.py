#!/usr/bin/env python
"""
Wrapper around ffmpeg to extract frames from a video.
"""
from __future__ import annotations

import argparse
import os

try:
    import timing  # optional

    assert timing  # silence warnings
except ImportError:
    pass


def create_dir(directory):
    if not os.path.isdir(directory):
        os.mkdir(directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Wrapper around ffmpeg to extract frames from a video.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "infile",
        metavar="file",
        # default='filename.mp4',
        help="Video file to extract",
    )
    parser.add_argument(
        "-o",
        "--outdir",
        metavar="directory",
        default="frames",
        help="Directory to save frames",
    )
    parser.add_argument(
        "-r", "--framerate", metavar="fps", default=25, type=float, help="Framerate"
    )
    parser.add_argument(
        "-s", "--size", metavar="WxH or abbreviation", help="Set frame size"
    )
    args = parser.parse_args()
    print(args)

    # REM set framesize=32x18
    # REM ffmpeg -i %1 -r 25 -s %framesize% smallframes\%%6d.jpg

    if " " in args.infile:
        args.infile = '"' + args.infile + '"'
    create_dir(args.outdir)
    output = os.path.join(args.outdir, "%6d.jpg")

    if args.size:
        size = "-s " + args.size
    else:
        size = ""

    cmd = "ffmpeg -i {} {} -r {} -q:v 1 {}".format(
        args.infile, size, str(args.framerate), output
    )
    print(cmd)
    os.system(cmd)

# End of file
