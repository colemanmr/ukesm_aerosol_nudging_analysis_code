#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 17 15:23:33 2021

@author: nn819853
"""

"""
Script to calculate mean bias of theta on levels and plot as vertical profile
for control error and adjustment for time slice experiments
"""

import sys
sys.path.append('/home/users/nn819853/Documents/python_code')

import diagnostics.radiative_fluxes.fluxes_module as flux_mod
import diagnostics.file_locations_module as file_loc
import numpy as np
import iris
import iris.plot as iplt
import matplotlib.pyplot as plt
import copy
import character_shortcuts as char

# set directory name 
diag_folder = 'other_adjustments/specific_humidity/'
diag_dir = file_loc.diag_dir + diag_folder
plot_dir = file_loc.plot_dir + 'other_adjustments/specific_humidity/'


# set suite names
cont_names = ['br793',
              'cb349',
              'cb108',
              ]

su_names = ['bv046',
            'cb350',
            'cb109',
            ]

bc_names = ['ce067',
            'ce304',
            'ce303',
            ]


# set lists for holind area meaned profiles
su_adjustment_profiles = []
bc_adjustment_profiles = []


# load time meaned q files and determine SU and BC adjustment for each
# nudging type
for i in range(3):
    cont_file = diag_dir + 'time_mean_q_'+cont_names[i]+'.nc'
    su_file = diag_dir + 'time_mean_q_'+su_names[i]+'.nc'
    bc_file = diag_dir + 'time_mean_q_'+bc_names[i]+'.nc'
    
    cont_cube = iris.load_cube(cont_file, 'time_mean_q')
    su_cube = iris.load_cube(su_file, 'time_mean_q')
    bc_cube = iris.load_cube(bc_file, 'time_mean_q')

    su_adjust = cont_cube - su_cube
    bc_adjust = cont_cube - bc_cube
    
    level_mean_su_adjust = flux_mod.area_mean_cube(su_adjust)
    level_mean_bc_adjust = flux_mod.area_mean_cube(bc_adjust)
    
    su_adjustment_profiles.append(level_mean_su_adjust)
    bc_adjustment_profiles.append(level_mean_bc_adjust)


# set labels for plots
labels = ['free',
          'uv-nudged',
          'uv'+char.theta()+'-nudged']

linestyles = ['-',
              '--',
              ':',]

# plot adjustments
plt.figure()
for i in range(3):
    iplt.plot(su_adjustment_profiles[i][0:63],
              su_adjustment_profiles[i][0:63].coord('level_height'),
              label = 'SU '+labels[i],
              color = 'darkorange',
              linestyle = linestyles[i])
    iplt.plot(bc_adjustment_profiles[i][0:63],
              bc_adjustment_profiles[i][0:63].coord('level_height'),
              label = 'BC '+labels[i],
              color = 'black',
              linestyle = linestyles[i])
plt.vlines(0, 0, 30000, linestyle = '--', color = 'darkgrey')
plt.ylabel('Altitude / m')
plt.xlabel(r'$\Delta$q / kg kg$^{-1}$')
plt.legend()
plt.savefig(plot_dir + 'level_mean_q_adjustments_profile', dpi=300)
plt.show()   



# def level_area_mean_q_suites(suite_list):
    
#     area_mean_profile_cubes = []
        
#     for suite in suite_list:
#         q_time_mean_file = diag_dir + 'time_mean_q_'+suite+'.pp'
#         cube = iris.load_cube(q_time_mean_file, 'mean_q')
        
        
        


# # load and calculate cont error and adjustment on each nudging setup
# for i in range(n_suites):
#     nudged_cont_file = diag_dir + 'time_mean_q_'+nudged_cont_names[i]+'.pp'
#     nudged_pert_file = diag_dir + 'time_mean_q_'+nudged_pert_names[i]+'.pp' 
    
#     nudged_cont = iris.load(nudged_cont_file)
#     nudged_cont_time_mean = nudged_cont[1]
    
#     nudged_pert = iris.load(nudged_pert_file)
#     nudged_pert_time_mean = nudged_pert[1]
    
#     cont_error = free_cont_time_mean_4years - nudged_cont_time_mean
#     adjustment = nudged_cont_time_mean - nudged_pert_time_mean
    
#     cont_error_copy = copy.deepcopy(cont_error)
#     adjustment_copy = copy.deepcopy(adjustment)
    
#     level_mean_cont_error = flux_mod.area_mean_cube(cont_error)
#     level_mean_adjustment = flux_mod.area_mean_cube(adjustment)
    
#     adjustment_list.append(level_mean_adjustment)
#     cont_error_list.append(level_mean_cont_error)
    
#     level_mean_cont_error_rms = flux_mod.area_rms_cube(cont_error_copy)
#     level_mean_adjustment_rms = flux_mod.area_rms_cube(adjustment_copy)
    
#     adjustment_rms_list.append(level_mean_adjustment_rms)
#     cont_error_rms_list.append(level_mean_cont_error_rms)    


# # plot level mean control errors
# plt.figure()
# for i in range(n_suites):
#     iplt.plot(cont_error_list[i][0:63], \
#               cont_error_list[i][0:63].coord('level_height'),
#               label = labels[i])
# plt.vlines(0, 0, 30000, linestyle = '--', color = 'darkgrey')
# plt.legend()
# plt.ylabel('Altitude / m')
# plt.xlabel('Potential temperature control error / K ')
# plt.savefig(plot_directory + 'level_mean_theta_cont_errors_profile', dpi=300)
# plt.show()

# # plot level mean adjustment rms
# plt.figure()
# for i in range(n_suites):
#     iplt.plot(adjustment_rms_list[i][0:63], \
#               adjustment_rms_list[i][0:63].coord('level_height'),
#               label = labels[i])
# iplt.plot(level_mean_free_adjustment_rms[0:63], \
#           level_mean_free_adjustment_rms[0:63].coord('level_height'),
#           label = 'free',
#           color = 'black')
# plt.savefig(plot_directory + 'level_mean_theta_su_adjustments_rms_profile', dpi=300)
# plt.legend()
# plt.show()

# # plot level mean control error rms
# plt.figure()
# for i in range(n_suites):
#     iplt.plot(cont_error_rms_list[i][0:63], \
#               cont_error_rms_list[i][0:63].coord('level_height'),
#               label = labels[i])
# plt.savefig(plot_directory + 'level_mean_theta_cont_errors_rms_profile', dpi=300)
# plt.legend()
# plt.show()
