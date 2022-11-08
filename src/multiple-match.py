# Usage:
# Get the data from https://ndvr-videos.s3.us-east-2.amazonaws.com/index-videos/videos.zip (see get_data.sh script)
# Extract it in the samples_directory

import subprocess
import shlex
import os
import argparse
import pandas as pd
import re

def process_pair(directory, filename_1, filename_2):
    pair = filename_1 + ' / ' + filename_2

    f1 = os.path.join(directory, filename_1)
    f2 = os.path.join(directory, filename_2)

    ffmpeg_params = shlex.split(f'ffmpeg -i {f1} -i {f2} -filter_complex "[0:v][1:v] signature=nb_inputs=2:detectmode=full:format=binary:filename={filename_1}%d.bin" -map :v -f null -')

    ffmpeg = subprocess.Popen(ffmpeg_params,
                            stdin =subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True,
                            bufsize=0)
    
    _, stderr = ffmpeg.communicate()

    for line in stderr.split('\n'):
        if 'no matching' in line.strip():
            print(pair + ': no match')
            return ['-', '-', 0]
        elif 'frames matching' in line.strip():
            matching_data = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", line.strip().split('matching of video 0 at')[1])
            # print(matching_data)
            # print(line.strip())
            first_match = float(matching_data[0])
            second_match = float(matching_data[2])
            frames_match = int(matching_data[3])

            print(pair + ':', first_match, ',', second_match, ',', frames_match)
            return [first_match, second_match, frames_match]
    
    return ['Processs error', 'Processs error', 'Processs error'] 

        
def parse_samples(directory):
    # iterate over files in
    # that directory
    for filename_1 in os.listdir(directory):
        # checking if it is a file
        if os.path.isfile(filename_1):
            for filename_2 in os.listdir(directory):
                if os.path.isfile(filename_2) and filename_2 != filename_1:
                    process_pair(directory, filename_1, filename_2)

def parse_annotations(samples_directory, annotations_directory):

    for filename in os.listdir(annotations_directory):
        annotations_file = os.path.join(annotations_directory, filename)
        matches_df = pd.DataFrame(columns=['VideoA', 'VideoB', 'Start-A', 'Start-B', 'Frames'])
        # checking if it is a file
        if os.path.isfile(annotations_file):
            print('Annotations found in: ', annotations_file)
            annotations_df = pd.read_csv(annotations_file, header=None)

            print(annotations_df)
            for filename_1 in annotations_df[0].unique():
                for filename_2 in annotations_df[1][annotations_df[0]==filename_1].unique():
                    
                    matches_df.loc[len(matches_df.index)] = [filename_1, filename_2] + process_pair(samples_directory, filename_1, filename_2)
                    print(matches_df)
                    matches_df.to_csv(filename.replace('txt','csv'))

                  
                  

parser = argparse.ArgumentParser()
parser.add_argument('samples')
parser.add_argument('--annotations')

args = parser.parse_args()

samples_directory = args.samples

if args.annotations:
    annotations_directory = args.annotations
    parse_annotations(samples_directory, annotations_directory)

else:
    parse_samples(samples_directory)

