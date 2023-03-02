import pickle as pkl
import glob as glob
import acoustic_plot as ap
import matplotlib.pyplot as plt
import numpy as np
"""
Plots:
- Subplots of all the sound profiles 
- One superimposed plot with error reference from the base mean
- Thrust values for plots 
- Thrust efficiency compared to baseline model

"""

#%% Subplots for all the sound profiles
plt.close('all')
# get all pkl files in the directory
pkl_files = glob.glob('*.pkl')


title_names = ['Base Model', 
    'Serrated Leading Edge with Shroud', 
    'Serrated Trailing Edge with Shroud', 
    'Three Propeller with Shroud']

mic_mean_dict = {}

for pkl_file in pkl_files:
    # get the rpm value from the pkl file name
    #rpm_value = re.findall(r'\d+', pkl_file)[0]
    # open the pkl file
    with open(pkl_file, 'rb') as f:
        # load the pkl file
        mic_dict = pkl.load(f)

        #if green 2 blade prop
        if 'Green' in pkl_file:
            value = mic_dict.pop('100% Mic Data.csv')
            
            mic_dict['100% Mic Data.csv'] = value
            print(mic_dict)

        # get the mean values from the pkl file
        mic_mean_dict[pkl_file] = mic_dict 

#pop off spider_plot_format.pkl from dictionary
spider_plot_format = mic_mean_dict.pop('spider_plot_format.pkl')

fig, axes = plt.subplots(nrows=2, ncols=2, 
        subplot_kw={'projection': 'polar'}, figsize=(12,12))

rows, col = axes.shape

throttle_percent_labels = ['25%', '50%', '75%', '100%']

for r in range(rows):
    for c in range(col):
        idx_key = list(mic_mean_dict.keys())[r*col+c]

        mic_data_dict = mic_mean_dict[idx_key]

        for i, (k,v) in enumerate(mic_data_dict.items()):
            axes[r,c].plot(spider_plot_format[0], v, label=throttle_percent_labels[i])
            axes[r,c].fill(spider_plot_format[0], v, alpha=0.1)

        #set title for each subplot
        axes[r,c].set_title(title_names[r*col+c], size=14)

        #set legend
axes[r,c].legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

for r in range(rows):
    for c in range(col):
        axes[r,c].set_xticks(spider_plot_format[0], spider_plot_format[1], 
            color='black', size=10)

        # Draw ylabels
        axes[r,c].set_rlabel_position(-22.5)

        # Draw ylabels
        axes[r,c].set_rlabel_position(-22.5)

        #set yticks color

        yticks = np.arange(0, 80, 10)
        ytick_labels = [str(ytick) for ytick in yticks]

        #axis.set_yticks(yticks, ytick_labels, color='red', size=10)
        axes[r,c].set_yticks(yticks, ytick_labels, color='red', size=8)

        #axes[r,c].set_rmax()

#tight layout
plt.tight_layout()

#save figure
fig.savefig('figures/all_sound_profiles.png', dpi=300)
fig.savefig('figures/all_sound_profiles.svg')

#%% Superimposed plot with error reference from the base mean
#compute error for each sound profile
idx_key = list(mic_mean_dict.keys())
base_model = mic_mean_dict[idx_key[0]]
base_keys = list(base_model.keys())

#compute error for each sound profile
error_dict = {} 
for k,v in mic_mean_dict.items():
    
    if k == idx_key[0]:
        continue

    error_list = []
    for i, (k2,v2) in enumerate(v.items()):
        #compute error for each sound profile
        error = np.array(v2) - np.array(base_model[base_keys[i]])
        #add error to dictionary
        error_list.append(error)

    error_dict[k] = error_list

#pop
quarter_throttle = [error_dict[k][0] for k in error_dict.keys()]
half_throttle = [error_dict[k][1] for k in error_dict.keys()]
three_quarter_throttle = [error_dict[k][2] for k in error_dict.keys()]
full_throttle = [error_dict[k][3] for k in error_dict.keys()]

full_list = [quarter_throttle, half_throttle, three_quarter_throttle, full_throttle]

throttle_configs = title_names[1:]

fig2, axes2 = plt.subplots(nrows=2, ncols=2, figsize=(12,10))    
rows, cols = axes2.shape

scatter_config = {'marker': '-o', 's': 10, 'alpha': 0.5}

#set seaborn style aesthetics
import seaborn as sns
sns.set_style('whitegrid')
sns.set_palette('muted')

degrees_of_interest = [70, 110, 250, 290]

#convert spider_plot_format string to number 
spider_plot_format[1] = [int(i) for i in spider_plot_format[1]]



for r in range(rows):
    for c in range(cols):
        
        throttle_info = full_list[r*cols+c]
        for i, throttle in enumerate(throttle_info):
            axes2[r,c].plot(spider_plot_format[1][:-1], 
                throttle[:-1], '-o', 
                label=throttle_configs[i])

        #get max and min from throttle_info
        max_val = np.max(throttle_info)
        min_val = np.min(throttle_info)

        for degree in degrees_of_interest:
            axes2[r,c].vlines(degree, color='red', 
                        linewidth=3, linestyle='--',
                        ymin=min_val, ymax=max_val)

        #set title for each subplot
        axes2[r,c].set_title(
            throttle_percent_labels[r*cols+c] + ' Throttle', size=14)
   
        if r == 1:
            axes2[r,c].set_xlabel('Angle (degrees)', size=12)

        if c == 0:
            axes2[r,c].set_ylabel('Sound Pressure Difference (dB)', size=12)
#set legend outside of plot

axes2[0,1].legend(loc='upper right', bbox_to_anchor=(1.3, 1.3))

# axes2[0,1].legend(loc='upper right', bbox_to_anchor=(1, 1))

#tight layout
#plt.tight_layout()

#save figure
fig2.savefig('figures/all_sound_profiles_error.png', dpi=300)
fig2.savefig('figures/all_sound_profiles_error.svg')

#%% Get throttle data performance







