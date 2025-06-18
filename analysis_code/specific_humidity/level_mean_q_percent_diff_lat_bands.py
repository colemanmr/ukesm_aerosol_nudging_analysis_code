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


# set lists for holding area meaned profiles
su_adjustment_profiles = [[],[],[],[]]
bc_adjustment_profiles = [[],[],[],[]]

level_mean_free_cont_list = []

lat_starts = [0,0,48,96]
lat_ends = [144,48,96,144]


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
    
    # change level coords
    cont_cube.coord('level_height').convert_units('km')
    su_cube.coord('level_height').convert_units('km')
    bc_cube.coord('level_height').convert_units('km')
    
     
    for j in range(4):
        # calculate level area means
        level_mean_cont = flux_mod.area_mean_cube(cont_cube[:,lat_starts[j]:lat_ends[j],:])
        level_mean_su = flux_mod.area_mean_cube(su_cube[:,lat_starts[j]:lat_ends[j],:])
        level_mean_bc = flux_mod.area_mean_cube(bc_cube[:,lat_starts[j]:lat_ends[j],:])
        
    # keep level area mean of baseline to calc percentage change
        if i == 0:
            # keep in list as updates for each lat band
            level_mean_free_cont_list.append(level_mean_cont)
    
        # take difference of cont - pert area means to get adjustment
        su_adjust = level_mean_cont - level_mean_su
        bc_adjust = level_mean_cont - level_mean_bc
        
        # weight by the free control level area mean
        su_adjust_percent = su_adjust*100/level_mean_free_cont_list[j]
        bc_adjust_percent = bc_adjust*100/level_mean_free_cont_list[j]
        
        su_adjustment_profiles[j].append(su_adjust_percent)
        bc_adjustment_profiles[j].append(bc_adjust_percent)


# set labels for plots
i_labels = ['free',
          'uv-nudged',
          'uv'+char.theta()+'-nudged']

linestyles = ['-',
              '--',
              ':',]

lat_bands = ['all',
             '90S-30S',
             '30S-30N',
             '30N-90N']

# plot adjustments
for j in range(1):
    
    plt.figure()
    for i in range(3):
        iplt.plot(su_adjustment_profiles[j][i][0:63],
                  su_adjustment_profiles[j][i][0:63].coord('level_height'),
                  label = 'SU '+i_labels[i],
                  color = 'darkorange',
                  linestyle = linestyles[i])
        iplt.plot(bc_adjustment_profiles[j][i][0:63],
                  bc_adjustment_profiles[j][i][0:63].coord('level_height'),
                  label = 'BC '+i_labels[i],
                  color = 'black',
                  linestyle = linestyles[i])
    plt.vlines(0, 0, 30, linestyle = '--', color = 'darkgrey')
    plt.xlim(-8,8)
    plt.ylabel('Altitude / km')
    plt.xlabel(r'$\Delta$q / %')
    plt.title('Percentage specific humidity adjustment ' + lat_bands[j])
    plt.legend(fontsize = 10)
    plt.savefig(plot_dir + 'level_mean_q_adjustments_profile_percent_' + lat_bands[j]\
                # + '_no_title'\
                    ,dpi=300)
    plt.show()   

