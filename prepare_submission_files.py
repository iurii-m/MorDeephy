# -*- coding: utf-8 -*-
"""
Script for copying the result performance files from the models directory to the the resective places of the submission directory

@author: iurii
"""

import argparse
import os
import csv
import glob
import numpy as np
import shutil

        
    
def parse_args():

    parser = argparse.ArgumentParser() 
    parser.add_argument('-m', '--model_name', default="test_model2", type=str, help='A string containing the name of the model for which the submission is being prepared')
    parser.add_argument('-s', '--submission_name', default="test_model_001", type=str, help=' A string containing the name of the submission.')
    parser.add_argument('-n', '--protocol_name', default=None, type=str, help='A string containing the name of the protocol for which the submission is being prepared. If this is not provided, then all protocols will be considered.')
    parser.add_argument('-p', '--models_path', default="./models", type=str, help='A string containing the path to the directory where the model is saved.')
    parser.add_argument('-b', '--submissions_path', default="./submissions", type=str, help='A string containing the path to the directory where the submission is to be saved')
    parser.add_argument('-r', '--predictions_filename', default="predictions.txt", type=str, help='A string containing the name of the predictions file.')
    parser.add_argument('-l', '--gt_labels_filename', default="gt_labels.txt", type=str, help='A string containing the name of the ground truth labels file')
    args = parser.parse_args()
      
    return args




def prepare_submission(args):
    """
    The function takes in an args object that contains several arguments needed for preparing a 
    submission. The function prepares a submission by copying the required files from the source 
    directory to the destination directory. The function performs the following tasks:
    
    -Lists all protocols if no specific protocol is provided or appends only the required 
    protocol if a specific protocol is provided.
    
    -Copies the predictions and ground truth labels files for each protocol from the 
    source directory to the destination directory, where the destination directory is determined by the submission_name argument.
    
    -Copies the README.md file from the source directory to the destination directory.
    
    """
    
    
    
    print("Model for submission", args.model_name)
    
    
    computed_protocols = []
    
    if not (args.protocol_name):
        #list all protocols
        computed_protocols = [f.replace(args.models_path+"/"+args.model_name, '') for f in glob.glob(args.models_path+"/"+args.model_name+"/" + "*"+"protocol"+ "*")]
    else:
        #append only required protocols
        computed_protocols.append("/"+args.protocol_name)
    
    print("Protocols for preparing submission", computed_protocols)

    #Copying files for the protocol
    for p in computed_protocols:
        try:
            #chech if predictions and labels files exists
            if os.path.exists("%s/%s/%s/%s" %(args.models_path,args.model_name,p,args.predictions_filename)) and os.path.exists("%s/%s/%s/%s" %(args.models_path,args.model_name,p,args.gt_labels_filename)):

                os.makedirs("%s/%s/%s/" %(args.submissions_path,p,args.submission_name), exist_ok = True)
                shutil.copy("%s/%s/%s/%s" %(args.models_path,args.model_name,p,args.predictions_filename), "%s/%s/%s/%s" %(args.submissions_path,p,args.submission_name,args.predictions_filename))        
                shutil.copy("%s/%s/%s/%s" %(args.models_path,args.model_name,p,args.gt_labels_filename), "%s/%s/%s/%s" %(args.submissions_path,p,args.submission_name,args.gt_labels_filename))        
                print("Copied files for protocol", p)         
            else:
                raise Exception("Prediction files does not exist")
        
        except:
            print("Error while copying submission files for protocol", p)
    
    
    #Copy Readme
    if os.path.exists("%s/%s/%s" %(args.models_path,args.model_name,"README.md")):
        try:
            os.makedirs("%s/%s/%s/" %(args.submissions_path,"supplementary",args.submission_name), exist_ok = True)
            shutil.copy("%s/%s/%s" %(args.models_path,args.model_name,"README.md"), "%s/%s/%s/%s" %(args.submissions_path,"supplementary",args.submission_name,"README.md"))        
            print("Copied model README.md")
        except:
            print("Error while copying the README.md")
    else:
        print("README.md doesnt exist for the respective model")
    
    
    
if __name__ == '__main__':
    args = parse_args()
    prepare_submission(args)