#!/usr/bin/env python3
import cv2
import os
from random import sample

#maskDir = "./MaskInput/"
maskDir = "../Vernissage_pipeline/3.ApplyMask/MaskInput/"
#styledDir = "./StyledInput/"
styledDir = "../Vernissage_pipeline/3.ApplyMask/StyledInput/"
#backgroundDir = "../backgroundImages/"
backgroundDir = "../Vernissage_pipeline/backgroundImages/selected/"
outputDir = "../Vernissage_pipeline/3.ApplyMask/Output/"

backgroundImages = os.listdir(backgroundDir)
N_backgroundImages = len(backgroundImages)
NumberList = range(N_backgroundImages)

images = os.listdir(maskDir)

for img in images:
    print(maskDir + img)
    mask = cv2.imread(maskDir + img)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(mask, 10, 255, cv2.THRESH_BINARY)
    print(styledDir + img.replace("mask","styled"))
    styled = cv2.imread(styledDir + img.replace("mask", "styled"))
    
    mask = cv2.blur(mask, (10,10))
    #fg = cv2.multiply(styled,mask)
    fg = cv2.bitwise_and(styled,styled,mask=mask)
    print(backgroundDir+backgroundImages[sample(NumberList, 1)[0]])
    bg = cv2.imread(backgroundDir+backgroundImages[sample(NumberList, 1)[0]])

    res = cv2.addWeighted(fg, .9, bg, 0.9, 0)
    cv2.imwrite(outputDir+img.replace("mask", "finale"), res)
    #cv2.imshow('dst',bg)
    #cv2.waitKey(0)
   
    print("---- "+img)

#cv2.destroyAllWindows()
