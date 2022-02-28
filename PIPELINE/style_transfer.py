#!/usr/bin/env python3
#comment fluegu
import subprocess
import os

# Functions
def makdirIfnotExists(dirName):
    if not os.path.exists(dirName):
        os.makedirs(dirName)

SUBPROCESS = True

print()
print("----")

cp = "./checkpoints/useForEvaluation/LargerTrainingDataSet_Train2014_and_WIDER_train_and_OI_Challenge_neonMask_epoches_8/"
#cp = os.path.abspath(cp)+"/"
print("checkpoint path: ", cp)

inputDir = "../Vernissage_pipeline/2.StyleTransfert/Input/"

print("---- Copying from Pipeline Input Directory")
subprocess.call("cp " + inputDir + "* ./input-image/", shell=True)

inputDir = "./input-image/"
# inputDir = os.path.abspath(inputDir)+"/"
print("input Path: ", inputDir)


outputDir = "../Vernissage_pipeline/2.StyleTransfert/Output/"
LocalOutputDir = "./pipelineOutput/"
# outputDir = os.path.abspath(outputDir)+"/"
print("output Path: ", outputDir)

print("---- CheckpointDir Exists: ", os.path.exists(cp))
print("---- input Dir Exists: ", os.path.exists(inputDir))
print("---- outputDir Exists: ", os.path.exists(outputDir))
#name = cp.replace("/","")
#name = cp.replace("./checkpoints","")
#outputDir = "./outputEvaluate/{0}".format(name)

makdirIfnotExists(LocalOutputDir)
print("----")
print("----")
command = "tensorman run --gpu -- python evaluate.py \
    --checkpoint {0} \
    --in-path {1} \
    --out-path {2} \
    --allow-different-dimensions".format(cp, inputDir, LocalOutputDir)

print("----", command)
if SUBPROCESS:
    subprocess.call(command, shell=True)
else:
    print("---- Testing -- set SUBPROCESS TO True")

print("---- Rename output Files")
images = os.listdir(LocalOutputDir)
for img in images:
    os.rename(LocalOutputDir+img, LocalOutputDir+"styled_"+img)
print("---- Copy back to Pipeline directory.")
subprocess.call("cp "+LocalOutputDir+"* "+outputDir, shell=True)
subprocess.call("rm "+LocalOutputDir+"*", shell=True)
subprocess.call("rm "+inputDir+"*", shell=True)
print("---- Returning to pipeline")
