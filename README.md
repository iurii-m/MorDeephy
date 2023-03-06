# Face Morphing Attack Detection benchmarking

This repo includes functionality for morphing attack detection benchmarking from the paper "MorDeephy: Face Morphing Detection Via Fused Classification".
The project may be used for performing benchmarks on your side and further submistting results for comparison between different developers.
The prorect only unifies the data, protocols, perfromance estimation, results comparizon. 
The extracting of the predictions data is up to the developer

## No-Reference benchmarking

1. [Prepare](./face_morphing_benchmark) and [align](./align_protocol_insf.py) data (for demo we use [MTCNN](https://github.com/ipazc/mtcnn) to align images).
We propose to have separate directories for different types of alignment.
2. Extracting predictions. You can store models files in the same directory together with the predictions and benchmark result data. It is up to you to adopt you algorithms and extract the respective predictions for protocols. This is not generalizable due to the various development enviroments. You may follow the demo script for extarcting predictions:
```
python sd_demo_extracting_predictions.py -m <your modelname> -n <protocol name> -d <path to the aligned images>
```
3. Computing the result performance curves:
```
python sd_benchmark_model.py -m <your modelname> -n <protocol name> 
```
 

## Differential benchmarking
### TODO


# Submistting and contributing
### How to submit your results
#### TODO
If you are not confident with git, suggest to have separate projects for development and for making submissions.


### Submitting protocols and data
If you have data related to face morphing, consider extending the functionality of this repo.
Uf you propose to use some custom protocol, you can generate them and PR to the repo [Protocols_generation](./face_morphing_benchmark)
Please separate those PRs from PRs for results submission 

## Results comparison
#### TODO


## Data for benchmarking

The benchmarking is based on the public data. 
It is firmly recommended not to use it during training of your algorithms in case you plan to submit your results here. 
See the preparation details here [(data_processing)](./face_morphing_benchmark)
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

If you find the results of our work useful in your research, please consider to cite the paper:

```
@article{MorDeephy,
    author = {Medvedev, Iurii and Shadmand, Farhad and Gonçalves, Nuno},
    year = {2022},
    journal={arXiv:2208.03110},
    month = {08},
    pages = {},
    title = {MorDeephy: Face Morphing Detection Via Fused Classification},
    doi = {10.48550/arXiv.2208.03110}
}
```
