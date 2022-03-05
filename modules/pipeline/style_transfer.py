#!/usr/bin/env python3
#comment fluegu
import subprocess
import os

# Functions
def makdirIfnotExists(dirName):
    if not os.path.exists(dirName):
        os.makedirs(dirName)

class StyleTransfert:
    def __init__(self, checkPointDirectory, inputDirectory, outputDirectory,SimMode = False):
        self.SIMULATION_MODE = SimMode
        print()
        print("----")
        self.checkPointDir = checkPointDirectory
        print("checkpoint path: ", self.checkPointDir)
        print(inputDirectory)
        self.inputDir = inputDirectory
        self.imgs = os.listdir(self.inputDir)
        #self.copyFromPipelineDirectory()
        self.outputDir = outputDirectory
        print("output Path: ", self.outputDir)
        self.LocalOutputDir = "./pipelineOutput/"
        makdirIfnotExists(self.LocalOutputDir)

        self.checkPathes()

    def copyFromPipelineDirectory(self):
        print("---- Copying from Pipeline Input Directory")
        subprocess.call("cp " + self.inputDir + "* ./input-image/", shell=True)
        self.inputDir = "./input-image/"
        print("input Path: ", inputDir)


    def checkPathes(self):
        print("---- CheckpointDir Exists: ", os.path.exists(self.checkPointDir))
        print("---- input Dir Exists: ", os.path.exists(self.inputDir))
        print("---- outputDir Exists: ", os.path.exists(self.outputDir))

    def setSubprocessComand(self):
        self.command = "tensorman run --gpu -- python evaluate.py \
             --checkpoint {0} \
             --in-path {1} \
             --out-path {2} \
             --allow-different-dimensions".format(self.checkPointDir, self.inputDir, self.LocalOutputDir)
        print("----", self.command)

    def _processImages(self):
        subprocess.call(self.command, shell=True)

    def run(self):
        if not self.SIMULATION_MODE:
            self._processImages()
            self._renameOutputFiles()
            self._copyBackToPipelineDirectory()
        else:
            self._sim_run()

    def _sim_run(self):
        import cv2
        import datetime
        print("---- Testing ---- This Step is run in SIMULATION MODE")
        print(self.imgs)
        for img in self.imgs:
            print(img)
            print(self.inputDir)
            if img.startswith("."):
                continue
            imgage = cv2.imread(self.inputDir + img)
            print("{}{}".format(self.inputDir, img))
            res = cv2.putText(imgage, "Image Processed - Sincerely your Style Transfert Braino", (50,250), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 5)
            res = cv2.putText(imgage, "{}".format(datetime.datetime.now()), (50,350), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 5)
            cv2.imwrite(self.outputDir+img, res)

    def _renameOutputFiles(self):
        print("---- Rename output Files")
        self.images = os.listdir(self.LocalOutputDir)
        for img in self.images:
            os.rename(self.LocalOutputDir+img, self.LocalOutputDir+"styled_"+img)

    def _copyBackToPipelineDirectory(self):
        print("---- Copy back to Pipeline directory.")
        subprocess.call("cp "+self.LocalOutputDir+"* "+self.outputDir, shell=True)
        subprocess.call("rm "+self.LocalOutputDir+"*", shell=True)
        subprocess.call("rm "+self.inputDir+"*", shell=True)
        print("---- Returning to pipeline")

if __name__ == "__main__":
    checkPointDir = "./checkpoints/useForEvaluation/LargerTrainingDataSet_Train2014_and_WIDER_train_and_OI_Challenge_neonMask_epoches_8/"
    inputDir =  "./Temp/2.1_StyleTransfertInput/"
    outputDir = "./Temp/2.2_StyleTransfertOutput/"

    styleTransfert = StyleTransfert(checkPointDir, inputDir, outputDir, SimMode=True) 
    styleTransfert.run()