# Adapting Band-Split Recurrent Neural Network (BSRNN) for the Task of Vocal Singing Separation

## General Notes
1. Remember that the directory paths in this readme are relative to the directory our team used during development. Please adjust them accordingly to your own directory.

2. Since the original paper was developed for general Musical Source Separation (separating 4 stems: vocals, bass, drums, other). Hence, we renamed our choir datasets to follow this 4 stems configuration for training convenience. Here is the mapping used:
   ```sh
    output_mapping = {
        "bass": "bass",
        "tenor": "vocals",
        "alto": "drums",
        "soprano": "other"
    }

3. For example, if we are separating the audio 'csd_esmuc_mix1' and the inference outputs 'csd_esmuc_mix1_drums' it means that it is separating out 'alto'. We have prepared the python script in ```bsrnn_inference_output\rename_wav_files.py``` that would rename the inference outputs back to Choir Songs' context.

# Getting Started

## Setting up virtual environment

1. Create virtual environment     
   ```sh
   python3 -m venv venv-BSRNN-3.10
   
2. Activate virtual environment  
   ```sh
   (for Bash):
   source venv-BSRNN-3.10/bin/activate
   cd src
   
3. Install modules in requirements.txt     
   ```sh
   pip install -r requirements.txt

4. Install ffmpeg
    ```sh
    conda install -c conda-forge ffmpeg

## After initial setup is done

1. Activate virtual environment
   ```sh
   (for Bash):
   cd Music-Demixing-with-Band-Split-RNN
   source venv-BSRNN-3.10/bin/activate
   cd src

2. Install any changes in requirements.txt (if necessary)
   ```sh
   pip install -r requirements.txt

3. Set Environment Variables
   ```sh
    export CUDA_VISIBLE_DEVICES=1
    export MUSDB_DIR="/DLVS4Audio2Sheet/datasets/combined_processed_dataset_converted_stereo" # change accordingly to where your dataset folder 'combined_processed_dataset_converted_stereo' is located in
    export WANDB_API_KEY="efec9d4452e32a791be2b6c0c7a59bb74c66f9ee" # or change to your own wandb API key

# Training the Model

If you do not want to train from scratch, we have saved the trained checkpoints in ```bsrnn_saved_models``` so you can skip Step 1-3 and go straight to Step 4: Inference.

1. Preprocess the datasets
   ```sh
   python3 prepare_dataset.py -i /DLVS4Audio2Sheet/datasets/combined_processed_dataset_converted_stereo -o /DLVS4Audio2Sheet/models/Music-Demixing-with-Band-Split-RNN/bsrnn_preprocessed_dataset/preprocessed_production_csd_esmuc -t bass drums vocals other
   ```
   ```sh
   python3 prepare_dataset.py -i /DLVS4Audio2Sheet/datasets/combined_processed_dataset_converted_stereo -o /DLVS4Audio2Sheet/models/Music-Demixing-with-Band-Split-RNN/bsrnn_preprocessed_dataset/preprocessed_production_csd_esmuc --subset test -t bass drums vocals other
   ```
   ```
   python3 prepare_dataset.py -i /DLVS4Audio2Sheet/datasets/combined_processed_dataset_converted_stereo -o /DLVS4Audio2Sheet/models/Music-Demixing-with-Band-Split-RNN/bsrnn_preprocessed_dataset/preprocessed_production_csd_esmuc --split valid -t bass drums vocals other
   ```
   ```
   options:
    -h, --help            show this help message and exit
    -i INPUT_DIR, --input_dir INPUT_DIR
                          Path to directory with musdb18 dataset
    -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                          Path to directory where output .txt file is saved
    --subset SUBSET       Train/test subset of the dataset to process
    --split SPLIT         Train/valid split of train dataset. Used if subset=train
    --sad_cfg SAD_CFG     Path to Source Activity Detection config file
    -t TARGET [TARGET ...], --target TARGET [TARGET ...]
                          Target source. SAD will save salient fragments of vocal audio.
   ```

