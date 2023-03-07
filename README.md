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
We propose to make a submission as a *pull request* (PR) to this repository.
How to PR to public repo is explained here: [manual official](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request), [manual simple](https://www.geeksforgeeks.org/creating-a-pull-request-on-any-public-repository-from-github-using-vs-code/)

The process can be summarized to the following pipeline:

1. Login to your github account and fork this repository.

2. Submit your results following the requirements to your fork and then make PR to the original repo.
    Here we propose two tested options: **Regular** and **Simple**.
    **Simple.** Uploading files right at the github website. 

    1. For each submitted protocol you need to create a directory in your fork.
    Use "Add File -> Create new file" option to create ```README.md``` file indicating its name with a realtive path to a corresponding results directory, which you want to add.
    Feel free to organize the ```README.md``` file to better represent your submission.
    2. Navigate to the created folder and use ```Add File -> Upload files``` to upload files for your submission.
    3. Make a PR to the original repo with the appeared ```Contribute``` button. 

    **Regular.**
    
    1. Clone your fork to your local machiene.
    
    ```
    git clone https://github.com/visteam-isr-uc/MorDeephy.git
    cd MorDeephy
    ```
    2. Optionally change your branch to the name of your submission (better practice).
    Howerer it is ok and indeed more simple to stay on *master*.
    
    ```
    git branch <your_submission_branch>
    ```   
    3. Execute the script for preparing submission or Copy your submission files to the corresponding folders.
    ```
    TODO
    ``` 	
    4. Add and commit your changes.
    ```
    git add <your files for submission or just "." to add all new>
    git commit -m “<submission name>”

    ``` 
    5. Push changes to the current branch of your forked repository.
    ```
    git push –set-upstream origin <your current branch>
    ```
    To authenticate this step github doesnt allow using regular credentials. We propose to [Generate classic token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token#creating-a-personal-access-token-classic). Further authentification for push can be made using it instead of a password.

    6. Configure a Remote for the Fork
    ```
    git remote add upstream https://github.com/iurii-m/MorDeephy.git
    git remote -v
    ```
    Output will be:
    ```
    origin  https://github.com/visteam-isr-uc/MorDeephy.git (fetch)
    origin  https://github.com/visteam-isr-uc/MorDeephy.git (push)
    upstream        https://github.com/iurii-m/MorDeephy.git (fetch)
    upstream        https://github.com/iurii-m/MorDeephy.git (push)
    ```
    7. Sync the fork
    ```
    git fetch upstream
    ```
    8. Open your forked repo on github and Create Pull Request with appeared alert button.
 


*If you are not confident with git, suggest to have separate projects for development and for making submissions and perform manual file copying.*

#### Submission requirements
##### TODO





### Submitting protocols and data
If you have data related to face morphing, consider extending the functionality of this repo.
If you propose to use some custom protocol, you can generate them and PR to the repo [Protocols_generation](./face_morphing_benchmark)
Please separate those PRs from PRs for results submission 

## Results comparison
#### TODO


## Data for benchmarking

The benchmarking is based on the public data. 
It is firmly recommended not to use it during training of your algorithms in case you plan to submit your results here. 
See the preparation details here [(data_processing)](./face_morphing_benchmark)
#### Bona Fide datasets
- [AR](https://www2.ece.ohio-state.edu/~aleix/ARdatabase.html)
- [PICS-Aberdeen](http://pics.stir.ac.uk/2D_face_sets.htm)
- [PICS-utrecht](http://pics.stir.ac.uk/2D_face_sets.htm)
- [FEI](https://fei.edu.br/~cet/facedatabase.html)
- [FRLL](https://figshare.com/articles/dataset/Face_Research_Lab_London_Set/5047666)
- [EFIEP](https://figshare.com/articles/dataset/Dataset_of_Ethnic_facial_images_of_Ecuadorian_people/8266730)
- [MIT-CBCL](http://cbcl.mit.edu/software-datasets/heisele/facerecognition-database.html)

#### Morph Datasets 
- [FRLL-Morphs](https://www.idiap.ch/en/dataset/frll-morphs)
- [Dustone_Morphs](https://www.linkedin.com/pulse/new-face-morphing-dataset-vulnerability-research-ted-dunstone/) (email request is required)

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
