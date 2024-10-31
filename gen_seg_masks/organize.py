import os
import shutil
import argparse
import logging
from tqdm import tqdm

def organize_nii_files(root_dir, dry_run=False):
    total_files = sum([len(files) for r, d, files in os.walk(root_dir) if any(f.endswith('.nii.gz') for f in files)])
    
    with tqdm(total=total_files, desc="Processing files") as pbar:
        for subdir, dirs, files in os.walk(root_dir):
            if not files:
                continue

            nii_files = [f for f in files if f.endswith('.nii.gz')]
            if not nii_files:
                continue

            images_dir = os.path.join(subdir, 'images')
            label1_dir = os.path.join(subdir, 'label1')
            label_up_dir = os.path.join(subdir, 'label_up')

            if not dry_run:
                os.makedirs(images_dir, exist_ok=True)
                os.makedirs(label1_dir, exist_ok=True)
                os.makedirs(label_up_dir, exist_ok=True)

            for file in nii_files:
                src_path = os.path.join(subdir, file)
                if file.startswith('label_up'):
                    dest_dir = label_up_dir
                elif file.startswith('label_'):
                    dest_dir = label1_dir
                else:
                    dest_dir = images_dir
                
                dest_path = os.path.join(dest_dir, file)
                
                if dry_run:
                    logging.info(f"Would move {src_path} to {dest_path}")
                else:
                    try:
                        shutil.move(src_path, dest_path)
                        logging.info(f"Moved {src_path} to {dest_path}")
                    except Exception as e:
                        logging.error(f"Error moving {src_path}: {str(e)}")
                
                pbar.update(1)

#organize_nii_files(r'C:\Users\Abbas Khan\Downloads\seg_masks')