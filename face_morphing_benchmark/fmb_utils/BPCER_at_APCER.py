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

    
    """
    Computes and plots the Receiver Operating Characteristic (ROC) curve for a binary classification model,
    along with the Area Under the Curve (AUC) score. Saves the ROC curve as a .png file.
    
    Parameters:
    ----------  
    - predictions (list or numpy array): predicted labels for each sample
    - gt_labels (list or numpy array): ground truth labels for each sample
    - protocol_name (str): name of the protocol being evaluated
    - model_name (str): name of the model being evaluated
    - benchmark_data_path (str): path to the directory where benchmarking data will be saved
    
    Returns: 
    ----------      
    None
    
    Output:
    ----------  
    - Saves the ROC curve plot as a PNG image in the benchmark_data_path folder, with a file name 
    containing the AUC value and the model and protocol names.
    - Saves the TPR and FPR values in a CSV file named "tpr_fpr.csv" in the protocol_name folder inside the model_name folder.
    - Calculates and saves the accuracy, FPR, FNR, and threshold values in a CSV file named 
    "ROC_metrics.csv" in the protocol_name folder inside the model_name folder.
    - Calculates and saves the maximum accuracy in a CSV file named "top_accuracy.csv" in the 
    protocol_name folder inside the model_name folder.
    - Calculates and saves the FNR at specific FPR values specified in the FMR_compare argument in a 
    CSV file named "FNMR@FMR.csv" in the protocol_name folder inside the model_name folder.
    """       
 
    
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
    
    """
    Computes and saves the Detection Error Tradeoff (DET) curve and Equal Error Rate (EER) for a given set of predictions
    and ground truth labels. 
    
    Parameters
    ----------
    - predictions (array-like): The predicted scores for each sample.
    - gt_labels (array-like): The ground truth labels (0 or 1) for each sample.
    - protocol_name (str): The name of the evaluation protocol.
    - model_name (str): The name of the model being evaluated.
    - benchmark_data_path (str): The path to the directory where the benchmark data is saved.
    - APCER_compare (list): A list of APCER values to compare against. Default is an empty list.
    
    Returns:
    ----------
    - None
    
    Saves:
    ----------
    - A CSV file with the APCER and BPCER values.
    - A PNG image of the DET curve.
    
    """
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
    
def plot_combined_roc(protocol_name, 
                      submissions_path, 
                      submission_names,
                      all_predictions, 
                      all_gt_labels, 
                      save_name):
    """
    Description: This function generates a combined ROC plot for multiple submissions 
    in a given evaluation protocol. It takes as input the protocol name, the path to 
    submission files, the list of submission names, the list of predicted scores, the 
    list of ground-truth labels, and the name to save the plot.

    Parameters
    ----------
    - protocol_name (str): The name of the evaluation protocol.
    - submissions_path (str): The path to the submission files.
    - submission_names (list of str): The list of names of the submissions to be evaluated.
    - all_predictions (list of ndarray): The list of predicted scores for each submission.
    - all_gt_labels (list of ndarray): The list of ground-truth labels for each submission.
    - save_name (str): The name of the file to save the plot.
    
    Returns
    -------
    None.
    
    Output
    -------
    A ROC plot with all the submissions superimposed on the same plot.
    The Area Under the Curve (AUC) for each submission is printed in the console.
    """

    
    fig = plt.figure(figsize=(8,5))
    lw = 1
    font_size = 14
    
    est_data = []
    #If no particular models are chosen, plot all models:
    for idx, submission in enumerate(submission_names):

      
        fpr, tpr, thresholds = roc_curve(all_gt_labels[idx], all_predictions[idx], pos_label=1)
        auc_res = roc_auc_score(all_gt_labels[idx], all_predictions[idx])
        auc_res_5f =  "{:.5f}".format(auc_res)
        print(submission, "AUC ROC - ", auc_res_5f)
        est_data.append((fpr, tpr, thresholds))
        legend_name =  submission+ " AUC ROC - "+ str(auc_res_5f)
        plt.plot(fpr, tpr, lw=lw, label = legend_name)
        
    # plt.xlim([0.0, 1.0])
    # plt.ylim([0.0, 1.0])
    plt.xticks(fontsize=font_size)
    plt.yticks(fontsize=font_size)
    plt.xlabel('False Positive Rate',fontsize = font_size)
    plt.ylabel('True Positive Rate',fontsize = font_size)
    plt.legend(loc="lower right")
    plt.legend(loc="lower right",fontsize=font_size)
    plt.tight_layout()
    plt.title('ROC_' + protocol_name,fontsize = font_size)
    #plt.yscale('log')
    #plt.xscale('log')
    plt.show()      
    fig.savefig(save_name)                 
        



