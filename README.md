Requirements
============
Some of these require Python Imaging Library (PIL), Open Source Computer Vision (OpenCV) or ImageMagick's `convert` command.

blockit.py
==========
See some images that used this at <a href="http://www.flickr.com/search/?q=pixel%3Atool%3Dblockit&ss=2&z=t">Flickr</a>.

```
usage: blockit.py [-h] [-i INSPEC] [-r] [-o OUTFILE] [-W pixels] [-H pixels]
                  [-b pixels] [-bw pixels] [-bh pixels] [-v] [-z] [-s]

Create image from blocks of other images. Requires PIL.

optional arguments:
  -h, --help            show this help message and exit
  -i INSPEC, --inspec INSPEC
                        Input file spec (default: 2*.jpg)
  -r, --recursive       Recurse directories (default: False)
  -o OUTFILE, --outfile OUTFILE
                        Output filename (default: None)
  -W pixels, --outwidth pixels
                        Width of output image (default: 640)
  -H pixels, --outheight pixels
                        Height of output image (default: 320)
  -b pixels, --blocksize pixels
                        Size of square block (default: 10)
  -bw pixels, --blockwidth pixels
                        Width of block (instead of blocksize) (default: None)
  -bh pixels, --blockheight pixels
                        Height of block (instead of blocksize) (default: None)
  -v, --vertical        Vertical stripes (instead of blocksize/blockheight)
                        (default: False)
  -z, --horizontal      Horizontal stripes (instead of blocksize/blockwidth)
                        (default: False)
  -s, --show            Show image when done (default: False)
```

contact_sheet.py
================
See some images that used this at <a href="http://www.flickr.com/search/?q=pixel%3Atool%3Dcontact_sheet&ss=2&z=t">Flickr</a>.

```
usage: contact_sheet.py [-h] [-i INSPEC] [-v] [-o OUTFILE] [-r ROWS] [-c COLS]
                        [-a ASPECT_RATIO] [-t pixels] [-hs] [-qs] [-m MARGINS]
                        [-p pixels] [-q QUALITY]

Make a contact sheet. Requires PIL.

optional arguments:
  -h, --help            show this help message and exit
  -i INSPEC, --inspec INSPEC
                        Input file spec (default: *.jpg)
  -v, --reverse         Reverse list of input files (default: False)
  -o OUTFILE, --outfile OUTFILE
                        Output filename (default: contact_sheet.jpg)
  -r ROWS, --rows ROWS  Number of rows (default: None)
  -c COLS, --cols COLS  Number of columns (default: None)
  -a ASPECT_RATIO, --aspect_ratio ASPECT_RATIO
                        Calculate rows and columns to approximate this aspect
                        ratio (eg 16,9) (default: None)
  -t pixels, --thumbsize pixels
                        Width,height tuple of the photo thumbs (default: None)
  -hs, --half           Shortcut to calculate --thumbsize as half input size
                        (default: False)
  -qs, --quarter        Shortcut to calculate --thumbsize as quarter input
                        size (default: False)
  -m MARGINS, --margins MARGINS
                        Margins (default: 5)
  -p pixels, --padding pixels
                        Padding between images (default: 1)
  -q QUALITY, --quality QUALITY
                        Output image's save quality (default: 90)
```

deframify.py
============

See also `framify.py`.

```
usage: deframify.py [-h] [-i spec] [-r fps] [-o filename]

Wrapper around ffmpeg to animate frames into a video.

optional arguments:
  -h, --help            show this help message and exit
  -i spec, --inspec spec
                        Image files to animate (default: *.jpg)
  -r fps, --framerate fps
                        Framerate (default: 25)
  -o filename, --outfile filename
                        Output video filename (default: timelapse.mp4)
```

face_cropper.py
===============
See some images that used this at <a href="http://www.flickr.com/search/?q=pixel%3Atool%3Dface_cropper&ss=2&z=t">Flickr</a>.


```
usage: face_cropper.py [-h] [-c CASCADE] [-i INSPEC] [-o OUTDIR] [-a] [-r]
                       [-t] [-s]

Find, crop and save faces (or other objects).  Requires OpenCV.

optional arguments:
  -h, --help            show this help message and exit
  -c CASCADE, --cascade CASCADE
                        Haar cascade file (default: D:\temp\opencv\data\haarca
                        scades\haarcascade_frontalface_alt.xml)
  -i INSPEC, --inspec INSPEC
                        Input file spec (default: *.jpg)
  -o OUTDIR, --outdir OUTDIR
                        Output directory (default: crop)
  -a, --findall         Find all objects in photo instead of biggest (slower)
                        (default: False)
  -r, --recursive       Recurse directories (default: False)
  -t, --tight_crop      Crop image tight around detected feature (otherwise a
                        margin is added) (default: False)
  -s, --show            Show detected image with box (default: False)
```

framify.py
==========
See some images and videos that used this at <a href="http://www.flickr.com/search/?q=pixel%3Atool%3Dframify&ss=2&s=int">Flickr</a>.

See also `deframify.py`.

