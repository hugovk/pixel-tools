#!/usr/bin/env python
"""
Find faces in images and save them to a "crop" subdirectory.

Based on opencv/samples/python/facedetect.py
Original C implementation by:  ?
Python implementation by: Roman Stanchak, James Bowman
"""
from __future__ import annotations

import argparse
import os
import sys

import cv2

import fileutils

# Optional, http://stackoverflow.com/a/1557906/724176
try:
    import timing

    assert timing  # silence warnings
except ImportError:
    pass

# Parameters for Haar detection. From the API:
# The default parameters (scale_factor=2, min_neighbors=3, flags=0) are tuned
# for accurate yet slow object detection.
# For a faster operation on real video images the settings are:
# scale_factor=1.2, min_neighbors=2, flags=CV_HAAR_DO_CANNY_PRUNING,
# min_size=<minimum possible face size

min_size = (20, 20)
image_scale = 2
haar_scale = 1.2  # 1.2
min_neighbors = 3  # 2
haar_flags = cv2.CASCADE_SCALE_IMAGE


def create_dir(directory):
    if not os.path.isdir(directory):
        os.mkdir(directory)


def detect_and_save(input_name, cascade, outdir, tight_crop=False, show=False):
    count = 0
    img = cv2.imread(input_name)

    # Convert color input image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Scale input image for faster processing
    fx = fy = 1.0 / image_scale
    small_img = cv2.resize(gray, (0, 0), fx=fx, fy=fy)

    gray = cv2.equalizeHist(gray, cv2.COLOR_BGR2GRAY)

    if cascade:
        t = cv2.getTickCount()
        faces = cascade.detectMultiScale(
            small_img,
            scaleFactor=haar_scale,
            minNeighbors=min_neighbors,
            minSize=min_size,
            flags=haar_flags,
        )
        t = cv2.getTickCount() - t
        print("detection time = %gms" % (t / (cv2.getTickFrequency() * 1000.0)))
        if len(faces):
            for (x, y, w, h) in faces:
                # The input to was resized, so scale the bounding box
                # of each face and convert it to two CvPoints

                w = int(w * image_scale)
                h = int(h * image_scale)
                x = int(x * image_scale)
                y = int(y * image_scale)
                x0, y0, w0, h0 = x, y, w, h
                # print(x, y, w, h)
                if not tight_crop:
                    # Widen box
                    x = int(x - w * 0.5)
                    # x = int(x - w)
                    y = int(y - h * 0.5)
                    w = int(w * 2)
                    # w = int(w * 3)
                    h = int(h * 2)
                    # h = int(h * 3.5)
                # Validate
                img_height, img_width, depth = img.shape
                if x < 0:
                    x = 0
                if y < 0:
                    y = 0
                if x + w > img_width:
                    w = img_width - x
                if y + h > img_height:
                    h = img_height - y
                # print(x, y, w, h)

                # This code draws a box on the original image
                # around the detected face
                if show:
                    # pt1 = (int(x * image_scale), int(y * image_scale))
                    pt1 = (x0, y0)
                    # pt2 = (
                    #     int((x + w) * image_scale),
                    #     int((y + h) * image_scale))
                    pt2 = ((x0 + w0), (y0 + h0))
                    cv2.rectangle(img, pt1, pt2, cv.RGB(255, 0, 0), 3, 8, 0)

                cropped = img[y : y + h, x : x + w]
                if show:
                    cv2.imshow("result", cropped)
                    cv2.waitKey(0)
                head, tail = os.path.split(input_name)
                outfile = os.path.join(outdir, tail + "_" + str(count) + ".jpg")
                if not os.path.isfile(outfile):
                    print("Save to", outfile)
                    cv2.imwrite(outfile, cropped, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
                count += 1

    # This code is show/save the original with boxes around detected faces
    if show:
        cv2.imshow("result", img)
        # outfile = os.path.join(outdir, input_name)
        # cv2.imwrite(outfile, img, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    return count


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Find, crop and save faces (or other objects). Requires OpenCV.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-c",
        "--cascade",
        # default='D:\\temp\\opencv\\data\\haarcascades\\'
        # 'haarcascade_frontalface_alt.xml',
        default="/usr/local/Cellar/opencv/3.4.1_2/share/OpenCV/haarcascades/"
        "haarcascade_frontalface_alt.xml",
        help="Haar cascade file",
    )
    parser.add_argument("-i", "--inspec", default="*.jpg", help="Input file spec")
    parser.add_argument("-o", "--outdir", default="crop", help="Output directory")
    parser.add_argument(
        "-a",
        "--findall",
        action="store_true",
        help="Find all objects in photo instead of biggest (slower)",
    )
    parser.add_argument(
        "-f", "--fast", action="store_true", help="Faster but less accurate detection"
    )
    parser.add_argument(
        "-r", "--recursive", action="store_true", help="Recurse directories"
    )
    parser.add_argument(
        "-t",
        "--tight_crop",
        action="store_true",
        help="Crop image tight around detected feature "
        "(otherwise a margin is added)",
    )
    parser.add_argument(
        "-s", "--show", action="store_true", help="Show detected image with box"
    )

    args = parser.parse_args()
    print(args)

    if args.findall:
        haar_flags = 0

    if args.fast:
        haar_scale = 1.2
        min_neighbors = 2
        haar_flags = haar_flags | cv.CV_HAAR_DO_CANNY_PRUNING

    cascade = cv2.CascadeClassifier(args.cascade)
    if args.show:
        cv.NamedWindow("result", 1)

    files = fileutils.find_files(args.inspec, args.recursive)
    total_files = len(files)
    if total_files == 0:
        sys.exit("No input files found.")

    print(total_files, " files found.")
    total_found = 0
    create_dir(args.outdir)
    for i, filename in enumerate(files):
        print(i + 1, "/", total_files)
        # try:
        total_found += detect_and_save(
            filename, cascade, args.outdir, args.tight_crop, args.show
        )
        #     total_found += detect_and_save(
        #         filename, cascade, args.outdir, args.tight_crop, args.show)
        # except Exception as e:
        #     print(os.getcwd())
        #     print("Cannot detect:", filename)
        #     print(str(e))
        #     print(repr(e))
        #     continue

    if args.show:
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    print("Total found:", total_found)

# End of file
