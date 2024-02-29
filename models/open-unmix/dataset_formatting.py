import os

directory = '../dataset/processed_csd'
output_mapping = {
    "bass": "bass",
    "vocals": "tenor",
    "drums": "alto",
    "other": "soprano"
}

for split in os.listdir(directory):
    mixes = os.path.join(directory, split)
    for mix in os.listdir(mixes):
        tracks = os.path.join(mixes, mix)
        for track in os.listdir(tracks):
            file = os.path.join(tracks, track)
            
            if track != 'mixture.wav':
                # print(os.path.join(tracks, track[7:-6] + '.wav'))

                # transform bass_1.wav to bass.wav
                os.rename(file, os.path.join(tracks, output_mapping[track[:-4]] + '.wav'))