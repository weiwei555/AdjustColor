# import the necessary packages
import random

from skimage import measure
import numpy as np
import imutils
import cv2

image_path = "input/input3.jpg"
output_path = "output/output3.jpg"
lower_bound = 50
color_bound_l = 70
color_bound_h = 255
upper_bound = 150

def processPatch(pts):
    intensities = image[pts[0], pts[1]]

    total = len(pts[0])
    down = total/4*3
    for j in range(len(pts[0])):
        ratio = 1
        if j > down:
            go = random.random()
            if go > 0.3:
                continue
        # row indices
        y = pts[0][j]
        # column indices
        x = pts[1][j]
        intensity = image_origin[y,x]
        r1 = intensity[2]
        g1 = intensity[1]
        b1 = intensity[0]
        max_v = max(r1,g1,b1)
        min_v = min(r1,g1,b1)

        # aims for comparison?
        r,g,b = comparison(r1,g1,b1,min_v,max_v)

        # blue, green, red?
        if (max_v - min_v) > 10 and max(r1,g1,b1) > color_bound_l and max(r1,g1,b1) < color_bound_h:
            r = r*0.9* ratio+r1*0.3+10
            g = g*0.4* ratio+g1*0.7+10
            b = b*0.7* ratio+b1*0.3+10
            r,g,b = overflow(r,g,b)
            rgb = [r,g,b]
            image[y,x] = rgb
            continue
        r = r*0.05* ratio+r1*0.9
        g = g*0.05* ratio+g1*0.9
        b = b*0.05* ratio+b1*0.9
        mean = (r+g+b)/3.0
        # averaging
        rgb = [r,g,b]
        if (max_v - min_v) < 50:
            for c in range(len(rgb)):
                if rgb[c] > mean:
                    rgb[c] -= (rgb[c]-mean)*0.8
                elif rgb[c] < mean:
                    rgb[c] += (mean-rgb[c])*0.8
        elif (max_v - min_v) > 50:
            for c in range(len(rgb)):
                if rgb[c] > mean:
                    rgb[c] -= (rgb[c]-mean)*0.3
                elif rgb[c] < mean:
                    rgb[c] += (mean-rgb[c])*0.3
        r,g,b = rgb[0], rgb[1], rgb[2]
        r,g,b = overflow(r,g,b)
        image[y,x] = [r,g,b]

    #process_brush(image, pts)

def overflow(r,g,b):
    if r > 255:
        r = 255
    if g > 255:
        g = 255
    if b > 255:
        b = 255
    if r < 0:
        r = 0
    if g < 0:
        g = 0
    if b < 0:
        b = 0
    return r,g,b

def comparison(r,g,b,min_v,max_v):
    change = 0.8
    if max_v == g:
        if min_v == r:
            r += 0.2*g
        else:
            b += 0.6*g
        g = 0
    if max_v == b:
        if min_v == g:
            g += 0.5*b
            r += 0.3*b
        else:
            r += 0.5*b
            g += 0.3*b
        b = 0.25*b
    if max_v == r:
        if min_v == b:
            b += 0.5*r
            g += 0.3*r
        else:
            b += 0.3*r
            g += 0.5*r
        r = 0.4*r
    return r,g,b

def process_brush(image):
    image_brush0 = cv2.imread("input/brush1.jpg")
    image_brush = image_brush0.copy()
    rows,cols,channels = image_brush.shape

    # ROI = image[y1:y2, x1:x2]
    roi = image[0:rows, 0:cols]
    roi2 = image[0:rows, 0:cols]

    # Now create a mask of brush and create its inverse mask also
    img2gray = cv2.cvtColor(image_brush,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 100, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    # Now black-out the area of brush in ROI
    img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)

    # Take only region of brush from brush image.
    img2_fg = cv2.bitwise_and(image_brush,image_brush,mask = mask)

    # Put brush in ROI and modify the main image
    dst = cv2.addWeighted(img1_bg, 1, img2_fg, 1, 0)
    image[0:rows, 0:cols] = dst


def main(image):
    ## start ##

    # load the image, convert it to grayscale, and blur it
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (11, 11), 0)

    # threshold the image to reveal light regions in the
    # blurred image
    # first number: threshold, second number: maxvalue. (200, 255) for bright patches
    #thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 135, 6)
    thresh = cv2.threshold(blurred, lower_bound, 150, cv2.THRESH_BINARY_INV)[1]
    process(thresh, image)
    thresh = cv2.threshold(blurred, upper_bound, 255, cv2.THRESH_BINARY)[1]
    process(thresh, image)


def process(thresh, image):
    # perform a series of erosions and dilations to remove
    # any small blobs of noise from the thresholded image
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=4)

    # perform a connected component analysis on the thresholded
    # image, then initialize a mask to store only the "large"
    # components
    labels = measure.label(thresh, background=0, connectivity=2)
    mask = np.zeros(thresh.shape, dtype="uint8")

    # loop over the unique components
    for label in np.unique(labels):
        # if this is the background label, ignore it
        if label == 0:
            continue
        # otherwise, construct the label mask and count the
        # number of pixels
        labelMask = np.zeros(thresh.shape, dtype="uint8")
        labelMask[labels == label] = 255
        numPixels = cv2.countNonZero(labelMask)
        # if the number of pixels in the component is sufficiently
        # large, then add it to our mask of "large blobs"
        if numPixels > 300:
            mask = cv2.add(mask, labelMask)

    # find the contours in the mask
    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    # For each list of contour points...
    for i in range(len(contours)):

        # Create a mask image that contains the contour filled in
        cimg = np.zeros_like(image)
        cv2.drawContours(cimg, contours, i, color=(255, 255, 255), thickness=-6)

        # Find the corresponding position of a patch we want to modify
        pts = np.where(cimg == (255, 255, 255))

        # Get all the intensities on all pixels in this patch
        intensities = image[pts[0], pts[1]]
        processPatch(pts)

        #cv2.drawContours(cimg, contours, i, color=lst_intensities[i], thickness=-1)

    # draw out the contours we've found
    # blank = np.zeros(image.shape, dtype = np.uint8)
    # contour_img = cv2.drawContours(image, contours, -1, (255,255,255), 2)

image_origin = cv2.imread(image_path)
image = image_origin.copy()
main(image)

# show the output image
cv2.imwrite(output_path, image)
#cv2.imwrite("output/contour.jpg", contour_img)
#cv2.imwrite("output/mask.jpg", mask)
#cv2.imwrite("output/cimg.jpg", cimg)
