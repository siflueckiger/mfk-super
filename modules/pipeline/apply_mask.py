#!/usr/bin/env python3
import cv2
import os
from random import sample

class ApplyMask:
    def __init__(self,maskDir, styledDir, backgroundDir, outputDir):
        self.maskDir = maskDir
        self.styledDir = styledDir
        self.backgroundDir = backgroundDir
        self.outputDir = outputDir
        self.imgs = os.listdir(maskDir)

    def _processImages(self):
        backgroundImages = os.listdir(backgroundDir)
        N_backgroundImages = len(backgroundImages)
        NumberList = range(N_backgroundImages)

        for img in self.imgs:
            if img.startswith("."):
                print(img)
                continue
            print(img)
            mask = cv2.imread(maskDir + img)
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(mask, 10, 255, cv2.THRESH_BINARY)
            styled = cv2.imread(styledDir + img.replace("mask", "styled"))
            
            mask = cv2.blur(mask, (10,10))
            fg = cv2.bitwise_and(styled,styled,mask=mask)
            bg = cv2.imread(backgroundDir+backgroundImages[sample(NumberList, 1)[0]])

            res = cv2.addWeighted(fg, .9, bg, 0.9, 0)
            cv2.imwrite(outputDir+img.replace("mask", "finale"), res)

    def _cleanUp(self):
        pass

    def run(self):
        self._processImages()
        self._cleanUp()

    def sim_run(self):
        print("Pretending to put images together.")

if __name__ == "__main__":
    
    maskDir = "./MaskOutput/"
    #maskDir = "../pipeline/3.ApplyMask/MaskInput/"
    #styledDir = "./StyledInput/"
    styledDir = "./StyleOutput/"
    #backgroundDir = "../backgroundImages/"
    backgroundDir = "./Backgrounds/"
    outputDir = "./ApplyOutput/"

    applyMask = ApplyMask(maskDir, styledDir, backgroundDir, outputDir)
    applyMask.run()
    



