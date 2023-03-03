"""
1: Calculate the analytical/theoretical RCS for the calibration sphere used in class (Diameter = 
25cm). Using another group’s calibration sphere data (Note: must use the same step size), 
create a table that has the received power (S21,std) for the eight orientations. 

2: Using the standard/calibration data from Problem 1 and the estimated RCS for the sphere, 
use your collected sphere data to create a polar plot of the RCS (of the sphere). How do 
your results match/compare to the theory? Example shown below. 

3: Using the VNA data collected from the baseline Skywalker X8 vehicle. Estimate the RCS 
polar plot (identical to Problem 2) for the Skywalker. What do you notice regarding the 
aircraft RCS?  
 
"""

import numpy as np
import pandas as pd
import os 
import glob 
import matplotlib.pyplot as plt
import seaborn as sns

def get_data_as_dict(csv_file_dir) -> dict:
    """
    returns a dictionary of all the csv information available
    """
    data_dict = {}
    
    for csv in csv_file_dir:
        if 'mean' in csv or 'std' in csv:
            continue
        
        df = pd.read_csv(csv)
        data_dict[csv] = df

    return data_dict

def convert_linear_vna_to_dbm(linear_vna_data):
    return 10*np.log10(linear_vna_data)

def compute_rcs_angle(sigma_theory_sphere, 
                      group_1_data,
                      group_2_data):
    
    return sigma_theory_sphere*10**((group_1_data - group_2_data)/10)

def get_mean_std_dbm_dict(data_dict:dict):
    """returns two dicionaries mean and std of dbm information"""
    mean_std_dict = {}
    for key, df in data_dict.items():
        df.dropna()
        #drop the first column
        df = df.iloc[:, 1:]
        mean_df = df.apply(lambda x: np.mean(convert_linear_vna_to_dbm(x)))
        std_df = df.apply(lambda x: np.std(convert_linear_vna_to_dbm(x)))
        
        #combine the two dataframes
        new_df = pd.concat([mean_df, std_df], axis=1)
        new_df.columns = ['mean', 'std']
        mean_std_dict[key] = new_df
        
    return mean_std_dict


def write_df_to_csv(df, extension_name, folder_dir):
    
    #check if file exists
    if os.path.exists(folder_dir+extension_name+'.csv'):
        print('file already exists')
        return
    else:
        df.to_csv(folder_dir+extension_name+'.csv')
        print('file saved to: ', folder_dir+extension_name+'.csv')
        return 

def format_spider_plot(locations,categories):
    fig, axis = plt.subplots(subplot_kw={'projection': 'polar'})
    axis.set_xticks(locations, categories, color='black', size=10)
    
    return fig,axis


if __name__ == '__main__':
    
    folder_name = '/radar_data/'
    cwd = os.getcwd()
    os.chdir(cwd+folder_name)
    csv_files = glob.glob('*.csv')
    data_dict = get_data_as_dict(csv_files)
    
    #sphere thereotical equation
    #sigma_sphere_theory = lambda r: np.pi * r**2
    r_sphere = 0.125 #meters
    sigma_sphere_theory =  np.pi * r_sphere**2

    mean_std_dict = get_mean_std_dbm_dict(data_dict)
    
    
    for key, df in mean_std_dict.items():
        #strip the .csv from the key
        file_name = key.split('.')[0]
        write_df_to_csv(df, file_name+'_mean_std', cwd+folder_name)
        
    #%% Format spider plots
    
    group_1 = None
    group_2 = None
    uav_info = None
    for (key, df), color in zip(mean_std_dict.items(), ['r', 'b', 'g', 'y']):
        #strip the .csv from the key

        
        file_name = key.split('.')[0]
        print("file name: ", file_name)
        df.dropna()

        if 'Drone' in key:
            print("theres a drone in my boot", key)
            uav_info = df 
            continue
        if 'skywalker' in key:
            print("theres a skywalker in my boot", key)
            continue

        if group_1 is None:
            group_1 = df
            continue
        
        if group_2 is None:
            group_2 = df
            continue
        

    mean_vna_group1 = np.array(group_1['mean'])
    mean_vn_group2 = np.array(group_2['mean'])
    mean_vn_uav = np.array(uav_info['mean'])
    sigma_target = compute_rcs_angle(sigma_sphere_theory,mean_vna_group1, mean_vn_group2)
    np.append(sigma_target, sigma_target[0])
    
    plt.close('all')
    angles = np.arange(0, 2*np.pi, np.pi/4)
    fig1, ax1 = format_spider_plot(angles, 
                                   ['0', '45', '90', '135', '180', '225', '270', '315'])

    
    ax1.plot(np.arange(0, 2*np.pi+np.pi/4, np.pi/4),
                sigma_target, color=color, label=file_name)
    #set yticks
    yticks = np.arange(0, 0.08, 0.02)
    ytick_labels = [str(ytick)+' m^2' for ytick in yticks]
    ax1.set_yticks(yticks, ytick_labels, color='red', size=6)

    #%% Plot the UAV
    uav_target = compute_rcs_angle(sigma_sphere_theory,
                                   mean_vn_uav, 
                                   mean_vn_group2)
    np.append(uav_target, uav_target[0])
    
    angles = np.arange(0, 2*np.pi, np.pi/4)
    fig2, ax2 = format_spider_plot(angles, 
                                   ['0', '45', '90', '135', '180', '225', '270', '315'])

    
    ax2.plot(np.arange(0, 2*np.pi+np.pi/4, np.pi/4),
                uav_target, color=color, label=file_name)
    #set yticks
    yticks = np.arange(0, 0.08, 0.02)
    ytick_labels = [str(ytick)+' m^2' for ytick in yticks]
    ax2.set_yticks(yticks, ytick_labels, color='red', size=6)
    
    


