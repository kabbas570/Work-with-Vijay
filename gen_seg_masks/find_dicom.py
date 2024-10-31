
import os
import pickle
import pydicom
import shutil

def find_dicom(base_folder_path,dicom_parent_directory,destination_directory):

    # List all pickle files in the main directory
    for pickle_filename in os.listdir(base_folder_path):
        if pickle_filename.endswith('.pickle'):
            # Extract the UID from the pickle file name
            uid_from_pickle = pickle_filename[:-7]  # Remove '.pickle'
            pickle_file_path = os.path.join(base_folder_path, pickle_filename)
    
            # Print the pickle file name
            #print(f"Processing Pickle File: {pickle_filename}")
    
            # Traverse all subdirectories to find matching DICOM files
            for root, _, files in os.walk(dicom_parent_directory):
                for dicom_filename in files:
                    dicom_file_path = os.path.join(root, dicom_filename)
                    try:
                        # Attempt to read the file as a DICOM file
                        dicom_data = pydicom.dcmread(dicom_file_path)
    
                        # Extract SOP Instance UID from the DICOM file
                        sop_instance_uid = dicom_data.SOPInstanceUID
    
                        # Compare with UID extracted from pickle file
                        if sop_instance_uid == uid_from_pickle:
                            #print(f"  Matching DICOM File: {dicom_filename} with SOP Instance UID: {sop_instance_uid}")
                            new_file_path = os.path.join(destination_directory, f"{uid_from_pickle}.dcm")
                            shutil.copy(dicom_file_path, new_file_path)
                    except Exception as e:
                        print(f"  Skipping non-DICOM file or error reading file: {dicom_filename}")
        
        
    