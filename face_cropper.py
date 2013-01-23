#!/usr/bin/python
"""
Find faces in images and save them to a "crop" subdirectory.

Based on opencv/samples/python/facedetect.py
Original C implementation by:  ?
Python implementation by: Roman Stanchak, James Bowman
"""
import argparse
import cv2.cv as cv
import filelist
import glob
import os
import sys

try: import timing # Optional, http://stackoverflow.com/a/1557906/724176
except: None

# Parameters for Haar detection. From the API:
# The default parameters (scale_factor=2, min_neighbors=3, flags=0) are tuned for accurate yet slow object detection. For a faster operation on real video images the settings are: 
# scale_factor=1.2, min_neighbors=2, flags=CV_HAAR_DO_CANNY_PRUNING, 
# min_size=<minimum possible face size

min_size = (20, 20)
image_scale = 2
haar_scale = 1.2
min_neighbors = 2
haar_flags = cv.CV_HAAR_FIND_BIGGEST_OBJECT 

def create_dir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)

def detect_and_draw(input_name, cascade, outdir):
    count = 0
    img = cv.LoadImage(input_name, 1)
    # Allocate temporary images
    gray = cv.CreateImage((img.width,img.height), 8, 1)
    small_img = cv.CreateImage((cv.Round(img.width / image_scale),
			       cv.Round (img.height / image_scale)), 8, 1)

    # Convert color input image to grayscale
    cv.CvtColor(img, gray, cv.CV_BGR2GRAY)

    # Scale input image for faster processing
    cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)

    cv.EqualizeHist(small_img, small_img)

    if(cascade):
        t = cv.GetTickCount()
        faces = cv.HaarDetectObjects(small_img, cascade, cv.CreateMemStorage(0),
                                     haar_scale, min_neighbors, haar_flags, min_size)
        t = cv.GetTickCount() - t
        print "detection time = %gms" % (t/(cv.GetTickFrequency()*1000.))
        if faces:
            for ((x, y, w, h), n) in faces:
                # The input to cv.HaarDetectObjects was resized, so scale the 
                # bounding box of each face and convert it to two CvPoints

                w = int(w * image_scale)
                h = int(h * image_scale)
                x = int(x * image_scale)
                y = int(y * image_scale)
                print x,y,w,h
                x = int(x - w*0.5)
                y = int(y - h*0.5)
                w = int(w * 2)
                h = int(h * 2)
                if x < 0: x = 0
                if y < 0: y = 0
                if x + w > img.width: w = img.width - x
                if y + h > img.height: h = img.height - y
                print x,y,w,h
                
                # This code draws a box on the original around the detected face
                # # pt1 = (int(x * image_scale), int(y * image_scale))
                # pt1 = (x, y)
                # # pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
                # pt2 = ((x + w), (y + h))
                # cv.Rectangle(img, pt1, pt2, cv.RGB(255, 0, 0), 3, 8, 0)

                cropped = cv.CreateImage((w, h), img.depth, img.nChannels)
                src_region = cv.GetSubRect(img, (x, y, w, h))
                cv.Copy(src_region, cropped)
                # cv.ShowImage("result", cropped)
                head, tail = os.path.split(input_name)
                outfile = os.path.join(outdir, tail + "_" + str(count) + ".jpg")
                print "Save to", outfile
                count += 1
                cv.SaveImage(outfile, cropped)

    # This code is show/save the original with boxes around detected faces
    # cv.ShowImage("result", img)
    # outfile = os.path.join(outdir, input_name)
    # cv.SaveImage(outfile, img)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Find, crop and save faces (or other objects).', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--cascade', default='D:\\temp\\opencv\\data\\haarcascades\\haarcascade_frontalface_alt.xml',
        help='Haar cascade file')
    parser.add_argument('-i', '--inspec', default='*.jpg',
        help='Input file spec')
    parser.add_argument('-o', '--outdir', default='crop',
        help='Output path')
    parser.add_argument('-a', '--findall', action='store_true', default=False,
        help='Find all objects in photo instead of biggest')
    parser.add_argument('-r', '--recursive', action='store_true',
        help='Recurse directories')
    
    args = parser.parse_args()
    print args
    
    if args.findall:
        haar_flags = 0
    
    cascade = cv.Load(args.cascade)
    # cv.NamedWindow("result", 1) # Needed for cv.ShowImage()

    files = filelist.find_files(args.inspec, args.recursive)
    if len(files) == 0:
        sys.exit("No input files found.")

    print len(files), " files found."
    create_dir(args.outdir)
    for file in files:
        try:
            detect_and_draw(file, cascade, args.outdir)
        except:
            print "Cannot detect:", file
            continue

    # cv.WaitKey(0) # Needed for cv.ShowImage()
    # cv.DestroyWindow("result") # Needed for cv.ShowImage()
