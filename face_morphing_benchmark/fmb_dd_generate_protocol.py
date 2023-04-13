# -*- coding: utf-8 -*-
"""
Generating the protocol for differential morphing detection.

Executing this file will lead to the generating of the new protocol in the specified folder

Labels 1 - Bona Fide ; 0 - Morph
@author: yrame
"""


import os
import math
import argparse
from glob import glob
import random
import sys

import numpy as np
import csv

import fmb_utils.fmb_utilities

default_image_file_extentions = [".jpg", ".png", ".ppm", ".bmp"]



def generate_bona_fide_pairs_from_paired_folders(datasets_path, 
                                                 image_folder_pathes,
                                                 name_range_crop_1 = (0,0),
                                                 name_range_crop_2 = (0,0),
                                                 image_file_extentions = default_image_file_extentions,
                                                 verbose = 0):
    
    #Function for printing verbosity
    def verboseprint(verbosity_level):
        """ Simplest verbosity print function """
        return (print if verbose>verbosity_level else lambda *a, **k: None)
    
    #lists for storing the dataset and lists   
    dataset_pairs = []
    dataset_fh = []
    dataset_sh = []
    labels = []
    dataset_full = []
    
    full_data_counter = 0
    
    #collect files in the first folder
    im_files_1 = []
    for ext in image_file_extentions:        
        #run through the files
        im_files_1 = im_files_1 + [f for f in glob(datasets_path + "/" + image_folder_pathes[0] + "/" + "*" + ext)]

    #collect files in the second folder
    im_files_2 = []
    for ext in image_file_extentions:        
        #run through the files
        im_files_2 = im_files_2 + [f for f in glob(datasets_path + "/" + image_folder_pathes[1] + "/" + "*" + ext)]
    
    #full dataset collect
    dataset_full = im_files_1 + im_files_2 
    
    #collect pairs
    
    for imf_1 in im_files_1:
        for imf_2 in im_files_2:
           
            item_fh = (imf_1).replace(datasets_path,'')
            item_fh = item_fh.replace(os.sep, '/')
            
            item_sh = (imf_2).replace(datasets_path,'')
            item_sh = item_sh.replace(os.sep, '/') 
           
            imf_1_id = item_fh.replace(image_folder_pathes[0], '')
            imf_1_id = imf_1_id.replace('/', '')
            imf_1_id = imf_1_id[name_range_crop_1[0]:len(imf_1_id)-name_range_crop_1[1]]
            
            imf_2_id = item_sh.replace(image_folder_pathes[1], '')
            imf_2_id = imf_2_id.replace('/', '')
            imf_2_id = imf_2_id[name_range_crop_2[0]:len(imf_2_id)-name_range_crop_2[1]]
            
            #if same identity - add pair
            if (imf_1_id in imf_2_id):
                # print(imf_1_id,imf_2_id)
                # print(item_fh,item_sh)
                dataset_pairs.append((item_fh,item_sh))
                dataset_fh.append(item_fh)
                dataset_sh.append(item_sh)
                labels.append(1)

    
    
    return(dataset_pairs, dataset_fh, dataset_sh, labels, dataset_full)


