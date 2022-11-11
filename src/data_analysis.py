import argparse
import pandas as pd
import os

def analyze(data_directory):

    data_df = pd.DataFrame(columns=['VideoA', 'VideoB', 'Start-A', 'Start-B', 'Frames'])
    for filename in os.listdir(data_directory):
        matches_filename = os.path.join(data_directory, filename)

        # checking if it is a file
        if os.path.isfile(matches_filename) and '.csv' in matches_filename:
            matches_df = pd.read_csv(matches_filename, index_col='Unnamed: 0')
            
            data_df = pd.concat([data_df, matches_df], axis=0, ignore_index=True)
    
    unprocessed_data_df = data_df[data_df['Frames'] == 'Processs error']
    FN_data_df = data_df[data_df['Frames'] == '0']
    print(unprocessed_data_df)
    print(len(FN_data_df['VideoA'].unique()))
    print(len(FN_data_df['VideoB'].unique()))

parser = argparse.ArgumentParser()
parser.add_argument('data')
parser.add_argument('--annotations')

args = parser.parse_args()

data_directory = args.data

analyze(data_directory)