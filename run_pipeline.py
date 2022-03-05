
#from asyncio.windows_utils import pipe
import os
import shutil
import subprocess
import sys
import time

from config import api_secret, api_key
from modules.flickr.flickrApi import Flickr

from modules.pipeline.image_segmentation import ImageSegmentation
from modules.pipeline.style_transfer import StyleTransfert

# Helper functions
def makdirIfnotExists(dirName):
    if not os.path.exists(dirName):
        os.makedirs(dirName)




class Pipeline:
    dropDir = "./drop/"
    maskInputDir = "./modules/pipeline/Temp/1.1_MaskInput/"
    maskOutputDir = "./modules/pipeline/Temp/1.2_MaskOutput/"
    styleTransfertInputDir = "./modules/pipeline/Temp/2.1_StyleTransfertInput/"
    styleTransfertOutputDir = "./modules/pipeline/Temp/2.2_StyleTransfertOutput/"
    checkpointDir = "./Some/Directory/"
    applyMaskInputDir = "./pipeline/3.ApplyMask/"
    rawImagesDir = "./rawImages/"


    def __init__(self, drpDir, outpDir, simulate = {"Mask" : False, "Transfert": False,"Apply" : False}):

        #dropDir = "./drop/
        #imgs = os.listdir(dropDir) 
        self.dropDir = drpDir
        self.updateImgs()
        self.outputDir = outpDir
        self.then = None
        self.now = None
        self.simMask = simulate["Mask"]
        self.simTrans = simulate["Transfert"]
        self.simApply = simulate["Apply"]

    def updateImgs(self):
        self.imgs = os.listdir(self.dropDir)

    def run(self):
        self.setThen()
        self.MoveImagesToPipeline()
        #this.CleanUp()
        print("############ Starting Pipeline ############")

        self.GenerateMask()
        self.StyleTransfer()
        #self.ApplyMask()
        #self.CleanUp()
        #self.MoveImagesToRaw()

        self.setNow()
        self.evaluatePipeline()
        self.uploadToFlicker()

    def setThen(self):
        self.then = time.time()

    def setNow(self):
        self.now = time.time()
        
    def evaluatePipeline(self):
        ellapsed = (self.now-self.then)
        minutes = round(ellapsed/60,0)
        seconds = round(ellapsed%60,2)
        nImages = len(self.imgs)
        perImage = ellapsed/nImages

        print("###### It took" ,minutes,"minutes and", seconds, "seconds to run" , nImages , "images.")

        print("###### This is", round(perImage, 2) ,"seconds per image.")

    def MoveImagesToPipeline(self):

        #print("############ There are : ", len(imgs)," images available. Moving 10 of em.")
        self.updateImgs()
        for i in self.imgs:
            if i.startswith("tmp_"):
                print("Temp Files " + i)
            else:
                print("Copie files " + i)
                shutil.copy(self.dropDir+i, self.maskInputDir+i)
                shutil.copy(self.dropDir+i, self.rawImagesDir+i)
                shutil.copy(self.dropDir+i, self.styleTransfertInputDir+i)
                os.remove(self.dropDir+i)
        
        """
        try:
            subprocess.check_call("mv  "+this.dropDir+"/* "+this.inputDir, shell=True)
        except subprocess.CalledProcessError:
            sys.exit("An error occured while copying the images from the shared Directory to the Pipeline..")
        """
        self.imgs = os.listdir(self.maskInputDir)

        print("############The following images were passed to the pipeline...")
        print()
        print(self.imgs, sep="/n")
        print()
    
    def MoveImagesToRaw(self):
        try:
            subprocess.check_call("mv "+self.inputDir+"* ./raw/", shell=True)
        except subprocess.CalledProcessError:
            sys.exit("An error occured while copying the images to the raw dir.")


    def CleanUp(self):

        print("########## Cleaning Up Pipeline\n")
        mask = os.listdir(self.maskDir)
        print(mask)
        if len(mask) > 0:
            try: 
                subprocess.check_call("rm -r ./1.Mask/*", shell=True)
            except subprocess.CalledProcessError:
                sys.exit("There was an error, while cleaning up maksDir.")

        style = os.listdir(self.styleTransfertDir)
        print(style)
        if (len(style) > 0):
            try: 
                subprocess.check_call("rm -r ./2.StyleTransfert/*", shell=True)
            except subprocess.CalledProcessError:
                sys.exit("There was an error, while cleaning up StyleTransfetDir")

        apply = os.listdir(self.applyMaskDir)
        print(apply)
        if (len(apply) > 0):
            try: 
                subprocess.check_call("rm -r ./3.ApplyMask/*", shell=True)
            except subprocess.CalledProcessError:
                sys.exit("There was an error, while cleaning up ApplyMaskDir")


    ##########################################
    ############## First Step ################
    ##########################################

    def GenerateMask(self):
        print("############ 1. Mask ############ ")

        imageSegmentation = ImageSegmentation(self.maskInputDir, self.maskOutputDir,  self.simMask)

        imageSegmentation.run()


    ###########################################
    ############## Second Step ################
    ###########################################
    def StyleTransfer(self):


        print("########### 2. StyleTransfert")
        #print("########### Moving to Directory")

        #cdToDir = "cd ../fast-style-transfer/; "
        #pythonFile = "./runEvaluation_pipeline.py"
        print(self.styleTransfertInputDir)
        styletransfert = StyleTransfert(self.checkpointDir, self.styleTransfertInputDir, self.styleTransfertOutputDir, self.simTrans)
        styletransfert.run()

        print()

        #print("########## Moving back to Pipeline Directory.")

        #subprocess.call("cd ./", shell=True)
        #subprocess.call("pwd", shell=True)
        #subprocess.call("ls ", shell=True)


    ###########################################
    ############## Third Step ################
    ###########################################

    def ApplyMask(self):
        MaskInputDir = "./3.ApplyMask/MaskInput/"
        StyledInputDir = "./3.ApplyMask/StyledInput/"
        ApplyedMaskOutputDir = "./3.ApplyMask/Output/"

        makdirIfnotExists(MaskInputDir)
        makdirIfnotExists(StyledInputDir)
        makdirIfnotExists(ApplyedMaskOutputDir)

        ## Output dirs from previous steps
        maskDirOutput = "./1.Mask/Output/"
        styleDirOutput = "./2.StyleTransfert/Output/"

        print()
        print('###########')
        print('########### Copying')
        print('########### from Step 1 output directory')
        print('########### to Step 3 inputMask directory')
        print('###########')
        print()


        try:
            subprocess.check_call("cp "+maskDirOutput+"* "+MaskInputDir, shell=True)
        except subprocess.CalledProcessError:
            sys.exit("An error occured copying images to the 3th Step...")

        print()
        print('###########')
        print('########### Copying')
        print('########### from Step 2 output directory')
        print('########### to Step 3 StyledInput directory')
        print('###########')
        print()


        try:
            subprocess.check_call("cp "+styleDirOutput+"* "+StyledInputDir, shell=True)
        except subprocess.CalledProcessError:
            sys.exit("An error occured coping images to the 3th Step..")

        print("########### 3. Apply Mask and add Background Image on Styled Image")

        pythonFile = "python3 ../ApplyMask/applyMask_pipeline.py"

        try:
            subprocess.check_call(pythonFile, shell=True)
        except subprocess.CalledProcessError:
            sys.exit("An error occured runing the applyMask_pipeline skript.")



        print("########## Copy files to the Pipeline Output Directory")

        subprocess.call("cp "+ ApplyedMaskOutputDir + "/* " + self.outputDir, shell=True)

    def countImages(self,imgs):
        n = 0
        for img in imgs:
            if not img.startswith("tmp_"):
                n+=1
        return n

    def handle(self):
        cond = False
        then = time.time()-55
    
        while True:
            imgs = os.listdir(self.dropDir)
            now = time.time()
            elapsed = (now-then)

            if elapsed > 5: 
                #elapsed = 0
                print("Waiting for images...          ",end = "\r")
            else:
                print("Starting pipeline in {}".format(round(60.-elapsed,3)),end='\r')
            cond = self.countImages(imgs) >= 1 and elapsed > 5
            #print(cond)
            if cond:
                time.sleep(3)
                self.run()
                then = time.time()


def main():

    DROP =  "/run/user/1000/gvfs/smb-share:server=raspberrypi.local,share=mfk-super-share/" # where the new images need to go
    DROP = "./drop/"
    OUTPUTDIR = "./pipeline/output/" # result of whole pipeline

    pipeline = Pipeline(DROP, OUTPUTDIR, simulate={"Mask" : True, "Transfert" : True, "Apply" : True})   
    pipeline.run()
    #pipeline.handle()

if __name__ == "__main__":
    main()

    """
    flickr = Flickr(api_key, api_secret)
    id = flickr.upload("./flickrQr/placeholder.png")
    id = flickr.putPlaceholder()
    photoUrl = flickr.getUrl(id)
    img = qrcode.make(photoUrl)
    resp = flickr.replace("./test.png", id)
    """
###### It took 1.0 minutes and 10.1 seconds to run 11 images.
###### This is  6.37 seconds per image.

###### It took 8.0 minutes and 37.88 seconds to run 101 images.
###### This is 4.53 seconds per image.
