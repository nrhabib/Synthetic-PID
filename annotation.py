# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 17:59:18 2021

@author: Noshin
"""

import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from skimage.morphology import label
from skimage.measure import regionprops
import os
import itertools

# Insert image path. Note: Must put metallic images in one folder. Choose path to save txt files (usually must be the same path as the photorealistic images)
path =  'C:\\Users\\nrhabib\\Documents\\Unreal Projects\\CrackDetection\\Saved\MovieRenders\\Fall4\\Metallic\\'
saveText = 'C:\\Users\\nrhabib\\Documents\\Unreal Projects\\CrackDetection\\Saved\MovieRenders\\Fall4\\'

#This code assumes only one class. Must insert more variables if more than one class exists. 
imgList = os.listdir(path)
for imageName in imgList:
    img =  cv2.imread(path+imageName,cv2.COLOR_BGR2GRAY) #Read image 
    y = img.shape[0] #Height
    x = img.shape[1] #Width
    # imgplot = cv2.imshow("Original",img)
    filename =imageName.replace("Metallic","") 
    filename =filename.replace(".jpeg","") + ".txt"
    filename = (saveText + filename) #Correct naming convention
    class_id = 0 # 0 for cracks. Can be multiple values if more than one class.
    mode = 'a' if os.path.exists(filename) else 'w+'
   
    f = open(filename, mode)
    
    img_mask = np.where(img > 0, 255, img) #Create mask from metallic images
    
    #imgplot2 = cv2.imshow("Final",img_mask)
    pixels = img_mask.flatten()
    
    lbl_0 = label(img_mask[:,:,0]) 
    img_1 = img.copy()
    props = regionprops(lbl_0) #For bounding boxes. Assigns regions depending on pixel connections
    for prop in props:
            if prop.bbox_area < 3000: #Ignore boxes that are connected but not large enough to count as a class. Do not skip this step. 
                continue
            width = (prop.bbox[3] - prop.bbox[1])/x
            height = (prop.bbox[2] - prop.bbox[0])/y
            centerx = ((prop.bbox[3]+prop.bbox[1])/2)/x 
            centery = ((prop.bbox[2]+prop.bbox[0])/2)/y
            f.write("{} {} {} {} {}\n" .format(class_id, centerx, centery, width, height)) #Write into text file with proper YOLO-format 
          #  print("{} {} {} {} {}\n" .format(class_id, centerx, centery, width, height))
            
           # cv2.rectangle(img_1, (prop.bbox[1], prop.bbox[0]), (prop.bbox[3], prop.bbox[2]), (255, 0, 0), 2)
           # print((prop.bbox[1], prop.bbox[0]), (prop.bbox[3], prop.bbox[2]))

            
            

    # fig, (ax1, ax3) = plt.subplots(1, 2, figsize = (15, 5))       
    
    
    # ax1.imshow(img)
    # ax1.set_title('Image')
   
    # ax3.set_title('Image with derived bounding box')

    # ax3.imshow(img_1)
    #fig.savefig(saveImg+imageName)
    f.close()

    
 
 


 

