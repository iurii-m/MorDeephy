# -*- coding: utf-8 -*-
"""
Simple generating predictions and lables for single image (no-reference) morphing detection.

Generates 2 files - predictions.npy (imitate model predictions) and gt_labels.npy (imitate ground truth labels)

@author: iurii.medvedev
"""

import os, argparse
import numpy as np
import sys
import random   

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--protocol_size', default=3000, type=int)
    parser.add_argument('-p', '--protocol_path', default='../../models/test_model/test_protocol2', type=str)
    parser.add_argument('-c', '--perfomance_coefficient', default=0.35, type=float)
    args = parser.parse_args()
    return args


def generate_test_predictions(protocol_size = 3000, 
                              protocol_path = './face_morphing_benchmark/benchmark_data/test_protocol',
                              perfomance_coefficient = 0.7):
    """
    Generates protocol prediction files for further test metrics enaluating.

    Parameters
    ----------
    protocol_size : int, optional
        Size of protocol. The default is 3000.
    protocol_path : str, optional
        Path of files for protocol. The default is './face_morphing_benchmark/benchmark_data/test_protocol'.
    perfomance_coefficient : float, optional
        Coefficient that controlls the perfomance of the generated predictions . The default is 0.7.

    Returns
    -------
    None.
    """
    

    
    #prediction and label lists
    predictions = []
    gt_labels = []
    
    #limiting the perfomance coefficient
    perfomance_coefficient = min(1,max(perfomance_coefficient, 0.0))
    
    
    #running throught the protocol size and generating predictions and labels
    for i in range(protocol_size):
        #generating label
        label = random.randint(0, 1)
        gt_labels.append(label)
        #generating corresponding prediction
        rnd_var_1 = min(1, max(abs(random.gauss(0, perfomance_coefficient)), 0.0))  #**perfomance_coefficient
        rnd_var_2 = min(1, max(abs(random.gauss(0, perfomance_coefficient)), 0.0))
        prediction = (1.0-label)*rnd_var_1 + (label)*(1.0-rnd_var_2)
        predictions.append(prediction)

    #saving results as np arrays
    print("predictions")
    print(predictions)
    print("gt_labels")
    print(gt_labels)
    
    #np.save('%s/%s' %(protocol_path, '/predictions.npy'), np.array(predictions))
    #np.save('%s/%s' %(protocol_path, '/gt_labels.npy'), np.array(gt_labels))
    
    if protocol_path:
        print("protocol path is not empty")
        #creating test protocol folder
        os.makedirs('%s' %(protocol_path), exist_ok=True)
        
        np.savetxt('%s/%s' %(protocol_path, '/predictions.txt'), np.array(predictions))
        np.savetxt('%s/%s' %(protocol_path, '/gt_labels.txt'), np.array(gt_labels))
    
    return np.array(predictions), np.array(gt_labels)

if __name__ == '__main__':
    args = parse_args()
    generate_test_predictions(protocol_size = args.protocol_size, 
                            protocol_path = args.protocol_path,
                            perfomance_coefficient = args.perfomance_coefficient)