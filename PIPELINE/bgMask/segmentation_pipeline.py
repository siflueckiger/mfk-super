#!/usr/bin/env python3

from os import listdir, remove

import mxnet as mx
from mxnet import image
from mxnet.gluon.data.vision import transforms
from gluoncv.data.transforms.presets.segmentation import test_transform
from gluoncv import model_zoo
from gluoncv.utils.viz import get_color_pallete


ctx = mx.gpu(0)

#Load model
model = model_zoo.get_model('fcn_resnet101_voc', pretrained=True, ctx=ctx)
#model(x.as_in_context(mx.gpu(0)))

inputDir = "../Vernissage_pipeline/1.Mask/Input/"
outputDir = "../Vernissage_pipeline/1.Mask/Output/"

imgs = listdir(inputDir)

for im_fname in imgs:

  # Load and transfomr
  img = image.imread(inputDir + im_fname)
  img = test_transform(img, ctx)

  #predict
  ouput = model.predict(img)
  predict = mx.nd.squeeze(mx.nd.argmax(ouput, 1)).asnumpy()

  # generate color Mask and save
  mask =  get_color_pallete(predict, 'pascale_voc')

  mask.save(outputDir + "mask_" + im_fname)

#delete input images

for im_fname in imgs:
  remove(inputDir + im_fname)

