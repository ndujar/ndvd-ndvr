# Usage:
# Get the data from https://ndvr-videos.s3.us-east-2.amazonaws.com/index-videos/videos.zip (see get_data.sh script)
# Extract it in the samples_directory

import subprocess
import shlex
import os
import argparse
import pandas as pd
from typing import NamedTuple
import json
import timeit

class FFProbeResult(NamedTuple):
    return_code: int
    json: str
    error: str


def get_video_data(file_path) -> FFProbeResult:
    command_array = ["ffprobe",
                     "-v", "quiet",
                     "-print_format", "json",
                     "-show_format",
                     "-show_streams",
                     file_path]
    result = subprocess.run(command_array, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    return FFProbeResult(return_code=result.returncode,
                         json=result.stdout,
                         error=result.stderr)
        
def parse_samples(directory, output_directory):

    process_df = pd.DataFrame(columns=['Title', 'duration', 'width', 'height', 'fps', 'process_time', 'file_size'])
    for filename in os.listdir(directory):
        f1 = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f1):
            try:

                start_time = timeit.default_timer()
                ffmpeg_params = shlex.split(f'ffmpeg -i {f1} -vf signature=filename={output_directory}/{filename}.bin -map 0:v -f null -')
                ffmpeg = subprocess.Popen(ffmpeg_params,
                                            stdin =subprocess.PIPE,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            universal_newlines=True,
                                            bufsize=0)
                stop = timeit.default_timer()
                execution_time = stop - start_time  # It returns time in seconds

                video_data = get_video_data(f1)

                file_size = os.path.getsize(f'{output_directory}/{filename}.bin')
                d = json.loads(video_data.json)
                for stream in d['streams']:
                    if stream['codec_type'] == 'video':
                        duration = d['format']['duration']
                        width = stream['coded_width']
                        height = stream['coded_height']
                        fps = float(stream['avg_frame_rate'].split('/')[0]) / float(stream['avg_frame_rate'].split('/')[1])
                        break
            
                process_df.loc[len(process_df.index)] = [filename, duration, width, height, fps, execution_time, file_size]
                print(process_df)
                process_df.to_csv('process.csv')

            except Exception as e:
                print('Unable to extract', f1, e)     
                print(d)           
            
          
                  

parser = argparse.ArgumentParser()
parser.add_argument('samples')
parser.add_argument('output_dir')

args = parser.parse_args()

samples_directory = args.samples
output_directory = args.output_dir


parse_samples(samples_directory, output_directory)
