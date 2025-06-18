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


# set directory name 
diag_folder = 'nudging_testing_new/theta/'
diag_dir = file_loc.diag_dir + diag_folder


# load free cont 4 year only theta data
free_cont_file_4years = diag_dir + 'time_mean_theta_br793_2015-2018.pp'
free_cont_4years = iris.load(free_cont_file_4years)
free_cont_time_mean_4years = free_cont_4years[1]

# convert level units
free_cont_time_mean_4years.coord('level_height').convert_units('km')


# load free cont and pert 34 year theta data
free_cont_file = diag_dir + 'time_mean_theta_br793.pp'
free_cont = iris.load(free_cont_file)
free_cont_time_mean = free_cont[1]

free_pert_su_file = diag_dir + 'time_mean_theta_bv046.pp'
free_pert_su = iris.load(free_pert_su_file)
free_pert_su_time_mean = free_pert_su[1]

free_pert_bc_file = diag_dir + 'time_mean_theta_ce067.pp'
free_pert_bc = iris.load(free_pert_bc_file)
free_pert_bc_time_mean = free_pert_bc[1]

free_cont_time_mean.coord('level_height').convert_units('km')
free_pert_su_time_mean.coord('level_height').convert_units('km')
free_pert_bc_time_mean.coord('level_height').convert_units('km')

# Calculate free adjustment bias and area RMS
free_su_adjustment = free_cont_time_mean - free_pert_su_time_mean
free_su_adjustment_copy = copy.deepcopy(free_su_adjustment)
level_mean_free_su_adjustment = flux_mod.area_mean_cube(free_su_adjustment)
level_mean_free_su_adjustment_rms = flux_mod.area_rms_cube(free_su_adjustment_copy)

free_bc_adjustment = free_cont_time_mean - free_pert_bc_time_mean
free_bc_adjustment_copy = copy.deepcopy(free_bc_adjustment)
level_mean_free_bc_adjustment = flux_mod.area_mean_cube(free_bc_adjustment)
level_mean_free_bc_adjustment_rms = flux_mod.area_rms_cube(free_bc_adjustment_copy)



# set nudged suite names
nudged_cont_names = [\
                      'cb108',
                      'cb349',
                      'cb108',
                      'cb349'
                     ]

nudged_pert_names = [\
                      'cb109',
                      'cb350',
                      'ce303',
                      'ce304'
                     ]

n_suites = len(nudged_cont_names)

# set empty lists to contain control errors and adjustments
adjustment_list = []
cont_error_list = []

adjustment_rms_list = []
cont_error_rms_list = []

# load and calculate cont error and adjustment on each nudging setup
for i in range(n_suites):
    nudged_cont_file = diag_dir + 'time_mean_theta_'+nudged_cont_names[i]+'.pp'
    nudged_pert_file = diag_dir + 'time_mean_theta_'+nudged_pert_names[i]+'.pp' 
    
    nudged_cont = iris.load(nudged_cont_file)
    nudged_cont_time_mean = nudged_cont[1]
    
    nudged_pert = iris.load(nudged_pert_file)
    nudged_pert_time_mean = nudged_pert[1]

    # convert height to km
    nudged_cont_time_mean.coord('level_height').convert_units('km')
    nudged_pert_time_mean.coord('level_height').convert_units('km')
    
    cont_error = free_cont_time_mean_4years - nudged_cont_time_mean
    adjustment = nudged_cont_time_mean - nudged_pert_time_mean
    
    cont_error_copy = copy.deepcopy(cont_error)
    adjustment_copy = copy.deepcopy(adjustment)
    
    level_mean_cont_error = flux_mod.area_mean_cube(cont_error)
    level_mean_adjustment = flux_mod.area_mean_cube(adjustment)
    
    adjustment_list.append(level_mean_adjustment)
    cont_error_list.append(level_mean_cont_error)
    
    level_mean_cont_error_rms = flux_mod.area_rms_cube(cont_error_copy)
    level_mean_adjustment_rms = flux_mod.area_rms_cube(adjustment_copy)
    
    adjustment_rms_list.append(level_mean_adjustment_rms)
    cont_error_rms_list.append(level_mean_cont_error_rms)    
    

# set plotting features 

labels = [\
          r'SU uv$\theta$-nudged', 
          'SU uv-nudged', 
          r'BC uv$\theta$-nudged',
          'BC uv-nudged'
          ]
    
