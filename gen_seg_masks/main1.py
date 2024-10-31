import os

from parse_cvi42_xml import parseFile
from find_dicom import find_dicom
from gen_nii import read_dicom_images
from organize import organize_nii_files
def find_cvi42wsx_files(parent_folder,dest_dir_1,dest_dir_2):
    # Traverse the parent directory
    for root, dirs, files in os.walk(parent_folder):
            
        # Look for any .cvi42wsx files in the current directory
        for file in files:
            if file.endswith(".cvi42wsx"):
                file_path = os.path.join(root, file)
                #print(f"Found .cvi42wsx file: {file_path}")
                
                #folder_name = os.path.basename(os.path.dirname(root)) 
                #print(folder_name)
                folder_name = root.split(os.sep)[-1]
                os.mkdir(os.path.join(dest_dir_1, folder_name)) 
                contours_folder_path = os.path.join(dest_dir_1, folder_name, 'Contours')
                os.mkdir(contours_folder_path)
                #print(contours_folder_path)
                
                _ = parseFile(file_path, contours_folder_path)

                # Check if we are in a folder ending with "_"
        if root.endswith('_'):
                    # Print the path of the folder
                    #print(f"Found folder ending with '_': {root}")
                    path_to__folder = root
                    
                    found_dicom_path = os.path.join(dest_dir_1, folder_name, 'Found')
                    os.mkdir(found_dicom_path)
                    
                    _ = find_dicom(contours_folder_path,path_to__folder,found_dicom_path)
                    
                    print('found_dicom_path',found_dicom_path)
                    print('contours_folder_path',contours_folder_path)
                    
                    dest_path = os.path.join(dest_dir_2, folder_name)
                    os.mkdir(dest_path)
                    _ = read_dicom_images(found_dicom_path,contours_folder_path,dest_path)

# Replace with the actual path to your parent folder
parent_folder_path = "/data/scratch/acw676/vijay/data1/"
dest_dir_1 = '/data/scratch/acw676/vijay/Again/temp/'
dest_dir_2 = '/data/scratch/acw676/vijay/Again/processed/'
find_cvi42wsx_files(parent_folder_path,dest_dir_1,dest_dir_2)
organize_nii_files(dest_dir_2)
