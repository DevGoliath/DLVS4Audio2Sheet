# DLVS4Audio2Sheet: Deep Learning-based Vocal Separation for Audio into Music Sheet Conversion

## Datasets
This repository contains scripts we used for data processing. The raw datasets have to be downloaded from their original sources as they are too large to host here.

* [Choral Singing Dataset](https://zenodo.org/records/1286570), put inside the folder ```datasets/csd```
* [Esmuc Choir Dataset](https://zenodo.org/records/5848990), put inside the folder ```datasets/esmuc```

After the datasets are download, follow these steps in order:
1. Instructions to set up and run the dataset preprocessing scripts are found inside the folder ```datasets/```.
2. run preprocess_csd_and_esmuc.py, check that now there exists the folder ```datasets/combined_processed_dataset```. This will be used specifically for Open-Unmix.
3. run batch_convert_mono_to_stereo_for_bsrnn.py, check that now there exists the folder ```datasets/combined_processed_dataset_converted_stereo```. This will be used specifically for BSRNN.

## Training the Models
Since the 3 models are very different from each other, we have put them individually inside their respective directories in ```models/model```. Inside each directory, please follow the respective README.md

## Results
1. Our models achieved the following Source-to-Distortion Ratio (SDR) results:

|             | Soprano |  Alto |  Tenor |  Bass | Average |
|-------------|---------|-------|--------|-------|---------|
| SOTA*       |   1.67  | 10.70 |  -7.13 |  7.42 |   2.88  |
| Open-Unmix  |   4.68  |  3.12 |   2.13 |  1.74 |   2.92  |
| BSRNN       |   2.16  |  3.12 |   2.86 |  3.21 |   2.84  |

\* P. Chandna, H. Cuesta, D. Petermann, and E. Gómez, “A Deep-Learning Based Framework for Source Separation, Analysis, and Synthesis of Choral Ensembles,” Front. Signal Process., vol. 2, p. 808594, Apr. 2022, doi: 10.3389/frsip.2022.808594.
