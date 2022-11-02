# Usage:
# Get the data from https://ndvr-videos.s3.us-east-2.amazonaws.com/index-videos/videos.zip (see get_data.sh script)
# Extract it in the samples_directory

import subprocess
import shlex
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('samples_directory')

args = parser.parse_args()

directory = args.samples_directory #'index-videos'
 
# iterate over files in
# that directory
for filename in os.listdir(directory):
    f1 = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f1):
        print('File 1:', f1)
        for filename in os.listdir(directory):
            f2 = os.path.join(directory, filename)
            if os.path.isfile(f2) and f2.split('.')[1] == f1.split('.')[1] and f2 != f1:
                print('File 2:', f2)

                ffmpeg_params = shlex.split(f'ffmpeg -i {f1} -i {f2} -filter_complex "[0:v][1:v] signature=nb_inputs=2:detectmode=full:format=xml:filename={filename}%d.xml" -map :v -f null -')

                ffmpeg = subprocess.Popen(ffmpeg_params,
                                        stdin =subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        universal_newlines=True,
                                        bufsize=0)
                
                stdout, stderr = ffmpeg.communicate()
                processed = False
                for line in stderr.split('\n'):
                    if 'Parsed_signature' in line.strip():
                        print(line.strip())
                        processed = True
                    elif 'matching' in line.strip():
                        print(line.strip())
                        processed = True
                if not processed:
                    print('There was an error')
                    print(stderr)                    
                    print(stdout)