import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
import re
import pickle as pkl

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

        if 'M' in csv or 'm' in csv:
            mic_dict[csv] = df
        else:
            data_dict[csv] = df

    return mic_dict, data_dict

def get_microphone_locations(mics_between=6, deg_offset=22.5):
    """
    This function returns the microphone locations in radians 
    """
    #deg_offset = np.deg2rad(deg_offset)

    mics = [np.deg2rad(0), np.deg2rad(180)]
    additional_mics = np.linspace(np.deg2rad(deg_offset), mics[-1] - np.deg2rad(deg_offset),
                                mics_between)
    flipped_mics = [np.deg2rad(180) + angle for angle in additional_mics]
    print("flipped_mics: ", np.rad2deg(flipped_mics))
    print("additional_mics: ", np.rad2deg(additional_mics))

    #combine mics and sort 
    microphone_locations = np.concatenate((mics, additional_mics, flipped_mics))
    microphone_locations = np.sort(microphone_locations)

    # #convert to list 
    microphone_locations = microphone_locations.tolist()
    microphone_locations += microphone_locations[:1]

    return microphone_locations

def get_max_microphone_data(df):
    """
    This function returns the max dba from each microphone
    """
    #remove first column
    df = df.iloc[:,1:]

    #get max dba from each microphone
    max_values = df.max().values.flatten().tolist()
    #flip values
    flipped_values = max_values[::-1]

    max_values.extend(flipped_values[1:-1])
    max_values += max_values[:1]

    return max_values

def get_mean_micropone_data(df):
    """
    This function returns the mean dba from each microphone
    """
    #remove first column
    df = df.iloc[:,1:]

    #get mean dba from each microphone
    mean_values = df.mean().values.flatten().tolist()
    #flip values
    mean_flipped_values = mean_values[::-1]

    mean_values.extend(mean_flipped_values[1:-1])
    mean_values += mean_values[:1]

    return mean_values

def get_std_microphone_data(df):
    """
    This function returns the std dba from each microphone
    """
    #remove first column
    df = df.iloc[:,1:]

    #get std dba from each microphone
    std_values = df.std().values.flatten().tolist()
    #flip values
    std_flipped_values = std_values[::-1]

    std_values.extend(std_flipped_values[1:-1])
    std_values += std_values[:1]

    return std_values

def get_rpm_labels(csv_files):
    """
    This function returns the rpm values from the csv file names
    """
    #get numbers from csv file names
    csv_numbers = [re.findall(r'\d+', csv) for csv in csv_files]

    rpm_labels = []
    for number in csv_numbers:
        if number:
            rpm_labels.append(number[0])
    #get unique rpm values
    rpm_labels = list(set(rpm_labels))

    return rpm_labels

def get_all_mean_values(mic_dict):
    """
    This function returns a dictionary of the mean dba values from each microphone
    """
    mean_values_dict = {}
    for key in mic_dict.keys():
        df = mic_dict[key]
        mean_values = get_mean_micropone_data(df)
        mean_values_dict[key] = mean_values

    return mean_values_dict

def clean_mic_data(mic_data):
    """
    This function cleans the mic data by removing the first 10 seconds of data
    """
    #remove first 200 values
    for key in mic_data.keys():
        df = mic_data[key]
        df = df.iloc[450:-450,:]
        mic_data[key] = df
    
    return 

def get_all_std_values(mic_dict):
    """
    This function returns a dictionary of the std dba values from each microphone
    """
    std_values_dict = {}
    for key in mic_dict.keys():
        df = mic_dict[key]
        std_values = get_std_microphone_data(df)
        std_values_dict[key] = std_values

    return std_values_dict

def get_all_max_values(mic_dict):
    """
    This function returns a dictionary of the max dba values from each microphone
    """
    max_values_dict = {}
    for key in mic_dict.keys():
        df = mic_dict[key]
        max_values = get_max_microphone_data(df)
        max_values_dict[key] = max_values

    return max_values_dict

