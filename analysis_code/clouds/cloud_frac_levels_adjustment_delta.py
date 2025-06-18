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


######### CHANGE HERE #########
# Set suites 
cont_suite1 = 'br793'
pert_suite1 = 'ce067'

cont_suite2 = 'cb349'
pert_suite2 = 'ce304'

# set base  name for plot titles
title = 'Circ adjustment BC'
# title = 'T adjustment BC'

###############################

# Set plot and diagnostic directories and save fig and title targets
diag_dir = file_loc.diag_dir + 'cloud_diags/'
plot_dir = file_loc.plot_dir + 'clouds/'

save_plot_target = plot_dir + 'cloud_adjustment_levels_' + cont_suite1 + '-' + pert_suite1 +\
    '_minus_' + cont_suite1 + '-' + pert_suite2 + '_map_'


#Diff 1
# Load control and perturbed files
cont_file1 = 'cloud_frac_' + cont_suite1 + '_apm.pp'
pert_file1 = 'cloud_frac_' + pert_suite1 + '_apm.pp'

cont_cube1 = iris.load_cube(diag_dir + cont_file1)
pert_cube1 = iris.load_cube(diag_dir + pert_file1)


# ensure only full years included in averaging
cont1_annual_mean = flux_mod.annual_mean(cont_cube1)
pert1_annual_mean = flux_mod.annual_mean(pert_cube1)


# remove spinup (1 year)
cont_annual_mean_no_spin1 = cont1_annual_mean[1:,:,:,:]
pert_annual_mean_no_spin1 = pert1_annual_mean[1:,:,:,:]
    
    
# calculate adjustment   
cloud_adjustment1 = cont_annual_mean_no_spin1 - pert_annual_mean_no_spin1 


# take time mean 
time_mean_adjustment1, time_mean_stdev1, time_mean_double_se1\
    = flux_mod.time_mean_cube(cloud_adjustment1)
    
    
#Diff 2
# Load control and perturbed files
cont_file2 = 'cloud_frac_' + cont_suite2 + '_apm.pp'
pert_file2 = 'cloud_frac_' + pert_suite2 + '_apm.pp'

cont_cube2 = iris.load_cube(diag_dir + cont_file2)
pert_cube2 = iris.load_cube(diag_dir + pert_file2)


# ensure only full years included in averaging
cont2_annual_mean = flux_mod.annual_mean(cont_cube2)
pert2_annual_mean = flux_mod.annual_mean(pert_cube2)


# remove spinup (1 year)
cont_annual_mean_no_spin2 = cont2_annual_mean[1:,:,:,:]
pert_annual_mean_no_spin2 = pert2_annual_mean[1:,:,:,:]
    
    
# calculate adjustment   
cloud_adjustment2 = cont_annual_mean_no_spin2 - pert_annual_mean_no_spin2 


# take time mean 
time_mean_adjustment2, time_mean_stdev2, time_mean_double_se2\
    = flux_mod.time_mean_cube(cloud_adjustment2)

    
# adjustment delta
delta_cloud_adjustment = time_mean_adjustment1 - time_mean_adjustment2
    

# average over model levels
adjustment_low_cloud_mean = delta_cloud_adjustment[:,2:15,:,:].collapsed('model_level_number', iris.analysis.MEAN)
adjustment_mid_cloud_mean = delta_cloud_adjustment[:,15:27,:,:].collapsed('model_level_number', iris.analysis.MEAN)
adjustment_high_cloud_mean = delta_cloud_adjustment[:,27:45,:,:].collapsed('model_level_number', iris.analysis.MEAN)


# set adjustments lists for looping
adjust_list = [adjustment_low_cloud_mean, adjustment_mid_cloud_mean, adjustment_high_cloud_mean]
height_label_list = ['low', 'mid', 'high']


# loop over each level grouping
for i in range(3):    
    
    # # determine area mean for overall mean value
    # area_time_mean_adjustment = flux_mod.area_mean_cube(time_mean_adjustment)
    # area_time_mean_float = str(np.round(area_time_mean_adjustment.data, 3))


    # plot map
    plt.figure()
    mesh = iplt.pcolormesh(time_mean_adjustment, 
                           cmap='seismic',
                            vmin=-0.02, vmax=0.02,
                           )
    plt.colorbar(mesh, shrink = 0.9, label = 'Cloud volume fraction adjustment', \
                  orientation = 'horizontal',
                   ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                  )
    current_map = plt.gca()
    current_map.coastlines(linewidth = 1)
    # plt.text(-170, -110, 'Mean = ' + area_time_mean_float)
    plt.title(title + ' ' + height_label_list[i] + ' cloud adjustment', \
               fontsize = 'medium')
    # plt.savefig(save_plot_target + height_label_list[i] + '_cloud_new', dpi = 300)
    plt.show()