2. Check your output directory above (argument '-o') and move the .txt files to /DLVS4Audio2Sheet/models/Music-Demixing-with-Band-Split-RNN/src/files

3. Run the training commands below (each choir stem has to be trained individually). Note that the training process for each choir stem takes a very long time.
   ```sh
   python /DLVS4Audio2Sheet/models/Music-Demixing-with-Band-Split-RNN/src/train.py
   ```
   ```sh
   python /DLVS4Audio2Sheet/models/Music-Demixing-with-Band-Split-RNN/src/train.py train_dataset.target=bass model=bandsplitrnnbass
   ```
   ```sh
   python /DLVS4Audio2Sheet/models/Music-Demixing-with-Band-Split-RNN/src/train.py train_dataset.target=drums model=bandsplitrnndrums
   ```
   ```sh
   python /DLVS4Audio2Sheet/models/Music-Demixing-with-Band-Split-RNN/src/train.py train_dataset.target=other


4. Inference (Inference script has to be run for each individual choir stem. The sample codes below assume you are using our trained checkpoints in ```bsrnn_saved_models``` to infer csd_esmuc_mix1.wav)
   ```sh
   python3 inference.py -i /DLVS4Audio2Sheet/models/Music-Demixing-with-Band-Split-RNN/bsrnn_inference_output/csd_esmuc_mix1.wav -o /DLVS4Audio2Sheet/models/Music-Demixing-with-Band-Split-RNN/bsrnn_inference_output/inference_production_csd_esmuc/ -t vocals -c /DLVS4Audio2Sheet/models/Music-Demixing-with-Band-Split-RNN/bsrnn_saved_models/trained_on_production_csd_esmuc/vocals/weights/epoch53-train_loss0.33.ckpt -d cuda
   ```
   ```sh
   python3 inference.py -i /DLVS4Audio2Sheet/models/Music-Demixing-with-Band-Split-RNN/bsrnn_inference_output/csd_esmuc_mix1.wav -o /DLVS4Audio2Sheet/models/Music-Demixing-with-Band-Split-RNN/bsrnn_inference_output/inference_production_csd_esmuc/ -t bass -c /DLVS4Audio2Sheet/models/Music-Demixing-with-Band-Split-RNN/bsrnn_saved_models/trained_on_production_csd_esmuc/bass/weights/epoch49-train_loss0.35.ckpt -d cuda
   ```
   ```sh
   python3 inference.py -i /DLVS4Audio2Sheet/models/Music-Demixing-with-Band-Split-RNN/bsrnn_inference_output/csd_esmuc_mix1.wav -o /DLVS4Audio2Sheet/models/Music-Demixing-with-Band-Split-RNN/bsrnn_inference_output/inference_production_csd_esmuc/ -t drums -c /DLVS4Audio2Sheet/models/Music-Demixing-with-Band-Split-RNN/bsrnn_saved_models/trained_on_production_csd_esmuc/drums/weights/epoch19-train_loss0.35.ckpt -d cuda
   ```
   ```sh
   python3 inference.py -i /DLVS4Audio2Sheet/models/Music-Demixing-with-Band-Split-RNN/bsrnn_inference_output/csd_esmuc_mix1.wav -o /DLVS4Audio2Sheet/models/Music-Demixing-with-Band-Split-RNN/bsrnn_inference_output/inference_production_csd_esmuc/ -t other -c /DLVS4Audio2Sheet/models/Music-Demixing-with-Band-Split-RNN/bsrnn_saved_models/trained_on_production_csd_esmuc/other/weights/epoch47-train_loss0.27.ckpt -d cuda
   ```
   ```
   options:
    -h, --help            show this help message and exit
    -i IN_PATH, --in-path IN_PATH
                          Path to the input directory/file with .wav/.mp3 extensions.
    -o OUT_PATH, --out-path OUT_PATH
                          Path to the output directory. Files will be saved in .wav format with sr=44100.
    -t TARGET, --target TARGET
                          Name of the target source to extract.
    -c CKPT_PATH, --ckpt-path CKPT_PATH
                          Path to model's checkpoint. If not specified, the .ckpt from SAVED_MODELS_DIR/{target} is used.
    -d DEVICE, --device DEVICE
                          Device name - either 'cuda', or 'cpu'.
    ```

5. Evaluation to get SDR scores (Evaluation script has to be run for each individual choir stem. The sample codes below assume you are using our trained checkpoints)
   ```sh
   python3 evaluate.py -d /DLVS4Audio2Sheet/models/Music-Demixing-with-Band-Split-RNN/bsrnn_saved_models/trained_on_production_csd_esmuc/vocals --device cuda --ckpt epoch53-train_loss0.33.ckpt
   ```
   ```sh
   python3 evaluate.py -d /DLVS4Audio2Sheet/models/Music-Demixing-with-Band-Split-RNN/bsrnn_saved_models/trained_on_production_csd_esmuc/bass --device cuda --ckpt epoch49-train_loss0.35.ckpt
   ```
   ```sh
   python3 evaluate.py -d /DLVS4Audio2Sheet/models/Music-Demixing-with-Band-Split-RNN/bsrnn_saved_models/trained_on_production_csd_esmuc/drums --device cuda --ckpt epoch19-train_loss0.35.ckpt
   ```
   ```sh
   python3 evaluate.py -d /DLVS4Audio2Sheet/models/Music-Demixing-with-Band-Split-RNN/bsrnn_saved_models/trained_on_production_csd_esmuc/other --device cuda --ckpt epoch47-train_loss0.27.ckpt
   ```
   ```
   options:
    -h, --help            show this help message and exit
    -d RUN_DIR, --run-dir RUN_DIR
                          Path to directory checkpoints, configs, etc
    --device DEVICE       Device name - either 'cuda', or 'cpu'.
    --ckpt                the checkpoint .ckpt file name you want to use