cont_error_labels = [\
          r'uv$\theta$-nudged', 
          'uv-nudged', 
          ]

colours = [\
            'darkorange',
            'darkorange',
            'black',
            'black'
            ]

linestyles = [\
              ':',   
              '--',   
              ':',   
              '--'  
              ]

# set plot directory
plot_directory = file_loc.plot_dir + 'nudging_testing_new/'
plt.tight_layout()
plt.rcParams.update({'font.size': 10})


# plot level mean adjustments
#!! not full height! !!#
plt.figure()
iplt.plot(level_mean_free_su_adjustment[0:63], \
          level_mean_free_su_adjustment[0:63].coord('level_height'),
          label = 'SU free',
          color = 'darkorange')
iplt.plot(level_mean_free_bc_adjustment[0:63], \
          level_mean_free_bc_adjustment[0:63].coord('level_height'),
          label = 'BC free',
          color = 'black')
for i in range(n_suites):
    iplt.plot(adjustment_list[i][0:63], \
              adjustment_list[i][0:63].coord('level_height'),
              label = labels[i],
              color = colours[i],
              linestyle = linestyles[i])
plt.vlines(0, 0, 28, linestyle = (0,(10,3)), color = 'darkgrey', alpha = 0.5)
plt.legend(loc = 'lower right', ncol = 1, fontsize = 'medium')
# plt.xlim(-0.2, 0.8)
plt.ylabel('Altitude / km')
plt.xlabel(r'$\theta$ adjustment / K ')
plt.savefig(plot_directory + 'level_mean_theta_adjustments_profile_best_case_su_bc', 
            dpi=300, bbox_inches='tight')
plt.show()

# # plot level mean control errors
# plt.figure()
# for i in range(2):
#     iplt.plot(cont_error_list[i][0:63], \
#               cont_error_list[i][0:63].coord('level_height'),
#               label = labels[i],
#               color = colours[i],
#               linestyle = linestyles[i])
# plt.vlines(0, 0, 28000, linestyle = (0,(10,3)), color = 'darkgrey', alpha = 0.5)
# plt.legend(loc = 'lower right', ncol = 1, fontsize = 'medium')
# plt.xlim(-1.5, 2.0)
# plt.ylabel('Altitude / m')
# plt.xlabel('Potential temperature control error / K ')
# # plt.savefig(plot_directory + 'level_mean_theta_cont_errors_profile_best_case_su_bc', dpi=300)
# plt.show()

# plot level mean adjustment rms
plt.figure()
iplt.plot(level_mean_free_su_adjustment_rms[0:63], \
          level_mean_free_su_adjustment_rms[0:63].coord('level_height'),
          label = 'SU free',
          color = 'darkorange')
iplt.plot(level_mean_free_bc_adjustment_rms[0:63], \
          level_mean_free_bc_adjustment_rms[0:63].coord('level_height'),
          label = 'BC free',
          color = 'black')
for i in range(n_suites):
    iplt.plot(adjustment_rms_list[i][0:63], \
              adjustment_rms_list[i][0:63].coord('level_height'),
              label = labels[i],
              color = colours[i],
              linestyle = linestyles[i])
plt.legend(loc = 'lower right', ncol = 2, fontsize = 'small')
plt.xlim(-0.1, 1.4)
plt.ylabel('Altitude / m')
plt.xlabel('Potential temperature RMS-adjustment / K ')
plt.savefig(plot_directory + 'level_mean_theta_adjustments_rms_profile_best_case_su_bc',
            dpi=300, bbox_inches='tight')
plt.show()

# # plot level mean control error rms
# plt.figure()
# for i in range(n_suites):
#     iplt.plot(cont_error_rms_list[i][0:63], \
#               cont_error_rms_list[i][0:63].coord('level_height'),
#               label = labels[i],
#               color = colours[i],
#               linestyle = linestyles[i])
# plt.legend(loc = 'lower right', ncol = 2, fontsize = 'small')
# plt.xlim(-0.1, 2.5)
# plt.ylabel('Altitude / m')
# plt.xlabel('Potential temperature RMS-control error / K ')
# plt.savefig(plot_directory + 'level_mean_theta_cont_errors_rms_profile_best_case_su', dpi=300)
# plt.show()

