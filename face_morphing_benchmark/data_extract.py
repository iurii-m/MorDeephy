# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 15:47:27 2023

@author: iurii
"""


import requests
import os, sys, inspect
import argparse
import zipfile
import tarfile, io
import zlib
#import py7zr
#import unlzw3
from pathlib import Path
from unlzw import unlzw
import gzip
import patoolib


Dustone_Password = "********" 

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data_raw_path', default="./data_raw/", type=str)
    parser.add_argument('-e', '--data_extracted_path', default="./data_extracted/", type=str)
    args = parser.parse_args()
    return args



args = parse_args()
os.makedirs(args.data_extracted_path, exist_ok=True)


#extract PICS-Aberdeen dataset
try:
    print("Start extracting PICS-Aberdeen")
    os.makedirs(os.path.dirname(args.data_extracted_path)+"/Aberdeen/", exist_ok=True) 
    with zipfile.ZipFile(args.data_raw_path + "/Aberdeen.zip", 'r') as zip_ref:
        zip_ref.extractall(args.data_extracted_path+ "/Aberdeen/") 
    print("PICS-Aberdeen is extracted")
except:
    print("Error while PICS-Aberdeen extracting")


#extract PICS-utrecht dataset
try:
    print("Start extracting PICS-utrecht")
    os.makedirs(os.path.dirname(args.data_extracted_path)+"/utrecht/", exist_ok=True) 
    with zipfile.ZipFile(args.data_raw_path + "/utrecht.zip", 'r') as zip_ref:
        zip_ref.extractall(args.data_extracted_path+ "/utrecht/") 
    print("PICS-Aberdeen is extracted")
except:
    print("Error while PICS-utrecht extracting")
 
   
# #Extract and decode AR dataset
# try:
#     print("Start extracting AR Face Database")
       
#     os.makedirs(os.path.dirname(args.data_extracted_path)+"/AR/", exist_ok=True) 
#     os.makedirs(os.path.dirname(args.data_extracted_path)+"/AR_raw/", exist_ok=True) 
#     URL = "http://cbcsl.ece.ohio-state.edu/protected-dir/dbf1.tar.tar"
#     response = requests.get(URL)
#     open(args.data_path+"/AR/dbf1.tar.tar", "wb").write(response.content)
    
#     # open and extracting files
#     file = tarfile.open(args.data_raw_path+"/AR/dbf1.tar.tar")
#     file.extractall(args.data_extracted_path+ "/AR_raw/")
    
#     file = tarfile.open(args.data_raw_path+"/AR/dbf2.tar")
#     file.extractall(args.data_extracted_path+ "/AR_raw/")
    
#     file = tarfile.open(args.data_raw_path+"/AR/dbf3.tar")
#     file.extractall(args.data_extracted_path+ "/AR_raw/")
    
#     file = tarfile.open(args.data_raw_path+"/AR/dbf4.tar")
#     file.extractall(args.data_extracted_path+ "/AR_raw/")
    
#     file = tarfile.open(args.data_raw_path+"/AR/dbf5.tar")
#     file.extractall(args.data_extracted_path+ "/AR_raw/")
    
#     #6,7,8 - header problems for zlib
    
#     print("AR Face Database is extracted")
      
# except:
#     print("Error while AR Face Database extracting")

#Suggest dearchive manually and convert raw to jpeg with a script from    
#https://github.com/matheustguimaraes/organize-AR-face-db
#Then Put all .jpg images to AR folder  


#Extract FEI dataset
try:
    print("Start extracting FEI Face Database")
    
    os.makedirs(os.path.dirname(args.data_extracted_path)+"/FEI/", exist_ok=True) 
    
    with zipfile.ZipFile(args.data_raw_path + "/FEI/originalimages_part1.zip", 'r') as zip_ref:
        zip_ref.extractall(args.data_extracted_path+ "/FEI/") 

    with zipfile.ZipFile(args.data_raw_path + "/FEI/originalimages_part2.zip", 'r') as zip_ref:
        zip_ref.extractall(args.data_extracted_path+ "/FEI/") 
        
    with zipfile.ZipFile(args.data_raw_path + "/FEI/originalimages_part3.zip", 'r') as zip_ref:
        zip_ref.extractall(args.data_extracted_path+ "/FEI/") 
        
    with zipfile.ZipFile(args.data_raw_path + "/FEI/originalimages_part4.zip", 'r') as zip_ref:
        zip_ref.extractall(args.data_extracted_path+ "/FEI/") 

    print("FEI Face Database is extracted")
except:
    print("Error while FEI Face Database extracting")



#Extract FRLL dataset
try:
    print("Start extracting Face_Research_Lab_London_Set")
    
    os.makedirs(os.path.dirname(args.data_extracted_path)+"/Face_Research_Lab_London_Set/", exist_ok=True) 
    
    with zipfile.ZipFile(args.data_raw_path + "/Face_Research_Lab_London_Set.zip", 'r') as zip_ref:
        zip_ref.extractall(args.data_extracted_path+ "/Face_Research_Lab_London_Set/") 
     
    with zipfile.ZipFile(args.data_extracted_path + "/Face_Research_Lab_London_Set/neutral_front.zip", 'r') as zip_ref:
        zip_ref.extractall(args.data_extracted_path+ "/Face_Research_Lab_London_Set/neutral_front") 
      
    with zipfile.ZipFile(args.data_extracted_path + "/Face_Research_Lab_London_Set/smiling_front.zip", 'r') as zip_ref:
        zip_ref.extractall(args.data_extracted_path+ "/Face_Research_Lab_London_Set/smiling_front") 

    print("Face_Research_Lab_London_Set is extracted")
except:
    print("Error while Face_Research_Lab_London_Set extracting")



#Extract Dataset of Ethnic Facial Images of Ecuadorian People
try:
    print("Start extracting Dataset of Ethnic Facial Images of Ecuadorian People")
    
    os.makedirs(os.path.dirname(args.data_extracted_path)+"/EFIEP/", exist_ok=True) 
    
    with zipfile.ZipFile(args.data_raw_path + "/EFIEP.zip", 'r') as zip_ref:
        zip_ref.extractall(args.data_extracted_path+ "/EFIEP/") 
     
    patoolib.extract_archive(args.data_extracted_path + "/EFIEP/Afro-ecuadorians.rar", outdir=args.data_extracted_path+ "/EFIEP/")   
    patoolib.extract_archive(args.data_extracted_path + "/EFIEP/European-descendants.rar", outdir=args.data_extracted_path+ "/EFIEP/") 
    patoolib.extract_archive(args.data_extracted_path + "/EFIEP/Indigenous.rar", outdir=args.data_extracted_path+ "/EFIEP/") 
    patoolib.extract_archive(args.data_extracted_path + "/EFIEP/Mestizos.rar", outdir=args.data_extracted_path+ "/EFIEP/") 


    print("Dataset of Ethnic Facial Images of Ecuadorian People is extracted")
except:
    print("Error while Dataset of Ethnic Facial Images of Ecuadorian People extracting")


#extract MIT-CBCL dataset
try:
    print("Start extracting MIT-CBCL")
    os.makedirs(os.path.dirname(args.data_extracted_path)+"/MIT-CBCL/", exist_ok=True) 
    with zipfile.ZipFile(args.data_raw_path + "/MIT-CBCL-facerec-database.zip", 'r') as zip_ref:
        zip_ref.extractall(args.data_extracted_path+ "/MIT-CBCL/") 
    print("MIT-CBCL is extracted")
except:
    print("Error while MIT-CBCL extracting")


#MORPH DATASETS

#Extract FRGC-Morphs dataset #unavailable at Feb2023
try:
    print("Start extracting FRGC-Morphs")
    os.makedirs(os.path.dirname(args.data_extracted_path)+"/FRGC-Morphs/", exist_ok=True)
    # open file
    file = tarfile.open(os.path.dirname(args.data_raw_path)+"/FRGC-Morphs.tar.gz")
    file.extractall(os.path.dirname(args.data_extracted_path)+"/FRGC-Morphs/")
    print("FRGC-Morphs dataset is extracted")
except:
    print("Error while FRGC-Morphs extracting")


#Extract FERET-Morphs dataset #unavailable at Feb2023
try:
    print("Start extracting FERET-Morphs")
    os.makedirs(os.path.dirname(args.data_extracted_path)+"/FERET-Morphs/", exist_ok=True)
    # open file
    file = tarfile.open(os.path.dirname(args.data_raw_path)+"/FERET-Morphs.tar.gz")
    file.extractall(os.path.dirname(args.data_extracted_path)+"/FERET-Morphs/")
    print("FERET-Morphs dataset is extracted")
except:
    print("Error while FERET-Morphs extracting")


#Extract Dustone-Morphs dataset
#Request here https://www.linkedin.com/pulse/new-face-morphing-dataset-vulnerability-research-ted-dunstone/
try:
    print("Start extracting Dustone_Morphs dataset")
    os.makedirs(os.path.dirname(args.data_extracted_path)+"/Dustone_Morphs/", exist_ok=True)
    with zipfile.ZipFile(args.data_raw_path + "/morph_set__1_.zip", 'r') as zip_ref:
        zip_ref.extractall(args.data_extracted_path+ "/Dustone_Morphs/",pwd = bytes(Dustone_Password, 'utf-8')) 
    print("Dustone_Morphs dataset is extracted")
except:
    print("Error while Dustone_Morphs dataset extracting")


#Extract FRLL-Morphs dataset
try:
    print("Start extracting FRLL-Morphs")
    os.makedirs(os.path.dirname(args.data_extracted_path)+"/FRLL-Morphs/", exist_ok=True)
    # open file
    file = tarfile.open(os.path.dirname(args.data_raw_path)+"/FRLL-Morphs.tar.gz")
    file.extractall(os.path.dirname(args.data_extracted_path)+"/FRLL-Morphs/")
    print("FRLL-Morphs dataset is extracted")
except:
    print("Error while FRLL-Morphs extracting")


