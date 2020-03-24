import os
import sys
import numpy as np 
import pandas as pd 
import pathlib
import multiprocessing as mp
import xml.etree.ElementTree as ET
from PIL import Image 


ANNOTATION_DIR = pathlib.Path('G:/Github/standford-dogs/annotations/Annotation/')
IMAGES_DIR = pathlib.Path('G:/Github/standford-dogs/images/Images')

BREED_DIR = [path for path in IMAGES_DIR.iterdir()]
BREED_DIR_NAME = [path.name for path in BREED_DIR]

# Gets object boundings
def parse_bounding(path):
    # Get annotation path from image path
    path = ANNOTATION_DIR / path.parent.name / path.stem
    
    # Parse boundings
    tree = ET.parse(path)
    bndbox = tree.getroot().findall('object')[0].find('bndbox')
    left = int(bndbox.find('xmin').text)
    right = int(bndbox.find('xmax').text) 
    upper = int(bndbox.find('ymin').text)
    lower = int(bndbox.find('ymax').text) 
    
    return (left, upper, right, lower)

# Crop and save images according to boundings
IMAGES_CROPPED_DIR = pathlib.Path('G:/Github/standford-dogs/tmp/images_cropped/')
IMAGES_CROPPED_DIR.mkdir(parents=True, exist_ok=True) 

def crop_and_save_image(path, save_dir = IMAGES_CROPPED_DIR):
    print('Processing {}'.format(path))
    box = parse_bounding(path)
    
    image = Image.open(path)
    image_cropped = image.crop(box)
    image_cropped = image_cropped.convert('RGB')
    image_cropped.save(save_dir / path.name)
    print('Done {} -> {}'.format(path, save_dir / path.name))