def generate_bona_fide_pairs_from_dataset(datasets_path, 
                                          image_folder_path,
                                          name_range_crop = (0,0),
                                          max_pairs_per_image = 1,
                                          image_file_extentions = default_image_file_extentions,
                                          verbose = 0):
    
    #Function for printing verbosity
    def verboseprint(verbosity_level):
        """ Simplest verbosity print function """
        return (print if verbose>verbosity_level else lambda *a, **k: None)
    
    #lists for storing the dataset and lists   
    dataset_pairs = []
    dataset_fh = []
    dataset_sh = []
    labels = []
    dataset_full = []
    
    full_data_counter = 0
    
    #collect files in the directory
    im_files = []
    for ext in image_file_extentions:        
        #run through the files
        im_files = im_files + [f for f in glob(datasets_path + "/" + image_folder_path + "/" + "*" + ext)]

       
    #full dataset collect
    dataset_full = im_files
    
    #shuffle image list
    random.shuffle(im_files)
    
    #collect pairs
    for i, imf_1 in enumerate(im_files):
        current_pairs_per_image = 0;
        for j, imf_2 in enumerate(im_files):
            #skip repeating comparisons
            if not i<j:
                continue
            
            if current_pairs_per_image>=max_pairs_per_image:
                #print("max pairs is achieved")
                continue
            
            item_fh = (imf_1).replace(datasets_path,'')
            item_fh = item_fh.replace(os.sep, '/')
            
            item_sh = (imf_2).replace(datasets_path,'')
            item_sh = item_sh.replace(os.sep, '/') 
           
            imf_1_id = item_fh.replace(image_folder_path, '')
            imf_1_id = imf_1_id.replace('/', '')
            imf_1_id = imf_1_id[name_range_crop[0]:len(imf_1_id)-name_range_crop[1]]
            
            imf_2_id = item_sh.replace(image_folder_path, '')
            imf_2_id = imf_2_id.replace('/', '')
            imf_2_id = imf_2_id[name_range_crop[0]:len(imf_2_id)-name_range_crop[1]]
            
            #if same identity - add pair
            if (imf_1_id == imf_2_id):
                # print(imf_1_id,imf_2_id)
                # print(item_fh,item_sh)
                dataset_pairs.append((item_fh,item_sh))
                dataset_fh.append(item_fh)
                dataset_sh.append(item_sh)
                labels.append(1)
                current_pairs_per_image+=1

    return(dataset_pairs, dataset_fh, dataset_sh, labels, dataset_full)


def generate_bona_fide_pairs_from_labeled_dataset(datasets_path, 
                                                  image_folder_path, 
                                                  max_pairs_per_class = 1,
                                                  image_file_extentions = default_image_file_extentions,
                                                  verbose = 0):
    
    
    
   #Function for printing verbosity
    def verboseprint(verbosity_level):
        """ Simplest verbosity print function """
        return (print if verbose>verbosity_level else lambda *a, **k: None)
    
    #lists for storing the dataset and lists   
    dataset_pairs = []
    dataset_fh = []
    dataset_sh = []
    labels = []
    dataset_full = []
    
    full_data_counter = 0
    
    
    #run through the src folder folder
    for subdir, dirs, files in fmb_utils.fmb_utilities.walklevel(datasets_path+ "/" + image_folder_path, level=0):
        
        verboseprint(1)(dirs)
        
        for dirct in dirs:
            
            im_files = []
            for ext in image_file_extentions:        
                #run through the files
                im_files = im_files + [f for f in glob(datasets_path + "/" + image_folder_path + "/" + dirct + "/" + "*" + ext)]
                
            #account all files
            for i, file in enumerate(im_files):                  
                # path handling
                new_filename = file.replace(datasets_path,'')
                new_filename = new_filename.replace(os.sep, '/')
                dataset_full.append(new_filename)
                full_data_counter +=1
                    
            #generating pairs
            number_of_pairs = min(max_pairs_per_class, math.floor(float(len(im_files))/2))
            
            for np in range(number_of_pairs):
                #random pair selection - 1)shuffle list; 2) choose first 2 items     
                random.shuffle(im_files)
                item_fh = (im_files[0]).replace(datasets_path,'')
                item_fh = item_fh.replace(os.sep, '/')
                
                item_sh = (im_files[1]).replace(datasets_path,'')
                item_sh = item_sh.replace(os.sep, '/')
                

                dataset_pairs.append((item_fh,item_sh))
                dataset_fh.append(item_fh)
                dataset_sh.append(item_sh)
                labels.append(1)
                

    print("Full number of images ", full_data_counter)   
    
    
    return(dataset_pairs, dataset_fh, dataset_sh, labels, dataset_full)