def plot_combined_det(protocol_name, 
                      submissions_path, 
                      submission_names, 
                      all_predictions, 
                      all_gt_labels, 
                      save_name):
    """

    This function plots a Detection Error Tradeoff (DET) curve for each submission 
    specified in submission_names. For each submission, the 
    APCER (Attack Presentation Classification Error Rate), 
    BPCER (Bona Fide Presentation Classification Error Rate), and thresholds are 
    calculated using the det_curve function. The Equal Error Rate (EER) is also calculated 
    and printed for each submission. The function then plots the APCER vs BPCER curves 
    for each submission on a log-log scale and saves the plot to a file specified by save_name.


    Parameters
    ----------
    protocol_name: a string representing the name of the protocol to plot (e.g. 'protocol_1')
    submissions_path: a string representing the path to the directory where the submission files are located
    submission_names: a list of strings representing the names of the submission files to plot
    all_predictions: a list of arrays representing the predicted scores for each submission
    all_gt_labels: a list of arrays representing the ground truth labels for each submission
    save_name: a string representing the name of the file to save the plot to
    
    Returns
    -------
    None.

    """
    
    fig = plt.figure(figsize=(8,5))
    lw = 1
    font_size = 14

    est_data = []
    for idx, submission in enumerate(submission_names):
        APCER, BPCER, thresholds = det_curve(all_gt_labels[idx], all_predictions[idx], pos_label=1)
       
        # Calculate EER
        substr = np.abs(APCER-BPCER)
        min_summy_idx = np.argmin(substr)
        EqER = APCER[min_summy_idx]
        EqER_4f = "{:.4f}".format(EqER)
        print(submission, "EER - ", EqER_4f)
        
        est_data.append((APCER, BPCER, thresholds))
        legend_name = submission + " EER - " + str(EqER_4f)
        plt.plot(APCER, BPCER, lw=lw, label=legend_name)

    plt.xticks(fontsize=font_size)
    plt.yticks(fontsize=font_size)
    plt.xlabel('APCER', fontsize=font_size)
    plt.ylabel('BPCER', fontsize=font_size)
    plt.legend(loc="lower left", fontsize=font_size)
    plt.title('DET_' + protocol_name, fontsize=font_size)
    plt.xscale('log')
    plt.yscale('log')
    plt.show()
    fig.savefig(save_name)

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
    protocol_name : string Name of the protocol to load the data from
    model_name : string Name of the model where the metrics file is
    metric_name : string, optional Name of the metric file to be loaded. The default is "tpr_fpr".
    models_path : string, optional Path to the models folder. The default is "models".
        
    Returns
    -------
    metrics_array : np.array  np.array of metric file
    """
    
    filename = metric_name + ".csv"
    metrics_array = np.genfromtxt(os.path.join(benchmark_data_path,model_name,protocol_name,filename), delimiter=",")
    
    return metrics_array

if __name__ == '__main__':
    #unit_test_ROC()
    #unit_test_ROC_2()
    
    #unit_test_DET()
    unit_test_DET_2()
