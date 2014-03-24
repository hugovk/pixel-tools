#!/usr/bin/env python
"""
Create a contact sheet (or montage/collage) of the input images.

Based on Rick Muller's recipe:
http://code.activestate.com/recipes/412982/
Licensed under the PSF License
"""
from __future__ import print_function
import argparse
import glob
import os
import sys
from PIL import Image
import factors

# PIL jpeg saving: Maximum supported image dimension is 65500 pixels
MAX_DIMENSION = 65500


def tuple_arg(s):
    try:
        if ',' in s:
            w, h = map(int, s.split(','))
        elif ':' in s:
            w, h = map(int, s.split(':'))
        elif 'x' in s:
            w, h = map(int, s.split('x'))
        return w, h
    except:
        raise argparse.ArgumentTypeError("Value must be w,h or w:h or wxh")


def aspect_ratio(number, thumbsize, aspect_ratio):
    """
    Find the best number of rows and columns to approximate
    a given aspect ratio:

    number          The number of images
    thumbsize       The width and height of each image (eg 80, 100)
    aspect_ratio    The width and height of an aspect ratio (eg 16,9)
    """
    from math import sqrt
    total_area = number * thumbsize[0] * thumbsize[1]
    ideal_width = sqrt(total_area * aspect_ratio[0] / aspect_ratio[1])
    ideal_height = total_area / ideal_width
    print(ideal_width, "x", ideal_height, "=", total_area)
    print(ideal_width, "x", ideal_height, "=", ideal_width * ideal_height)

    best_overlap = 0
    best_factor = None

    factors_list = factors.factors(number)
    for factor in factors_list:
        width = factor * thumbsize[0]
        height = total_area / width
        overlap = min(width, ideal_width) * min(height, ideal_height)
        if overlap > best_overlap:
            best_overlap = overlap
            best_factor = factor
        # print(factor, "\t", overlap, "\t", best_overlap)

    cols = best_factor
    rows = number / cols
    print(cols, "cols,", rows, "rows")
    return cols, rows


def make_contact_sheet(fnames, ncols_nrows, photow_photoh,
                       marl_mart_marr_marb,
                       padding):
    """
    Make a contact sheet from a group of filenames:

    fnames       A list of names of the image files

    ncols        Number of columns in the contact sheet
    nrows        Number of rows in the contact sheet
    photow       The width of the photo thumbs in pixels
    photoh       The height of the photo thumbs in pixels

    marl         The left margin in pixels
    mart         The top margin in pixels
    marr         The right margin in pixels
    marb         The bottom margin in pixels

    padding      The padding between images in pixels

    returns a PIL image object.
    """
    ncols, nrows = ncols_nrows
    photow, photoh = photow_photoh
    marl, mart, marr, marb = marl_mart_marr_marb

    # Calculate the size of the output image, based on the
    #  photo thumb sizes, margins, and padding
    marw = marl+marr
    marh = mart+marb

    padw = (ncols-1)*padding
    padh = (nrows-1)*padding
    isize = (int(ncols*photow+marw+padw), int(nrows*photoh+marh+padh))

    print("Image size:", isize)
    if isize[0] > MAX_DIMENSION:
        sys.exit(
            "Output image is too wide: " + str(isize[0]) +
            " (Max: " + str(MAX_DIMENSION) + "). Tip: use --thumbsize "
            "(or --half or --quarter).")
    if isize[1] > MAX_DIMENSION:
        sys.exit(
            "Output image is too high: " + str(isize[1]) +
            " (Max: " + str(MAX_DIMENSION) + "). Tip: use --thumbsize "
            "(or --half or --quarter).")

    # Create the new image. The background doesn't have to be white
    white = (255, 255, 255)
    inew = Image.new('RGB', isize, white)

    count = 0
    # Insert each thumb:
    for irow in range(nrows):
        for icol in range(ncols):
            sys.stdout.write(
                '\rProcessing file ' + str(count+1) + "/" + str(len(fnames)))
            left = marl + icol*(photow+padding)
            right = left + photow
            upper = mart + irow*(photoh+padding)
            lower = upper + photoh
            bbox = (left, upper, right, lower)
            try:
                # Read in an image and resize appropriately
                img = Image.open(
                    fnames[count]).resize((photow, photoh), Image.ANTIALIAS)
            except KeyboardInterrupt:
                sys.exit("Keyboard interrupt")
            except:
                break
            inew.paste(img, bbox)
            count += 1
    sys.stdout.write('\r\n')
    return inew


