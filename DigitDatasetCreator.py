## @package DigitDatasetCreator
#
#

import imageio
import matplotlib.pyplot
import numpy
import time
from PIL import Image, ImageDraw, ImageFont
import cv2
import os
import csv
import random
from tqdm import tqdm

matplotlib.pyplot.ion()

def displayFile (filename):
    print(filename)
    img=cv2.imread(filename,cv2.IMREAD_GRAYSCALE)
    img_data = 255.0 - img.reshape(28*28)
    img_data = (img_data / 255.0 * 0.99) + 0.01
    image_array = numpy.asfarray(img_data).reshape((28,28))
    matplotlib.pyplot.imshow(image_array,cmap='binary',interpolation=None)
pass

progress=0
maxValue=1000*6*10
pbar = tqdm(total=maxValue,desc="Generating digits")

counter=0
directory = os.getcwd()
with open("dataset.csv", "ab") as f:
    for i in range (1000):
        for file in os.listdir(directory + "/fonts"):
            fontname = os.fsdecode(file)
            if fontname.endswith(".ttf"):
                fnt = ImageFont.truetype("fonts/"+fontname, random.randrange(18,26))
                for number in range(10):
                    new_img = Image.new('RGB', (28, 28), color = (255, 255, 255))
                    d = ImageDraw.Draw(new_img) 
                    w, h = d.textsize(str(number), font=fnt)
                    d.text(( ((28-w)/2 + random.randrange(-5,5)) ,(28-h)/2+ random.randrange(-5,5)), str(number), font=fnt, fill="black")
                    new_img=new_img.rotate(random.randrange(-20,20),Image.NEAREST,fillcolor='white')
                    gauss = numpy.random.normal(0,5,28*28)
                    gauss = gauss.reshape(28,28).astype('int16')

                    opencvImage = numpy.array(new_img)
                    opencvImage = cv2.cvtColor(opencvImage,cv2.COLOR_RGB2GRAY)
                
                    new_gauss=cv2.add(opencvImage.astype('int16'),gauss).astype('int16')
                    new_gauss[new_gauss < 0] = 0
                    new_gauss[new_gauss > 255] = 255
                    new_gauss=new_gauss.astype('uint8')
                    new_img = Image.fromarray(new_gauss)
                    #new_img.save('dataset_pictures/'+str(number)+'_'+str(counter)+'.png')
                    img_data = 255.0 - new_gauss.reshape(1,28*28)
                    img_data=numpy.insert(img_data,0,str(number))
                    img_data=img_data.reshape(1,28*28+1)
                    numpy.savetxt(f,img_data,delimiter=",",fmt="%g")

                    #print("Created picture %d using font %s" %(counter, fontname))
                    counter=counter+1
                    pbar.update()
                pass
        pass
    pass
pbar.close()
print("Created %d pictures." %(counter))

    



