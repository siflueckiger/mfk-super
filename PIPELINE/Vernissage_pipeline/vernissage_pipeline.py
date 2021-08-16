import os
import shutil
import subprocess
import sys
import time

# Functions
def makdirIfnotExists(dirName):
    if not os.path.exists(dirName):
        os.makedirs(dirName)




class Pipeline:
    maskDir = "./1.Mask/"
    styleTransfertDir = "./2.StyleTransfert/"
    applyMaskDir = "./3.ApplyMask/"


    def __init__(this,inpDir, drpDir, outpDir):

        #dropDir = "./drop/
        #imgs = os.listdir(dropDir) 
        this.dropDir = drpDir
        this.inputDir = inpDir
        this.updateImgs()
        this.outputDir = outpDir

    def updateImgs(this):
        this.imgs = os.listdir(this.dropDir)

    def run(this):

        then = time.time()
        this.MoveImagesToPipeline()
        #this.CleanUp()
        print("############ Starting Pipeline ############")

        this.GenerateMask()
        this.StyleTransfert()
        this.ApplyMask()
        this.CleanUp()
        this.MoveImagesToRaw()


        now = time.time()

        ellapsed = (now-then)
        minutes = round(ellapsed/60,0)
        seconds = round(ellapsed%60,2)
        nImages = len(this.imgs)
        perImage = ellapsed/nImages

        print("###### It took" ,minutes,"minutes and", seconds, "seconds to run" , nImages , "images.")

        print("###### This is", round(perImage, 2) ,"seconds per image.")

    def MoveImagesToPipeline(this):

        #print("############ There are : ", len(imgs)," images available. Moving 10 of em.")
        this.updateImgs()
        for i in this.imgs:
            if i.startswith("tmp_"):
                print("Temp Files " + i)
            else:
                print("Copie files " + i)
                shutil.copy(this.dropDir+i, this.inputDir+i)
                os.remove(this.dropDir+i)
        
        """
        try:
            subprocess.check_call("mv  "+this.dropDir+"/* "+this.inputDir, shell=True)
        except subprocess.CalledProcessError:
            sys.exit("An error occured while copying the images from the shared Directory to the Pipeline..")
        """
        this.imgs = os.listdir(this.inputDir)

        print("############The following images were passed to the pipeline...")
        print()
        print(this.imgs, sep="/n")
        print()
    
    def MoveImagesToRaw(this):
        try:
            subprocess.check_call("mv "+this.inputDir+"* ./raw/", shell=True)
        except subprocess.CalledProcessError:
            sys.exit("An error occured while copying the images to the raw dir.")


    def CleanUp(this):


        print("########## Cleaning Up Pipeline\n")
        mask = os.listdir(this.maskDir)
        print(mask)
        if len(mask) > 0:
            try: 
                subprocess.check_call("rm -r ./1.Mask/*", shell=True)
            except subprocess.CalledProcessError:
                sys.exit("There was an error, while cleaning up maksDir.")

        style = os.listdir(this.styleTransfertDir)
        print(style)
        if (len(style) > 0):
            try: 
                subprocess.check_call("rm -r ./2.StyleTransfert/*", shell=True)
            except subprocess.CalledProcessError:
                sys.exit("There was an error, while cleaning up StyleTransfetDir")

        apply = os.listdir(this.applyMaskDir)
        print(apply)
        if (len(apply) > 0):
            try: 
                subprocess.check_call("rm -r ./3.ApplyMask/*", shell=True)
            except subprocess.CalledProcessError:
                sys.exit("There was an error, while cleaning up ApplyMaskDir")




    ##########################################
    ############## First Step ################
    ##########################################

    def GenerateMask(this):
        print("############ 1. Mask ############ ")

        pythonFile = "../bgMask/segmentation_pipeline.py"

        maskDirInput = "./1.Mask/Input/"
        maskDirOutput = "./1.Mask/Output/"

        makdirIfnotExists(maskDirInput)
        makdirIfnotExists(maskDirOutput)

        for img in this.imgs:
            shutil.copy(this.inputDir+img,maskDirInput+img)

        try:
            subprocess.check_call(pythonFile, shell=True)
        except subprocess.CalledProcessError:
            sys.exit("An error occured generating the masks..")


    ###########################################
    ############## Second Step ################
    ###########################################
    def StyleTransfert(this):

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

        for img in this.imgs:
            shutil.copy(this.inputDir+img, styleDirInput+img)

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

    def ApplyMask(this):
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

        subprocess.call("cp "+ ApplyedMaskOutputDir + "/* " + this.outputDir, shell=True)

    def countImages(this,imgs):
        n = 0
        for img in imgs:
            if not img.startswith("tmp_"):
                n+=1
        return n

    def handle(this):
        cond = False
        then = time.time()-55
    
        while True:
            imgs = os.listdir(this.dropDir)
            now = time.time()
            elapsed = (now-then)

            if elapsed > 60: 
                #elapsed = 0
                print("Waiting for images...          ",end = "\r")
            else:
                print("Starting pipeline in {}".format(round(60.-elapsed,3)),end='\r')
            cond = this.countImages(imgs) >= 1 and elapsed > 60
            #print(cond)
            if cond:
                time.sleep(3)
                this.run()
                then = time.time()


def main():
    #NUM_IMAGES = len(imgs) #### FOR TESTING !!!!!
    """
    if len(imgs) < NUM_IMAGES:
        print("############ There are less then 10 images. Exiting..")
        sys.exit()
        
    """
    DROP =  "/run/user/1000/gvfs/smb-share:server=raspberrypi.local,share=mfk-super-share/" # where the new images need to go
    INPUTDIR =  "./input/" # move to input dir to start prcdocessing
    OUTPUTDIR = "./output/" # result of whole pipeline

    pipeline = Pipeline(INPUTDIR, DROP, OUTPUTDIR)
    #while true:
    #pipeline.CleanUp()
    
    #pipeline.run()

    pipeline.handle()

if __name__ == "__main__":
    main()

###### It took 1.0 minutes and 10.1 seconds to run 11 images.
###### This is  6.37 seconds per image.

###### It took 8.0 minutes and 37.88 seconds to run 101 images.
###### This is 4.53 seconds per image.
