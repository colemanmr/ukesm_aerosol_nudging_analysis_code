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


# # load time meaned q files and determine SU and BC adjustment for each
# # nudging type
# ### percent change as percent of area mean ###
# for i in range(3):
#     cont_file = diag_dir + 'time_mean_q_'+cont_names[i]+'.nc'
#     su_file = diag_dir + 'time_mean_q_'+su_names[i]+'.nc'
#     bc_file = diag_dir + 'time_mean_q_'+bc_names[i]+'.nc'
    
#     cont_cube = iris.load_cube(cont_file, 'time_mean_q')
#     su_cube = iris.load_cube(su_file, 'time_mean_q')
#     bc_cube = iris.load_cube(bc_file, 'time_mean_q')

#     su_adjust = cont_cube - su_cube
#     bc_adjust = cont_cube - bc_cube
    
# # keep level area mean of baseline to calc percentage change
#     if i == 0:
#         level_mean_free_cont = flux_mod.area_mean_cube(cont_cube)
    
#     level_mean_su_adjust = flux_mod.area_mean_cube(su_adjust)
#     level_mean_bc_adjust = flux_mod.area_mean_cube(bc_adjust)
    
# # calc percentage adjustment as adjustment area mean divided by baseline area mean
#     level_mean_su_adjust_percent = level_mean_su_adjust * 100 / level_mean_free_cont
#     level_mean_bc_adjust_percent = level_mean_bc_adjust * 100 / level_mean_free_cont
    
#     su_adjustment_profiles.append(level_mean_su_adjust_percent)
#     bc_adjustment_profiles.append(level_mean_bc_adjust_percent)


# # load time meaned q files and determine SU and BC adjustment for each
# # nudging type
# ### percent change as percent of each point then area meaned ###
# for i in range(3):
#     cont_file = diag_dir + 'time_mean_q_'+cont_names[i]+'.nc'
#     su_file = diag_dir + 'time_mean_q_'+su_names[i]+'.nc'
#     bc_file = diag_dir + 'time_mean_q_'+bc_names[i]+'.nc'
    
#     cont_cube = iris.load_cube(cont_file, 'time_mean_q')
#     su_cube = iris.load_cube(su_file, 'time_mean_q')
#     bc_cube = iris.load_cube(bc_file, 'time_mean_q')

#     su_adjust = cont_cube - su_cube
#     bc_adjust = cont_cube - bc_cube
    
# # keep baseline to calc percentage change
#     if i == 0:
#         free_cont = cont_cube
        
# # calc percentage adjustment as adjustment divided by baseline at each point
#     su_adjust_percent = su_adjust * 100 / free_cont
#     bc_adjust_percent = bc_adjust * 100 / free_cont
    
#     level_mean_su_adjust_percent = flux_mod.area_mean_cube(su_adjust_percent)
#     level_mean_bc_adjust_percent = flux_mod.area_mean_cube(bc_adjust_percent)
    
#     su_adjustment_profiles.append(level_mean_su_adjust_percent)
#     bc_adjustment_profiles.append(level_mean_bc_adjust_percent)


# load time meaned q files and determine SU and BC adjustment for each
# nudging type
### percent change as diff in area means weighted by area mean
for i in range(3):
    cont_file = diag_dir + 'time_mean_q_'+cont_names[i]+'.nc'
    su_file = diag_dir + 'time_mean_q_'+su_names[i]+'.nc'
    bc_file = diag_dir + 'time_mean_q_'+bc_names[i]+'.nc'
    
    cont_cube = iris.load_cube(cont_file, 'time_mean_q')
    su_cube = iris.load_cube(su_file, 'time_mean_q')
    bc_cube = iris.load_cube(bc_file, 'time_mean_q')
       
    # calculate level area means
    level_mean_cont = flux_mod.area_mean_cube(cont_cube)
    level_mean_su = flux_mod.area_mean_cube(su_cube)
    level_mean_bc = flux_mod.area_mean_cube(bc_cube)
    
# keep level area mean of baseline to calc percentage change
    if i == 0:
        level_mean_free_cont = level_mean_cont
    
    # take difference of cont - pert area means to get adjustment
    su_adjust = level_mean_cont - level_mean_su
    bc_adjust = level_mean_cont - level_mean_bc
    
    # weight by the free control level area mean
    su_adjust_percent = su_adjust*100/level_mean_free_cont
    bc_adjust_percent = bc_adjust*100/level_mean_free_cont
    
    su_adjustment_profiles.append(su_adjust_percent)
    bc_adjustment_profiles.append(bc_adjust_percent)


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
plt.xlabel(r'$\Delta$q / %')
plt.legend()
plt.savefig(plot_dir + 'level_mean_q_adjustments_profile_percent_by_mean_diff_weighting', dpi=300)
plt.show()   

