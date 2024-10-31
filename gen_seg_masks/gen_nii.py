import os
import re
import pickle
import cv2
import pydicom as dicom
import SimpleITK as sitk
import numpy as np
import nibabel as nib
import pathlib

class BaseImage(object):
    """ Representation of an image by an array, an image-to-world affine matrix and a temporal spacing """
    volume = np.array([])
    affine = np.eye(4)
    dt = 1

    def WriteToNifti(self, filename):
        nim = nib.Nifti1Image(self.volume, self.affine)
        nim.header['pixdim'][4] = self.dt
        nim.header['sform_code'] = 1
        nib.save(nim, filename)


def find_series(dir_name, T=1, cvi42_dir=None):

    files = sorted(os.listdir(dir_name))
    if len(files) > T:
        # Sort the files according to their series UIDs
        series = {}
        for f in files:
            d = dicom.dcmread(os.path.join(dir_name, f))
            suid = d.SeriesInstanceUID
            if suid in series:
                series[suid].append(f)
            else:
                series[suid] = [f]

        # Find the series which has been annotated, otherwise use the last series.
        if cvi42_dir:
            find_series_flag = False
            for suid, suid_files in series.items():
                for f in suid_files:
                    contour_pickle = os.path.join(cvi42_dir, os.path.splitext(f)[0] + '.pickle')
                    if os.path.exists(contour_pickle):
                        find_series_flag = True
                        choose_suid = suid
                        break
            if not find_series_flag:
                choose_suid = sorted(series.keys())[-1]
        else:
            choose_suid = sorted(series.keys())[-1]
        
        print('There are multiple series. Use series {0}.'.format(choose_suid))
        files = sorted(series[choose_suid])

    if len(files) < T:
        print('Warning: {0}: Number of files < CardiacNumberOfImages! '
              'We will fill the missing files using duplicate slices.'.format(dir_name))
    
    return files

# output_dir = r'C:\Users\Abbas Khan\Downloads\vijay\images\D10\D10\correct_name'
# dicom_found_path = r'C:\Users\Abbas Khan\Downloads\vijay\images\D10\D10\found'
# pickel_path  = r'C:\Users\Abbas Khan\Downloads\vijay\images\D10\D10\contours'


required_tags = [
't2map_truefisp sa_mid_moco_t2',
'molli t1map_longt1 4ch_moco_t1',
't2map_truefisp sa_base_moco_t2',
'molli t1map_longt1 2ch_moco_t1',
'molli t1map_longt1 sa_base_moco_t1',
't2map_truefisp 4ch_moco_t2',
't2map_truefisp 2ch_moco_t2',
'molli t1map_longt1 sa_mid_moco_t1']


