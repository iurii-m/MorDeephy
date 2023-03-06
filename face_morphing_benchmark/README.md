# Data and Protocols Details

## Data for benchmarking

The benchmarking is based on the public data. 
It is firmly recommended not to use it during training of your algorithms in case you plan to submit your results here. 

#### Bona Fide datasets
-[AR](https://www2.ece.ohio-state.edu/~aleix/ARdatabase.html)
-[PICS-Aberdeen](http://pics.stir.ac.uk/2D_face_sets.htm)
-[PICS-utrecht](http://pics.stir.ac.uk/2D_face_sets.htm)
-[FEI](https://fei.edu.br/~cet/facedatabase.html)
-[FRLL](https://figshare.com/articles/dataset/Face_Research_Lab_London_Set/5047666)
-[EFIEP](https://figshare.com/articles/dataset/Dataset_of_Ethnic_facial_images_of_Ecuadorian_people/8266730)
-[MIT-CBCL](http://cbcl.mit.edu/software-datasets/heisele/facerecognition-database.html)

#### Morph Datasets 
-[FRLL-Morphs](https://www.idiap.ch/en/dataset/frll-morphs)
-[Dustone_Morphs](https://www.linkedin.com/pulse/new-face-morphing-dataset-vulnerability-research-ted-dunstone/)

Some data ([FRGC-Morphs](https://www.idiap.ch/en/dataset/frgc-morphs) and [FERET-Morphs](https://www.idiap.ch/en/dataset/feret-morphs) datasets) is now unavailable due to the withdrawal.


### Downloading the data.   
```
cd face_morphing_benchmark
python download_data.py
```
AR dataset should be downloaded, extracted and converted to jpg manually (the data is old and several python packages doesnt handle it properly). Suggest using [7-Zip](https://www.7-zip.org/) and [converter](https://github.com/matheustguimaraes/organize-AR-face-db).

MIT-CBCL dataset should be downloaded manually.

### Extracting the data
To extract Dustone morphs dataset automatically set the Dustone_Password in data_extract.py
```
cd face_morphing_benchmark
python data_extract.py
```

## No-Reference Protocols generation

New protocols can be denerated with fmb_sd_generate_protocol.py script. The manual definition of the included datasets in the script is required.

## Differential Protocols generation
### TODO


