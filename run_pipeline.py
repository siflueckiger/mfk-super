
#from asyncio.windows_utils import pipe
import os
import shutil
import subprocess
import sys
import time

from modules.pipeline.image_segmentation import ImageSegmentation
from modules.pipeline.style_transfer import StyleTransfert
from modules.pipeline.apply_mask import ApplyMask
from modules.flickr.flickrApi import Flickr

from config import api_key, api_secret

# Helper functions
def makdirIfnotExists(dirName):
    if not os.path.exists(dirName):
        os.makedirs(dirName)


class Pipeline:
    dropDir = "./drop/"
    tempDir = "./modules/pipeline/Temp/"
    maskInputDir = "./modules/pipeline/Temp/1.1_MaskInput/"
    maskOutputDir = "./modules/pipeline/Temp/1.2_MaskOutput/"
    styleTransfertInputDir = "./modules/pipeline/Temp/2.1_StyleTransfertInput/"
    styleTransfertOutputDir = "./modules/pipeline/Temp/2.2_StyleTransfertOutput/"
    checkpointDir = "./Some/Directory/"

    applyMaskInputDirMask = maskOutputDir
    applyMaskInputDirStyle = styleTransfertOutputDir
    applyMaskBackgroundDir = "./modules/pipeline/3.1_Backgrounds/selected/"
    applyMaskOutputDir = "./modules/pipeline/Temp/3.2_Output/"

    finalOutputDir = "./pipelineOutput/"
    rawImagesDir = "./rawImages/"


    def __init__(self, drpDir, outpDir, simulate = {"Mask" : False, "Transfert": False,"Apply" : False}):
        self.dropDir = drpDir
        self.updateImgs()
        self.outputDir = outpDir
        self.then = None
        self.now = None
        self.simMask = simulate["Mask"]
        self.simTrans = simulate["Transfert"]
        self.simApply = simulate["Apply"]

        self.flickr = Flickr(api_key=api_key, api_secret=api_secret)

    def updateImgs(self):
        self.imgs = os.listdir(self.dropDir)

    def run(self):
        self.CleanUp()
        self.setupTempDir()
        self.setThen()
        self.MoveImagesToPipeline()
        
        print("############ Starting Pipeline ############")

        self.GenerateMask()
        self.StyleTransfer()
        self.ApplyMask()
        self.MoveFinalImagesToPipelineOutput()
        #self.CleanUp()

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
        
        self.imgs = os.listdir(self.maskInputDir)

        print("############The following images were passed to the pipeline...")
        print()
        print(self.imgs, sep="/n")
        print()

    def MoveFinalImagesToPipelineOutput(self):
        try: 
            subprocess.check_call("cp -r {}* {}".format(self.applyMaskOutputDir, self.finalOutputDir), shell=True)
        except subprocess.CalledProcessError:
            sys.exit("There was an error, while cleaning up maksDir.")


    def CleanUp(self):
        try: 
            subprocess.check_call("rm -r {}".format(self.tempDir), shell=True)
        except subprocess.CalledProcessError:
            sys.exit("There was an error, while deleting Temp directory.")

    def setupTempDir(self):
        directories = [
                        self.tempDir,
                        self.maskInputDir,
                        self.maskOutputDir,
                        self.styleTransfertInputDir,
                        self.styleTransfertOutputDir,
                        self.applyMaskOutputDir
        ]

        for dir in directories:
            makdirIfnotExists(dir)

    def GenerateMask(self):
        print("############ 1. Mask ############ ")
        imageSegmentation = ImageSegmentation(self.maskInputDir, self.maskOutputDir,  self.simMask)
        imageSegmentation.run()

    def StyleTransfer(self):
        print("########### 2. StyleTransfert")
        #print("########### Moving to Directory")

        #cdToDir = "cd ../fast-style-transfer/; "
        #pythonFile = "./runEvaluation_pipeline.py"
        print(self.styleTransfertInputDir)
        styletransfert = StyleTransfert(self.checkpointDir, self.styleTransfertInputDir, self.styleTransfertOutputDir, self.simTrans)
        styletransfert.run()

        print()

    def ApplyMask(self):
        applyMask = ApplyMask(self.applyMaskInputDirMask, self.applyMaskInputDirStyle, self.applyMaskBackgroundDir, self.applyMaskOutputDir, self.simApply)
        applyMask.run()

    def uploadToFlicker(self):
        uploadImages = os.listdir(self.finalOutputDir)
        for img in uploadImages:
            if img.startswith("."):
                continue
            print(img.split("_"))
            id = img.split("_")[4]
            id = id.split(".")[0]
            resp = self.flickr.replace(self.finalOutputDir+img, id)
            print(resp)

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
    #DROP = "./drop/"
    OUTPUTDIR = "./pipeline/output/" # result of whole pipeline

    pipeline = Pipeline(DROP, OUTPUTDIR, simulate={"Mask" : True, "Transfert" : True, "Apply" : True})   
    #pipeline.run()
    pipeline.handle()

if __name__ == "__main__":
    ##### For Debugging !!!!!!!!!!
    """
    try: 
        subprocess.check_call("cp -r {} {}".format("./rawImages/", "./drop/"), shell=True)
    except subprocess.CalledProcessError:
        sys.exit("There was an error, while cleaning up maksDir.")
    """

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
