import os
import nibabel as nib
import numpy as np
from pathlib import Path


unique_values = set()
import matplotlib.pyplot as plt


def find_cvi42wsx_files(parent_folder=r'C:\Users\Abbas Khan\Downloads\processed'):
    # Traverse the parent directory
    for root, dirs, files in os.walk(parent_folder):
            
        # Look for any .cvi42wsx files in the current directory
        for file in files:
            if file.endswith(".nii.gz"):
                file_path = os.path.join(root, file)
                
                case_id = root.split(os.sep)[5]
                #print(case_id)
                
                if 'label_up' in file_path:
                
                    img = nib.load(file_path)
    
                    # Get the image data as a numpy array
                    img = img.get_fdata()
                    img = img[:,:,0,0]
                    
                    # Append unique values from the current dataset to the set
                    unique_values.update(np.unique(img))
                    
                    file_name = Path(file_path).stem
                    
                    plt.imsave(r'C:\Users\Abbas Khan\Downloads\viz_data/' + case_id +'_' + file_name + '.png', img)
                

def find_cvi42wsx_files_imgs(parent_folder=r'C:\Users\Abbas Khan\Downloads\processed'):
    # Traverse the parent directory
    for root, dirs, files in os.walk(parent_folder):
            
        # Look for any .cvi42wsx files in the current directory
        for file in files:
            if file.endswith(".nii.gz"):
                file_path = os.path.join(root, file)
                
                case_id = root.split(os.sep)[5]
                #print(case_id)
                
                if 'label' not in file_path:
                
                    img = nib.load(file_path)
    
                    # Get the image data as a numpy array
                    img = img.get_fdata()
                    img = img[:,:,0,0]
                    
                    # Append unique values from the current dataset to the set
                    unique_values.update(np.unique(img))
                    
                    file_name = Path(file_path).stem
                    
                    plt.imsave(r'C:\Users\Abbas Khan\Downloads\images/' + case_id +'_' + file_name + '.png', img)
                    

_ = find_cvi42wsx_files_imgs()



# img = nib.load(r"C:\Users\Abbas Khan\Downloads\processed\D26\label_up\label_up_t2map_truefisp 2ch_moc.nii.gz")

# # Get the image data as a numpy array
# img = img.get_fdata()
# img = img[:,:,0,0]