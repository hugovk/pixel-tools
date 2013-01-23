#!/usr/bin/python
"""
Create a contact sheet (or montage/collage) of the input images.

Based on Rick Muller's recipe:
http://code.activestate.com/recipes/412982/
Licensed under the PSF License
"""
import argparse
import glob
from PIL import Image

try: import timing # optional
except: pass

def tuple_arg(s):
    try:
        w, h = map(int, s.split(','))
        return w, h
    except:
        raise argparse.ArgumentTypeError("Thumbnail must be w,h")

def make_contact_sheet(fnames, (ncols,nrows), (photow,photoh),
                       (marl,mart,marr,marb),
                       padding):
    """\
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

    # Calculate the size of the output image, based on the
    #  photo thumb sizes, margins, and padding
    marw = marl+marr
    marh = mart+ marb

    padw = (ncols-1)*padding
    padh = (nrows-1)*padding
    isize = (ncols*photow+marw+padw,nrows*photoh+marh+padh)

    # Create the new image. The background doesn't have to be white
    white = (255,255,255)
    inew = Image.new('RGB',isize,white)

    count = 0
    # Insert each thumb:
    for irow in range(nrows):
        for icol in range(ncols):
            left = marl + icol*(photow+padding)
            right = left + photow
            upper = mart + irow*(photoh+padding)
            lower = upper + photoh
            bbox = (left,upper,right,lower)
            try:
                # Read in an image and resize appropriately
                img = Image.open(fnames[count]).resize((photow,photoh))
            except:
                break
            inew.paste(img,bbox)
            count += 1
    return inew

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Make a contact sheet.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--inspec', default='*.jpg',
        help='Input file spec')
    parser.add_argument('-o', '--outfile', default='contact_sheet.jpg',
        help='Output filename')
    parser.add_argument('-r', '--rows', type=int,
        help='Number of rows')
    parser.add_argument('-c', '--cols', type=int,
        help='Number of columns')
    parser.add_argument('-t', '--thumbsize', type=tuple_arg, metavar='pixels',
        help='Width,height tuple of the photo thumbs')
    parser.add_argument('-m', '--margins', type=int, default=5,
        help='Margins')
    parser.add_argument('-p', '--padding', metavar='pixels',
        type=int, default=1,
        help='Padding between images')
    args = parser.parse_args()
    print args

    ncols,nrows = args.cols,args.rows

    files = glob.glob(args.inspec)

    if not args.thumbsize:
        args.thumbsize = Image.open(files[0]).size
        
    def factors(n):
        return set(reduce(list.__add__, 
                    ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

    if not nrows and not ncols:
        # Grab a middle-ish factor for the number of columns
        factors_set = factors(len(files))
        factors_list = list(sorted(factors_set))
        ncols = factors_list[int(len(factors_list)/2)]
        
    if nrows and not ncols:
        ncols = len(files) / nrows
    elif not nrows and ncols:
        nrows = len(files) / ncols
    # print len(files),ncols,nrows,ncols*nrows

    # Don't bother reading in files we aren't going to use
    if len(files) > ncols*nrows: files = files[:ncols*nrows]

    margins = [args.margins,args.margins,args.margins,args.margins]

    print "Making contact sheet"
    inew = make_contact_sheet(files, (ncols,nrows), args.thumbsize, margins, args.padding)
    print "Saving to", args.outfile
    inew.save(args.outfile, quality=100)
    print "Done."
    # inew.show()
