#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 16:32:39 2023

@author: nn819853
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
import iris.quickplot as qplt


# set directory name 
diag_folder = 'aerosols/'
diag_dir = file_loc.diag_dir + diag_folder
plot_dir = file_loc.plot_dir + 'aerosols/'


### Load in time mean mode separated mass aerosol per mass of air data
# create list to contain a CubeList of four cubes (modes) from each suite
cubelists = []

# list of suite names: free, uv-nudged, uvt-nudged
suite_names = [\
                'br793',
                # 'bv046',
                'ce067',
                'cb349',
                # 'cb350',
                'ce304',
                'cb108',
                # 'cb109',
                'ce303',
               ]

# calculate number of suites
no_suites = len(suite_names)

# load cubes into cubelists
for i in range(no_suites):
    cubes = iris.load(diag_dir + 'aer_burden_mmr_bc_' \
                      + suite_names[i] + '_time_mean.pp')
        
    cubelists.append(cubes)
    

### For each suite calculate total burden
# create lists to hold these
tot_burdens = []

# calculate the two quantities for each suite
for i in range(no_suites):
    cubes = cubelists[i]
    print(cubes)
    
    tot_burden = cubes[0] + cubes[1] + cubes[2] + cubes[3]
    # tot_burden = cubes[0]  ### aitken mode only
    # tot_burden = cubes[0] + cubes[1] + cubes[2] ### soluble modes only
    
    tot_burdens.append(tot_burden)
    

### Caclulate adjustment in each quantity
# create list for each adjustment
tot_adjs = []
percent_adjs = []

# calc number of nudging types of experiments
no_nudging_types = int(no_suites/2)

# Calculate adjustments in burden
for i in range(no_nudging_types):
    cont = tot_burdens[i*2]
    # su_pert = tot_burdens[i*3+1]
    bc_pert = tot_burdens[i*2+1]
    
    # tot_adj_su = cont - su_pert
    tot_adj_bc = cont - bc_pert
    
    tot_adjs.append(tot_adj_bc)
    
    # calculate percent adjustment as fraction of free control burden
    # percent_adj_su = tot_adj_su * 100 / tot_burdens[0]
    percent_adj_bc = tot_adj_bc * 100 / tot_burdens[0]
    
    percent_adjs.append(percent_adj_bc)    
    

### Plotting
# set contour intervals
adj_intervals = np.linspace(start = - 0.6* 1e-9, stop = 0.3e-9, num = 19)
cont_intervals = np.linspace(start = 0, stop = 0.5e-8, num = 9)
# percent_intervals = np.linspace(start = -0.22, stop = 0, num = 23)*100
percent_intervals = np.linspace(start = -1.0, stop = 1.0, num = 21)*100

# loop over however many nudging types there are
for i in range (no_nudging_types):
    
    # separate SU and BC adjustment
    # tot_adj_pair = tot_adjs[i]
    # tot_adj_su = tot_adj_pair[0]
    # tot_adj_bc = tot_adj_pair[1]
    tot_adj_bc = tot_adjs[i]
    
    # # take MIN or MAX over lower trop levels    
    # tot_adj_su_max = tot_adj_su[3:16].collapsed('model_level_number', \
    #                                             iris.analysis.MIN)
    # tot_adj_bc_max = tot_adj_bc[3:16].collapsed('model_level_number', \
    #                                             iris.analysis.MIN)
    
    # percent_adj_pair = percent_adjs[i]
    # percent_adj_su = percent_adj_pair[0]
    # percent_adj_bc = percent_adj_pair[1]
    percent_adj_bc = percent_adjs[i]
    
    # take control for each nudging type
    cont = tot_burdens[i*2]
    cont_max = cont[3:16].collapsed('model_level_number', \
                                                iris.analysis.MAX)
    

    
    # plot BC perturbed pair adjustment
    plt.figure()
    mesh = iplt.contourf(percent_adj_bc[11],\
                         # .collapsed('model_level_number', \
                         #                        iris.analysis.MAX), \
                    levels = percent_intervals,\
                  cmap = 'seismic')
    plt.colorbar(mesh,  fraction = 0.070, label = 'mmr adjustment / %', \
                  orientation = 'horizontal')
    plt.title('all mode BC burden 1km % adjustment ' + \
              suite_names[i*2] + '-' + suite_names[i*2+1])
    figure = plt.gca()
    figure.coastlines(linewidth = 1)
    plt.savefig(plot_dir + 'aer_burden_1km_percent_adjustment_bc_all_modes_' +\
        suite_names[i*2] + '-' + suite_names[i*2+1])
    plt.show()
    
    
    # Plot control burdens
    plt.figure()
    qplt.contourf(cont[11], \
                    levels = cont_intervals,\
                  cmap = 'magma')
    plt.title('all mode BC burden 1km in control ' + \
              suite_names[i*2])
    figure = plt.gca()
    figure.coastlines(linewidth = 1)
    plt.savefig(plot_dir + 'aer_burden_lev11_cont_bc_all_modes_' +\
        suite_names[i*2])
    plt.show()    
    

# More plotting - diff of diffs
free_minus_uv_adj_bc = percent_adjs[0] - percent_adjs[1]
uv_minus_uvt_adj_bc = percent_adjs[1] - percent_adjs[2]
# free_minus_uv_adj_su = percent_adjs[0][0] - percent_adjs[1][0]
# free_minus_uv_adj_su = percent_adjs[0][0] - percent_adjs[1][0]

# set intervals
diffofdiff_intervals = np.linspace(start = -24, stop = 24, num = 13)


# free minus uv-nudged percentage BC burden adjustment
plt.figure()
mesh = iplt.contourf(free_minus_uv_adj_bc[11],\
                     # .collapsed('model_level_number', \
                     #                        iris.analysis.MAX), \
                levels = diffofdiff_intervals, \
              cmap = 'seismic')
plt.colorbar(mesh,  fraction = 0.070, label = 'BC mmr adjustment difference / %', \
              orientation = 'horizontal')    
plt.title('all mode BC burden free minus uv-nudged % adjustment')
figure = plt.gca()
figure.coastlines(linewidth = 1)
plt.savefig(plot_dir + 'aer_burden_lev11_percent_free-uv_adjust_bc_all_modes_' +\
    suite_names[0] + '-' + suite_names[1] + '_minus_' +\
        suite_names[2] + '-' + suite_names[3])
plt.show()


# uv-nudged minus uvt-nudged percentage BC burden adjustment
plt.figure()
mesh = iplt.contourf(uv_minus_uvt_adj_bc[11],\
                     # .collapsed('model_level_number', \
                     #                        iris.analysis.MAX), \
                levels = diffofdiff_intervals, \
              cmap = 'seismic')
plt.colorbar(mesh,  fraction = 0.070, label = 'BC mmr adjustment difference / %', \
              orientation = 'horizontal')    
plt.title('all mode BC burden uv- minus uvt-nudged % adjustment')
figure = plt.gca()
figure.coastlines(linewidth = 1)
plt.savefig(plot_dir + 'aer_burden_lev11_percent_uv-uvt_adjust_bc_all_modes_' +\
    suite_names[2] + '-' + suite_names[3] + '_minus_' +\
        suite_names[4] + '-' + suite_names[5])
plt.show()
