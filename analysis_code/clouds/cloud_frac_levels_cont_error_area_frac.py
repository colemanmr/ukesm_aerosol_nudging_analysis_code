#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 16 15:00:17 2021

@author: nn819853
"""

import sys
sys.path.append('/home/users/nn819853/Documents/python_code')

import iris
import numpy as np
import diagnostics.file_locations_module as file_loc
import diagnostics.radiative_fluxes.fluxes_module as flux_mod
import iris.plot as iplt
import iris.quickplot as qplt
import matplotlib.pyplot as plt
import character_shortcuts as char


# model levels:
    # 3 = 76.666 - 130.000 m
    # 16 = 1810.00 - 2036.66 m
    # 28 = 5409.99 - 5796.66 m
    # 44 = 13197.907  - 13798.679 m
    
    # Model level divisions (inclusive): 
    # 3 - 15 = low
    # 16 - 27 = mid
    # 28 - 44 = high
 
# Revised models levels???
# level 20 = [2.7966665 km - 3.0766667 km]
# 3-20 = mid


######### CHANGE HERE #########
# Set suites 
free_cont_suite = 'br793'
nudged_cont_suite = 'cb108'

# set base  name for plot titles
# title = 'Nudged uv (G=1/6, bl=1, r=1)'
title = r'Nudged uv$\theta$ (G=1/6, bl=1, r=1)' 

###############################

# Set plot and diagnostic directories and save fig and title targets
diag_dir = file_loc.diag_dir + 'cloud_diags/'
plot_dir = file_loc.plot_dir + 'clouds/'

save_plot_target = plot_dir + 'cloud_cont_error_levels_' + free_cont_suite + '-' + nudged_cont_suite + '_map_'

########## CHANGE YEAR RANGE HERE #######
# Load control and perturbed files - 02261 = area frac diag seen by SOCRATES
free_cont_file = 'cloud_frac_02261_' + free_cont_suite + '_ap5_2014-2048.pp'
nudged_cont_file = 'cloud_frac_02261_' + nudged_cont_suite + '_ap5_2014-2020.pp'
############################################

free_cont_cube = iris.load_cube(diag_dir + free_cont_file)
nudged_cont_cube = iris.load_cube(diag_dir + nudged_cont_file)


# ensure only full years included in averaging
free_cont_annual_mean = flux_mod.annual_mean(free_cont_cube)
nudged_cont_annual_mean = flux_mod.annual_mean(nudged_cont_cube)


# remove spinup (1 year) and constrain to years 2-5 for cont error
free_cont_annual_mean_no_spin = free_cont_annual_mean[1:5,:,:,:]
nudged_cont_annual_mean_no_spin = nudged_cont_annual_mean[1:5,:,:,:]
    
    
# calculate cont_error   
cloud_cont_error = free_cont_annual_mean_no_spin - nudged_cont_annual_mean_no_spin 
    

# average over model levels
cont_error_low_cloud_mean = cloud_cont_error[:,2:15,:,:].collapsed('model_level_number', iris.analysis.MIN)
cont_error_mid_cloud_mean = cloud_cont_error[:,15:27,:,:].collapsed('model_level_number', iris.analysis.MIN)
cont_error_high_cloud_mean = cloud_cont_error[:,27:45,:,:].collapsed('model_level_number', iris.analysis.MIN)


# set cont_errors lists for looping
adjust_list = [cont_error_low_cloud_mean, cont_error_mid_cloud_mean, cont_error_high_cloud_mean]
height_label_list = ['low', 'mid', 'high']


# loop over each level grouping
for i in range(3):
    
    # take time mean 
    time_mean_cont_error, time_mean_stdev, time_mean_double_se\
        = flux_mod.time_mean_cube(adjust_list[i])
    
    
    # # determine area mean for overall mean value
    # area_time_mean_adjustment = flux_mod.area_mean_cube(time_mean_adjustment)
    # area_time_mean_float = str(np.round(area_time_mean_adjustment.data, 3))


    # plot map
    plt.figure()
    mesh = iplt.pcolormesh(time_mean_cont_error, 
                           cmap='seismic',
                            vmin=-0.05, vmax=0.05,
                           )
    plt.colorbar(mesh, shrink = 0.9, label = 'Cloud area fraction cont error', \
                  orientation = 'horizontal',
                    ticks = [-0.04, -0.02, 0, 0.02, 0.04]
                  )
    current_map = plt.gca()
    current_map.coastlines(linewidth = 1)
    # plt.text(-170, -110, 'Mean = ' + area_time_mean_float)
    plt.title(title + ' ' + height_label_list[i] + ' cloud area frac cont error', \
               fontsize = 'medium')
    plt.savefig(save_plot_target + height_label_list[i] + '_cloud_area_frac_cont_error_min', dpi = 300)
    plt.show()


