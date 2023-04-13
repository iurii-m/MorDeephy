# -*- coding: utf-8 -*-
"""
Demo sctipt for extracting predictions.

@author: iurii
"""

import os, argparse
import numpy as np
import sys
import random   

def parse_args():
    
    parser = argparse.ArgumentParser() 
    parser.add_argument('-m', '--model_name', default="test_model", type=str, help='name of the model')
    parser.add_argument('-n', '--protocol_name', default="protocol_dd_asml", type=str, help='name of the protocol')
    parser.add_argument('-b', '--benchmark_protocols_path', default="./face_morphing_benchmark/benchmark_protocols/", type=str)
    parser.add_argument('-d', '--data_path', default="./face_morphing_benchmark/data_aligned/insf/", type=str)
    parser.add_argument('-p', '--models_path', default="./models", type=str, help='path to the models')
    parser.add_argument('-r', '--predictions_filename', default="predictions.txt", type=str, help='path to the models')
    parser.add_argument('-l', '--gt_labels_filename', default="gt_labels.txt", type=str, help='path to the models')
    args = parser.parse_args()
      
    return args


if __name__ == '__main__':
    
    args = parse_args()


    #prediction and label lists
    predictions = []
    gt_labels = []
    

    #Loading protocol
    dataset = (np.loadtxt('%s/%s/%s' %(args.benchmark_protocols_path,args.protocol_name,'dataset_pairs.txt'), dtype='str')).tolist()
    labels= (np.loadtxt('%s/%s/%s' %(args.benchmark_protocols_path,args.protocol_name,'labels.txt'), dtype='str')).tolist()
      
        
    #running throught the protocol size and generating predictions and labels
    for i, file in enumerate(dataset):

        
        label = int(labels[i])
        files = (str(file)).split(" ")
        filename1, filename2 = '%s/%s' %(args.data_path,str(files[0])), '%s/%s' %(args.data_path,str(files[1]))
        #print(filename1, filename2 , label)
        
#To me modified to your inference:
#------------------------------------------------------------------------------------------
        
        #Demo inference # generating random prediction
        #For differential detection the final prediction is supposed to be extracted basing on differential
        #comparizon of filename1, filename2
        
        perfomance_coefficient = 0.32
        #limiting the perfomance coefficient
        perfomance_coefficient = min(1,max(perfomance_coefficient, 0.0))
        #generating corresponding prediction
        
        rnd_var_1 = min(1, max(abs(random.gauss(0, perfomance_coefficient)), 0.0))  #**perfomance_coefficient
        rnd_var_2 = min(1, max(abs(random.gauss(0, perfomance_coefficient)), 0.0))
        
        prediction1 = (1.0-label)*rnd_var_1 
        prediction2 = (label)*(1.0-rnd_var_2)
        
        prediction = prediction1 + prediction2
        
#------------------------------------------------------------------------------------------
        
        predictions.append(prediction)
        gt_labels.append(label)
  
    print("predictions")
    print(predictions)
    print("gt_labels")
    print(gt_labels)
    print("len ", len(predictions), len(gt_labels))

       
    #creating test protocol folder
    os.makedirs('%s/%s/%s' %(args.models_path, args.model_name, args.protocol_name), exist_ok=True)
    
    np.savetxt('%s/%s/%s/%s' %(args.models_path, args.model_name, args.protocol_name, 'predictions.txt'), np.array(predictions))
    np.savetxt('%s/%s/%s/%s' %(args.models_path, args.model_name, args.protocol_name, 'gt_labels.txt'), (np.array(gt_labels)).astype(int))
    


