"""

"""
import pandas as pd
import utils 
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import pickle as pkl
"""
Get throttle data from each csv file 
and plot the data

Interpolate the data based on RPM 
"""

#%% 
if __name__ == '__main__':

    folder_name='/Green 2 Blade Prop/'

    cwd = os.getcwd()

    os.chdir( cwd+folder_name )
    csv_files = glob.glob( '*.csv' )

    mic_dict, data_dict = utils.get_mic_data_dictionary(csv_files)

    #put 2nd key in data dict into last key
    data_dict = dict(sorted(data_dict.items()))
    
    #pop the first key
    value = data_dict.pop('100% Thrust Data.csv')
    data_dict['100% Thrust Data.csv'] = value

    
    #interpolate esc values based on thrust values
    #get the esc values
    esc_values = []
    thrust_values = []

    for key in data_dict.keys():
        print(key)
        if key == 'Calibrate':
            continue 
        esc_values.append(data_dict[key]['ESC (µs)'].values)
        thrust_values.append( data_dict[key]['Thrust (N)'].values )


    esc_mean = []
    thrust_mean = []

    for esc, thrust in zip(esc_values, thrust_values):
        esc_mean.append(np.mean(esc))
        thrust_mean.append(np.mean(thrust)) 

    #convert to numpy array
    esc_mean = np.array(esc_mean)
    thrust_mean = np.array(thrust_mean)

    f = interpolate.interp1d(esc_mean, thrust_mean, kind='quadratic')

    esc_map = np.array([1350, 1500, 1650, 1800])

    thrust_output = f(esc_map)
    
    base_thrust = {'ESC (µs)': esc_map, 'Thrust (N)': thrust_output}
    
    #save base thrust data as pkl file
    with open('base_thrust.pkl', 'wb') as f:
        pkl.dump(base_thrust, f)

#%% searching for the propeller thrust  
folder_dir = '/TrailingEdgeSerrated/'
# folder_dir = '/LeadingEdgeSerrated/'
# folder_dir = '/ThreeProp/'
#get the csv files
csv_files = utils.get_csv_files(folder_dir)

# #get the data dictionary
mic_dict, data_dict = utils.get_mic_data_dictionary(csv_files)
thrust_key = 'Thrust (N)'
data_dict = dict(sorted(data_dict.items()))

throttle_values = [ '25%', '50%', '75%', '100%']

throttle_list = []
for i, (key, dataframe) in enumerate(data_dict.items()):

    esc_value = dataframe['ESC (µs)'].mode()[0]
    condition = dataframe['ESC (µs)'] == esc_value

    index_dataframe = dataframe[condition]
    thrust_value = index_dataframe[thrust_key].mean()
    
    throttle_list.append(thrust_value)

os.chdir('../')

#save the throttle values as a pkl file
with open(folder_dir[1:-1]+'throttle_values.pkl', 'wb') as f:
    pkl.dump(throttle_list, f)    






