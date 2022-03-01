#!/usr/bin/env python3

import os

import mxnet as mx
from mxnet import image
from mxnet.gluon.data.vision import transforms
from gluoncv.data.transforms.presets.segmentation import test_transform
from gluoncv import model_zoo
from gluoncv.utils.viz import get_color_pallete


class ImageSegmentation:

  def __init__(self, inputDir, outputDir) -> None:
    """
    Generates foreground/background mask of an image.

    Args:
        inputDir (String): location of input Images
        outputDir (String): where the output Images are going
    """    
    self.ctx = mx.cpu()
    self.model = model_zoo.get_model('fcn_resnet101_voc', pretrained=True, ctx=self.ctx)
    self.inputDir = inputDir
    self.outputDir = outputDir
    self.imgs = os.listdir(inputDir)
  
  def _processImages(self):

    for im_fname in self.imgs:

      # Load and transfomr
      img = image.imread(self.inputDir + im_fname)
      img = test_transform(img, self.ctx)

      #predict
      ouput = self.model.predict(img)
      predict = mx.nd.squeeze(mx.nd.argmax(ouput, 1)).asnumpy()

      # generate color Mask and save
      mask =  get_color_pallete(predict, 'pascale_voc')

      mask.save(self.outputDir + "mask_" + im_fname)
  
  def _cleanUp(self):
    for im_fname in self.imgs:
      os.remove(inputDir + im_fname)

  def run(self):
    """Processes a set of Images.
    """    
    self._processImages()
    self._cleanUp()

  def sim_run(self):
    print("Pretending to run segmentation step.")

    

if __name__ == "__main__":

  
  inputDir = "./1.Mask/Input/"
  outputDir = "./1.Mask/Output/"
  os.makedirs(inputDir)
  os.makedirs(outputDir)
  os.popen("cp ./input/* "+inputDir)
  imageSegemntator = ImageSegmentation(inputDir, outputDir)
  imageSegemntator.run()


