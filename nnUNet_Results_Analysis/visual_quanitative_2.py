import SimpleITK as sitk
import glob
import numpy as np
import matplotlib.pyplot as plt
from skimage import feature
import os
from medpy import metric  
def calculate_metric_percase(pred, gt):      
      dice = metric.binary.dc(pred, gt)
      hd = metric.binary.hd95(pred, gt)
      return dice, hd
  
epi = 1 
endo = 2 
def blend(image1,gt,pre):
    
    image1 = normalize(image1)
    image1 = np.stack((image1,)*3, axis=2)
    
    #gt = np.stack((gt,)*3, axis=-1)
    #pre = np.stack((pre,)*3, axis=-1)
    
    indices = np.where((gt == 1) & (pre == 1))
    for i, j in zip(indices[0], indices[1]):
        image1[i, j] = (0, 0.8, 0)
        
    indices = np.where((gt == 1) & (pre == 0))
    for i, j in zip(indices[0], indices[1]):
        image1[i, j] = (0.8, 0, 0)
    
    indices = np.where((gt == 0) & (pre == 1))
    for i, j in zip(indices[0], indices[1]):
        image1[i, j] = (0.8, 0.8, 0)
        
    return image1
        
        
preds_path = r"C:\My_Data\Vijay\nnUNetTrainer__nnUNetPlans__2d\preds/"
gts_path = r"C:\My_Data\Vijay\nnUNetTrainer__nnUNetPlans__2d\data/"
imgs_path = r"C:\My_Data\Vijay\nnUNetTrainer__nnUNetPlans__2d\data/"
results = r"C:\My_Data\Vijay\nnUNetTrainer__nnUNetPlans__2d\endo/"

names = []
for infile in sorted(glob.glob(preds_path + "/*.nii.gz")):
    names.append(os.path.basename(infile[:-7]))
 
def normalize(x):
    return np.array((x - np.min(x)) / (np.max(x) - np.min(x)))


Dice = 0
HD = 0
for i in range(278):
        
    pred = sitk.ReadImage(preds_path + names[i] + '.nii.gz')
    pred = sitk.GetArrayFromImage(pred)
    pred = pred[0,:]
    
    gt = sitk.ReadImage(gts_path + names[i] + '_gt.nii.gz')
    gt = sitk.GetArrayFromImage(gt)
    gt = gt[0,:]
    
    img = sitk.ReadImage(imgs_path + names[i] + '.nii.gz')
    img = sitk.GetArrayFromImage(img)
    img = img[0,:]
    
    roi_pred = np.zeros(pred.shape)
    roi_pred[np.where(pred==1)] = 1
    
    roi_gt = np.zeros(gt.shape)
    roi_gt[np.where(gt==1)] = 1

    #single_dice,single_hd = 0,0
    if np.sum(roi_pred) != 0 and np.sum(roi_gt) != 0:

        single_dice,single_hd = calculate_metric_percase(roi_pred,roi_gt)
    Dice+=single_dice
    HD+=single_hd

    #result  = blend(img,roi_gt,roi_pred)
    
    #plt.imsave(results + names[i] + '.png', result)
    
print(Dice/278)
print(HD/278)