def generate_bona_fide_pairs_from_directory(datasets_path, 
                                          image_folder_path, 
                                          max_pairs_per_class = 1,
                                          image_file_extentions = default_image_file_extentions,
                                          verbose = 0):
    
    
    
   #Function for printing verbosity
    def verboseprint(verbosity_level):
        """ Simplest verbosity print function """
        return (print if verbose>verbosity_level else lambda *a, **k: None)
    
    #lists for storing the dataset and lists   
    dataset_pairs = []
    dataset_fh = []
    dataset_sh = []
    labels = []
    dataset_full = []
    
    full_data_counter = 0
    
    
    #run through the src folder folder
    for subdir, dirs, files in fmb_utils.fmb_utilities.walklevel(datasets_path+ "/" + image_folder_path, level=0):
        
        verboseprint(1)(dirs)
        
        for dirct in dirs:
            
            im_files = []
            for ext in image_file_extentions:        
                #run through the files
                im_files = im_files + [f for f in glob(datasets_path + "/" + image_folder_path + "/" + dirct + "/" + "*" + ext)]
                
            #account all files
            for i, file in enumerate(im_files):                  
                # path handling
                new_filename = file.replace(datasets_path,'')
                new_filename = new_filename.replace(os.sep, '/')
                dataset_full.append(new_filename)
                full_data_counter +=1
                    
            #generating pairs
            number_of_pairs = min(max_pairs_per_class, math.floor(float(len(im_files))/2))
            
            for np in range(number_of_pairs):
                #random pair selection - 1)shuffle list; 2) choose first 2 items     
                random.shuffle(im_files)
                item_fh = (im_files[0]).replace(datasets_path,'')
                item_fh = item_fh.replace(os.sep, '/')
                
                item_sh = (im_files[1]).replace(datasets_path,'')
                item_sh = item_sh.replace(os.sep, '/')
                

                dataset_pairs.append((item_fh,item_sh))
                dataset_fh.append(item_fh)
                dataset_sh.append(item_sh)
                labels.append(1)
                

    print("Full number of images ", full_data_counter)   
    
    
    return(dataset_pairs, dataset_fh, dataset_sh, labels, dataset_full)

def generate_morph_pairs_from_paired_folders(datasets_path, 
                                            image_folder_pathes,
                                            name_range_crop_1 = (0,0),
                                            name_range_crop_2 = (0,0),
                                            image_file_extentions = default_image_file_extentions,
                                            verbose = 0):
    """
    in image_folder_pathes - first is morph secon dis bonafide
    """
    #Function for printing verbosity
    def verboseprint(verbosity_level):
        """ Simplest verbosity print function """
        return (print if verbose>verbosity_level else lambda *a, **k: None)
    
    #lists for storing the dataset and lists   
    dataset_pairs = []
    dataset_fh = []
    dataset_sh = []
    labels = []
    dataset_full = []
    
    full_data_counter = 0
    
    #collect files in the first folder
    im_files_1 = []
    for ext in image_file_extentions:        
        #run through the files
        im_files_1 = im_files_1 + [f for f in glob(datasets_path + "/" + image_folder_pathes[0] + "/" + "*" + ext)]

    #collect files in the second folder
    im_files_2 = []
    for ext in image_file_extentions:        
        #run through the files
        im_files_2 = im_files_2 + [f for f in glob(datasets_path + "/" + image_folder_pathes[1] + "/" + "*" + ext)]
    
    #full dataset collect
    dataset_full = im_files_1 + im_files_2 
    
    # print(len(im_files_1))
    # print(len(im_files_2),image_folder_pathes[1])
    # sys.exit()
    #collect pairs
    
    for imf_1 in im_files_1:
        for imf_2 in im_files_2:
           
            item_fh = (imf_1).replace(datasets_path,'')
            item_fh = item_fh.replace(os.sep, '/')
            
            item_sh = (imf_2).replace(datasets_path,'')
            item_sh = item_sh.replace(os.sep, '/') 
           
            imf_1_id = item_fh.replace(image_folder_pathes[0], '')
            imf_1_id = imf_1_id.replace('/', '')
            
            imf_2_id = item_sh.replace(image_folder_pathes[1], '')
            imf_2_id = imf_2_id.replace('/', '')
            
            imf_1_id = imf_1_id[name_range_crop_1[0]:len(imf_1_id)-name_range_crop_1[1]]
            imf_2_id = imf_2_id[name_range_crop_2[0]:len(imf_2_id)-name_range_crop_2[1]]
            
            #print(imf_2_id,imf_1_id)
            
            
            #if bf identity is in morph - add pair
            if (imf_2_id in imf_1_id):
                # print(item_fh,item_sh)
                # print(imf_2_id, imf_1_id)
                dataset_pairs.append((item_fh,item_sh))
                dataset_fh.append(item_fh)
                dataset_sh.append(item_sh)
                labels.append(0)

    
    
    return(dataset_pairs, dataset_fh, dataset_sh, labels, dataset_full)




