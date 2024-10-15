import SimpleITK as sitk
import glob
import numpy as np
import matplotlib.pyplot as plt
from skimage import feature
import os

preds_path = r"C:\My_Data\Vijay\nnUNetTrainer__nnUNetPlans__2d\preds/"
gts_path = r"C:\My_Data\Vijay\nnUNetTrainer__nnUNetPlans__2d\data/"
imgs_path = r"C:\My_Data\Vijay\nnUNetTrainer__nnUNetPlans__2d\data/"
results = r"C:\My_Data\Vijay\nnUNetTrainer__nnUNetPlans__2d\viz_R/"

names = []

for infile in sorted(glob.glob(preds_path + "/*.nii.gz")):
    names.append(os.path.basename(infile[:-7]))
 
    
def normalize(x):
    return np.array((x - np.min(x)) / (np.max(x) - np.min(x)))

def blend(image,pred,edges): 

    image = normalize(image)
    image = np.stack((image,)*3, axis=2)
    image[np.where(pred==1)] = [0.9,0.9,0]
    image[np.where(pred==2)] = [0.9,0,0]    
    image[np.where(edges!=0)] = 1
    
    return image


for i in range(278):
    
    print(names[i])
    
    pred = sitk.ReadImage(preds_path + names[i] + '.nii.gz')
    pred = sitk.GetArrayFromImage(pred)
    pred = pred[0,:]
    
    gt = sitk.ReadImage(gts_path + names[i] + '_gt.nii.gz')
    gt = sitk.GetArrayFromImage(gt)
    gt = gt[0,:]
    
    img = sitk.ReadImage(imgs_path + names[i] + '.nii.gz')
    img = sitk.GetArrayFromImage(img)
    img = img[0,:]

    combined_GT = np.zeros(gt.shape)
    combined_GT[np.where(gt!=0)] = 1
    edges = feature.canny(combined_GT)
        
    result  = blend(img,pred,edges)
    
    plt.imsave(results + names[i] + '.png', result)
     
