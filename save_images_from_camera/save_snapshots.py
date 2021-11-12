#!/usr/bin/env python3

"""
Saves a series of snapshots with the current camera as snapshot_<width>_<height>_<nnn>.jpg

Arguments:
    --f <output folder>     default: current folder
    --n <file name>         default: snapshot
    --w <width px>          default: none
    --h <height px>         default: none

Buttons:
    q           - quit
    space bar   - save the snapshot
    
  
"""

import cv2
import time
import sys
import argparse
import os


def save_snaps(width=640, height=480, name="snapshot", folder="images", raspi=False):

    # if raspi:
    #     os.system('sudo modprobe bcm2835-v4l2')

    print(width,height)

    cam = cv2.VideoCapture('/dev/video0')

    cam.set(cv2.CAP_PROP_FRAME_WIDTH, width )
    
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height )

    # cap = cv2.VideoCapture(0)

    # cap.set(3,1280)

    # cap.set(4,1024)

    time.sleep(2)

    # cap.set(15, -8.0)

    if width > 0 and height > 0:
        print("Setting the custom Width and Height")
        # cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    try:
        if not os.path.exists(folder):
            os.makedirs(folder)
            # ----------- CREATE THE FOLDER -----------------
            folder = os.path.dirname(folder)
            try:
                os.stat(folder)
            except:
                os.mkdir(folder)
    except:
        pass

    nSnap   = 0
    w       = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
    h       = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

    fileName    = "%s/%s_%d_%d_" %(folder, name, w, h)

    while True:
        ret, frame = cam.read()

        cv2.imshow('camera', frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        if key == ord('s'):
            print("Saving image ", nSnap)
            cv2.imwrite("%s%d.jpg"%(fileName, nSnap), frame)
            nSnap += 1

    cam.release()
    cv2.destroyAllWindows()




def main():

    # ---- DEFAULT VALUES ---
    SAVE_FOLDER = "images"
    FILE_NAME = "snapshot"
    FRAME_WIDTH = 640
    FRAME_HEIGHT = 480

    # ----------- PARSE THE INPUTS -----------------

    parser = argparse.ArgumentParser(description="Saves snapshot from the camera. \n q to quit \n spacebar to save the snapshot")
    parser.add_argument("--folder", default=SAVE_FOLDER, help="Path to the save folder (default: current)")
    parser.add_argument("--name", default=FILE_NAME, help="Picture file name (default: snapshot)")
    parser.add_argument("--dwidth", default=FRAME_WIDTH, type=int, help="<width> px (default the camera output)")
    parser.add_argument("--dheight", default=FRAME_HEIGHT, type=int, help="<height> px (default the camera output)")
    parser.add_argument("--raspi", default=False, type=bool, help="<bool> True if using a raspberry Pi")
    args = parser.parse_args()

    SAVE_FOLDER = args.folder
    FILE_NAME = args.name
    FRAME_WIDTH = 640 #args.dwidth
    FRAME_HEIGHT = 480 #args.dheight

    print(SAVE_FOLDER,FILE_NAME,FRAME_WIDTH,FRAME_HEIGHT,'+',args.dwidth,args.dheight)

    save_snaps(width=args.dwidth, height=args.dheight, name=args.name, folder=args.folder, raspi=args.raspi)

    print("Files saved")

if __name__ == "__main__":
    main()