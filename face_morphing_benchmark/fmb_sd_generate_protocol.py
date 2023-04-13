# -*- coding: utf-8 -*-
"""
Generating the protocols for No-Reference MAD.
To generate - Set the values for Bona-fide and morph datasets in the protocol. 
Executing this file will lead to the generating the new protocol in the specified folder

@author: iurii
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

def read_images_in_folder_unspecified(datasets_path, 
                                    image_folder_path, 
                                    label,
                                    image_file_extentions = default_image_file_extentions,
                                    verbose = 0):
    """
    Generating datasets and labels lists from directory and its subdirectories. 
    """
    im_files = []
    
    #collect files for each extention
    #print("data_path is : ",datasets_path + "/" + image_folder_path)
    for ext in image_file_extentions:
        
        #print(os.path.join(datasets_path, image_folder_path, '**','*'+ext))
        files = [f for f in glob(os.path.join(datasets_path, image_folder_path,'**','*' + ext),recursive=True)]   
        im_files = im_files + files
        
    #print(im_files)
   
    dataset = []
    labels = []
    
    for i, file in enumerate(im_files):  
        
        # path handling
        relative_filename = file.replace(datasets_path,'')
        relative_filename = relative_filename.replace(os.sep, '/')
        #print(relative_filename)
        dataset.append(relative_filename)
        
        # label handling
        labels.append(label)
        
    return dataset, labels
    

def read_folder_with_images(datasets_path, 
                            image_folder_path, 
                            label, 
                            image_file_extentions = default_image_file_extentions,
                            verbose = 0):
    
    """
    Generating datasets and labels lists from folder with images. 
    """
    #lists for storing the dataset and lists
    dataset = []
    labels = []
    
    #run through the files
    #print("path", datasets_path+"/"+image_folder_path+"/")
    for ext in image_file_extentions:
        im_files = [f for f in glob(datasets_path+"/"+image_folder_path+"/" + "*" + ext)]
        #print("all files", im_files)
        for i, file in enumerate(im_files):  
            
            # path handling
            relative_filename = file.replace(datasets_path,'')
            relative_filename = relative_filename.replace(os.sep, '/')
            #print(relative_filename)
            dataset.append(relative_filename)
            
            # label handling
            labels.append(label)
       
    return dataset, labels


def read_folder_with_folders_of_images(datasets_path,
                                       image_folder_path, 
                                       label,
                                       image_file_extentions = default_image_file_extentions,
                                       verbose = 0):

    """
    Generating datasets and labels lists from directory with folders of images. 
    """
    #Function for printing verbosity
    def verboseprint(verbosity_level):
        """ Simplest verbosity print function """
        return (print if verbose>verbosity_level else lambda *a, **k: None)
    
    #lists for storing the dataset and lists
    dataset = []
    labels = []
    
    full_counter = 0
    
    
    #run through the src folder folder
    for subdir, dirs, files in fmb_utils.fmb_utilities.walklevel(datasets_path+ "/" + image_folder_path, level=0):
        
        verboseprint(1)(dirs)
        
        for dirct in dirs:
            
            for ext in image_file_extentions:        
                #run through the files
                im_files = [f for f in glob(datasets_path + "/" + image_folder_path + "/" + dirct + "/" + "*" + ext)]
                
                for i, file in enumerate(im_files):  
                    
                    # path handling
                    # print(file)
                    new_filename = file.replace(datasets_path,'')
                    new_filename = new_filename.replace(os.sep, '/')
                
                    dataset.append(new_filename)
                    
                    # label handling
                    labels.append(label)
                    full_counter +=1

    print("Full number of images ", full_counter)    

    return dataset, labels



def generate_protocol(datasets_path = "", 
                      morphing_datasets_list_unspecified = [],
                      original_datasets_list_unspecified = [],
                      morphing_datasets_list_as_folder_with_images = [],
                      original_datasets_list_as_folder_with_images = [],
                      morphing_datasets_list_as_folder_with_folders_of_images = [],
                      original_datasets_list_as_folder_with_folders_of_images = [],
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
    dataset = []
    labels = []
    labels_numbers = []
    
    #Make predictions and write them with the labels into a file 
    verboseprint(1)("start extracting dataset and lables file")
   
    
    #Extracting from the foleders with images
    verboseprint(1)("Extract morphing samples from the folders with images")
    for i, dtst in enumerate(morphing_datasets_list_as_folder_with_images):
        dataset_i, labels_i = read_folder_with_images(datasets_path, 
                                                      dtst, 
                                                      0)
        dataset = dataset + dataset_i
        labels = labels + labels_i
        full_counter = full_counter +len(dataset_i)
    

    verboseprint(1)("Extract original samples from the folders with images")
    for i, dtst in enumerate(original_datasets_list_as_folder_with_images):
        dataset_i, labels_i = read_folder_with_images(datasets_path, 
                                                      dtst, 
                                                      1)
        dataset = dataset + dataset_i
        labels = labels + labels_i
        full_counter = full_counter +len(dataset_i)




    #Extracting from the folders with folders with images
    verboseprint(1)("Extract morphing samples from the folders with folders with images")
    for i, dtst in enumerate(morphing_datasets_list_as_folder_with_folders_of_images):
        dataset_i, labels_i = read_folder_with_folders_of_images(datasets_path, 
                                                      dtst, 
                                                      0)
        dataset = dataset + dataset_i
        labels = labels + labels_i
        full_counter = full_counter +len(dataset_i)
    

    verboseprint(1)("Extract original samples from the folders with folders with images")
    for i, dtst in enumerate(original_datasets_list_as_folder_with_folders_of_images):
        dataset_i, labels_i = read_folder_with_folders_of_images(datasets_path, 
                                                      dtst, 
                                                      1)
        dataset = dataset + dataset_i
        labels = labels + labels_i
        full_counter = full_counter +len(dataset_i)




    #Extracting from the folders with folders with images
    verboseprint(1)("Extract morphing samples from unspecified folders")
    for i, dtst in enumerate(morphing_datasets_list_unspecified):
        dataset_i, labels_i = read_images_in_folder_unspecified(datasets_path, 
                                                                dtst, 
                                                                0)
        dataset = dataset + dataset_i
        labels = labels + labels_i
        full_counter = full_counter +len(dataset_i)
    

    verboseprint(1)("Extract original samples from unspecified folders")
    for i, dtst in enumerate(original_datasets_list_unspecified):
        dataset_i, labels_i = read_images_in_folder_unspecified(datasets_path, 
                                                                dtst, 
                                                                1)
        dataset = dataset + dataset_i
        labels = labels + labels_i
        full_counter = full_counter +len(dataset_i)

    
    verboseprint(3)("Dataset")
    verboseprint(3)(dataset)
    verboseprint(3)("Labels")
    verboseprint(3)(labels)
    verboseprint(3)("Full Counter")
    verboseprint(3)(full_counter)
    verboseprint(3)("length",len(dataset),len(labels))
    
    #saving dataset and labels
    np.savetxt("%s/%s/%s" %(protocols_path,protocol_name,'/dataset.txt'),  np.array(dataset),fmt="%s",)
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



def generate_public_sd_protocol():
    
    print("generating new protocol start")
    
    test_datasets_folder = "./data_aligned/insfmorph_renamed/"
   
    
    morphing_datasets_list_unspecified = []
    original_datasets_list_unspecified = []
     
    morphing_datasets_list_as_folder_with_images = [
                                                     "FRLL-Morphs/facelab_london/morph_amsl",
                                                     "FRLL-Morphs/facelab_london/morph_facemorpher",
                                                     "FRLL-Morphs/facelab_london/morph_opencv",
                                                     "FRLL-Morphs/facelab_london/morph_stylegan",
                                                     "FRLL-Morphs/facelab_london/morph_webmorph",
                                                     "Dustone_Morphs/morph_set"
                                                    ]
    
    original_datasets_list_as_folder_with_images = ["Face_Research_Lab_London_Set/neutral_front/neutral_front",
                                                    "AR",
                                                    "FEI",
                                                    "Aberdeen",
                                                    "utrecht",
                                                    "MIT-CBCL/training-originals"]
    
    
    morphing_datasets_list_as_folder_with_folders_of_images = []
    original_datasets_list_as_folder_with_folders_of_images = ["EFIEP"]
    
    #Protocol parameters
    protocol_name = "protocol_sd_full"
    
    protocols_path = "./benchmark_protocols"      
    
    #generate protocol if it is not yet generated
    if os.path.exists(protocols_path + "/" + protocol_name):
        sys.exit("protocol already exist. force generating manually if required. (Comment this line when needed)")
        pass
    
    generate_protocol(test_datasets_folder, 
                      morphing_datasets_list_unspecified,
                      original_datasets_list_unspecified,
                      morphing_datasets_list_as_folder_with_images,
                      original_datasets_list_as_folder_with_images,
                      morphing_datasets_list_as_folder_with_folders_of_images,
                      original_datasets_list_as_folder_with_folders_of_images,
                      protocol_name, 
                      protocols_path,
                      verbose = 10
                      )
    
    #gererate the protocol description:
     
    protocol_description_file = open(os.path.join(protocols_path, protocol_name,"protocol_description.txt"), "w")
    
    protocol_description_file.write("Protocol for Single Image Morphing detection:\n")
    protocol_description_file.write("\n")
    protocol_description_file.write("Morped datasets in the protocol:\n")
    for i in morphing_datasets_list_unspecified:
        protocol_description_file.write(i+"\n")
    for i in morphing_datasets_list_as_folder_with_images:
        protocol_description_file.write(i+"\n")
    for i in morphing_datasets_list_as_folder_with_folders_of_images:
        protocol_description_file.write(i+"\n")
    
    protocol_description_file.write("\n")
    protocol_description_file.write("Bona Fide datasets in the protocol:\n")
    for i in original_datasets_list_unspecified:
        protocol_description_file.write(i+"\n")
    for i in original_datasets_list_as_folder_with_images:
        protocol_description_file.write(i+"\n")
    for i in original_datasets_list_as_folder_with_folders_of_images:
        protocol_description_file.write(i+"\n")
        
    
    protocol_description_file.close()
    
       
if __name__ == '__main__':
    
    #test_read_folder_with_folders_of_images()
    #test_read_images_in_folder_unspecified()
    generate_public_sd_protocol()
    
    