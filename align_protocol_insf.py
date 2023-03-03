# -*- coding: utf-8 -*-
"""
Demo for data alignment.
Processing the dataset for the benchmark protocol.
Detect and align faces. Then copy resized files to the dst folder.
In case of non detection - resizing original image to the targes size
@author: iurii
"""

from alignment import _align_faces
import cv2
import glob
import os, sys, inspect, argparse
import numpy as np
from mtcnn.mtcnn import MTCNN


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--src_data_path', default="./face_morphing_benchmark/data_extracted/", type=str)
    parser.add_argument('-d', '--dst_data_path', default="./face_morphing_benchmark/data_aligned/", type=str)
    parser.add_argument('-b', '--benchmark_protocols_path', default="./face_morphing_benchmark/benchmark_protocols/", type=str)
    parser.add_argument('-p', '--protocol_name', default="protocol_sd_real", type=str)
    parser.add_argument('-a', '--alignment_name', default="insf", type=str)
    parser.add_argument('-i', '--image_size', default=300, type=int)
    parser.add_argument('-e', '--if_skip_existing_images', default=True, type=bool)
    args = parser.parse_args()
    return args



def main(args):
    
     
    src_folder = args.src_data_path
    dst_folder = str(args.dst_data_path)+"/"+str(args.alignment_name)
    face_size=(int(args.image_size), int(args.image_size))
    
    
    detector = MTCNN()
    

    #load dataset pathes 
    dataset_path = os.path.join(str(args.benchmark_protocols_path), str(args.protocol_name), "dataset.txt")
    dataset = np.loadtxt(dataset_path, dtype='str')
    
    print(dataset)
    print("dataset shape", dataset.shape)
     
    print("start alignment")
    well_aligned_counter = 0
    badly_aligned_counter = 0
    exists_counter = 0
    non_detected_list = []

    for i, file in enumerate(dataset):  

        #src filename
        filename = str(src_folder)+"/"+file
        #new filename
        new_filename = str(dst_folder)+"/"+file
        
        
        if args.if_skip_existing_images and os.path.exists(new_filename):
            print(new_filename, "exists")
            exists_counter += 1
            continue
        
        #creating folder fo image
        print("dirname", os.path.dirname(new_filename))
        os.makedirs(os.path.dirname(new_filename), exist_ok=True) 
        
        #loading image
        image = cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2RGB)
        
        #run alignment    
        result, number_of_detected, main_idx , landmarks = _align_faces(cv_image = image,
                                                                        detector = detector, 
                                                                        face_size = face_size, 
                                                                        main_face_criteria = "size")
       

        
        
        if (number_of_detected>0):

            print("Saving aligned image", new_filename)
            cv2.imwrite(new_filename, cv2.cvtColor(result[main_idx], cv2.COLOR_RGB2BGR))
            well_aligned_counter += 1
            

        else:
            print("No detected face", new_filename, "Resizing original image")
            image_res = cv2.resize(image, face_size)
            cv2.imwrite(new_filename, cv2.cvtColor(image_res, cv2.COLOR_RGB2BGR))
            non_detected_list.append(file)
            badly_aligned_counter +=1
               
    
    #Final results
    print('all images - ', len(dataset), ' well_aligned_counter - ', well_aligned_counter, "badly_aligned_counter", badly_aligned_counter)
    if args.if_skip_existing_images:
        print("exists_counter", exists_counter)
    print("Non detected faces:")
    print(non_detected_list)


if __name__ == '__main__':
    args = parse_args()
    main(args)