```
usage: framify.py [-h] [-o directory] [-r fps] file

Wrapper around ffmpeg to extract frames from a video.

positional arguments:
  file                  Video file to extract

optional arguments:
  -h, --help            show this help message and exit
  -o directory, --outdir directory
                        Directory to save frames (default: frames)
  -r fps, --framerate fps
                        Framerate (default: 25)
```

image_packer.py
==========
See some images and videos that used this at <a href="http://www.flickr.com/search/?q=pixel%3Atool%3Dimage_packer&ss=2&s=int">Flickr</a>.

Based on <a href="http://code.activestate.com/recipes/442299/">S W's recipe</a>.

```
usage: image_packer.py [-h] [-o OUTFILE] [-s pixels] [-l] [-t]

Pack multiple images of different sizes into one image.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTFILE, --outfile OUTFILE
                        Output image file (default: output.png)
  -s pixels, --size pixels
                        Size (width,height tuple) of the image we're packing
                        into (default: 1024,1024)
  -l, --largest_first   Pack largest images first (default: False)
  -t, --tempfiles       Save temporary files to show filling (default: False)
```

padims.py
============

See some images that used this at <a href="http://www.flickr.com/search/?q=pixel%3Atool%3Dpadims&ss=2&z=t">Flickr</a>.

```
usage: padims.py [-h] [-i INSPEC] [-o OUTDIR] [-ha {centre,left,right}]
                 [-va {centre,top,bottom}]

Pad images

optional arguments:
  -h, --help            show this help message and exit
  -i INSPEC, --inspec INSPEC
                        Input file spec (default: *.jpg)
  -o OUTDIR, --outdir OUTDIR
                        Output directory (default: out)
  -ha {centre,left,right}, --halign {centre,left,right}
                        Horizontal alignment (default: centre)
  -va {centre,top,bottom}, --valign {centre,top,bottom}
                        Vertical alignment (default: centre)
```

Python dependencies: Python Imaging Library (PIL)

pixelator.py
============

See some images that used this at <a href="http://www.flickr.com/search/?q=pixel%3Atool%3Dpixelator&ss=2&z=t">Flickr</a>.

```
usage: pixelator.py [-h] [-i INSPEC] [-o OUTFILE]
                    [-e {average,random,nowt,test,test2}] [-n [NORMALISE]]
                    [-k] [-b BATCH_SIZE] [-s]
```
Create a composite image either by averaging or selecting random pixels from
input images. 

If images are not the same size, they can be normalised first, either to the 
mode, mean or a specified size.

If there are many images to average, ImageMagick uses a lot of RAM causing
very slow paging. To counter this, average in (preferably equal-sized)
batches, which creates temp averages from a smaller number and then averages
those.

```
optional arguments:
  -h, --help            show this help message and exit
  -i INSPEC, --inspec INSPEC
                        Input file spec (default: *.jpg)
  -o OUTFILE, --outfile OUTFILE
                        Output file name (default: out.jpg)
  -e {average,random,nowt,test,test2}, --effect {average,random,nowt,test,test2}
                        Effect to apply (default: average)
  -n [NORMALISE], --normalise [NORMALISE]
                        If images are different sizes, normalise them first.
                        [mode|mean|width,height] (default: None)
  -k, --keep_normals    Keep normalised images (default: False)
  -b BATCH_SIZE, --batch-size BATCH_SIZE
                        For average: Batch size. For best results, should be a
                        factor of the total number. Use 'auto' to calculate
                        size. (default: None)
  -s, --show            For random: Show the output image (default: False)
```

Python dependencies: Python Imaging Library (PIL)
External dependencies: ImageMagick's `convert`

slitscan.py
===========
See some images that used this at <a href="http://www.flickr.com/search/?s=int&z=t&ss=2&w=all&q=pixel%3Atool%3Dslitscan&m=text">Flickr</a>.
```
usage: slitscan.py [-h] [-i INSPEC] [-o OUTFILE]
                   [-m {eiriksmagick,central,all}]
                   [-d {vertical,v,horizontal,h}] [-t THICKNESS] [-u]
                   [-c CACHE]

Slice input files into an output file. Requires PIL.

optional arguments:
  -h, --help            show this help message and exit
  -i INSPEC, --inspec INSPEC
                        Input file spec (default: *.jpg)
  -o OUTFILE, --outfile OUTFILE
                        Output file name (default: None)
  -m {eiriksmagick,central,all}, --mode {eiriksmagick,central,all}
                        How to slice images. 'central' takes just the middle
                        slices from each image, 'eiriksmagick' takes a
                        different slice from each, moving from left to right
                        (or top to bottom). Both create a single image. 'all'
                        makes lots of image, each with slices from the same
                        place. (default: eiriksmagick)
  -d {vertical,v,horizontal,h}, --direction {vertical,v,horizontal,h}
                        Direction to slitify (default: vertical)
  -t THICKNESS, --thickness THICKNESS
                        Slit thickness in pixels. Default is to calculate
                        based on number of input images. (default: None)
  -u, --useallinput     Use every input file even if more than the width or
                        height (default: False)
  -c CACHE, --cache CACHE
                        Load this many images into memory, the rest will be
                        read on demand from disk (for: --mode all) (default:
                        None)
```


Utilities
=======================
factors.py, filelist.py