# Our Results and Discussions

## Notable Changes from the Original Model
Hyperparameter Adjustments
- Batch Size: Decreased from 8 to 4 due to GPU limitations
- Epochs: Significantly reduced from 100-500 to 30-50 due to the 24-hour time limit and decreased batch size
- SAD Time Split Window: Increased from 6 to 8 seconds to capture individual voices more effectively.
- Audio Channel: Mono audios (if applicable), were converted to Stereo

These changes were made to adapt BSRNN to the specific characteristics of SATB choir songs and also enhance the model's performance given the constraints on our team's access to computing resources.

## SDR Results
Our BSRNN model achieved the following Source-to-Distortion Ratio (SDR) results:
|        | Soprano |  Alto |  Tenor |  Bass | Average |
|--------|---------|-------|--------|-------|---------|
| SOTA*  |   1.67  | 10.70 |  -7.13 |  7.42 |   2.88  |
| BSRNN  |   2.16  |  3.12 |   2.86 |  3.21 |   2.84  |

\* P. Chandna, H. Cuesta, D. Petermann, and E. Gómez, “A Deep-Learning Based Framework for Source Separation, Analysis, and Synthesis of Choral Ensembles,” Front. Signal Process., vol. 2, p. 808594, Apr. 2022, doi: 10.3389/frsip.2022.808594.

## Results Analysis
Our BSRNN performed well, with the average SDR coming very close to the SOTA results. It outperforms the SOTA results for Soprano and Tenor. Tenor is a choir part that is notoriously difficult to separate, as seen from the negative SDR score even among the best SOTA models. 

This success is possibly explained by BSRNN’s unique component of band-split (or frequency-split) configurations. This component suits separating Choir Music very well since the main differentiating factors between the 4 choir parts are mainly frequencies (as opposed to, for example, separating vocals from drums in the original Musical Source Separation). Thus, it allows BSRNN to work across the board, as seen by how relatively close the individual choir part’s results are to the average results. 

We believe that BSRNN can perform much better and come on top for the average score, provided that we have access to greater computing power and a longer time limit, since we had to significantly cut down on our batch size and epoch.

## Final Words
Feel free to explore and experiment with the codebase to further improve the model's capabilities. If you encounter any issues or have suggestions, please don't hesitate to reach out or open an issue.