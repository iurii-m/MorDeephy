# -*- coding: utf-8 -*-
"""
Script for downloading source data for face morphing detection 

@author: iurii
"""

import requests
import os, sys, inspect
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data_path', default="./data_raw/", type=str)
    args = parser.parse_args()
    return args


args = parse_args()
args.data_path+"/"

os.makedirs(args.data_path, exist_ok=True)


#BONA-FIDE DATASETS

#Get PICS-Aberdeen dataset
try:
    print("Start Downloading PICS-Aberdeen")
    URL = "http://pics.stir.ac.uk/zips/Aberdeen.zip"
    response = requests.get(URL)
    open(args.data_path+"/Aberdeen.zip", "wb").write(response.content)
    print("PICS-Aberdeen is downloaded")
except:
    print("Error while PICS-Aberdeen download")
    
#Get PICS-utrecht dataset
try:
    print("Start Downloading PICS-utrecht")
    URL = "http://pics.stir.ac.uk/zips/utrecht.zip"
    response = requests.get(URL)
    open(args.data_path+"/utrecht.zip", "wb").write(response.content)
    print("PICS-utrecht is downloaded")
except:
    print("Error while PICS-utrecht download")

#Get AR dataset
try:
    print("Start Downloading AR Face Database")
   
    os.makedirs(os.path.dirname(args.data_path)+"/AR/", exist_ok=True) 
   
    URL = "http://cbcsl.ece.ohio-state.edu/protected-dir/dbf1.tar.tar"
    response = requests.get(URL)
    open(args.data_path+"/AR/dbf1.tar.tar", "wb").write(response.content)

    URL = "http://cbcsl.ece.ohio-state.edu/protected-dir/dbf2.tar"
    response = requests.get(URL)
    open(args.data_path+"/AR/dbf2.tar", "wb").write(response.content)
    
    URL = "http://cbcsl.ece.ohio-state.edu/protected-dir/dbf3.tar"
    response = requests.get(URL)
    open(args.data_path+"/AR/dbf3.tar", "wb").write(response.content)
    
    URL = "http://cbcsl.ece.ohio-state.edu/protected-dir/dbf4.tar"
    response = requests.get(URL)
    open(args.data_path+"/AR/dbf4.tar", "wb").write(response.content)
    
    URL = "http://cbcsl.ece.ohio-state.edu/protected-dir/dbf5.tar"
    response = requests.get(URL)
    open(args.data_path+"/AR/dbf5.tar", "wb").write(response.content)
    
    URL = "http://cbcsl.ece.ohio-state.edu/protected-dir/dbf6.tar.Z"
    response = requests.get(URL)
    open(args.data_path+"/AR/dbf6.tar.Z", "wb").write(response.content)
    
    URL = "http://cbcsl.ece.ohio-state.edu/protected-dir/dbf7.tar.Z"
    response = requests.get(URL)
    open(args.data_path+"/AR/dbf7.tar.Z", "wb").write(response.content)
    
    URL = "http://cbcsl.ece.ohio-state.edu/protected-dir/dbf8.tar.Z"
    response = requests.get(URL)
    open(args.data_path+"/AR/dbf8.tar.Z", "wb").write(response.content)
    
    print("AR Face Database is downloaded")
      
except:
    print("Error while AR Face Database download")

#Get FEI dataset
try:
    print("Start Downloading FEI Face Database")
   
    os.makedirs(os.path.dirname(args.data_path)+"/FEI/", exist_ok=True) 
   
    URL = "https://fei.edu.br/~cet/originalimages_part1.zip"
    response = requests.get(URL)
    open(args.data_path+"/FEI/originalimages_part1.zip", "wb").write(response.content)
    
    URL = "https://fei.edu.br/~cet/originalimages_part2.zip"
    response = requests.get(URL)
    open(args.data_path+"/FEI/originalimages_part2.zip", "wb").write(response.content)
    
    URL = "https://fei.edu.br/~cet/originalimages_part3.zip"
    response = requests.get(URL)
    open(args.data_path+"/FEI/originalimages_part3.zip", "wb").write(response.content)
    
    URL = "https://fei.edu.br/~cet/originalimages_part4.zip"
    response = requests.get(URL)
    open(args.data_path+"/FEI/originalimages_part4.zip", "wb").write(response.content)
    
    print("FEI Face Database is downloaded")
      
except:
    print("Error while FEI Face Database download")
    
    
#Get FRLL dataset
try:
    print("Start Downloading Face_Research_Lab_London_Set")
    URL = "https://figshare.com/ndownloader/articles/5047666/versions/5"
    response = requests.get(URL)
    open(args.data_path+"/Face_Research_Lab_London_Set.zip", "wb").write(response.content)
    print("Face_Research_Lab_London_Set is downloaded")
except:
    print("Error while Face_Research_Lab_London_Set download")



#MORPH DATASETS

#Get FRGC-Morphs dataset #unavailable at Feb2023
# try:
#     print("Start Downloading FRGC-Morphs")
#     URL = "https://zenodo.org/record/4415270/files/FRGC-Morphs.tar.gz?download=1"
#     response = requests.get(URL)
#     open(args.data_path+"/FRGC-Morphs.tar.gz", "wb").write(response.content)
#     print("FRGC-Morphs dataset is downloaded")
# except:
#     print("Error while FRGC-Morphs download")



# #Get FERET-Morphs dataset #unavailable at Feb2023
# try:
#     print("Start Downloading FERET-Morphs")
#     URL = "https://zenodo.org/record/4415202/files/FERET-Morphs.tar.gz?download=1"
#     response = requests.get(URL)
#     open(args.data_path+"/FERET-Morphs.tar.gz", "wb").write(response.content)
#     print("FERET-Morphs dataset is downloaded")
# except:
#     print("Error while FERET-Morphs download")


#Get Dustone-Morphs dataset
#Request here https://www.linkedin.com/pulse/new-face-morphing-dataset-vulnerability-research-ted-dunstone/
#Put the archive morph_set__1_.zip to args.data_path directory


#Get FRLL-Morphs dataset
try:
    print("Start Downloading FRLL-Morphs")
    URL = "https://zenodo.org/record/4415159/files/FRLL-Morphs.tar.gz?download=1"
    response = requests.get(URL)
    open(args.data_path+"/FRLL-Morphs.tar.gz", "wb").write(response.content)
    print("FRLL-Morphs dataset is downloaded")
except:
    print("Error while FRLL-Morphs download")