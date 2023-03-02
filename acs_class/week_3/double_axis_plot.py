import pandas as pd
import utils
import seaborn as sns
import matplotlib.pyplot as plt
import re
import numpy as np
"""
Create a double Y-axis figure with 
thrust on the left y-axis, 
power consumptions on the right y-axis 
and RPM on the x-axis. 

"""

plt.close('all')

folder_dir = '/OGpropmics/'
folder_dir = '/mic_acs_data/'
folder_dir = '/TrailingEdgeSerrated/'
folder_dir = '/LeadingEdgeSerrated/'
folder_dir = '/ThreeProp/'
#get the csv files
csv_files = utils.get_csv_files(folder_dir)

# #get the data dictionary
mic_dict, data_dict = utils.get_mic_data_dictionary(csv_files)

#sort the dictionary by key value
data_dict = dict(sorted(data_dict.items()))

thrust_key = 'Thrust (kgf)'
voltage_key = 'Voltage (V)'
current_key = 'Current (A)'
rpm_key = 'Motor Optical Speed (RPM)'

#set seaborn gradient
sns.set_palette("husl")

fig,ax = plt.subplots()
#double y axis
ax2 = ax.twinx()

#plot the thrust data
rpm_values = []
thrust_values = []
power_values = []

min_rpm = 0 
max_rpm = 10000 

percent_throttle = np.arange(25, 125, 25)

for i, (key, dataframe) in enumerate(data_dict.items()):
    
    #remove rows that have 0 rpm
    dataframe = dataframe[dataframe[rpm_key] != 0]

    label_name = re.findall(r'\d+', key)
    #convert string to int
    esc_value = int(label_name[0])
    tolerance = 25

    #get mode of rpm
    rpm_value = dataframe[rpm_key].mode()[0]    

    condition = (dataframe[rpm_key] >= rpm_value - tolerance) & \
        (dataframe[rpm_key] <= rpm_value + tolerance)

    index_dataframe = dataframe[condition]
    #get all values for rpm if between 1000 and 2000
    current = abs(np.mean(index_dataframe[current_key].dropna()))
    voltage = abs(np.mean(index_dataframe[voltage_key].dropna()))
    power = current * voltage

    thrust = abs(np.mean(index_dataframe[thrust_key].dropna()))
    print(rpm_value)
    print(thrust)


    rpm_values.append(rpm_value)
    thrust_values.append(thrust)
    power_values.append(power)


ax.plot(percent_throttle, thrust_values, color='red', 
    label='Thrust (kgf)', marker='o')
ax2.plot(percent_throttle, power_values ,color='blue', 
    label='Power (W)', marker='x')

ax.set_xticks(percent_throttle)
#set xticks 
# ax.set_xlim(1100, 2000)
# ax.set_ylim(0, max(thrust_values)+0.5)
ax.set_xlabel('Percent Throttle (%)')
ax.set_ylabel('Thrust (kgf)')
ax2.set_ylabel('Power (W)')

ax.legend(loc='upper left', labelspacing=0.1)
ax2.legend(loc='lower right', labelspacing=0.1)

#save the figure
fig.savefig('thrust_power.svg')