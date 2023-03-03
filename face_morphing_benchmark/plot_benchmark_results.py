# -*- coding: utf-8 -*-
"""
Ploting selected scores for estimating their thresholds.

1 . loading scores and ground truth labels
2 . getting min and max , normalizing scores,
3 . calculating rates and thresholds
4 . plotting 

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
import cv2


from scipy import stats

import numpy as np
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt
from sklearn import metrics

def find_nearest_value(array, value):
    """
    Simple function to find nearest value in np array

    Parameters
    ----------
    array : numpy array
        array to search the value
    value : float
        value to search

    Returns
    -------
    closest_element : numpy input array element type
        Closest element in the array
    idx : int
        index of the closest elemets

    """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    closest_element = array[idx]

    return  closest_element, idx

def build_plot(ax,
               gr_colors = None,
               gr_legend = None,
               
               #data vars
               bench_data_path = "",
               model_names = None,
               model_names_toshow = None,
                   
               #protocol vars
               protocol_name = None,
               protocol_show_name = None,
               legenda = None,
               score_nature = None,
               APCER_compare = [0.5,0.2,0.1,0.05,0.01, 0.005, 0.001],
               BPCER_compare = [0.5,0.2,0.1,0.05,0.01, 0.005, 0.001]):

   
    
    

    if not score_nature:
        scores = 1 - scores

    #loading scores
    result_predictions = []
    result_labels = []
    
    for i,model_name in enumerate(model_names):
        pred = np.loadtxt('%s/%s/%s/%s' %(bench_data_path, model_name, protocol_name, "result_predictions.txt"))  
        
        
        #normalizing predictions to 0-1
        minmax = (np.amin(pred ), np.amax(pred ))
        pred = (pred-minmax[0]) / (minmax[1]-minmax[0])
        
        if score_nature[i]:
            pred = 1 - pred
        
        result_predictions.append(pred)
        
        lbl = np.loadtxt('%s/%s/%s/%s' %(bench_data_path, model_name, protocol_name, "result_labels.txt"))
        result_labels.append(lbl)
        
        
        APCER, BPCER, thresholds = metrics.det_curve(lbl, pred, pos_label=1)
        
        lw = 1
        ax.plot(APCER, BPCER, color=gr_colors[i] ,lw=lw, label=gr_legend[i])
        
        
        # print fpr and fnr in a file
        with open('%s/%s/%s/APCER_BPCER.csv' %(bench_data_path, model_name, protocol_name), mode='w') as tfrates_file:
            csv_writer = csv.writer(tfrates_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(APCER)
            csv_writer.writerow(BPCER)
        
        # extracting metrics BPCER@APCER
        if(len(APCER_compare)>0):
    
            BPCER_results = []
            
            for i in range(len(APCER_compare)):
                
                APCER_closest, APCER_closest_index = find_nearest_value(APCER, APCER_compare[i])
                #print("APCER closest", APCER_closest, APCER_closest_index)
                BPCER_results.append(BPCER[APCER_closest_index])
    
            print("APCER @ values", APCER_compare)
            print("BPCER values", BPCER_results)     
             
            with open('%s/%s/%s/BPCER@APCER.csv' %(bench_data_path, model_name, protocol_name), mode='w') as BPCER_APCER_file:
                    csv_writer = csv.writer(BPCER_APCER_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    csv_writer.writerow(APCER_compare)
                    csv_writer.writerow(BPCER_results)    
      
        
        # extracting metrics APCER@BPCER
        if(len(BPCER_compare)>0):
    
            APCER_results = []
            
            for i in range(len(BPCER_compare)):
                
                BPCER_closest, BPCER_closest_index = find_nearest_value(BPCER, BPCER_compare[i])
                #print("APCER closest", APCER_closest, APCER_closest_index)
                APCER_results.append(APCER[BPCER_closest_index])
    
            print("BPCER @ values", BPCER_compare)
            print("APCER values", APCER_results)     
             
            with open('%s/%s/%s/APCER@BPCER.csv' %(bench_data_path, model_name, protocol_name), mode='w') as APCER_BPCER_file:
                    csv_writer = csv.writer(APCER_BPCER_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    csv_writer.writerow(BPCER_compare)
                    csv_writer.writerow(APCER_results)     
      

    leg = None
    if legenda:
        
        leg = ax.legend(loc=(1.05, 0.2))
    
    ax.set_title(protocol_show_name)
    # ax.set_xscale('log')
    # ax.set_yscale('log')
    # ax.set_xlim([0.05, 1.0])
    # ax.set_ylim([0.05, 1.0])


  


    
    #ploting DET curve
    # plt.figure()
    # lw = 1
    # plt.plot(APCER, BPCER, color='black',lw=lw, label='DET' +model_name+ ' curve ')
    # plt.xlim([0.01, 1.0])
    # plt.ylim([0.01, 1.0])
    # plt.xlabel('APCER')
    # plt.ylabel('BPCER')
    # plt.xscale('log')
    # plt.yscale('log')
    # plt.title('DET_' + model_name +"_" + protocol_name)
    # plt.legend(loc="lower right")
    # #plt.show()
    # #save ROC curve with appropriate name
    # ROC_name = benchmark_data_path +"/" + model_name +"/" + protocol_name + "/DET" + ".png"
    # plt.savefig(ROC_name)
    
    
   

    return leg

    



def main():
    
    benchmark_data_folder = "./benchmark_data_act/"
     
    #define model names
    model_names = [
              "model_ResNet_softmax_VGGFace2_SS2C_org_morphP4_selfN50_0.0vs1.0_activated_512d_1_ep_default"
              ,"model_ResNet_softmax_VGGFace2_SS2C_org_morphP4_selfN50_0.01vs1.0_activated_512d_1_ep_default"
              ,"model_ResNet_softmax_VGGFace2_SS2C_org_morphP4_selfN50_0.05vs1.0_activated_512d_1_ep_default"
              ,"model_ResNet_softmax_VGGFace2_SS2C_org_morphP4_selfN50_0.2vs1.0_activated_512d_1_ep_default"
              ,"model_ResNet_softmax_VGGFace2_SS2C_org_morphP4_selfN50_1.0vs1.0_activated_512d_1_ep_default"
              ,"model_ResNet_softmax_VGGFace2_SS2C_org_morphP4_selfN50_1.0vs0.1_activated_512d_1_ep_default"
              ,"model_ResNet_softmax_VGGFace2_SS2C_org_morphP4_selfN50_1.0vs0.0_activated_512d_1_ep_default"
              ]
    
    #define legend label names
    model_names_toshow = [
              "α = 0"
              ,"α/β = 0.01"
              ,"α/β = 0.05"
              ,"α/β = 0.2"
              ,"α/β = 1"
              ,"α/β = 10"
              ,"β = 0"
              ]

    #define scores names
    protocol_names = [
              "protocol_fmsd_public2"
              ,"protocol_fmsd_face_morpher_public"
              ,"protocol_fmsd_webmorph_public"
              ,"protocol_fmsd_stylegan_public"
              ]
    
    protocol_show_names = [
              "protocol_real"
              ,"protocol-facemorpher"
              ,"protocol_webmorph"
              ,"protocol_stylegan"
              ]

    legends = [
        False,
        False,
        False,
        True
            ]

    #the variable indicates if the score has inverted nature.
    scores_nature = [
              [False,False,False,False,False,False,False],
              [False,False,False,False,False,False,False],
              [False,False,False,False,False,False,False],
              [False,False,False,False,False,False,False]
              ]
    
        
    colors=[
        "red",    
        "blue",
        "yellow",
        "green",
        "purple",
        "dodgerblue",
        "lime"
           ]
        
      

        
    fig, axs = plt.subplots(1, 4, figsize=(13,3))
    
    #fig.suptitle('Vertically stacked subplots')
    fig.tight_layout()
    
    leg = None
    
    plt.xlabel("    ")
    
    plt.ylabel("    ", )

    fig.text(0.5, -0.01, 'APCER', ha='center')
    fig.text(-0.01, 0.5, 'BPCER', va='center', rotation='vertical')
    
    #calculating rates and plotting result 
    for i, name in enumerate(protocol_names):
        
        if i==0:
            axs[i].set_ylabel("  ", fontsize=10)
        
        #print(score, ground_truth_acceptance, minmaxes[i][0], minmaxes[i][1], selected_scores_folder, scores_names[i])
        leg = build_plot(axs[i], 
                   gr_colors = colors,
                   gr_legend = model_names_toshow ,
                   
                   bench_data_path = benchmark_data_folder,
                   model_names = model_names,
                   model_names_toshow = model_names_toshow,
                   
                   protocol_name = protocol_names[i],
                   protocol_show_name = protocol_show_names[i],
                   legenda = legends[i],
                   score_nature = scores_nature[i]
                   )
    
    
    
    fig.savefig('%s/%s.pdf' %(benchmark_data_folder, "combined_lin"), bbox_extra_artists=(leg,), bbox_inches='tight')    
        
    fig.show()
    
if __name__ == '__main__':
    main()