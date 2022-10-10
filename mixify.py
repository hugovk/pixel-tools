#!/usr/bin/env python
"""
Wrapper around ffmpeg to mix audio from one video into another video.
"""
from __future__ import annotations

import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Wrapper around ffmpeg to mix audio from one video into another video."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-a",
        "--audio",
        metavar="filename",
        default="audio.mp4",
        help="File to take audio from",
    )
    parser.add_argument(
        "-v",
        "--video",
        metavar="filename",
        default="video.mp4",
        help="File to take video from",
    )
    parser.add_argument(
        "-o",
        "--outfile",
        metavar="filename",
        default="mixed-video.mp4",
        help="Output filename",
    )
    args = parser.parse_args()

    try:
        import timing  # optional

        assert timing  # silence warnings
    except ImportError:
        pass

    print(args)

    if not os.path.isfile(args.audio) and not os.path.isfile(args.video):
        import sys

        sys.exit("Cannot find audio or video file")
    elif not os.path.isfile(args.audio):
        import sys

        sys.exit("Cannot find audio file")
    elif not os.path.isfile(args.video):
        import sys

        sys.exit("Cannot find video file")

    cmd = (
        "ffmpeg -i {} -i {} -map 0:v:0 -map 1:a:0 -codec copy -shortest "
        '-af "afade=t=out:st=3:30:d=2" {}'
    ).format(args.video, args.audio, args.outfile)
    print(cmd)
    os.system(cmd)

# End of file
