from esmuc.preprocess_esmuc_like_musdb import preprocess_esmuc_like_musdb
from csd.preprocess_csd_like_musdb import preprocess_csd_like_musdb
import os
import shutil
import concurrent.futures

def combine_mixes(input_folders, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    mix_number = 1
    for folder_path in input_folders:
        for subdir, _, files in os.walk(folder_path):
            # Get the relative path from the input folder
            rel_path = os.path.relpath(subdir, folder_path)
            data_split = os.path.dirname(rel_path)

            if data_split == "":
                continue

            # Create corresponding directories in the output folder
            output_subdir = os.path.join(output_folder, data_split, f"Mix{mix_number}")
            os.makedirs(output_subdir, exist_ok=True)

            for file in files:
                if file.endswith('.wav'):
                    # Copy the mix files to the output folder
                    shutil.copy2(os.path.join(subdir, file), output_subdir)
            mix_number += 1    

def run_io_tasks_in_parallel(tasks):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        running_tasks = [executor.submit(task) for task in tasks]
        for running_task in running_tasks:
            running_task.result()
        concurrent.futures.wait(running_tasks)
        

if __name__ == "__main__":
    raw_csd_dataset = "csd/ChoralSingingDataset"
    csd_output_dir = "processed_csd"

    raw_esmuc_dataset = "esmuc/EsmucChoirDataset_v1.0.0"
    esmuc_output_dir = "processed_esmuc"

    run_io_tasks_in_parallel([
        lambda: preprocess_esmuc_like_musdb(raw_esmuc_dataset, esmuc_output_dir), 
        lambda: preprocess_csd_like_musdb(raw_csd_dataset, csd_output_dir)])

    input_folders = ['processed_esmuc', 'processed_csd']
    output_folder = 'combined_processed_dataset'

    combine_mixes(input_folders, output_folder)
    shutil.rmtree(esmuc_output_dir)
    shutil.rmtree(csd_output_dir)


