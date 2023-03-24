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
    return 10*np.emath.log10(linear_vna_data)

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
    # axis.set_xticks(locations, categories, color='black', size=10)
    
    return fig,axis

def get_data_dictionary(folder_dir):
    os.chdir(folder_dir)
    csv_files = glob.glob('*.csv')
    data_dict = get_data_as_dict(csv_files)
    #go back one directory
    os.chdir('..')
    print("current directory", os.getcwd())

    return data_dict    

def dBm_to_RCS(theory_rcs, reference_rcs, target_rcs):
    rcs_tgt_lin = theory_rcs*10**((reference_rcs - target_rcs)/10)
    rcs_tgt_dbsm = 10*np.log10(rcs_tgt_lin)
    
    return rcs_tgt_dbsm
    
def make_total_spider_plot(some_dict, title_name, folder_dir='figures/', save=True):
    fig10,ax10 = format_spider_plot(radian_angles, angle_labels)
    ax10.set_thetamax(30)
    ax10.set_thetamin(-30)
    ax10.set_theta_zero_location('N')
    ax10.set_theta_direction(-1)
    
    color_list = ['red', 'blue', 'green', 'orange', 'purple']
    for i,(k,v) in enumerate(some_dict.items()):
        mean_val = v['mean']
        if 'level' in k:
            label = 'level'
        if 'positive' in k:
            label = '+5 degrees'
        if 'negative' in k:
            label = '-5 degrees'
        
        ax10.plot(angle_measurements, dBm_to_RCS(sigma_sphere_theory, mean_val, sphere_mean), 
                   label=label, color=color_list[i])
    
    #set y label
    ax10.set_ylabel('RCS (dBsm)')
    ax10.legend(loc='upper right')
    ax10.set_title(title_name)
    
    if save == True:
        fig10.savefig(folder_dir+title_name+'.svg')
        fig10.savefig(folder_dir+title_name+'.png')

def plot_comparison_db(some_dict, title, folder_dir='figures/', save=False):
    some_fig, some_ax = plt.subplots(1,1,figsize=(10,10))
    linestyle_list = ['-', '-', '-.', ':']
    
    for i, (k,v) in enumerate(some_dict.items()):
        if 'wakanda' in k:
            label = 'Wakanda'
            color = 'blue'
            
        if 'foil' in k:
            label = 'Foil'
            color = 'green'

        rcs_val = dBm_to_RCS(sigma_sphere_theory, v, sphere_mean)
        base_rcs_val = baseline_vals[0]
        compare = rcs_val - base_rcs_val            
        some_ax.plot(np.rad2deg(angle_measurements), compare, 
                    label=label, color=color, linestyle=linestyle_list[i])
        
    #draw dashed line at 0
    some_ax.axhline(y=0, color='red', linestyle='--', label='baseline')
    some_ax.legend(loc='upper right')
    some_ax.set_xlabel('Angle (deg)')
    some_ax.set_ylabel('RCS (dBsm)')
    some_ax.set_title(title)
    
    if save == True:
        some_fig.savefig(folder_dir+title+'.svg')
        some_fig.savefig(folder_dir+title+'.png')
        #print save directory
        print('file saved to: ', folder_dir+title+'.svg')

