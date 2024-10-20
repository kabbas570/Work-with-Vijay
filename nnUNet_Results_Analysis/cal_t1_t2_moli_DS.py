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


num_t1 = 0
num_t2 = 0
for i in range(278):
        
    pred = sitk.ReadImage(preds_path + names[i] + '.nii.gz')
    pred = sitk.GetArrayFromImage(pred)
    pred = pred[0,:]
    
    gt = sitk.ReadImage(gts_path + names[i] + '_gt.nii.gz')
    gt = sitk.GetArrayFromImage(gt)
    gt = gt[0,:]
    
    
    roi_pred = np.zeros(pred.shape)
    roi_pred[np.where(pred==1)] = 1
    
    roi_gt = np.zeros(gt.shape)
    roi_gt[np.where(gt==1)] = 1
    
    if 't2' not in names[i] and 't1' not in names[i]:

        
        num_t1+=1
    
        print(names[i])

        single_dice,single_hd = 0,0
        if np.sum(roi_pred) != 0 and np.sum(roi_gt) != 0:
    
            single_dice,single_hd = calculate_metric_percase(roi_pred,roi_gt)
        Dice+=single_dice
        HD+=single_hd

    
print(Dice/num_t1)
print(HD/num_t1)



a = (4.3177147853518765+ 1.8591420431249512 + 2.7967470754970507
)/3

