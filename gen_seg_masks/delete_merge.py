import os
import shutil

# Define the root folder where D1, D2, D3, etc. are located
root_dir = '/path/to/your/folder'

# Function to delete 'label_up' folder and its contents
def delete_label_up(subfolder):
    label_up_dir = os.path.join(subfolder, 'label_up')
    if os.path.exists(label_up_dir):
        shutil.rmtree(label_up_dir)
        print(f"Deleted {label_up_dir}")

# Function to merge 'label1' and 'images' folder contents into the subfolder and delete them
def merge_and_delete(subfolder):
    label1_dir = os.path.join(subfolder, 'label1')
    images_dir = os.path.join(subfolder, 'images')

    # Merge the contents of 'label1' and 'images' into the parent folder
    if os.path.exists(label1_dir):
        for item in os.listdir(label1_dir):
            item_path = os.path.join(label1_dir, item)
            shutil.move(item_path, subfolder)
        print(f"Merged contents of {label1_dir} into {subfolder}")

    if os.path.exists(images_dir):
        for item in os.listdir(images_dir):
            item_path = os.path.join(images_dir, item)
            shutil.move(item_path, subfolder)
        print(f"Merged contents of {images_dir} into {subfolder}")

    # Delete 'label1' and 'images' folders after merging
    if os.path.exists(label1_dir):
        shutil.rmtree(label1_dir)
        print(f"Deleted {label1_dir}")

    if os.path.exists(images_dir):
        shutil.rmtree(images_dir)
        print(f"Deleted {images_dir}")

# Iterate over the subfolders (D1, D2, D3, etc.)
for subfolder_name in os.listdir(root_dir):
    subfolder_path = os.path.join(root_dir, subfolder_name)

    if os.path.isdir(subfolder_path):
        delete_label_up(subfolder_path)
        merge_and_delete(subfolder_path)

print("Operation completed.")
