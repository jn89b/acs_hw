import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import glob

"""
Acoustic plot with angles on outside 
axis is the dbA from the mic data

Plot spider as max dba from each mic
Plot spider as average dba from each mic with std
"""


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

        if 'M' in csv:
            mic_dict[csv] = df
        else:
            data_dict[csv] = df

    return mic_dict, data_dict


if __name__ == '__main__':
    plt.close('all')

    folder_name = '/mic_acs_data/'
    cwd = os.getcwd()

    os.chdir( cwd+folder_name )
    csv_files = glob.glob( '*.csv' )

    #get all the csv files in the folder
    mic_dict, data_dict = get_mic_data_dictionary(csv_files)

    #angle location of microphone data
    mics_between = 6
    deg_offset = np.deg2rad(22.5)

    mics = [np.deg2rad(0), np.deg2rad(180)]
    additional_mics = np.linspace(deg_offset, mics[-1] - deg_offset, mics_between)
    flipped_mics = [np.deg2rad(180) + angle for angle in additional_mics]

    #combine mics and sort 
    microphone_locations = np.concatenate((mics, additional_mics, flipped_mics))
    microphone_locations = np.sort(microphone_locations)
    
    #convert to list 
    microphone_locations = microphone_locations.tolist()
    microphone_locations += microphone_locations[:1]

    #get first dataframe from mic dictionary 
    df = mic_dict[ list(mic_dict.keys())[0] ]
    #remove first column
    df = df.iloc[:,1:]

    #first row of dataframe
    values = df.iloc[0].values.flatten().tolist()
    
    #flip values
    flipped_values = values[::-1]

    values.extend(flipped_values[1:-1])
    values += values[:1]

    #initialize spider plot
    ax = plt.subplot(111, polar=True)    

    #draw one axe per variable + add labels
    categories = [str(round(np.rad2deg(angle))) for angle in microphone_locations]
    plt.xticks(microphone_locations, categories, color='grey', size=8)

    # Draw ylabels
    ax.set_rlabel_position(-22.5)

    #set yticks color 
    plt.yticks(color="grey", size=7)
    ax.set_rmax(100)

    # Plot data
    ax.plot(microphone_locations, values, 
        linewidth=1, linestyle='solid', label='Test')
    
    # Fill area
    ax.fill(microphone_locations, values, 'b', alpha=0.1)

    #set label for plots
    ax.set_title('Noise Profile')
    ax.legend(loc=(0.9,0.9), labelspacing=0.1)