# -*- coding: utf-8 -*-
"""
Script for estimating the performance basing on the predictions of the model.

@author: iurii
"""

import argparse
import os
import csv
from glob import glob
import numpy as np

import face_morphing_benchmark.fmb_utils.fmb_utilities as fmb_utilities
import face_morphing_benchmark.fmb_utils.BPCER_at_APCER as bpcer_apcer

        
    
def parse_args():
    
    parser = argparse.ArgumentParser() 
    parser.add_argument('-m', '--model_name', default="test_model", type=str, help='name of the model')
    parser.add_argument('-n', '--protocol_name', default="test_protocol", type=str, help='name of the protocol')
    parser.add_argument('-p', '--models_path', default="./models", type=str, help='path to the models')
    parser.add_argument('-r', '--predictions_filename', default="predictions.txt", type=str, help='path to the models')
    parser.add_argument('-l', '--gt_labels_filename', default="gt_labels.txt", type=str, help='path to the models')
    args = parser.parse_args()
      
    return args




def benchmark_model(args):
   
    predictions = (np.loadtxt("%s/%s/%s/%s" %(args.models_path, args.model_name, args.protocol_name, args.predictions_filename), dtype=np.dtype(float))).tolist()
    gt_labels = (np.loadtxt("%s/%s/%s/%s" %(args.models_path, args.model_name, args.protocol_name, args.gt_labels_filename), dtype=np.dtype(float))).tolist()
     
    # print(predictions)
    # print(gt_labels)
    
    #extract metrics
    FMR_compare = [0.2, 0.1, 0.01, 0.001, 0.0001]
    bpcer_apcer.get_ROC_metric(predictions, 
                               gt_labels, 
                               args.protocol_name, 
                               args.model_name, 
                               benchmark_data_path = args.models_path, 
                               FMR_compare = FMR_compare)
    
 
    APCER_compare = [0.2, 0.1, 0.01, 0.001, 0.0001]
    bpcer_apcer.get_DET_metric(predictions, 
                               gt_labels, 
                               args.protocol_name, 
                               args.model_name, 
                               benchmark_data_path = args.models_path, 
                               APCER_compare = APCER_compare)    

    
if __name__ == '__main__':
    args = parse_args()
    benchmark_model(args)
    
    
    