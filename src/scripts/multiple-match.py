# Usage:
# Get the data from https://ndvr-videos.s3.us-east-2.amazonaws.com/index-videos/videos.zip (see get_data.sh script)
# Extract it in the samples_directory

import subprocess
import shlex
import os
import argparse
import pandas as pd
import re
import time

def process_pair(directory, filename_1, filename_2, th_xh):
    pair = filename_1 + ' / ' + filename_2

    f1 = os.path.join(directory, filename_1)
    f2 = os.path.join(directory, filename_2)

    import time
    start_time = time.time()

    ffmpeg_params = shlex.split(f'ffmpeg -i {f1} -i {f2} -filter_complex "[0:v][1:v] signature=nb_inputs=2:detectmode=full:th_xh={th_xh}:format=binary:filename={filename_1}%d.bin" -map :v -f null -')

    ffmpeg = subprocess.Popen(ffmpeg_params,
                            stdin =subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True,
                            bufsize=0)


    _, stderr = ffmpeg.communicate()
    execution_time = time.time() - start_time  # It returns time in seconds

    for line in stderr.split('\n'):
        if 'no matching' in line.strip():
            print(pair + ': no match')
            return ['-', '-', 0, execution_time]
        elif 'frames matching' in line.strip():
            matching_data = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", line.strip().split('matching of video 0 at')[1])

            first_match = float(matching_data[0])
            second_match = float(matching_data[2])
            frames_match = int(matching_data[3])

            print(pair + ':', first_match, ',', second_match, ',', frames_match)
            return [first_match, second_match, frames_match, execution_time]
    
    return ['Process error', 'Process error', 'Process error', execution_time] 

        
def parse_samples(directory, th_xh=116):
    # iterate over files in
    # that directory
    for filename_1 in os.listdir(directory):
        # checking if it is a file
        if os.path.isfile(filename_1):
            for filename_2 in os.listdir(directory):
                if os.path.isfile(filename_2) and filename_2 != filename_1:
                    process_pair(directory, filename_1, filename_2, th_xh)


def process_annotations(samples_directory, annotations_df, max_pairs, th_xh):

    matches_df = pd.DataFrame(columns=['VideoA', 'VideoB', 'Start-A', 'Start-B', 'Frames', 'Time'])
    for filename_1 in annotations_df[0].unique():
        for filename_2 in annotations_df[1][annotations_df[0]==filename_1].unique():
            process_data = process_pair(samples_directory, filename_1, filename_2, th_xh)
            
            if  'Process error' in process_data:
                print('FFmpeg process error, flipping input videos to see if it fixes:')
                process_data = process_pair(samples_directory, filename_2, filename_1, th_xh)

            matches_df.loc[len(matches_df.index)] = [filename_1, filename_2] + process_data
            print(matches_df)
            if (max_pairs > 0 and len(matches_df.index) >= max_pairs):
                print('Maximum number of pairs compared, exiting now')
                return matches_df
    return matches_df

def parse_annotations(samples_directory, annotations_directory, max_pairs=0, th_xh=116):

    for filename in os.listdir(annotations_directory):
        annotations_file = os.path.join(annotations_directory, filename)
        
        # checking if it is a file
        if os.path.isfile(annotations_file):
            print('Annotations found in: ', annotations_file)
            annotations_df = pd.read_csv(annotations_file, header=None)

            matches_df = process_annotations(samples_directory, annotations_df, max_pairs, th_xh)
            print('Dataframe:', matches_df, filename)
            print('Saving dataframe to ', filename)
            matches_df.to_csv(filename.replace('txt','csv'))


parser = argparse.ArgumentParser()
parser.add_argument('samples')
parser.add_argument('--annotations')
parser.add_argument('--max_pairs')
parser.add_argument('--th_xh')

args = parser.parse_args()

samples_directory = args.samples

if args.annotations:
    annotations_directory = args.annotations
    parse_annotations(samples_directory, annotations_directory, int(args.max_pairs), int(args.th_xh))

else:
    parse_samples(samples_directory, int(args.th_xh))