if __name__ == '__main__':
    
    folder_name = '/lab2_data/'
    cwd = os.getcwd()
    os.chdir(cwd+folder_name)
    # csv_files = glob.glob('*.csv')
    # data_dict = get_data_as_dict(csv_files)
    sphere_dict = get_data_dictionary(cwd+folder_name)
    baseline_no_skid = get_data_dictionary(cwd+folder_name+'/baseline/no_skid/')
    baseline_skid = get_data_dictionary(cwd+folder_name+'/baseline/skid/')
    foil_design_dict = get_data_dictionary(cwd+folder_name+'/foil_design/')
    wakanda_design_dict = get_data_dictionary(cwd+folder_name+'/wakanda_design/')
    
    #sphere thereotical equation
    #sigma_sphere_theory = lambda r: np.pi * r**2
    r_sphere = 0.125 #meters
    sigma_sphere_theory =  np.pi * r_sphere**2
    
    sphere_mean_dict = get_mean_std_dbm_dict(sphere_dict)
    baseline_no_skid_mean_dict = get_mean_std_dbm_dict(baseline_no_skid)
    baseline_skid_mean_dict = get_mean_std_dbm_dict(baseline_skid)
    foil_mean_dict = get_mean_std_dbm_dict(foil_design_dict)
    wakanda_mean_dict = get_mean_std_dbm_dict(wakanda_design_dict)    
    
    # #%% Format spider plots
    level_dict = {}
    positive_dict = {}
    negative_dict = {}
    baseline_vals = [0,0,0]
    
    for k,v in sphere_mean_dict.items():
        sphere_mean = v['mean']
        sphere_std = v['std']
        
        if 'level' in k:
            level_dict[k] = v
        if 'positive' in k:
            positive_dict[k] = v
        if 'negative' in k:
            negative_dict[k] = v
    
    for k,v in baseline_skid_mean_dict.items():
        baseline_mean = v['mean']/1.1
        baseline_std_mean = v['std']/1.1                
        
        if 'level' in k:
            # level_dict[k] = dBm_to_RCS(sigma_sphere_theory, baseline_mean, sphere_mean)
            baseline_vals[1] = dBm_to_RCS(sigma_sphere_theory, baseline_mean, sphere_mean)
            
        if 'positive' in k:
            # positive_dict[k] = dBm_to_RCS(sigma_sphere_theory, baseline_mean, sphere_mean)
            baseline_vals[2] = dBm_to_RCS(sigma_sphere_theory, baseline_mean, sphere_mean)
            
        if 'negative' in k:
            # negative_dict[k] = dBm_to_RCS(sigma_sphere_theory, baseline_mean, sphere_mean)
            baseline_vals[0] = dBm_to_RCS(sigma_sphere_theory, baseline_mean, sphere_mean)
                
    #baseline no skid
    for k,v in wakanda_mean_dict.items():
        wakanda_mean = v['mean']
        wakanda_std_mean = v['std']

        if 'level' in k:
            level_dict[k] = v['mean']
        if 'positive' in k: 
            positive_dict[k] = v['mean']
        if 'negative' in k:
            negative_dict[k] = v['mean']
                                        
    for k,v in foil_mean_dict.items():
        foil_mean = v['mean']
        baseline_std_mean = v['std']
 
        if 'level' in k:
            level_dict[k] = v['mean']
        if 'positive' in k:
            positive_dict[k] = v['mean']
        if 'negative' in k:
            negative_dict[k] = v['mean']
                 
    sigma_baseline = dBm_to_RCS(sigma_sphere_theory, baseline_mean, sphere_mean)
    sigma_wakanda_mean = dBm_to_RCS(sigma_sphere_theory, wakanda_mean, sphere_mean)
    sigma_foil_mean = dBm_to_RCS(sigma_sphere_theory, foil_mean, sphere_mean)

    plt.close('all')
    angles = np.arange(0, 2*np.pi, np.pi/4)
    radian_angles = np.arange(0, np.deg2rad(30)+np.deg2rad(1), np.deg2rad(1))
    angle_labels = [str(np.rad2deg(angle)) for angle in radian_angles] 
    angle_measurements = np.arange(-np.deg2rad(30), np.deg2rad(30)+np.deg2rad(1), np.deg2rad(1))

    make_total_spider_plot(baseline_skid_mean_dict, 'Baseline Skid', save=True)
    make_total_spider_plot(baseline_no_skid_mean_dict, 'Baseline No Skid', save=True)
    make_total_spider_plot(foil_mean_dict, 'Foil Design', save=True)
    make_total_spider_plot(wakanda_mean_dict, 'Wakanda Design', save=True)
        
    fig100,ax100 = plt.subplots(1,1,figsize=(10,10))
    #list of dashed lines
    linestyle_list = ['-', '-', '-.', ':']
    
    for i,(k,v) in enumerate(level_dict.items()):
        # mean_val = v['mean']/1.05
        if 'wakanda' in k:
            label = 'Wakanda'
            color = 'blue'
            
        if 'foil' in k:
            label = 'Foil'
            color = 'green'

        rcs_val = dBm_to_RCS(sigma_sphere_theory, v, sphere_mean)
        base_rcs_val = baseline_vals[0]
        compare = rcs_val - base_rcs_val            
        ax100.plot(np.rad2deg(angle_measurements), compare, 
                   label=label, color=color, linestyle=linestyle_list[i])        
        
    #draw dashed line at 0
    ax100.axhline(y=0, color='red', linestyle='--', label='baseline')
    ax100.legend(loc='upper right')
    ax100.set_xlabel('Angle (deg)')
    ax100.set_ylabel('RCS (dBsm)')
    ax100.set_title('RCS Comparison: Level')
    
            
    plot_comparison_db(level_dict, 'Level', save=True)
    plot_comparison_db(positive_dict, 'Positive 5', save=True)
    plot_comparison_db(negative_dict, 'Negative 5', save=True)
    
    # fig1, ax1 = format_spider_plot(radian_angles, angle_labels)
    # ax1.set_thetamax(30)
    # ax1.set_thetamin(-30)
    # #rotate the plot
    # ax1.set_theta_zero_location('N')
    # #flip the plot
    # ax1.set_theta_direction(-1)
    
    # ax1.plot(angle_measurements, sigma_baseline, color='red', label='baseline')
    # # ax1.fill_between(angle_measurements, sigma_target-sphere_std, sigma_target+sphere_std, color='red', alpha=0.2)
    # ax1.plot(angle_measurements, sigma_wakanda_mean, color='blue', label='wakanda')
    # ax1.plot(angle_measurements, sigma_foil_mean, color='green', label='foil')
    # ax1.legend()
        
    # fig2, ax2 = format_spider_plot(radian_angles, angle_labels)
    # ax2.set_thetamax(30)
    # ax2.set_thetamin(-30)
    # #rotate the plot
    # ax2.set_theta_zero_location('N')
    # ax2.set_theta_direction(-1)
    
    # ax2.plot(angle_measurements, baseline_mean, color='red', label='baseline')
    # ax2.plot(angle_measurements, wakanda_mean, color='blue', label='wakanda')
    # ax2.plot(angle_measurements, foil_mean, color='green', label='foil')
    # ax2.legend()
    
    # ax1.plot(np.arange(0, 2*np.pi+np.pi/4, np.pi/4),
    #             sigma_target, color=color, label=file_name)
    # #set yticks
    # yticks = np.arange(0, 0.08, 0.02)
    # ytick_labels = [str(ytick)+' m^2' for ytick in yticks]
    # ax1.set_yticks(yticks, ytick_labels, color='red', size=6)

    # #%% Plot the UAV
    # uav_target = compute_rcs_angle(sigma_sphere_theory,
    #                                mean_vn_uav, 
    #                                mean_vn_group2)
    # np.append(uav_target, uav_target[0])
    
    # angles = np.arange(0, 2*np.pi, np.pi/4)
    # fig2, ax2 = format_spider_plot(angles, 
    #                                ['0', '45', '90', '135', '180', '225', '270', '315'])

    
    # ax2.plot(np.arange(0, 2*np.pi+np.pi/4, np.pi/4),
    #             uav_target, color=color, label=file_name)
    # #set yticks
    # yticks = np.arange(0, 0.08, 0.02)
    # ytick_labels = [str(ytick)+' m^2' for ytick in yticks]
    # ax2.set_yticks(yticks, ytick_labels, color='red', size=6)
    
    


