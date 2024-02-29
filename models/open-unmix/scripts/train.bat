@echo off
:: Enable ANSI escape codes
ansicon

:: Define ANSI escape codes for red text and reset color
set RED_TEXT="\033[91m"
set RESET_COLOR="\033[0m"

:: List of voice parts
set "voice_parts=soprano alto tenor bass"

:: Iterate over each voice part and execute the common script
for %%v in (%voice_parts%) do (
    echo %RED_TEXT%Training %%v...%RESET_COLOR%
    python train.py --dataset aligned --root ../../dataset/combined_processed_dataset --output ../saved_models/final --input-file mixture.wav --output-file %%v.wav --seq-dur 8 --epochs 200 --batch-size 64 --audio-backend soundfile --nb-channels 1
)
