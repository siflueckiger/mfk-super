#!/usr/bin/env python3
import cv2
import os
from random import sample

class ApplyMask:
    def __init__(self,maskDir, styledDir, backgroundDir, outputDir, SimMode = False):
        self.maskDir = maskDir
        self.styledDir = styledDir
        self.backgroundDir = backgroundDir
        self.outputDir = outputDir
        self.imgs = os.listdir(maskDir)
        self.SIMULATION_MODE = SimMode

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
        if not self.SIMULATION_MODE:
            self._processImages()
            self._cleanUp()
        else:
            self.sim_run()

    def sim_run(self):
        backgroundImages = os.listdir(backgroundDir)
        N_backgroundImages = len(backgroundImages)
        NumberList = range(N_backgroundImages)

        for img in self.imgs:
            if img.startswith("."):
                continue
            print(img)
            mask = cv2.imread(maskDir + img)
            styled = cv2.imread(styledDir + img.replace("mask", "styled"))
            
            bg = cv2.imread(backgroundDir+backgroundImages[sample(NumberList, 1)[0]])
            res = cv2.putText(styled, "Image Processed - Sincerely your Apply Mask Braino", (50,500), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 5)
            cv2.imwrite(outputDir+img.replace("mask", "finale"), res)

if __name__ == "__main__":
    
    maskDir = "./MaskOutput/"
    #maskDir = "../pipeline/3.ApplyMask/MaskInput/"
    #styledDir = "./StyledInput/"
    styledDir = "./StyleOutput/"
    #backgroundDir = "../backgroundImages/"
    backgroundDir = "./Backgrounds/"
    outputDir = "./ApplyOutput/"

    applyMask = ApplyMask(maskDir, styledDir, backgroundDir, outputDir, True)
    applyMask.run()
    



