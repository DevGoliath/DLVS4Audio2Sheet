# Steps to generate dataset similar to MUSDB18-HQ

* Unzip Choral Singing Dataset and ESMUC Choir Dataset to their respective directories. The path should look like this:
```
/datasets/csd/ChoralSingingDataset
/datasets/esmuc/EsmucChoirDataset_v1.0.0
```

* Install dependencies
```
pip install pydub
pip install soundfile
```
## Running the preprocessing script
* Open command line or terminal in this directory (`/datasets/`)

* Run the preprocess script
```
python preprocess_csd_and_esmuc.py
```

It should take around 5 minutes and the result should be a folder similar to MUSDB18-HQ

inside the directory '/datasets/csd/':
- processed_csd
  - test
    - Mix1
      - bass.wav
      - drums.wav
      - mixture.wav
      - other.wav
      - vocals.wav
    - Mix2
  - train
    - Mix1
    - Mix2

inside the directory '/datasets/esmuc/':
- processed_esmuc
  - test
    - Mix1
      - bass.wav
      - drums.wav
      - mixture.wav
      - other.wav
      - vocals.wav
    - Mix2
  - train
    - Mix1
    - Mix2


## Optional: modifications you can make in 'preprocess_csd_like_musdb.py' and 'preprocess_esmuc_like_musdb.py'
* If you need to generate different names, you can change get_modified_filename which exist in both python files
  * The files are grouped by voice type at this stage, so edit the **values** of the output_mapping for different filenames
  * Additionally, you will have to change to split by "\\" if you're on Windows
This section looks like this:
```
def get_modified_filename(source_filename):
    output_mapping = {
        "bass": "bass",
        "tenor": "vocals",
        "alto": "drums",
        "soprano": "other"
    }
    parts = source_filename.split('/') # need to change to '\\' for windows
    voice_type = parts[-2]
    modified_name = output_mapping[voice_type] 
    return modified_name + ".wav"
```

* If you wish to change the folder names or the input & output directories, change it accordingly in the bottom of both files. An example of the section in 'preprocess_csd_like_musdb.py' looks like this:

```
if __name__ == "__main__":
    root_dir = "./ChoralSingingDataset"
    output_dir = "./processed_csd"
    preprocess_csd_like_musdb(root_dir, output_dir)
```

`root_dir` should be the correct folder name of the ChoralSingingDataset you downloaded
`output_dir` will be where you want the preprocessed data to be output into.