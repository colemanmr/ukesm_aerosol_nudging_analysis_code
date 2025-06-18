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
cont_suite = 'br793'
pert_suite = 'bv046'

# set species
species = 'SU'

# set base  name for plot titles
title = 'Free ' + species
# title = 'Nudged uv (G=1/6, bl=1, r=1) ' + species
# title = r'Nudged uv$\theta$ (G=1/6, bl=1, r=1) ' + species

###############################

# Set plot and diagnostic directories and save fig and title targets
diag_dir = file_loc.diag_dir + 'cloud_diags/'
plot_dir = file_loc.plot_dir + 'clouds/'

save_plot_target = plot_dir + 'cloud_volume_frac_max_over_levels_adjustment_levels_' + cont_suite + '-' + pert_suite + '_map_'


# Load control and perturbed files
cont_file = 'cloud_frac_' + cont_suite + '_apm.pp'
pert_file = 'cloud_frac_' + pert_suite + '_apm.pp'

cont_cube = iris.load_cube(diag_dir + cont_file)
pert_cube = iris.load_cube(diag_dir + pert_file)


# ensure only full years included in averaging
cont_annual_mean = flux_mod.annual_mean(cont_cube)
pert_annual_mean = flux_mod.annual_mean(pert_cube)


# remove spinup (1 year)
cont_annual_mean_no_spin = cont_annual_mean[1:,:,:,:]
pert_annual_mean_no_spin = pert_annual_mean[1:,:,:,:]


# time mean cubes
cont_time_mean,_,_ = flux_mod.time_mean_cube(cont_annual_mean_no_spin)
pert_time_mean,_,_ = flux_mod.time_mean_cube(pert_annual_mean_no_spin)
    

# find max value over model levels
cont_low_cloud_max = cont_time_mean[2:16,:,:].collapsed('model_level_number', iris.analysis.MAX)
cont_mid_cloud_max = cont_time_mean[16:31,:,:].collapsed('model_level_number', iris.analysis.MAX)
cont_high_cloud_max = cont_time_mean[31:45,:,:].collapsed('model_level_number', iris.analysis.MAX)

pert_low_cloud_max = pert_time_mean[2:16,:,:].collapsed('model_level_number', iris.analysis.MAX)
pert_mid_cloud_max = pert_time_mean[16:31,:,:].collapsed('model_level_number', iris.analysis.MAX)
pert_high_cloud_max = pert_time_mean[31:45,:,:].collapsed('model_level_number', iris.analysis.MAX)

# calculate adjustments
adjustment_low_cloud = cont_low_cloud_max - pert_low_cloud_max
adjustment_mid_cloud = cont_mid_cloud_max - pert_mid_cloud_max
adjustment_high_cloud = cont_high_cloud_max - pert_high_cloud_max


# set adjustments lists for looping
adjust_list = [adjustment_low_cloud, adjustment_mid_cloud, adjustment_high_cloud]
height_label_list = ['low', 'mid', 'high']


# loop over each level grouping
for i in range(3): 
    
    # # determine area mean for overall mean value
    # area_time_mean_adjustment = flux_mod.area_mean_cube(time_mean_adjustment)
    # area_time_mean_float = str(np.round(area_time_mean_adjustment.data, 3))


    # plot map
    plt.figure()
    mesh = iplt.pcolormesh(adjust_list[i], 
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
    # plt.title(title + ' ' + height_label_list[i] + ' cloud max over levels adjustment volume frac', \
    #            fontsize = 'medium')
    plt.savefig(save_plot_target + height_label_list[i] + '_no_title', dpi = 300,\
                bbox_inches='tight')
    plt.margins(x=0)
    plt.show()


