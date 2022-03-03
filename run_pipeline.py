
import os
import shutil
import subprocess
import sys
import time

from flickr.config import api_secret, api_key
from flickr.flickrApi import Flickr

from pipeline.image_segmentation import ImageSegmentation

# Helper functions
def makdirIfnotExists(dirName):
    if not os.path.exists(dirName):
        os.makedirs(dirName)




class Pipeline:
    maskDir = "./pipeline/1.Mask/"
    maskInputDir = "./modules/pipeline/Temp/1.1_MaskInput/"
    maskOutputDir = "./modules/pipeline/Temp/1.2_MaskOutput/"
    styleTransfertDir = "./pipeline/2.StyleTransfert/"
    applyMaskDir = "./pipeline/3.ApplyMask/"


    def __init__(self,inpDir, drpDir, outpDir, simulate = False):

        #dropDir = "./drop/
        #imgs = os.listdir(dropDir) 
        self.dropDir = drpDir
        self.inputDir = inpDir
        self.updateImgs()
        self.outputDir = outpDir
        self.then = None
        self.now = None
        self.sim = simulate

    def updateImgs(self):
        self.imgs = os.listdir(self.dropDir)

    def run(self):
        self.setThen()
        self.MoveImagesToPipeline()
        #this.CleanUp()
        print("############ Starting Pipeline ############")

        self.GenerateMask()
        #self.StyleTransfert()
        #self.ApplyMask()
        self.CleanUp()
        self.MoveImagesToRaw()

        self.setNow()
        self.evaluatePipeline()

    def setThen(self):
        self.then = time.time()

    def setNow(self):
        self.now = time.time()
        
    def evaluatePipeline(self,now, then):
        ellapsed = (now-then)
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
                shutil.copy(self.dropDir+i, self.inputDir+i)
                os.remove(self.dropDir+i)
        
        """
        try:
            subprocess.check_call("mv  "+this.dropDir+"/* "+this.inputDir, shell=True)
        except subprocess.CalledProcessError:
            sys.exit("An error occured while copying the images from the shared Directory to the Pipeline..")
        """
        self.imgs = os.listdir(self.inputDir)

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

        imageSegmentation = ImageSegmentation(self.maskInputDir, self.maskOutputDir, )

        for img in self.imgs:
            shutil.copy(self.inputDir+img,maskDirInput+img)

        if self.sim:
            imageSegmentation.sim_run()
        else:
            imageSegmentation.run()


    ###########################################
    ############## Second Step ################
    ###########################################
    def StyleTransfert(self):

        styleDirInput = "./2.StyleTransfert/Input/"
        styleDirOutput = "./2.StyleTransfert/Output/"

        makdirIfnotExists(styleDirInput)
        makdirIfnotExists(styleDirOutput)

        print()
        print('###########')
        print('########### Copying')
        print('########### from Pipeline input directory')
        print('########### to Step 2 input directory')
        print('###########')
        print()

        for img in self.imgs:
            shutil.copy(self.inputDir+img, styleDirInput+img)

        print("########### 2. StyleTransfert")
        print("########### Moving to Directory")

        cdToDir = "cd ../fast-style-transfer/; "
        pythonFile = "./runEvaluation_pipeline.py"

        try:
            subprocess.check_call(cdToDir+pythonFile, shell=True)
        except subprocess.CalledProcessError:
            sys.exit("An error occured at styletrasfert stage.")

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
    DROP = "./pipeline/drop/"
    INPUTDIR =  "./pipeline/input/" # move to input dir to start prcdocessing
    OUTPUTDIR = "./pipeline/output/" # result of whole pipeline

    pipeline = Pipeline(INPUTDIR, DROP, OUTPUTDIR, simulate=True)

    pipeline.handle()

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
