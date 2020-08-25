## @package datasetMerge Randomly merges to given datasets in .csv format
# 
#

import os
import random
import numpy
from tqdm import tqdm

## Merges two data sets into one
# @param src1 First data set
# @param scr2 Second data set
# @param dest Destination directory
#
def merge (src1, src2, dest):
    sizeSrc1 = os.path.getsize(src1)
    sizeSrc2 = os.path.getsize(src2)
    p1 = sizeSrc1/(sizeSrc1+sizeSrc2)
    p2 = sizeSrc2/(sizeSrc1+sizeSrc2)
    print ("%s is %i Bytes, %s is %i Bytes." %(os.fsdecode(src1),sizeSrc1,os.fsdecode(src2),sizeSrc2))
    print ("%s has %.2f %% probability to be chosen, %s has %.2f %% chance" %(os.fsdecode(src1), p1*100, os.fsdecode(src2), p2*100))

    src1_file = open(src1,'r')
    src1_list = src1_file.readlines()
    src1_file.close()
    src1_list_pointer = len(src1_list)

    src2_file = open(src2,'r')
    src2_list = src2_file.readlines()
    src2_file.close()
    src2_list_pointer = len(src2_list)

    dest_list = []

    # Prepare progress bar
    progress=0
    maxValue=src1_list_pointer+src2_list_pointer
    pbar = tqdm(total=maxValue,desc="Merging data")

    while (src1_list_pointer != 0) or (src2_list_pointer != 0):
        value = random.random()
        if (value < p1 and src1_list_pointer != 0) or (src2_list_pointer == 0):
            dest_list.append(src1_list[src1_list_pointer-1].strip("\n"))
            src1_list_pointer=src1_list_pointer-1
        else:
            dest_list.append(src2_list[src2_list_pointer-1].strip("\n"))
            src2_list_pointer=src2_list_pointer-1
        pass 
        pbar.update()
    pbar.close()
    print("Merging complete.")
    numpy.savetxt(dest, dest_list, delimiter=',', fmt='%s')
pass