def read_dicom_images(dicom_found_path,pickel_path,output_dir):
        """ Read dicom images and store them in a 3D-t volume. """
        
        for name in os.listdir(dicom_found_path):
            file_path = os.path.join(dicom_found_path, name)
            data = {}
            # Read the image volume
            # Number of slices
            Z = 1
            d = dicom.read_file(file_path)
            tag = d.get('SeriesDescription', '').lower()
            #file_name = tag
            file_name = tag + '_' + name.split('.')[-2]
            #if tag in required_tags:

            if 'cine' not in tag and 'psir' not in tag and 'post_molli' not in tag and 'fitparam' not in tag:               
                T = d.CardiacNumberOfImages
    
                # Read a dicom file from the correct series when there are multiple time sequences
                d = dicom.read_file(file_path)
                X = d.Columns
                Y = d.Rows
                T = d.CardiacNumberOfImages
                dx = float(d.PixelSpacing[1])
                dy = float(d.PixelSpacing[0])
    
                pos_ul = np.array([float(x) for x in d.ImagePositionPatient])
                pos_ul[:2] = -pos_ul[:2]
    
                # Image orientation
                axis_x = np.array([float(x) for x in d.ImageOrientationPatient[:3]])
                axis_y = np.array([float(x) for x in d.ImageOrientationPatient[3:]])
                axis_x[:2] = -axis_x[:2]
                axis_y[:2] = -axis_y[:2]
    
                if Z >= 2:
                    # Read a dicom file at the second slice
                    d2 = dicom.read_file(os.path.join(dir[1], sorted(os.listdir(dir[1]))[0]))
                    pos_ul2 = np.array([float(x) for x in d2.ImagePositionPatient])
                    pos_ul2[:2] = -pos_ul2[:2]
                    axis_z = pos_ul2 - pos_ul
                    axis_z = axis_z / np.linalg.norm(axis_z)
                else:
                    axis_z = np.cross(axis_x, axis_y)
    
                # Determine the z spacing
                if hasattr(d, 'SpacingBetweenSlices'):
                    dz = float(d.SpacingBetweenSlices)
                elif Z >= 2:
                    print('Warning: can not find attribute SpacingBetweenSlices. '
                          'Calculate from two successive slices.')
                    dz = float(np.linalg.norm(pos_ul2 - pos_ul))
                else:
                    print('Warning: can not find attribute SpacingBetweenSlices. '
                          'Use attribute SliceThickness instead.')
                    dz = float(d.SliceThickness)
    
                # Affine matrix which converts the voxel coordinate to world coordinate
                affine = np.eye(4)
                affine[:3, 0] = axis_x * dx
                affine[:3, 1] = axis_y * dy
                affine[:3, 2] = axis_z * dz
                affine[:3, 3] = pos_ul
    
                # The 4D volume
                volume = np.zeros((X, Y, Z, T), dtype='float32')
                    # Save both label map in original resolution and upsampled label map.
                    # The image annotation by defaults upsamples the image using cvi42 and then
                    # annotate on the upsampled image.
                up = 4
                label = np.zeros((X, Y, Z, T), dtype='int16')
                label_up = np.zeros((X * up, Y * up, Z, T), dtype='int16')
    
                # Go through each slice
                for z in range(0, Z):
                    files_time = name #= # sorted(files_time, key=lambda x: x[1])
    
                    # Read the images
                    for t in range(0, T):
                        try:
                            f = files_time[t][0]
                            d = dicom.read_file(file_path)
                            volume[:, :, z, t] = d.pixel_array.transpose()
                        except IndexError:
                            print('Warning: dicom file missing for {0}: time point {1}. '
                                  'Image will be copied from the previous time point.'.format(dir[z], t))
                            volume[:, :, z, t] = volume[:, :, z, t - 1]
                        except (ValueError, TypeError):
                            print('Warning: failed to read pixel_array from file {0}. '
                                  'Image will be copied from the previous time point.'.format(os.path.join(dir[z], f)))
                            volume[:, :, z, t] = volume[:, :, z, t - 1]
                        except NotImplementedError:
                            print('Warning: failed to read pixel_array from file {0}. '
                                  'pydicom cannot handle compressed dicom files. '
                                  'Switch to SimpleITK instead.'.format(os.path.join(dir[z], f)))
                            reader = sitk.ImageFileReader()
                            reader.SetFileName(os.path.join(dir[z], f))
                            img = sitk.GetArrayFromImage(reader.Execute())
                            volume[:, :, z, t] = np.transpose(img[0], (1, 0))
    
                        cvi42_dir = True
                        if cvi42_dir:
                            # Check whether there is a corresponding cvi42 contour file for this dicom
                            contour_pickle = os.path.join(pickel_path, name[:-4]+ '.pickle')
                            if os.path.exists(contour_pickle):
                                with open(contour_pickle, 'rb') as f:
                                    contours = pickle.load(f)
    
                                    # Constants for each contour key
                                    laepi = 1
                                    saepi = 1
                                    
                                    laendo = 2
                                    saendo = 2
                                    
                                    laxLv = 3
                                    sacardialRef = 4
                                    laxLa = 6
                                    sacardialInferior = 8
      
                                    ordered_contours = []
    
                                    if 'laepicardialContour' in contours:
                                        ordered_contours += [(contours['laepicardialContour'], laepi)]
                                    if 'laendocardialContour' in contours:
                                        ordered_contours += [(contours['laendocardialContour'], laendo)]
                                    if 'laxLvContour' in contours:
                                        ordered_contours += [(contours['laxLvContour'], laxLv)]
                                    if 'sacardialRefContour' in contours:
                                        ordered_contours += [(contours['sacardialRefContour'], sacardialRef)]
                                        
                                    if 'saepicardialContour' in contours:
                                        ordered_contours += [(contours['saepicardialContour'], saepi)]
                                            
                                    if 'saendocardialContour' in contours:
                                        ordered_contours += [(contours['saendocardialContour'], saendo)]   
                                    if 'laxLaContour' in contours:
                                        ordered_contours += [(contours['laxLaContour'], laxLa)]
                                    if 'sacardialInferiorContour' in contours:
                                        ordered_contours += [(contours['sacardialInferiorContour'], sacardialInferior)]
                                    lab_up = np.zeros((Y * up, X * up))
                                    
                                    for c, l in ordered_contours:
                                        coord = np.round(c * up).astype(int)
                                        cv2.fillPoly(lab_up, [coord], l)
    
                                    label_up[:, :, z, t] = lab_up.transpose()
                                    label[:, :, z, t] = lab_up[::up, ::up].transpose()
    
                # Temporal spacing
                #dt = (files_time[1][1] - files_time[0][1]) * 1e-3
                dt = 1
                # Store the image
                data[file_name] = BaseImage()
                data[file_name].volume = volume
                data[file_name].affine = affine
                data[file_name].dt = dt
                
                cvi42_dir = True
                if cvi42_dir:
                    # Only save the label map if it is non-zero
                    if np.any(label):
                        data['label_' + file_name] = BaseImage()
                        data['label_' + file_name].volume = label
                        data['label_' + file_name].affine = affine
                        data['label_' + file_name].dt = dt
    
                    if np.any(label_up):
                        data['label_up_' + file_name] = BaseImage()
                        data['label_up_' + file_name].volume = label_up
                        up_matrix = np.array([[1.0/up, 0, 0, 0], [0, 1.0/up, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
                        data['label_up_' + file_name].affine = np.dot(affine, up_matrix)
                        data['label_up_' + file_name].dt = dt


            for name, image in data.items():
                image.WriteToNifti(os.path.join(output_dir, '{0}.nii.gz'.format(name)))
        #return ordered_contours    

# dicom_found_path = r'C:\My_Data\Vijay\D16/Found'
# pickel_path = r'C:\My_Data\Vijay\D16/Contours'
# output_dir = r'C:\My_Data\Vijay\D16\Result'
# _ = read_dicom_images(dicom_found_path,pickel_path,output_dir)