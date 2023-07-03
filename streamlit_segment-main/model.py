import torch
import torchvision
import sys
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import cv2
import urllib.request
import os

url = 'https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth'
filename = 'sam_vit_h_4b8939.pth'
if not os.path.isfile(filename):
  urllib.request.urlretrieve(url, filename)
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor


def show_anns(anns):
    if len(anns) == 0:
        return
    sorted_anns = sorted(anns, key=(lambda x: x['area']), reverse=True)
    ax = plt.gca()
    ax.set_autoscale_on(False)

    img = np.ones((sorted_anns[0]['segmentation'].shape[0], sorted_anns[0]['segmentation'].shape[1], 4))
    img[:,:,3] = 0
    for ann in sorted_anns:
        m = ann['segmentation']
        color_mask = np.concatenate([np.random.random(3), [0.35]])
        img[m] = color_mask
    return img


@st.cache_resource
def model(frame,threshold):
    image = frame
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    width, height = image.shape[0],image.shape[1]
    area = width * height
    
    sam_checkpoint = "sam_vit_h_4b8939.pth"
    model_type = "vit_h"
    device = "pu"
    sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    sam.to("cpu")
    mask_generator = SamAutomaticMaskGenerator(sam)
    
    masks = mask_generator.generate(image)
    max=0
    for idx, mask in enumerate(masks):
       if(mask["area"]>max):
           max=mask["area"]
           id=idx
    print(max)       
    intensity = max/area
    if intensity>threshold:
        return show_anns,intensity
      
    
    

    
    