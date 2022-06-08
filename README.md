# AdjustColor
CSE 455 final project - a basic color adjuster based on values on a painting

## Introduction
Welcome to AdjustColor!

This project aims to add color variety on paintings and save the painters' time, and also show variations of their painting for inspiring.

Painters can upload their painting in the input file (also need to have a copy in output file), and change the "image_path", "output_path" in HidingColor.py as their image file name.

This project uses mainly knowledges of rgb colorspace, color theorem, contour finding and patch processing. Patches with different values are extracted and their color can be changed accordingly. For this rough version of the project, I only provides limited functions due to the time reason. Therefore, there are 4 parameters that the user should adjust according to their paintings and the output of the program. Constantly change the parameter and see the result, until you are satisfied with it!

Below are some sample input image, parameters, output image for referencing:

parameters:
```
image_path = "input/input3.jpg"
output_path = "output/output3.jpg"
lower_bound = 50
color_bound_l = 70
color_bound_h = 255
upper_bound = 150
```

<img src="https://github.com/weiwei555/AdjustColor/blob/main/input/input3.jpg" alt="input image" width="400"> <img src="https://github.com/weiwei555/AdjustColor/blob/main/output/output3.jpg" alt="output image" width="400">

