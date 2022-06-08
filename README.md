# AdjustColor
CSE 455 final project - a basic color adjuster based on values on a painting

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
parameters 2:
```
image_path = "input/input6.jpg"
output_path = "output/output6.jpg"
lower_bound = 30
color_bound_l = 20
color_bound_h = 140
upper_bound = 150
```

<img src="https://github.com/weiwei555/AdjustColor/blob/main/input/input6.jpg" alt="input image" width="400"> <img src="https://github.com/weiwei555/AdjustColor/blob/main/output/output6.jpg" alt="output image" width="400">


## Technique explaination
This project mainly uses python and openCV. The thought behind is to extract the darkest patches and the brightest patches of a painting respectively, then give them different colors based on their original color.

# To extract the darkest/lightest patches:
We need to turn the image into grayscale and blur it like this:

```
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (11, 11), 0)
```

Then we can use the grab_contour function provided by openCV to do extractions. Notice that different parameters are needed for extracting darkest and brightest patches. Here, we mainly use the 2 parameters given by user: lower_bound, upper_bound.
lower_bound: pixels with value less than this bound won't be extracted into lowest set
upper_bound: pixels with value more than this bound won't be extracted into brightest set

```
thresh = cv2.threshold(blurred, lower_bound, 150, cv2.THRESH_BINARY_INV)[1]
process(thresh, image)
thresh = cv2.threshold(blurred, upper_bound, 255, cv2.THRESH_BINARY)[1]
process(thresh, image)
```