def make(
        ncols_nrows, inspec, reverse, outfile, thumbsize,
        half, quarter, margins, padding, quality):
    ncols, nrows = ncols_nrows
    files = glob.glob(inspec)
    if len(files) == 0:
        sys.exit("No input files found.")
    if outfile in files:
        files.remove(outfile)  # don't include any pre-existing montage
    if reverse:
        files = files[::-1]

    if not thumbsize:
        thumbsize = Image.open(files[0]).size
        if half:
            thumbsize = (thumbsize[0]/2, thumbsize[1]/2)
        elif quarter:
            thumbsize = (thumbsize[0]/4, thumbsize[1]/4)

    if args.aspect_ratio:
        ncols, nrows = aspect_ratio(len(files), thumbsize, args.aspect_ratio)

    if not nrows and not ncols:
        # Grab a middle-ish factor for the number of rows
        nrows = factors.get_middleish_factor(len(files))

    if nrows and not ncols:
        ncols = len(files) // nrows
    elif not nrows and ncols:
        nrows = len(files) // ncols
    # print(len(files),ncols,nrows,ncols*nrows)
    print("Files:\t", len(files))
    print("Rows:\t", nrows)
    print("Cols:\t", ncols)

    # Don't bother reading in files we aren't going to use
    if len(files) > ncols*nrows:
        files = files[:ncols*nrows]

    margins = [margins, margins, margins, margins]

    print("Making contact sheet")
    inew = make_contact_sheet(
        files, (ncols, nrows), thumbsize, margins, padding)
    print("Saving to", outfile)
    inew.save(outfile, quality=quality)
    print("Done.")
    # inew.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Make a contact sheet. Requires PIL.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-i', '--inspec', default='*.jpg',
        help='Input file spec')
    parser.add_argument(
        '-v', '--reverse', action='store_true',
        help='Reverse list of input files')
    parser.add_argument(
        '-o', '--outfile', default='contact_sheet.jpg',
        help='Output filename')
    parser.add_argument(
        '-r', '--rows', type=int,
        help='Number of rows')
    parser.add_argument(
        '-c', '--cols', type=int,
        help='Number of columns')
    parser.add_argument(
        '-a', '--aspect_ratio', type=tuple_arg,
        help='Calculate rows and columns to approximate this '
        'aspect ratio (eg 16,9)')
    parser.add_argument(
        '-t', '--thumbsize', type=tuple_arg, metavar='pixels',
        help='Width,height tuple of the photo thumbs')
    parser.add_argument(
        '-hs', '--half', action='store_true',
        help='Shortcut to calculate --thumbsize as half input size')
    parser.add_argument(
        '-qs', '--quarter', action='store_true',
        help='Shortcut to calculate --thumbsize as quarter input size')
    parser.add_argument(
        '-m', '--margins', type=int, default=5,
        help='Margins')
    parser.add_argument(
        '-p', '--padding', metavar='pixels',
        type=int, default=1,
        help='Padding between images')
    parser.add_argument(
        '-q', '--quality', default=90, type=int,
        help="Output image's save quality")
    parser.add_argument(
        '-nc', '--noclobber', action='store_true',
        help="Don't clobber pre-exisiting output file")
    args = parser.parse_args()

    try:
        import timing  # optional
    except:
        pass
    print(args)

    if args.noclobber and os.path.exists(args.outfile):
        sys.exit("Output file (" + args.outfile + ") already exists, exiting")

    make(
        (args.cols, args.rows), args.inspec, args.reverse, args.outfile,
        args.thumbsize, args.half, args.quarter, args.margins,
        args.padding, args.quality)

# End of file