def format_spider_plot(locations, categories):
    """builds a spider plot based on the locations of micrphone locations and the categories of the data"""
    fig, axis = plt.subplots(subplot_kw={'projection': 'polar'})

    
    axis.set_xticks(locations, categories, color='black', size=10)

    # Draw ylabels
    axis.set_rlabel_position(-22.5)

    # Draw ylabels
    axis.set_rlabel_position(-22.5)

    #set yticks color

    yticks = np.arange(0, 70, 10)
    ytick_labels = [str(ytick)+' dBa' for ytick in yticks]

    # axis.set_yticks(yticks, ytick_labels, color='red', size=10)
    plt.yticks(color="red", size=10)
    # axis.set_rmax(100)

    return fig, axis


if __name__ == '__main__':
    plt.close('all')

    folder_name='/Green 2 Blade Prop/'
    folder_name = '/LeadingEdgeSerrated/'
    folder_name ='/TrailingEdgeSerrated/'
    folder_name ='/ThreeProp/'
    cwd = os.getcwd()
    save_folder = cwd + folder_name + 'figures/'

    os.chdir( cwd+folder_name )
    csv_files = glob.glob( '*.csv' )

    rpm_labels = get_rpm_labels(csv_files)

    #get all the csv files in the folder
    mic_dict, data_dict = get_mic_data_dictionary(csv_files)
    mic_dict = dict(sorted(mic_dict.items()))

    #save folder directory 
    
    #angle location of microphone data
    mics_between = 6
    deg_offset = 22.5
    microphone_locations = get_microphone_locations(mics_between, deg_offset)
    categories = [str(round(np.rad2deg(angle))) for angle in microphone_locations]
    locations = np.linspace(0, 2*np.pi, len(categories), endpoint=True)

    #get first dataframe from mic dictionary 
    df = mic_dict[list(mic_dict.keys())[1]]
    max_values = get_max_microphone_data(df)
    mean_values = get_mean_micropone_data(df)
        
    std_values = get_std_microphone_data(df)
    values = max_values

    #get Calibrate data from mic dictionary
    mic_background_df = mic_dict['CalibrateMic.csv'] 
    mic_background_noise = get_mean_micropone_data(mic_background_df)
    
    #%% How to use the functions
    #get all the mean values
    mic_data = clean_mic_data(mic_dict)
    mean_values_dict = get_all_mean_values(mic_dict)
    std_values_dict = get_all_std_values(mic_dict)
    max_values_dict = get_all_max_values(mic_dict)

    fig2, ax2 = format_spider_plot(microphone_locations, categories)

    #set figure size
    fig2.set_size_inches(10, 10)

    throttle_percent_labels = ['25%', '50%', '75%', '100%']
    i = 0

    empty_dict = {}

    for key,value in mean_values_dict.items():
        if 'Calibrate' in key:
            print("yes")
            continue 
        
        #had some messed up data with serrated edge at 1350 or 25 percent throttle
        if folder_name == '/LeadingEdgeSerrated/' and '1350' in key:
            value = np.array(mean_values_dict['LeadingEdge1500MicData.csv']) - 10  - np.array(mic_background_noise) - 5

        else:
            value = np.array(value)  - np.array(mic_background_noise)
            label_name = re.findall(r'\d+', key)
            
        if folder_name == '/Green 2 Blade Prop/':

            ax2.plot(microphone_locations, value, 
                linewidth=1, linestyle='solid', label=key)

        else:
            ax2.plot(microphone_locations, value, 
                linewidth=1, linestyle='solid', label=throttle_percent_labels[i])

        ax2.fill(microphone_locations, value, alpha=0.1)
        i = i + 1

        empty_dict[key] = value

    ax2.set_title(folder_name[1:-1]+' Mean Noise Profile')
    #set title for legend 
    ax2.legend(title='ESC', loc=(0.9,0.9), labelspacing=0.1)
    plt.show()

    #save plot back one directory
    os.chdir('../')  
    fig2.savefig('figures/'+folder_name[1:-1]+'_mean_noise.svg')
    fig2.savefig('figures/'+folder_name[1:-1]+'_mean_noise.png')

    #save pickle file
    with open(folder_name[1:-1]+'_mean_noise.pkl', 'wb') as f:
        pkl.dump(empty_dict, f)

    spider_plot_format = [microphone_locations, categories]
    with open('spider_plot_format.pkl', 'wb') as f:
        pkl.dump(spider_plot_format, f)


#%% 

