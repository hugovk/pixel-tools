#!/usr/bin/env python
"""
Pad images of different sizes so all are centred with black borders.
"""
import argparse
import glob
import os
import shutil
import sys

from PIL import Image

import fileutils
try: import timing # Optional, http://stackoverflow.com/a/1557906/724176
except: None

def sanity_check(files):
    num_files = len(files)
    print "Number of input images:", num_files
    if num_files < 2:
        sys.exit("Not enough input images")
    
def pad_images(files):
    # Find max width and height
    max_width, max_height = 0,0 
    for file in files:
        width, height = Image.open(file).size
        if width > max_width:
            max_width = width
        if height > max_height:
            max_height = height

    print "Max width:\t", max_width
    print "Max height:\t", max_height

    fileutils.create_dir(args.outdir)
    black = (0,0,0)
    white = (255,255,255)
    for file in files:
        # Create a new blank image
        inew = Image.new('RGB', (max_width, max_height), black)
        img = Image.open(file)
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
        outfile = os.path.join(args.outdir, file)
        print "Saving to", outfile
        inew.save(outfile, quality=100)
        
        # sys.stdout.write('\rProcessing file ' + str(i))
    # sys.stdout.write('\r\n')
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pad images', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--inspec', default='*.jpg',
        help='Input file spec')
    parser.add_argument('-o', '--outdir', default='out',
        help='Output directory')
    parser.add_argument('-ha', '--halign', default='centre', choices=('centre', 'left', 'right'),
        help="Horizontal alignment")
    parser.add_argument('-va', '--valign', default='centre', choices=('centre', 'top', 'bottom'),
        help="Vertical alignment")
    args = parser.parse_args()
    print args

    files = glob.glob(args.inspec)
    sanity_check(files)
    pad_images(files)

# End of file
