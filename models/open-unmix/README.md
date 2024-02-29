This folder contains the Choral Voice Separation implementation of [Open-Unmix](https://github.com/sigsep/open-unmix-pytorch). To get started, refer to the original [README](OPEN_UNMIX_README.md) file provided by the sigsep team.

## Training
To train the model, follow the original Open-Unmix training details in the separate document [here](docs/training.md). Alternatively, you can run the provided batch file to perform training on all four voices (Bass, Tenor, Alto, and Soprano) in one go:
```powershell
scripts/train.bat
```

### Hyperparameter Tuning
We have made several changes to the original model to better suit our needs. Notable modifications include adjustments to the number of epochs, batch size, sequence duration, and audio channel. For more details, refer to the [Notable Changes](#notable-changes-from-the-original-model) section.

## Inference
To perform inference, follow the guide [here](docs/inference.md), or run our batch file to get the estimates by running:
```powershell
scripts/get_estimates.bat
```
Additionally, you can explore inference in our [jupter notebook](inference.ipynb).

## Results
Our model achieved the following Source-to-Distortion Ratio (SDR) results:
|     | Soprano | Alto | Tenor | Bass | Average |
|-----|---------|------|-------|------|---------|
| SDR |   4.68  | 3.12 |  2.13 | 1.74 |   2.92  |

### Notable Changes from the Original Model
Hyperparameter Adjustments
- Epochs: Increased from variable to a fixed value of 200 for improved convergence.
- Batch Size: Increased from 16 to 64 for faster training.
- Sequence Duration: Extended from 6 to 8 seconds to capture individual voices more effectively.
- Audio Channel: Changed from stereo to mono to align with the single-channel nature of our dataset.
These changes were made to enhance the model's performance and adapt it to the specific characteristics of choir tracks.

Feel free to explore and experiment with the codebase to further improve the model's capabilities. If you encounter any issues or have suggestions, please don't hesitate to reach out or open an issue.