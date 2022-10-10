[![GitHub Actions status](https://github.com/hugovk/pixel-tools/workflows/Test/badge.svg)](https://github.com/hugovk/pixel-tools/actions)
[![Codecov](https://codecov.io/gh/hugovk/pixel-tools/branch/main/graph/badge.svg)](https://codecov.io/gh/hugovk/pixel-tools)
[![Code Health](https://landscape.io/github/hugovk/pixel-tools/master/landscape.png)](https://landscape.io/github/hugovk/pixel-tools/master)
[![Python: 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

# Requirements

Some of these require Python Imaging Library (Pillow or PIL), Open Source Computer
Vision (OpenCV) or ImageMagick's `convert` command. Some requirements can be installed
via pip:

`pip install -r requirements.txt`

# blockit.py

[![](https://farm9.staticflickr.com/8230/8419697276_d1b73743c7_n.jpg)](https://www.flickr.com/photos/hugovk/8419697276/)
[![](https://farm9.staticflickr.com/8328/8418636329_435c2520cf_n.jpg)](https://www.flickr.com/photos/hugovk/8418636329/)

See some images that used this at
<a href="https://secure.flickr.com/search/?q=pixel%3Atool%3Dblockit&m=tags&ss=2&ct=6&mt=all&w=all&adv=1">Flickr</a>.

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

# colour_clock.py

<a href="https://www.flickr.com/photos/hugovk/12548247524/" title="Abroad by hugovk, on Flickr"><img src="https://farm6.staticflickr.com/5530/12548247524_469440a329_m.jpg" width="240" height="240" alt="Abroad"></a><a href="https://www.flickr.com/photos/hugovk/12547743955/" title="The Lorax by Dr. Seuss by hugovk, on Flickr"><img src="https://farm4.staticflickr.com/3730/12547743955_37630df4d4_m.jpg" width="240" height="240" alt="The Lorax by Dr. Seuss"></a><a href="https://www.flickr.com/photos/hugovk/12548247834/" title="Cinderella by hugovk, on Flickr"><img src="https://farm3.staticflickr.com/2891/12548247834_aa4fb026ed_m.jpg" width="240" height="240" alt="Cinderella"></a>

See some images that used this at
<a href="https://secure.flickr.com/search/?q=pixel:tool=colour_clock&m=tags&ss=2&ct=6&mt=all&w=all&adv=1">Flickr</a>.

```
usage: colour_clock.py [-h] [-o OUTFILE] input

Make a colour clock of the five most dominant colours on each page of a book

positional arguments:
  input                 An input PDF, or file spec of images (eg *.jpg)

optional arguments:
  -h, --help            show this help message and exit
  -o OUTFILE, --outfile OUTFILE
                        Output filename (default: None)
```

# contact_sheet.py

<a href="https://www.flickr.com/photos/hugovk/8095019379" title="2012 Helsinki municipal elections by hugovk, on Flickr"><img src="https://farm9.staticflickr.com/8048/8095019379_7eccb87c54_m.jpg" width="161" height="240" alt="2012 Helsinki municipal elections"></a>
<a href="https://www.flickr.com/photos/hugovk/8006067282" title="234 portraits of trees by hugovk, on Flickr"><img src="https://farm9.staticflickr.com/8457/8006067282_39a8c5ab27_m.jpg" width="240" height="147" alt="234 portraits of trees"></a>
<a href="https://www.flickr.com/photos/hugovk/12030586174" title="3pm Tromsø triptych by hugovk, on Flickr"><img src="https://farm4.staticflickr.com/3829/12030586174_65bfb7cbd2_m.jpg" width="240" height="48" alt="3pm Tromsø triptych"></a>

See some images that used this at
<a href="https://secure.flickr.com/search/?q=pixel%3Atool%3Dcontact_sheet&m=tags&ss=2&ct=6&mt=all&adv=1&s=int">Flickr</a>.

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

# deframify.py

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

# face_cropper.py

See some images that used this at
<a href="https://secure.flickr.com/search/?q=pixel%3Atool%3Dface_cropper&m=tags&ss=2&ct=6&mt=all&adv=1">Flickr</a>.

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

# framify.py

See some images and videos that used this at
<a href="https://secure.flickr.com/search/?q=pixel%3Atool%3Dframify&m=tags&ss=2&ct=6&mt=all&adv=1&s=int">Flickr</a>.

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

# image_packer.py

<a href="https://www.flickr.com/photos/hugovk/9150635285/in/photolist-eWBp4T" title="All the Free News (and Ads) That’s Fit to Print"><img src="https://farm4.staticflickr.com/3788/9150635285_e8d66283cb_m.jpg" width="212" height="240" alt="All the Free News (and Ads) That’s Fit to Print"></a>

See some images and videos that used this at
<a href="https://secure.flickr.com/search/?q=pixel%3Atool%3Dimage_packer&m=tags&ss=2&ct=6&mt=all&adv=1&s=int">Flickr</a>.

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

# kaleidoscope.py

<a href="https://www.flickr.com/photos/hugovk/13142941153/in/photolist-m2p1vF-m2pQyf-m1wyjz-m2p1tB-m2omgM-m2omb6-m2p1eD-m2om6M-m1y2Eo-m2p15F-m1xc8c-m1xbD6-m1y3tY" title="Chrysanthemum_kaleidoscope"><img src="https://farm8.staticflickr.com/7317/13142941153_7f93c2e31f_m.jpg" width="240" height="180" alt="Chrysanthemum_kaleidoscope"></a>
<a href="https://www.flickr.com/photos/hugovk/13142812185/in/photolist-m1wyjz-m2p1vF-m2pQyf-m1xbD6-m2p1tB-m2omgM-m1y3tY-m2p15F-m2p1eD-m2om6M-m1y2Eo-m2omb6-m1xc8c" title="Koala_kaleidoscope"><img src="https://farm8.staticflickr.com/7309/13142812185_8f075c76a8_m.jpg" width="240" height="180" alt="Koala_kaleidoscope"></a>
<a href="https://www.flickr.com/photos/hugovk/13142939703/in/photolist-m1wyjz-m2p1vF-m2pQyf-m1xbD6-m2p1tB-m2omgM-m1y3tY-m2p15F-m2p1eD-m2om6M-m1y2Eo-m2omb6-m1xc8c" title="Tulips_kaleidoscope"><img src="https://farm4.staticflickr.com/3833/13142939703_50e21e4f51_m.jpg" width="240" height="180" alt="Tulips_kaleidoscope"></a>

See some images that used this at
<a href="http://www.flickr.com/search/?q=pixel%3Atool%3Dkaleidoscope&m=tags&ss=2&ct=6&mt=all&adv=1&s=int">Flickr</a>.

```
usage: kaleidoscope.py [-h] [-o OUTFILE] [-w WIDTH] infile

Kaleidoscope an image

positional arguments:
  infile                An input image

optional arguments:
  -h, --help            show this help message and exit
  -o OUTFILE, --outfile OUTFILE
                        Output filename (default: None)
  -w WIDTH, --width WIDTH
                        Width of triangle (default: 200)
```

# kantavaesto.py

See some images and videos that used this at
<a href="https://secure.flickr.com/search/?q=pixel%3Atool%3Dkantavaesto&m=tags&ss=2&ct=6&mt=all&adv=1&s=int">Flickr</a>.

```
usage: kantavaesto.py [-h] [-i INSPEC] [-o OUTFILE]

Make a collage of photos inspired by Nana & Felix's Kanta|Väestö

optional arguments:
  -h, --help            show this help message and exit
  -i INSPEC, --inspec INSPEC
                        Input image file spec, must all be the same size
                        (default: *.jpg)
  -o OUTFILE, --outfile OUTFILE
                        Output filename (default: kantavaesto.jpg)
```

# mixify.py

See some images and videos that used this at
<a href="https://secure.flickr.com/search/?q=pixel%3Atool%3Dmixify&m=tags&ss=2&ct=6&mt=all&adv=1&s=int">Flickr</a>.

```
usage: mixify.py [-h] [-a filename] [-v filename] [-o filename]

Wrapper around ffmpeg to mix audio from one video into another video.

optional arguments:
  -h, --help            show this help message and exit
  -a filename, --audio filename
                        File to take audio from (default: audio.mp4)
  -v filename, --video filename
                        File to take video from (default: video.mp4)
  -o filename, --outfile filename
                        Output filename (default: mixed-video.mp4)
```

# padims.py

See some images that used this at
<a href="https://secure.flickr.com/search/?q=pixel%3Atool%3Dpadims&m=tags&ss=2&ct=6&mt=all&adv=1&s=int">Flickr</a>.

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

# pixelator.py

See some images that used this at
<a href="https://secure.flickr.com/search/?q=pixel%3Atool%3Dpixelator&m=tags&ss=2&ct=6&mt=all&adv=1&s=int">Flickr</a>.

```
usage: pixelator.py [-h] [-i INSPEC] [-o OUTFILE]
                    [-e {average,random,nowt,test,test2}] [-n [NORMALISE]]
                    [-k] [-b BATCH_SIZE] [-s]
```

Create a composite image either by averaging or selecting random pixels from input
images.

If images are not the same size, they can be normalised first, either to the mode, mean
or a specified size.

If there are many images to average, ImageMagick uses a lot of RAM causing very slow
paging. To counter this, average in (preferably equal-sized) batches, which creates temp
averages from a smaller number and then averages those.

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

Python dependencies: Python Imaging Library (PIL) External dependencies: ImageMagick's
`convert`

# slitscan.py

<a href="https://www.flickr.com/photos/hugovk/8619861336" title="Easter Sunday stroll (IIIa) by hugovk, on Flickr"><img src="https://farm9.staticflickr.com/8384/8619861336_d04f6fe674_n.jpg" width="320" height="149" alt="Easter Sunday stroll (IIIa)"></a>
<a href="https://www.flickr.com/photos/hugovk/8618756693" title="Easter Sunday stroll (IIId) by hugovk, on Flickr"><img src="https://farm9.staticflickr.com/8116/8618756693_58119556b4_n.jpg" width="320" height="183" alt="Easter Sunday stroll (IIId)"></a>

See some images that used this at
<a href="https://secure.flickr.com/search/?q=pixel%3Atool%3Dslitscan&m=tags&ss=2&ct=6&mt=all&adv=1&s=int">Flickr</a>.

```
usage: slitscan.py [-h] [-i INSPEC] [-o OUTFILE]
                   [-m {eiriksmagick,central,all}]
                   [-d {vertical,v,horizontal,h}] [-t THICKNESS] [-u]
                   [-c CACHE]

Slice input files into an output file. Requires PIL.

optional arguments:
  -h, --help            show this help message and exit
  -i INSPEC, --inspec INSPEC
  -v, --reverse         Reverse list of input files (default: False)
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

# Utilities

factors.py, filelist.py
