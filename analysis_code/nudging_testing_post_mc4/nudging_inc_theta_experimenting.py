#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 12:42:39 2021

@author: nn819853
"""

import sys
sys.path.append('/home/users/nn819853/Documents/python_code')

import diagnostics.radiative_fluxes.fluxes_module as flux_mod
import diagnostics.file_locations_module as file_loc
import numpy as np
import iris
import iris.plot as iplt
import iris.quickplot as qplt
import matplotlib.pyplot as plt
import copy


# Process month mean diags
# Load theta nudging and other increments for cont and pert G=1/6 BL uvt nudged
diag_loc = file_loc.diag_dir + 'nudging_testing_post_mc4/theta_inc_diags/'

cont_nudge_inc_theta_file = 'month_mean_nudge_inc_theta_cb108.pp'
cont_other_inc_theta_file = 'month_mean_other_inc_theta_cb108.pp'
pert_nudge_inc_theta_file = 'month_mean_nudge_inc_theta_cb109.pp'
pert_other_inc_theta_file = 'month_mean_other_inc_theta_cb109.pp'

cont_nudge_inc_theta = iris.load_cube(diag_loc + 'month_mean_nudge_inc_theta_cb108.pp')
cont_other_inc_theta = iris.load_cube(diag_loc + 'month_mean_other_inc_theta_cb108.pp')
pert_nudge_inc_theta = iris.load_cube(diag_loc + 'month_mean_nudge_inc_theta_cb109.pp')
pert_other_inc_theta = iris.load_cube(diag_loc + 'month_mean_other_inc_theta_cb109.pp')

diags = [cont_nudge_inc_theta, cont_other_inc_theta, pert_nudge_inc_theta, pert_other_inc_theta]
area_mean_diags = []

# Calculate area means 
for diag in diags:
    cube = flux_mod.area_mean_cube(diag)
    area_mean_diags.append(cube)
    
    
# process hourly diags
# hourly_cont_other_inc_theta_file = diag_loc+ 'hourly_other_inc_theta_cb108_2014.pp'
# hourly_cont_other_inc_theta = iris.load_cube(hourly_cont_other_inc_theta_file)

# cube = flux_mod.area_mean_cube(hourly_cont_other_inc_theta)    
    

# Plot time series
diag_labels = ['cont nudge inc', 'cont other inc', 'pert nudge inc', 'pert other inc']
linestyles = ['-',(0,(1,1)),':',(0,(5,2,1,2))]

months = np.linspace(1, 60, num = 60)
hours = np.linspace(1, 12, num = 24*360)

level = 70
index_level = level - 1

save_target = file_loc.plot_dir + '/nudging_testing_post_mc4/theta_increments_time_series_cb108_cb109_lat113_lon0_level_' + str(level)
# save_target = file_loc.plot_dir + '/nudging_testing_post_mc4/theta_increments_time_series_cb108_cb109_area_mean_level_' + str(level)

plt.figure()
for i, diag in enumerate(diags):
    area_mean_diag_array = diag[:,index_level, 113, 0].data
    plt.plot(months, area_mean_diag_array, label = diag_labels[i], marker = 'x', linestyle = linestyles[i])
# plt.plot(hours, cube[:,55].data, marker = 'o')
plt.title('Monthly mean theta increments, G=1/6 BL uvt, level ' + str(level))
plt.legend()
plt.savefig(save_target, dpi=300)
plt.show


    