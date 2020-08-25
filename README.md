# Digit Dataset Creator
### Used to generate images of digits to use for neural networks

This module uses several fonts (can be provided in directory, must be .ttf format) to generate labeled 28 x 28 pixel images of numerical digits 0...9. 
Random image rotation, position and noise is added to the images to create a larger dataset. Output format is standardized .csv for easy use 
(Every line is an image, first entry is the label. Pixel value ranges from 0 to 255). Compatible with project linked below.

There is also a function to merge two datasets together (e.g. a dataset created by this module and a MNIST-based one).

Neural Network can be found [here](https://github.com/stgloorious/OCR_Mnist_Digits)

![Digits](https://github.com/stgloorious/DigitDatasetCreator/blob/master/docs/digits.png)
