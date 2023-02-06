import pandas as pd
import os 
import glob

def get_mic_data_dictionary( csv_file_dir):
    """
    This function takes in a list of csv files and returns a dictionary of the data
    as a dataframe. The dictionary is keyed by the csv file name.
    """

    mic_dict = {}
    data_dict = {}
    for csv in csv_file_dir:
        #read the csv file
        df = pd.read_csv(csv)

        if 'M' in csv or 'm' in csv:
            mic_dict[csv] = df
        else:
            data_dict[csv] = df

    return mic_dict, data_dict


def get_csv_files(folder_name):
    cwd = os.getcwd()
    os.chdir( cwd+folder_name)
    csv_files = glob.glob( '*.csv' )

    return csv_files