# -*- coding: utf-8 -*-
"""

Load generated metrics data for several models and draw them on a single plot.

"""


import argparse
import os
import csv
import glob
import numpy as np
from sklearn.metrics import roc_auc_score, roc_curve, det_curve, accuracy_score
import matplotlib.pyplot as plt
import face_morphing_benchmark.fmb_utils.BPCER_at_APCER as bpcer_apcer

     
    
def parse_args():
    
    parser = argparse.ArgumentParser() 
    parser.add_argument('-n', '--protocol_name', default=None, type=str, help='name of the protocol')
    parser.add_argument('-b', '--submissions_path', default="./submissions", type=str, help='path to the submissions')
    parser.add_argument('-e', '--exclude_submissions_list', nargs='+', default=[], help='list with submissions to exclude')
    parser.add_argument('-r', '--predictions_filename', default="predictions.txt", type=str, help='path to the models')
    parser.add_argument('-l', '--gt_labels_filename', default="gt_labels.txt", type=str, help='path to the models')
    args = parser.parse_args()
      
    return args



if __name__ == "__main__":
           
    args = parse_args()
    
    #Define the protocols for proceeding
    protocols_to_proceed = []
    
    if not (args.protocol_name):
        #list all protocols
        protocols_to_proceed = [(f.replace(args.submissions_path, '')).replace(os.path.sep, '') for f in glob.glob(args.submissions_path+"/" + "*"+"protocol"+ "*")]
    else:
        #append only required protocols
        protocols_to_proceed.append(args.protocol_name)
    
    print("protocols_to_proceed", protocols_to_proceed)
    
    for pr, protocol in enumerate(protocols_to_proceed):
        
        #get app model names
        submission_names = [(f.replace(args.submissions_path+"/"+protocol, '')).replace(os.path.sep, '') for f in glob.glob(args.submissions_path+"/"+protocol+"/" + "*")]
        

        #exclude filenames:
        submission_names = [item for item in submission_names if not os.path.isfile(os.path.join(args.submissions_path+"/"+protocol, item))]
        #exclude specially excluded submission names
        submission_names = [item for item in submission_names if not any(excluded_submission in item for excluded_submission in args.exclude_submissions_list)]
        
        print(submission_names)
        
        submission_predictions = []
        submission_gt_labels = []
        
        for sn, sub_name in enumerate(submission_names):
            print("read", sub_name)
            #load 
            predictions = (np.loadtxt("%s/%s/%s/%s" %(args.submissions_path, protocol, sub_name, args.predictions_filename), dtype=np.dtype(float))).tolist()
            gt_labels = (np.loadtxt("%s/%s/%s/%s" %(args.submissions_path, protocol, sub_name, args.gt_labels_filename), dtype=np.dtype(float))).tolist()
            submission_predictions.append(predictions)
            submission_gt_labels.append(gt_labels)
            #print(predictions, gt_labels)
            
        #call the result plotting for the protocol
        bpcer_apcer.plot_combined_roc(protocol_name = protocol, 
                                      submissions_path = args.submissions_path, 
                                      submission_names = submission_names,
                                      all_predictions = submission_predictions, 
                                      all_gt_labels = submission_gt_labels, 
                                      save_name ='%s/%s/ROC.png' %(args.submissions_path, protocol))
           
        bpcer_apcer.plot_combined_det(protocol_name = protocol, 
                                      submissions_path = args.submissions_path, 
                                      submission_names = submission_names,
                                      all_predictions = submission_predictions, 
                                      all_gt_labels = submission_gt_labels, 
                                      save_name ='%s/%s/DET.png' %(args.submissions_path, protocol))

    
    