# AdjustColor
CSE 455 final project - a basic color adjuster based on values on a painting
Owner: Wei Wu (wuwei33)

Paintings used as examples are credited to: @Zeen Chin, @weng weng chim

## Introduction
Welcome to AdjustColor!

This project aims to add color variety on paintings and save the painters' time, and also show variations of their painting for inspiring.

Painters can upload their painting in the input file (also need to have a copy in output file), and change the "image_path", "output_path" in HidingColor.py as their image file name.

This project uses mainly knowledges of rgb colorspace, color theorem, contour finding and patch processing. Patches with different values are extracted and their color can be changed accordingly. For this rough version of the project, I only provides limited functions due to the time reason. Therefore, there are 4 parameters that the user should adjust according to their paintings and the output of the program. Constantly change the parameter and see the result, until you are satisfied with it!

Below are some sample input image, parameters, output image for referencing:

### Image example 1
parameters 1:
```
image_path = "input/input3.jpg"
output_path = "output/output3.jpg"
lower_bound = 50
color_bound_l = 70
color_bound_h = 255
upper_bound = 150
```

<img src="https://github.com/weiwei555/AdjustColor/blob/main/input/input3.jpg" alt="input image" width="400"> <img src="https://github.com/weiwei555/AdjustColor/blob/main/output/output3.jpg" alt="output image" width="400">

parameters 2:
```
image_path = "input/input3.jpg"
output_path = "output/output3.jpg"
lower_bound = 50
color_bound_l = 70
color_bound_h = 190
upper_bound = 150
```

<img src="https://github.com/weiwei555/AdjustColor/blob/main/input/input3.jpg" alt="input image" width="400"> <img src="https://github.com/weiwei555/AdjustColor/blob/main/output/output3_2.jpg" alt="output image" width="400">

### Image example 2
parameters 1:
```
image_path = "input/input6.jpg"
output_path = "output/output6.jpg"
lower_bound = 30
color_bound_l = 20
color_bound_h = 140
upper_bound = 150
```

<img src="https://github.com/weiwei555/AdjustColor/blob/main/input/input6.jpg" alt="input image" width="400"> <img src="https://github.com/weiwei555/AdjustColor/blob/main/output/output6.jpg" alt="output image" width="400">


### Image example 3
parameters 1:
```
image_path = "input/input7.jpg"
output_path = "output/output7.jpg"
lower_bound = 70
color_bound_l = 20
color_bound_h = 136
upper_bound = 150
```

<img src="https://github.com/weiwei555/AdjustColor/blob/main/input/input7.jpg" alt="input image" width="300"> <img src="https://github.com/weiwei555/AdjustColor/blob/main/output/output7.jpg" alt="output image" width="300">


## Techniques explaination
This project mainly uses python and openCV. The thought behind is to extract the darkest patches and the brightest patches of a painting respectively, then give them different colors based on their original color.

### Parameters explain:
```
lower_bound = pixels with value < this will be affected
color_bound_l = pixels with value > this will have higher saturation after change
color_bound_h = pixels with value < this will have higher saturation after change
upper_bound = pixels with value > this will be affected
```

### To extract the darkest/brightest patches:
We need to turn the image into grayscale and blur it like this:

```
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (11, 11), 0)
```

Then we can use the grab_contour function provided by openCV to do extractions. Notice that different parameters are needed for extracting darkest and brightest patches. Here, we mainly use the 2 parameters given by user: lower_bound, upper_bound.

```
thresh = cv2.threshold(blurred, lower_bound, 150, cv2.THRESH_BINARY_INV)[1]
process(thresh, image)
thresh = cv2.threshold(blurred, upper_bound, 255, cv2.THRESH_BINARY)[1]
process(thresh, image)
```


The next important step is to draw and grab contours around these patches, so that we can really grab the contents inside the patches and modify them later:
```
contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)
```

Then, we process each patch among all the patches we've found. This step aims to get the patch shape (and all the pixel positions in this patch) by processing the contours we've found.

```
for i in range(len(contours)):
        # Create a mask image that contains the contour filled in
        cimg = np.zeros_like(image)
        cv2.drawContours(cimg, contours, i, color=(255, 255, 255), thickness=-6)

        # Find the corresponding position of a patch we want to modify
        pts = np.where(cimg == (255, 255, 255))

        # Get all the intensities on all pixels in this patch
        intensities = image[pts[0], pts[1]]
        processPatch(pts)
```

Finally, we use our algorithm inside processPatch(pts) to change the colors inside each patch, and save it as the output.

For the algorithm which chooses color, we try to change its hue by minimizing the largest component among R,G,B and make addition to the smaller components among them. Also, we handled the saturation of the colors so that they are increased but not too different from the original one.

To make a transition between the patches with changed color and the unchanged one, we decrease the number of colored pixels at the bottom of each patch. This can be improved in the future by recognizing where the transition with strongest comparisons happens and decrease number of colored pixels at that direction.

A brush function is also included in HidingColor.py. This is a try that apply the figure of a brush to the painting and will be able to increase textures of each patch randomly in the future, after further implementation.
