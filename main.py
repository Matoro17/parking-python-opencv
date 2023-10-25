# importing everything we need
import cv2
import csv
import time
import os
import numpy as np


# declaring a static variable
class spots:
    loc = 0


camFeed = 'http://www.insecam.org/en/view/883184/'
location = "https://www.google.com/maps/place/37%C2%B028'38.0%22N+126%C2%B051'59.0%22E/@37.477038,126.8665127,19z/data=!4m5!3m4!1s0x0:0x0!8m2!3d37.47722!4d126.86639"
# function to determine if a spot is free/occupied
# params: image source, individual spot coordinates


def drawRectangle(img, a, b, c, d):
    # cutting the image based on the coodrinates
    sub_img = img[b:b + d, a:a + c]
    # extracting the edges
    edges = cv2.Canny(sub_img, lowThreshold, highThreshold)
    # counting the white pixels
    pix = cv2.countNonZero(edges)
    # testing if the pixels number is in the given range
    if pix in range(min, max):
        # drawing a green rectangle on the source image using the given coordinates
        # and increasing the number of available spots
        cv2.rectangle(img, (a, b), (a + c, b + d), (0, 255, 0), 3)
        spots.loc += 1
    else:
        # drawing a red rectangle on the source image if the pixels number is not in the range
        cv2.rectangle(img, (a, b), (a + c, b + d), (0, 0, 255), 3)


# empty callback function for creating trackar
def callback(foo):
    pass


def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images


# getting the spots coordinates into a list
with open('../coordenadas.csv', 'r', newline='') as inf:
    csvr = csv.reader(inf)
    rois = list(csvr)
# converting the values to integer
rois = [[int(float(j)) for j in i] for i in rois]

# creating the parameters window with trackbars
cv2.namedWindow('parameters')
cv2.createTrackbar('Threshold1', 'parameters', 410, 700, callback)
cv2.createTrackbar('Threshold2', 'parameters', 700, 700, callback)
cv2.createTrackbar('Min pixels', 'parameters', 0, 1500, callback)
cv2.createTrackbar('Max pixels', 'parameters', 102, 1500, callback)

# select the video source; 0 - integrated webcam; 1 - external webcam;

# start the live feed
while True:
    imagens_stack = load_images_from_folder('../data')
    for fr in imagens_stack:
        # set the number of spots to 0
        spots.loc = 0
        frame = fr
        # define the range of pixels and the thresholds for Canny function
        min = cv2.getTrackbarPos('Min pixels', 'parameters')
        max = cv2.getTrackbarPos('Max pixels', 'parameters')
        lowThreshold = cv2.getTrackbarPos('Threshold1', 'parameters')
        highThreshold = cv2.getTrackbarPos('Threshold2', 'parameters')

        # apply the function for every list of coordinates
        for i in range(len(rois)):
            drawRectangle(frame, rois[i][0], rois[i]
                          [1], rois[i][2], rois[i][3])

        # adding the number of available spots on the shown image
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, 'Available spots: ' + str(spots.loc),
                    (10, 30), font, 1, (0, 255, 0), 3)

        imS = cv2.resize(frame, (960, 540))                # Resize image
        cv2.imshow("output", imS)
        time.sleep(2)
        # listen for 'Q' key to stop the stream
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# when everything is done, release the capture

cv2.destroyAllWindows()
