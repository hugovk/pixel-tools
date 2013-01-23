import argparse
import datetime
import glob
from operator import itemgetter
from PIL import Image, ImageOps
import os
import random
import shutil
import sys

try: import timing # Optional, http://stackoverflow.com/a/1557906/724176
except: None

# From a bunch of images, make a composite from average or random pixels
# Python dependencies: Python Imaging Library (PIL)
# External dependencies: ImageMagick's convert

TEMP_DIR = "temp"
TEMP_PREFIX = "tmp"
TEMP_SUFFIX = ".png"
temp_dirs = []

def encode_time():
    # Return a short, unique-ish string for creating a temp dir 
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    encoded = ''
    # "%S%f" is "SecondsMicroseconds"
    n = int(datetime.datetime.now().strftime("%S%f"))/1000
    while n > 0:
        n, r = divmod(n, len(alphabet))
        encoded = alphabet[r] + encoded
    return encoded

def create_temp_dir():
    dir = TEMP_DIR + encode_time()
    if os.path.isdir(dir):
        shutil.rmtree(dir)
    if not os.path.isdir(dir):
        os.mkdir(dir)
    temp_dirs.append(dir)
    return dir

def remove_temp_dirs():
    for dir in temp_dirs:
        shutil.rmtree(dir)

def mean(values):
    """Computes the arithmetic mean of a list of numbers.

    >>> print mean([20, 30, 70])
    40.0
    """
    return sum(values, 0.0) / len(values)

def mode(values):
    """Computes the mode of a list of numbers.

    >>> print mode([1, 2, 2, 3, 70])
    2
    """
    d = {}
    mode, freq = 0, 0
    for i in values:
        if d.has_key(i):
            d[i] += 1
        else:
            d[i] = 1

        if d[i] > freq:
            mode = i
            freq = d[i]

    # print "Found mode", mode, "frequency", freq
    return mode

def sanity_check(files):
    num_files = len(files)
    print "Number of input images:", num_files
    if num_files is 0:
        sys.exit("Not enough input images")
    
    # If only one input image, just copy it to output!
    if num_files is 1:
        shutil.copy2(files[0], args.outfile)
        sys.exit()

def get_file_list(spec):
    files = glob.glob(spec)
    sanity_check(files)
    return files
    
def imagemagick_average(inspec, outfile):
    command = "convert " + inspec + " -evaluate-sequence mean " + outfile
    print command
    os.system(command)

def create_average_in_one_go(inspec):
    # Create with one IM call
    if ' ' in inspec:
        inspec = '"' + inspec + '"'
    if ' ' in args.outfile:
        args.outfile = '"' + args.outfile + '"'
    imagemagick_average(inspec, args.outfile)

def create_average_in_batches(files):
    # Create in batches

    i = 0
    batch_number = 0
    batch = " "

    number = len(files)
    number_of_batches = number/args.batch_size
    print "Number of files:", number
    print "Number of batches:", number_of_batches
    remainder = number % args.batch_size
    print "Remainder:", remainder
    if remainder is not 0: print "Warning: Get better results when batches are all the same size with zero remainder"

    temp_dir = create_temp_dir()
    
    for file in files:
        if i < (args.batch_size):
            # print i
            batch += '"' + file + '" '
            i += 1
        else:
            temp_file = os.path.join(temp_dir, TEMP_PREFIX + str(batch_number) + TEMP_SUFFIX)

            print "Batch number:", batch_number+1, "/", number_of_batches
            print "Number in batch:", i
            imagemagick_average(batch, temp_file)
            batch_number += 1
            i = 0
            batch = " "
            
        # print batch
        # print i
    # Now make an average from the temp files
    imagemagick_average(os.path.join(temp_dir, TEMP_PREFIX + "*" + TEMP_SUFFIX), args.outfile)