def generate_protocol_dd(datasets_path,  
                      bona_fide_labeled_datasets,
                      bona_fide_datasets,
                      bona_fide_datasets_list_as_paired_folders,
                      morph_pairs_from_paired_folders,
                      protocol_name = "", 
                      protocols_path = "",
                      verbose = 1
                      ):
    
    """
    Function that generates the protocol from the folder with test datasets and the list of the benchmark datasets
    
    Returns
    -------
    None. But saves the protocol files

    """     
    
    #Function for printing verbosity
    def verboseprint(verbosity_level):
        """ Simplest verbosity print function """
        return (print if verbose>verbosity_level else lambda *a, **k: None)
    
    #create protocol folder
    os.makedirs('%s/%s' %(protocols_path, protocol_name), exist_ok=True)
    
    #Counters
    full_counter = 0
    
    #init lists of dataset and labels
    dataset_pairs = []
    dataset_fh = []
    dataset_sh = []
    labels = []
    dataset_full = []
    
    #Make predictions and write them with the labels into a file 
    verboseprint(1)("start extracting dataset and lables file")
   
    
   
    
    #Extracting from the labeled folders with images
    verboseprint(1)("Extract bona_fide_labeled_datasets")
    for i, dtst in enumerate(bona_fide_labeled_datasets):
        dataset_pairs_i, dataset_fh_i, dataset_sh_i, labels_i, dataset_full_i = generate_bona_fide_pairs_from_labeled_dataset(
                                                  datasets_path, 
                                                  dtst, 
                                                  max_pairs_per_class = 5)
            
        dataset_pairs = dataset_pairs + dataset_pairs_i
        dataset_fh = dataset_fh + dataset_fh_i
        dataset_sh = dataset_sh + dataset_sh_i
        labels = labels + labels_i
        dataset_full = dataset_full + dataset_full_i
    
    #Extracting from the directory with images
    verboseprint(1)("Extract bona_fide_datasets")
    for i, dtst in enumerate(bona_fide_datasets):
        dataset_pairs_i, dataset_fh_i, dataset_sh_i, labels_i, dataset_full_i = generate_bona_fide_pairs_from_dataset(
                                                  datasets_path, 
                                                  dtst[0], 
                                                  (dtst[1],dtst[2]),
                                                  1)
            
        dataset_pairs = dataset_pairs + dataset_pairs_i
        dataset_fh = dataset_fh + dataset_fh_i
        dataset_sh = dataset_sh + dataset_sh_i
        labels = labels + labels_i
        dataset_full = dataset_full + dataset_full_i




    verboseprint(1)("Extract bona_fide_datasets_list_as_paired_folders")
    for i, dtst in enumerate(bona_fide_datasets_list_as_paired_folders):
        dataset_pairs_i, dataset_fh_i, dataset_sh_i, labels_i, dataset_full_i = generate_bona_fide_pairs_from_paired_folders(
                                                  datasets_path, 
                                                  (dtst[0][0],dtst[1][0]),
                                                  (dtst[0][1],dtst[0][2]),
                                                  (dtst[1][1],dtst[1][2]))
        
        
        dataset_pairs = dataset_pairs + dataset_pairs_i
        dataset_fh = dataset_fh + dataset_fh_i
        dataset_sh = dataset_sh + dataset_sh_i
        labels = labels + labels_i
        dataset_full = dataset_full + dataset_full_i




    #Extracting from the folders with folders with images
    verboseprint(1)("Extract morph_pairs_from_paired_folders")
    for i, dtst in enumerate(morph_pairs_from_paired_folders):
        dataset_pairs_i, dataset_fh_i, dataset_sh_i, labels_i, dataset_full_i = generate_morph_pairs_from_paired_folders(
                                                  datasets_path, 
                                                  (dtst[0][0],dtst[1][0]),
                                                  (dtst[0][1],dtst[0][2]),
                                                  (dtst[1][1],dtst[1][2]))
        
        dataset_pairs = dataset_pairs + dataset_pairs_i
        dataset_fh = dataset_fh + dataset_fh_i
        dataset_sh = dataset_sh + dataset_sh_i
        labels = labels + labels_i
        dataset_full = dataset_full + dataset_full_i
    

    
    # verboseprint(3)("dataset_full")
    # verboseprint(3)(dataset_full)
    
    # verboseprint(3)("dataset_pairs")
    # verboseprint(3)(dataset_pairs)
    # verboseprint(3)("Labels")
    # verboseprint(3)(labels)
    
    # verboseprint(3)("dataset_fh")
    # verboseprint(3)(dataset_fh)
    
    # verboseprint(3)("dataset_sh")
    # verboseprint(3)(dataset_sh)
    
    
    verboseprint(3)("length_full",len(dataset_full),"length",len(dataset_pairs), len(labels))
    
    #saving dataset and labels
    np.savetxt("%s/%s/%s" %(protocols_path,protocol_name,'/dataset_full.txt'),  np.array(dataset_full),fmt="%s",)
    np.savetxt("%s/%s/%s" %(protocols_path,protocol_name,'/dataset_pairs.txt'),  np.array(dataset_pairs),fmt="%s",)
    np.savetxt("%s/%s/%s" %(protocols_path,protocol_name,'/dataset_fh.txt'),  np.array(dataset_fh),fmt="%s",)
    np.savetxt("%s/%s/%s" %(protocols_path,protocol_name,'/dataset_sh.txt'),  np.array(dataset_sh),fmt="%s",)
    np.savetxt("%s/%s/%s" %(protocols_path,protocol_name,'/labels.txt'), np.array(labels),fmt="%u")


