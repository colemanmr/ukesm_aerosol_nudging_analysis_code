
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


# load free cont and pert 34 year theta data
free_cont_file = diag_dir + 'time_mean_theta_br793.pp'
free_cont = iris.load(free_cont_file)
free_cont_time_mean = free_cont[1]

free_pert_file = diag_dir + 'time_mean_theta_ce067.pp'
free_pert = iris.load(free_pert_file)
free_pert_time_mean = free_pert[1]


# Calculate free LTS adjustment
# Calc LTS as diff in theta at ~3km - surface
free_cont_lts = free_cont_time_mean[20] - free_cont_time_mean[0]
free_pert_lts = free_pert_time_mean[20] - free_pert_time_mean[0]

# Calc adjustmnt in LTS
free_lts_adjustment = free_cont_lts - free_pert_lts


# set nudged suite names
nudged_cont_names = ['by937',
                     'cb108',
                     'bz531',
                     'cb349',
                     ]

nudged_pert_names = ['cd563',
                     'ce303',
                     'cb470',
                     'ce304',
                     ]

n_suites = len(nudged_cont_names)

# set empty lists to contain LTS adjustments
nudged_lts_adjustment_list = []


# load and calculate cont error and adjustment on each nudging setup
for i in range(n_suites):
    nudged_cont_file = diag_dir + 'time_mean_theta_'+nudged_cont_names[i]+'.pp'
    nudged_pert_file = diag_dir + 'time_mean_theta_'+nudged_pert_names[i]+'.pp' 
    
    nudged_cont = iris.load(nudged_cont_file)
    nudged_cont_time_mean = nudged_cont[1]
    
    nudged_pert = iris.load(nudged_pert_file)
    nudged_pert_time_mean = nudged_pert[1]
    
    # Calc LTS as diff in theta at ~3km - surface
    cont_lts = nudged_cont_time_mean[20] - nudged_cont_time_mean[0]
    pert_lts = nudged_pert_time_mean[20] - nudged_pert_time_mean[0]
    
    # Calc adjustmnt in LTS
    lts_adjustment = cont_lts - pert_lts
    
    nudged_lts_adjustment_list.append(lts_adjustment)
            

# set plotting features 

titles = [r'uv$\theta$, G=1/6',
          r'uv$\theta$, BL no-ramp',
          'uv, G=1/6',
          'uv, BL no-ramp',
          ]


# set plot directory
plot_dir = file_loc.plot_dir + 'other_adjustments/lts/'


plt.figure()
mesh = iplt.pcolormesh(free_cont_lts, cmap = 'viridis')
plt.colorbar(mesh, shrink = 0.9, label = 'LTS / K',\
             orientation = 'horizontal')
current_map = plt.gca()
current_map.coastlines(linewidth = 1)
# plt.title('Free control LTS')
plt.savefig(plot_dir + 'free_cont_lts', dpi = 300, bbox_inches='tight')
plt.show()


plt.figure()
mesh = iplt.pcolormesh(free_lts_adjustment, cmap = 'seismic',\
                       vmin = -1.25, vmax = 1.25)
# plt.colorbar(mesh, shrink = 0.9, label = u'\u0394 LTS / K',\
#              orientation = 'horizontal')
current_map = plt.gca()
current_map.coastlines(linewidth = 1)
# plt.title('Free BC LTS adjustment')
plt.savefig(plot_dir + 'lts_adjustment_free_bc_br793-ce067', dpi = 300, bbox_inches='tight')
plt.show()

for i in range(n_suites):
    plt.figure()
    mesh = iplt.pcolormesh(nudged_lts_adjustment_list[i], cmap = 'seismic',\
                           vmin = -1.25, vmax = 1.25)
    # plt.colorbar(mesh, shrink = 0.9, label = u'\u0394 LTS / K',\
    #              orientation = 'horizontal')
    current_map = plt.gca()
    current_map.coastlines(linewidth = 1)
    # plt.title('Nudged '+ titles[i] + ' BC LTS adjustment')
    plt.savefig(plot_dir + 'lts_adjustment_nudged_bc_' + nudged_cont_names[i]\
                + '-' + nudged_pert_names[i], dpi = 300, bbox_inches='tight')
    plt.show()