def normalise_files(spec):
    files = get_file_list(spec)
    widths, heights = [], []

    normalise_needed = False
    print "Checking sizes"
    for i, file in enumerate(files):
        print file
        try:
            width, height = Image.open(file).size
            # print width, "x, height, height * 1.0/width, file
            widths.append(width)
            heights.append(height)
            if (not normalise_needed and 
                    i > 0 and 
                    (width != widths[0] or 
                    height != heights[0])):
                normalise_needed = True
        except:
            print "Ignoring problem file:", file
            # Add dummy data
            widths.append(0)
            heights.append(0)
            continue

    if not normalise_needed:
        print "Images all the same size. Normalising not needed."
        return spec

    # Else we need to normalise
    if args.normalise == 'mode':
        width = mode(widths)
        height = mode(heights)
        print "Mode:", width, "x", height
        size = (width, height)
    elif args.normalise == 'mean':
        width = mean(widths)
        height = mean(heights)
        print "Mean:", width, "x", height
        size = (width, height)
    else:
        width,height = args.normalise.split(',')
        size = (int(width), int(height))
    
    temp_dir = create_temp_dir()
    
    for i, file in enumerate(files):
        if widths[i] == 0 and heights[i] == 0:
            # Ignore problem file
            continue
        print widths[i], "x", heights[i], file
        
        if ((widths[i], heights[i]) == size):
            print "Don't need to convert"
            shutil.copy2(file, temp_dir)
        else:
            print "Need to convert"
            filename = os.path.split(file)[1]
            temp_file = os.path.join(temp_dir, filename)
            
            try:
                im = Image.open(file)
                # im = im.resize(size)
                im = ImageOps.fit(im, size, Image.ANTIALIAS, (0.5, 0.5))
                im.save(temp_file)
            except:
                print "Ignoring problem file:", filename
                continue

    spec = os.path.split(spec)[1]
    spec = os.path.join(temp_dir, spec)
    return spec

def create_randomised_image(files):
    # All files should be the same dimension, so let's check the first one
    first_image = Image.open(files[0])
    width, height = first_image.size
    print "Format:", first_image.format
    print "Mode:", first_image.mode
    print width, "x", height
    # Create new blank image
    new_image = Image.new('RGBA', (width, height))
    new_pix = new_image.load()
    
    # For each pixel, pick a random image and store its index
    print "Pick random images"
    random_indices = []
    num_files = len(files)
    for y in range(0, height):
        # print y, height
        for x in range(0, width):
            # Pick the x,y pixel from a random file
            rand_no = random.randrange(0, num_files)
            # print rand_no
            random_indices.append((rand_no, (x,y)))
                 
    # Now sort by image index
    print "Sort images"
    random_indices.sort(key=itemgetter(0))

    # Now open each image in turn and get the pixel
    open_index = -1
    open_pix = ""
    for index, coord in random_indices:
        # print open_index, index
        if open_index != index:
            open_index = index
            # print "Get pixels from file", index
            open_pix = Image.open(files[index]).load()
        new_pix[coord] = open_pix[coord]

    # We have all the random pixels, save them
    save_im(new_image)

def save_im(im):
    if args.show:
        print "Show image"
        im.show()
    print "Save image"
    try:
        im.save(args.outfile)
    except IOError:
        print "Cannot save"


import doctest
doctest.testmod()   # automatically validate the embedded tests

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a composite image either by averaging or selecting random pixels from input images. If images are not the same size, they can be normalised first. If there are many images to average, ImageMagick uses a lot of RAM causing very slow paging. To counter this, average in (preferably equal-sized) batches, which creates temp averages from a smaller number and then averages those.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--inspec', default='*.jpg',
        help='Input file spec')
    parser.add_argument('-o', '--outfile', default='out.jpg',
        help='Output file name')
    parser.add_argument('-e', '--effect', default='average', choices=('average', 'random'),
        help="Effect to apply")
    parser.add_argument('-n', '--normalise', nargs='?', const='mode',
        help="If images are different sizes, normalise them first. [mode|mean|width,height]")

    # For averaged composites:
    parser.add_argument('-b', '--batch-size', type=int, 
        help='For average: Batch size. For best results, should be a factor of the total number.')
    
    # For random-pixel composites:
    parser.add_argument('-s', '--show', action="store_true", default=False, 
        help='For random: Show the output image')
    args = parser.parse_args()
    inspec = args.inspec
    print args

    try:
        if args.normalise:
            print "Normalise input images"
            inspec = normalise_files(inspec)
            print inspec
        
        print "Effect:", args.effect
        if args.effect == 'average':
            if args.batch_size:
                create_average_in_batches(get_file_list(inspec))
            else:
                create_average_in_one_go(inspec)
            
        elif args.effect == 'random':
            create_randomised_image(get_file_list(inspec))

    except KeyboardInterrupt:
        print "Keyboard interrupt"

    remove_temp_dirs()

# End of file
