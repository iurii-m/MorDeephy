# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 16:33:29 2021

@author: iurii
"""

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, roc_curve, det_curve, accuracy_score
import matplotlib.pyplot as plt
import csv
import os
from generate_test_predictions import generate_test_predictions

from fmb_utilities import find_nearest_value



def get_ROC_metric(predictions, 
                   gt_labels, 
                   protocol_name, 
                   model_name, 
                   benchmark_data_path = "models", 
                   FMR_compare = []):

    
    #create protocol folder in the model folder if so far not created
    os.makedirs('%s/%s/%s' %(benchmark_data_path, model_name, protocol_name), exist_ok=True)

    #Area under the curve
    auc_res = roc_auc_score(gt_labels, predictions)
    auc_res_5f =  "{:.5f}".format(auc_res)
    print("AUC ROC - ", auc_res_5f)
    
    fpr, tpr, thresholds = roc_curve(gt_labels, predictions, pos_label=1)
    # print tpr and fpr  in a file
    with open('%s/%s/%s/tpr_fpr.csv' %(benchmark_data_path, model_name, protocol_name), mode='w') as tfrates_file:
        csv_writer = csv.writer(tfrates_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(tpr)
        csv_writer.writerow(fpr)
        
    #calculate FMR and FNMR
    FMR = fpr
    FNMR = 1-tpr

    # print(FMR)
    # print(FNMR)
    # print(thresholds)
    # print(predictions)
    # print(gt_labels)

    #accuracy
    accuracy_ls = []
    y_test = gt_labels
    for thres in thresholds:
        y_pred = np.where(predictions>thres,1,0)
        accuracy_ls.append(accuracy_score(y_test, y_pred, normalize=True))

        
    #print accuracy, threshold, FMR and FNMR in a file
    with open('%s/%s/%s/ROC_metrics.csv' %(benchmark_data_path, model_name, protocol_name), mode='w') as metrics_file:
        csv_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        csv_writer.writerow(thresholds)
        csv_writer.writerow(accuracy_ls)
        csv_writer.writerow(FMR)
        csv_writer.writerow(FNMR)
    
    
    with open('%s/%s/%s/top_accuracy.csv' %(benchmark_data_path, model_name, protocol_name), mode='w') as metrics_file:
        csv_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([str(max(accuracy_ls))])

    
    #plot ROC curve
    plt.figure()
    lw = 1
    plt.plot(fpr, tpr, color='black',lw=lw, label='Default. texture. ROC curve (area = '+str(auc_res_5f)+')')
    # plt.xlim([0.0, 1.0])
    # plt.ylim([0.0, 1.0])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC_' + model_name +"_" + protocol_name)
    plt.legend(loc="lower right")
    #plt.show()
    #save ROC curve with appropriate name
    ROC_name = benchmark_data_path +"/" + model_name +"/" + protocol_name + "/ROC_AUC-" +str(auc_res_5f)+ ".png"
    plt.savefig(ROC_name)
    
    
    # extracting metrics FNMR @ FMR
    if(len(FMR_compare)>0):

        FNMR_results = []
        
        for i in range(len(FMR_compare)):
            
            FMR_closest, FMR_closest_index = find_nearest_value(FMR, FMR_compare[i])
            #print("FMR closest", FMR_closest, FMR_closest_index)
            FNMR_results.append(FNMR[FMR_closest_index])

    
        print(FMR_compare)
        print(FNMR_results)     
         
        with open('%s/%s/%s/FNMR@FMR.csv' %(benchmark_data_path, model_name, protocol_name), mode='w') as FNMR_FMR_file:
                csv_writer = csv.writer(FNMR_FMR_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow(FMR_compare)
                csv_writer.writerow(FNMR_results)


 

def get_DET_metric(predictions, 
                   gt_labels, 
                   protocol_name, 
                   model_name, 
                   benchmark_data_path = "models", 
                   APCER_compare = []):
    
    
    #create protocol folder in the model folder if so far not created
    os.makedirs('%s/%s/%s' %(benchmark_data_path, model_name, protocol_name), exist_ok=True)


    APCER, BPCER, thresholds = det_curve(gt_labels, predictions, pos_label=1)

    # print fpr and fnr in a file
    with open('%s/%s/%s/APCER_BPCER.csv' %(benchmark_data_path, model_name, protocol_name), mode='w') as tfrates_file:
        csv_writer = csv.writer(tfrates_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(APCER)
        csv_writer.writerow(BPCER)

    #computing EER
    substr = np.abs(APCER-BPCER)
    min_summy_idx = np.argmin(substr)
    EqER = APCER[min_summy_idx]
    EqER_4f =  "{:.4f}".format(EqER)
    print("EER - " , EqER_4f)

    
    #ploting DET curve
    plt.figure()
    lw = 1
    plt.plot(APCER, BPCER, color='black',lw=lw, label='DET_EER-'+str(EqER_4f) +"_"+ model_name+ ' curve ')
    # plt.xlim([0.01, 1.0])
    # plt.ylim([0.01, 1.0])
    plt.xlabel('APCER')
    plt.ylabel('BPCER')
    plt.xscale('log')
    plt.yscale('log')
    plt.title('DET_' + model_name +"_" + protocol_name)
    plt.legend(loc="lower right")
    #plt.show()
    #save ROC curve with appropriate name
    ROC_name = benchmark_data_path +"/" + model_name +"/" + protocol_name + "/DET_EER-"+str(EqER_4f) + ".png"
    plt.savefig(ROC_name)
    
    

    
    
    with open('%s/%s/%s/DET_EER.csv' %(benchmark_data_path, model_name, protocol_name), mode='w') as metrics_file:
        csv_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([str(EqER)])
    
    # extracting metrics FNMR @ FMR
    if(len(APCER_compare)>0):

        BPCER_results = []
        
        for i in range(len(APCER_compare)):
            
            APCER_closest, APCER_closest_index = find_nearest_value(APCER, APCER_compare[i])
            #print("APCER closest", APCER_closest, APCER_closest_index)
            BPCER_results.append(BPCER[APCER_closest_index])

        print("APCER @ values", APCER_compare)
        print("BPCER values", BPCER_results)     
         
        with open('%s/%s/%s/BPCER@APCER.csv' %(benchmark_data_path, model_name, protocol_name), mode='w') as BPCER_APCER_file:
                csv_writer = csv.writer(BPCER_APCER_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow(APCER_compare)
                csv_writer.writerow(BPCER_results)


def get_accuracy_metric():
    #accuracy
    #if not os.path.exists('%s/metrics.csv' %model_protocol_path):
    accuracy_ls = []
    y_test = gt_labels
    for thres in thresholds:
        y_pred = np.where(predictions>thres,1,0)
        accuracy_ls.append(accuracy_score(y_test, y_pred, normalize=True))

        
    #print accuracy, threshold, FMR and FNMR in a file
    with open('%s/%s/%s/metrics.csv' %(benchmark_data_path, model_name, protocol_name), mode='w') as metrics_file:
        csv_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        csv_writer.writerow(thresholds)
        csv_writer.writerow(accuracy_ls)
        csv_writer.writerow(FMR)
        csv_writer.writerow(FNMR)
    

def unit_test_ROC():
    #basic test
    
    gt_labels = np.array([0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0 ,1])
    predictions = np.array([0.01058, 0.02543, 0.79634, 0.80573, 0.29474, 0.50843, 0.370573, 0.91037, 0.053913,
                       0.30347, 0.80264, 0.8935, 0.02104, 0.03637, 0.050735,0.970038, 0.962312, 0.99, 
                       0.8547, 0.76035, 0.872636, 0.07048, 0.12025, 0.212735, 0.00019, 1.00])
    
    # print("predictions:")  
    # print(predictions)   
    # print("gt_labels:")
    # print(gt_labels)  
    
    protocol_name = "test_protocol"
    model_name = "test_model"
    benchmark_data_path = "../../models/"
    FMR_compare = [0.2, 0.1, 0.01, 0.001, 0.0001]
    
    get_ROC_metric(predictions, gt_labels, protocol_name, model_name, benchmark_data_path, FMR_compare)
    

def unit_test_ROC_2():
    #basic test
    predictions, gt_labels = generate_test_predictions(protocol_size = 3000, 
                                                       protocol_path = '../../models/test_model/test_protocol',
                                                       perfomance_coefficient = 0.3)
    # print("predictions:")  
    # print(predictions)   
    # print("gt_labels:")
    # print(gt_labels)  
    
    protocol_name = "test_protocol"
    model_name = "test_model"
    benchmark_data_path = "../../models/"
    FMR_compare = [0.2, 0.1, 0.01, 0.001, 0.0001]
    
    get_ROC_metric(predictions, gt_labels, protocol_name, model_name, benchmark_data_path, FMR_compare)


def unit_test_DET():
    #basic test
    
    gt_labels = np.array([0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0 ,1])
    predictions = np.array([0.01058, 0.02543, 0.79634, 0.80573, 0.29474, 0.50843, 0.370573, 0.91037, 0.053913,
                       0.30347, 0.80264, 0.8935, 0.02104, 0.03637, 0.050735,0.970038, 0.962312, 0.99, 
                       0.8547, 0.76035, 0.872636, 0.07048, 0.12025, 0.212735, 0.00019, 1.00])
    
    # print("predictions:")  
    # print(predictions)   
    # print("gt_labels:")
    # print(gt_labels)  
    
    protocol_name = "test_protocol_manual"
    model_name = "test_model"
    benchmark_data_path = "../../models/"
    APCER_compare = [0.2, 0.1, 0.01, 0.001, 0.0001]
    
    get_DET_metric(predictions, gt_labels, protocol_name, model_name, benchmark_data_path, APCER_compare)
    

def unit_test_DET_2():
    #basic test
    predictions, gt_labels = generate_test_predictions(protocol_size = 3000, 
                                                     protocol_path = '../../models/test_model/test_protocol',
                                                     perfomance_coefficient = 0.3)
    # print("predictions:")  
    # print(predictions)   
    # print("gt_labels:")
    # print(gt_labels)  
    
    protocol_name = "test_protocol"
    model_name = "test_model"
    benchmark_data_path = "../../models/"
    APCER_compare = [0.2, 0.1, 0.01, 0.001, 0.0001]
    
    get_DET_metric(predictions, 
                   gt_labels, 
                   protocol_name, 
                   model_name, 
                   benchmark_data_path, 
                   APCER_compare)    


def load_metrics_data(protocol_name, model_name, metric_name = "tpr_fpr", benchmark_data_path = "models"):
    """
    Loads metrics data from previously saved files

    Parameters
    ----------
    protocol_name : string
        Name of the protocol to load the data from
    model_name : string
        Name of the model where the metrics file is
    metric_name : string, optional
        Name of the metric file to be loaded. The default is "tpr_fpr".
    models_path : string, optional
        Path to the models folder. The default is "models".
        
    Returns
    -------
    metrics_array : np.array 
        np.array of metric file
    """
    filename = metric_name + ".csv"
    metrics_array = np.genfromtxt(os.path.join(benchmark_data_path,model_name,protocol_name,filename), delimiter=",")
    
    return metrics_array

if __name__ == '__main__':
    #unit_test_ROC()
    #unit_test_ROC_2()
    
    #unit_test_DET()
    unit_test_DET_2()
