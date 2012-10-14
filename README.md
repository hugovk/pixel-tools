pixelator.py
============
```
usage: pixelator.py [-h] [-o OUTFILE] [-e EFFECT] [-n [NORMALISE]]
                    [-b BATCH_SIZE] [-s]
                    inspec
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
positional arguments:
  inspec                Input file spec

optional arguments:
  -h, --help            show this help message and exit
  -o OUTFILE, --outfile OUTFILE
                        Output file name
  -e EFFECT, --effect EFFECT
                        Effect to apply: average / random. Default: average
  -n [NORMALISE], --normalise [NORMALISE]
                        If images are different sizes, normalise them first.
                        [mode|mean|width,height]
  -b BATCH_SIZE, --batch-size BATCH_SIZE
                        For average: Batch size. For best results, should be a
                        factor of the total number.
  -s, --show            For random: Show the output image
```

Python dependencies: Python Imaging Library (PIL)
External dependencies: ImageMagick's convert

