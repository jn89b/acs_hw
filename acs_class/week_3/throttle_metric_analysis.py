import pickle as pkl
import glob as glob
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

plt.close('all')

pkl_files = glob.glob('*throttle_values.pkl')

title_names = ['Base Model',
    'Serrated Leading Edge with Shroud',
    'Serrated Trailing Edge with Shroud',
    'Three Propeller with Shroud']

title_names = [title_names[-1],
               title_names[-2],
               title_names[1]]

percent_throttle = [25, 50, 75, 100]
throttle_lists = []

for pkl_file in pkl_files:
    # get the rpm value from the pkl file name
    #rpm_value = re.findall(r'\d+', pkl_file)[0]
    # open the pkl file
    with open(pkl_file, 'rb') as f:
        # load the pkl file
        print(pkl_file)
        throttle_info = pkl.load(f)

        throttle_lists.append(throttle_info)
        
        # get the mean values from the pkl file


throttle_lists[-1] = throttle_lists[-1]['Thrust (N)']

#convert to numpy array
throttle_lists = np.array(throttle_lists)

throttle_lists = abs(throttle_lists / throttle_lists[-1]) * 100

sns.set_style('whitegrid')
sns.set_palette('muted')
# get three colors from the palette
colors = sns.color_palette('muted', n_colors=3)
colors = colors[::-1]
fig, ax = plt.subplots(figsize=(8,8))

for i, name in enumerate(title_names):
    ax.plot(percent_throttle, throttle_lists[i], label=name, 
            marker='o', markersize=10, color=colors[i])


    #ax.plot(throttle_list, label=title_names[i])
ax.hlines(99, label='Baseline', xmin=26, 
        xmax=100, color='k', linestyle='--')
ax.set_xlabel('Throttle Percent', fontsize=16)
ax.set_ylabel('Thrust Efficiency (%)', fontsize=16)
ax.legend(fontsize=10)

fig.savefig('figures/throttle_metric_analysis.png', dpi=300)
fig.savefig('figures/throttle_metric_analysis.svg') 


