#!/usr/bin/env python
"""
Make a collage of photos inspired by Nana & Felix's Kanta|Väestö
http://www.nana-felix.com/
http://www.hippolyte.fi/nana-felix-3/?lang=en
"""
from __future__ import annotations

import argparse
import glob
import sys

from PIL import Image


def kantavaesto(inspec, outfile):

    files = glob.glob(inspec)
    if len(files) == 0:
        sys.exit("No input files")

    im = Image.open(files[0])

    print(len(files), im.size)
    w, h = im.size
    left = 0
    upper = 0
    right = w
    lower = h

    # How much smaller should the next image be cropped by?
    delta = float(im.size[0] / 2) / len(files)
    print(delta)

    last_bbox = None

    for f in files[1:]:
        left += delta
        upper += delta
        right -= delta
        lower -= delta
        bbox = (int(left), int(upper), int(right), int(lower))
        if last_bbox != bbox:
            last_bbox = bbox
            print(bbox)
            next_im = Image.open(f).crop(bbox)
            # next_im.show()
            im.paste(next_im, bbox)
            # im.show()

    # im.show()
    print("Saving to", outfile)
    im.save(outfile, quality=95)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Make a collage of photos inspired by "
        "Nana & Felix's Kanta|Väestö",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-i",
        "--inspec",
        default="*.jpg",
        help="Input image file spec, must all be the same size",
    )
    parser.add_argument(
        "-o", "--outfile", default="kantavaesto.jpg", help="Output filename"
    )
    args = parser.parse_args()
    print(args)

    try:  # Optional, http://stackoverflow.com/a/1557906/724176
        import timing

        assert timing  # silence warnings
    except ImportError:
        pass

    kantavaesto(args.inspec, args.outfile)

# End of file
