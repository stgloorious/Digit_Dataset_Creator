## @package DigitDatasetCreator creates a series of labeled pictures of digits for neural network training and testing.
#
#   This package creates pictures of digits that are in various fonts located in directory "/fonts", randomly rotated and positioned. 
#   Some random noise gets added to every picture. The output is in .csv-Format, like the digits in the MNIST database.
#

import imageio
import numpy
import time
from PIL import Image, ImageDraw, ImageFont
import cv2
import os
import csv
import random
from tqdm import tqdm

import datasetMerge

# *** SETTINGS *** #
Overall_Iterations  = 2   # To get total number of digits multiply this by the number of fonts and 10 digits
Fontsize_Min        = 18
Fontsize_Max        = 26
Position_Error_Min  = -5
Position_Error_Max  = 5
Rotation_Min        = -20
Rotation_Max        = 20
Noise_Intensity     = 5
# ***           *** #
Number_of_Fonts     = 6 # only used by progress bar

def create ():
    # Prepare progress bar
    progress=0
    maxValue=Overall_Iterations*Number_of_Fonts*10
    pbar = tqdm(total=maxValue,desc="Generating digits")

    ## keeps track of how many digit images have been created yet
    counter=0

    directory = os.getcwd() # find out working directory
    with open("dataset.csv", "ab") as f: # create or open "dataset.csv" in append mode
        for i in range (Overall_Iterations):
            for file in os.listdir(directory + "/fonts"): # iterate through all available fonts
                fontname = os.fsdecode(file) # get filename of the font file
                if fontname.endswith(".ttf"): # fonts must be in .ttf format
                    # Select font and size
                    fnt = ImageFont.truetype("fonts/"+fontname, random.randrange(Fontsize_Min,Fontsize_Max))
                    for number in range(10): # There are ten digits

                        # Create new blank digit
                        img = Image.new('RGB', (28, 28), color = (255, 255, 255))
                        d = ImageDraw.Draw(img) 
                        w, h = d.textsize(str(number), font=fnt) # write the digit on top of the image

                        # Position the digit (randomly around center)
                        d.text(( ((28-w)/2 + random.randrange(Position_Error_Min,Position_Error_Max)) ,(28-h)/2+ random.randrange(Position_Error_Min,Position_Error_Max)), str(number), font=fnt, fill="black")
                        
                        # Rotate the image randomly
                        img=img.rotate(random.randrange(Rotation_Min,Rotation_Max),Image.NEAREST,fillcolor='white')

                        # NOISE ADDING
                        # Create a noise mask which can be laid on top of the image
                        noise_mask = numpy.random.normal(0,Noise_Intensity,28*28)
                        noise_mask =  noise_mask.reshape(28,28).astype('int16')
                        # convert the image to openCV format
                        cvImg = numpy.array(img) 
                        cvImg = cv2.cvtColor(cvImg,cv2.COLOR_RGB2GRAY)
                        # add the noise mask to the image
                        noisy_img=cv2.add(cvImg.astype('int16'),noise_mask).astype('int16')
                        # make sure noise can not cause integer under/overflow
                        noisy_img[noisy_img < 0] = 0
                        noisy_img[noisy_img > 255] = 255
                        # convert back to "Image" format
                        noisy_img=noisy_img.astype('uint8')
                        # Save in png format
                        #img = Image.fromarray(noisy_img)
                        #img.save('dataset_pictures/'+str(number)+'_'+str(counter)+'.png') 
                        # reshape
                        img_data = 255.0 - noisy_img.reshape(1,28*28)

                        # insert label
                        img_data=numpy.insert(img_data,0,str(number))

                        # reshape and save to csv
                        img_data=img_data.reshape(1,28*28+1)
                        numpy.savetxt(f,img_data,delimiter=",",fmt="%g")

                        counter=counter+1
                        pbar.update()
                    pass
            pass
        pass
    pbar.close()
    print("Created %d pictures." %(counter))
pass
    
datasetMerge.merge("C:/Users/stefa/Desktop/mnist_train.csv","C:/Users/stefa/Dropbox/Documents/Hobby/Software/Python/DigitDatasetCreator/training.csv",
"C:/Users/stefa/Dropbox/Documents/Hobby/Software/Python/DigitDatasetCreator/merged_training.csv")