def test_read_images_in_folder_unspecified():
    
    test_datasets_path = "./data/test_data/"
    
    test_dataset  = "test_morphs/"
    test_label = 0
    
    dataset, labels = read_images_in_folder_unspecified(test_datasets_path, 
                                    test_dataset, 
                                    test_label,
                                    image_file_extentions = default_image_file_extentions)
    print(dataset)
    print(labels)


def test_read_folder_with_folders_of_images():
    
    test_datasets_path = "./data/test_data/"
    
    test_dataset  = "test_morphs/"
    test_label = 0
    
    dataset, labels = read_folder_with_folders_of_images(test_datasets_path, 
                                    test_dataset, 
                                    test_label,
                                    image_file_extentions = default_image_file_extentions)
    print(dataset)
    print(labels)







def generate_public_dd_protocol():
    """
    For Differential Detection it is important to match images by identities 
    For the automatic generation supposes that the identity-matched images have similar names.
    Here we crop some part of the image name to define if they are identity matched.
    bona_fide_labeled_datasets assumes that the images for identities are locaded in separate subdirectories of dataset path.
    
    For bona_fide_datasets, bona_fide_datasets_list_as_paired_folders and 
    morph_pairs_from_paired_folders the matching is made by image names. 
    Thus the dataset name is defined as follows: 
    (<relative_dataset_path>, <int number of symbols to remove from the beggining>, <int number of symbols to remove from the end>)
    
    """
    
    print("generating new protocol start")
    
    test_datasets_folder = "./data_aligned/insfmorph_renamed/"
    
    #path to the labelled datasets
    bona_fide_labeled_datasets = [#"FRLL-Morphs/facelab_london/"
                                  ]
    
    
    bona_fide_datasets = [#("FEI", 0, 5),
                          #("Aberdeen", 0, 5),
                         ]
    
    bona_fide_datasets_list_as_paired_folders = [(("Face_Research_Lab_London_Set/neutral_front/neutral_front", 0, 6), ("Face_Research_Lab_London_Set/smiling_front/smiling_front", 0, 6)),
                                                 (("Utrecht", 0, 4),("Utrecht", 0, 5)) #this is executed on the same folder with different name formatting
                                                 ]
    
    #here the first - morph directory, second - original directory
    morph_pairs_from_paired_folders = [
                                     #(("FRLL-Morphs/facelab_london/morph_amsl", 0, 4), ("Face_Research_Lab_London_Set/neutral_front/neutral_front", 0, 7)),
                                     #(("FRLL-Morphs/facelab_london/morph_facemorpher", 0, 4), ("Face_Research_Lab_London_Set/neutral_front/neutral_front", 0, 7))
                                     #(("FRLL-Morphs/facelab_london/morph_opencv", 0, 4), ("Face_Research_Lab_London_Set/neutral_front/neutral_front", 0, 7))
                                     #(("FRLL-Morphs/facelab_london/morph_stylegan", 0, 4), ("Face_Research_Lab_London_Set/neutral_front/neutral_front", 0, 7))
                                     #(("FRLL-Morphs/facelab_london/morph_webmorph", 0, 4), ("Face_Research_Lab_London_Set/neutral_front/neutral_front", 0, 7))

                                     ]
    


    #Protocol parameters
    #protocol_name = "protocol_dd_test"
    #protocol_name = "protocol_dd_opencv_v2"
    #protocol_name = "protocol_dd_facemorpher_v2"
    #protocol_name = "protocol_dd_asml_v2"
    #protocol_name = "protocol_dd_stylegan_v2"
    #protocol_name = "protocol_dd_webmorph_v2"
    
    
    protocols_path = "./benchmark_protocols"      
    
    
    #generate protocol if it is not yet generated
    if os.path.exists(protocols_path + "/" + protocol_name):
        #sys.exit("protocol already exist. force generating manually if required. (Comment this line when needed)")
        pass
    
    generate_protocol_dd(test_datasets_folder, 
                      bona_fide_labeled_datasets,
                      bona_fide_datasets,
                      bona_fide_datasets_list_as_paired_folders,
                      morph_pairs_from_paired_folders,
                      protocol_name, 
                      protocols_path,
                      verbose = 10
                      )
    
    # #gererate the protocol description:
     
    protocol_description_file = open(os.path.join(protocols_path, protocol_name,"protocol_description.txt"), "w")
    
    protocol_description_file.write("Protocol for Differential Image Morphing detection:\n")
    protocol_description_file.write("\n")
    protocol_description_file.write("Morped datasets in the protocol:\n")
    for i in morph_pairs_from_paired_folders:
        protocol_description_file.write(i[0][0]+" against "+i[1][0]+"\n")

    
    protocol_description_file.write("\n")
    protocol_description_file.write("Bona Fide datasets in the protocol:\n")
    for i in bona_fide_labeled_datasets:
        protocol_description_file.write(i+" labeled \n")
    for i in bona_fide_datasets:
        protocol_description_file.write(i[0]+" non_labeled \n")
    for i in bona_fide_datasets_list_as_paired_folders:
        protocol_description_file.write(i[0][0]+" against "+i[1][0]+"\n")
        
    protocol_description_file.close()
    
    
def generate_main_sd_protocol():
    pass
    
if __name__ == '__main__':
    
    #test_read_folder_with_folders_of_images()
    #test_read_images_in_folder_unspecified()
    #test_generate_protocol()
    generate_public_dd_protocol()
    