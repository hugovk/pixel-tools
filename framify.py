#!/usr/bin/env python
"""
Wrapper around ffmpeg to extract frames from a video.
"""
import argparse
import os

def create_dir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wrapper around ffmpeg to extract frames from a video.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('infile', metavar='file',
        # default='filename.mp4',
        help='Video file to extract')
    parser.add_argument('-o', '--outdir', metavar='directory',
        default='frames',
        help='Directory to save frames')
    parser.add_argument('-r', '--framerate', metavar='fps',
         default=25, type=int,
        help='Framerate')
    args = parser.parse_args()
    print args

    # REM set framesize=32x18
    # REM ffmpeg -i %1 -r 25 -s %framesize% smallframes\%%6d.jpg

    create_dir(args.outdir)
    output = os.path.join(args.outdir, "%6d.jpg")
    cmd = "ffmpeg -i " + args.infile + " -r " + str(args.framerate) + " -q:v 1 " + output
    print cmd
    os.system(cmd)
    
# End of file
