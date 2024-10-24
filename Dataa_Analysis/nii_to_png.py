import os
import nibabel as nib
import numpy as np
from PIL import Image
import pathlib
import matplotlib.pyplot as plt

def convert_nii_to_png(nii_file, output_folder):
    # Load the .nii.gz file
    img = nib.load(nii_file)
    data = img.get_fdata()
    
    name = pathlib.Path(nii_file).stem
    #data.save(os.path.join(output_folder, name + '.png'))
    plt.imsave(os.path.join(output_folder,name+".png"),data)

def process_folder(input_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through the folder hierarchy
    for root, dirs, files in os.walk(input_folder):
        # Identify .nii.gz files
        for file in files:
            if file.endswith(".nii.gz"):
                nii_file_path = os.path.join(root, file)
                
                # Create corresponding output folder
                relative_path = os.path.relpath(root, input_folder)
                output_subfolder = os.path.join(output_folder, relative_path)
                os.makedirs(output_subfolder, exist_ok=True)
                
                # Convert and save .png files in the same folder structure
                convert_nii_to_png(nii_file_path, output_subfolder)

import os

def count_nii_files(folder):
    # Count the number of .nii.gz files in a folder
    return len([f for f in os.listdir(folder) if f.endswith('.nii.gz')])

def process_subfolders(input_folder):
    mismatch_cases = []

    # Iterate through the subfolders in the input folder
    for root, dirs, files in os.walk(input_folder):
        # Check if it contains the 'images', 'label_up', and 'label1' folders
        if 'images' in dirs and 'label_up' in dirs and 'label1' in dirs:
            images_folder = os.path.join(root, 'images')
            label_up_folder = os.path.join(root, 'label_up')
            label1_folder = os.path.join(root, 'label1')

            # Count the .nii.gz files in each folder
            images_count = count_nii_files(images_folder)
            label_up_count = count_nii_files(label_up_folder)
            label1_count = count_nii_files(label1_folder)

            print(f"Subfolder: {root}")
            print(f"  Images folder count: {images_count}")
            print(f"  Label_up folder count: {label_up_count}")
            print(f"  Label1 folder count: {label1_count}")

            # Check for mismatches in file counts between the folders
            if images_count != label_up_count or images_count != label1_count:
                mismatch_cases.append({
                    'subfolder': root,
                    'images_count': images_count,
                    'label_up_count': label_up_count,
                    'label1_count': label1_count
                })
    
    return mismatch_cases

# Set the input folder path
input_folder = r"C:\Users\Abbas Khan\Downloads\processed_oct" # Replace with your folder path

# Process the subfolders and find any mismatches
mismatch_cases = process_subfolders(input_folder)

# Print any mismatched cases
if mismatch_cases:
    print("\nMismatched file counts found in the following subfolders:")
    for case in mismatch_cases:
        print(f"Subfolder: {case['subfolder']}")
        print(f"  Images count: {case['images_count']}")
        print(f"  Label_up count: {case['label_up_count']}")
        print(f"  Label1 count: {case['label1_count']}")
else:
    print("\nNo mismatches found in file counts.")


# # Set the input and output folders
# input_folder = r"C:\Users\Abbas Khan\Downloads\processed_oct"  # Replace with the path to your folder
# output_folder = r"C:\Users\Abbas Khan\Downloads\ivc"  # Replace with the path where you want to save PNGs

# # Run the conversion process
# process_folder(input_folder, output_folder)
