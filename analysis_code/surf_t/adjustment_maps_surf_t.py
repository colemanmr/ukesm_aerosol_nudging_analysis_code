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
diag_folder = 'other_adjustments/surf_t/'
diag_dir = file_loc.diag_dir + diag_folder
plot_dir = file_loc.plot_dir + 'other_adjustments/surf_t/'


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


# set lists for holiding each adjustment map
su_maps = []
bc_maps = []


# set lists for holding adjustment means
su_mean = []
bc_mean = []


# load time meaned surf_t files and determine SU and BC adjustment for each
# nudging type
for i in range(3):
    cont_file = diag_dir + 'time_mean_surf_t_'+cont_names[i]+'.nc'
    su_file = diag_dir + 'time_mean_surf_t_'+su_names[i]+'.nc'
    bc_file = diag_dir + 'time_mean_surf_t_'+bc_names[i]+'.nc'
    
    cont_cube = iris.load_cube(cont_file, 'time_mean_surf_t')
    su_cube = iris.load_cube(su_file, 'time_mean_surf_t')
    bc_cube = iris.load_cube(bc_file, 'time_mean_surf_t')

    su_adjust = cont_cube - su_cube
    bc_adjust = cont_cube - bc_cube
    
    su_maps.append(su_adjust)
    bc_maps.append(bc_adjust)


# calculate adjustment difference plots for T and circ adjustments
for i in range(2):
    su_adjustment_diff = su_maps[i] - su_maps[i+1]
    bc_adjustment_diff = bc_maps[i] - bc_maps[i+1]
    
    su_maps.append(su_adjustment_diff)
    bc_maps.append(bc_adjustment_diff)


# calculate area mean adjustments
for i in range(5):
    area_mean_su_adjust = flux_mod.area_mean_cube(su_maps[i])
    area_mean_bc_adjust = flux_mod.area_mean_cube(bc_maps[i])
    
    su_mean.append(area_mean_su_adjust)
    bc_mean.append(area_mean_bc_adjust)


# round and make string o means for inclusion in plot
su_mean_string = []
bc_mean_string = []

for i in range(5):
    rounded_mean_su = np.round(su_mean[i].data, 3)
    rounded_mean_bc = np.round(bc_mean[i].data, 3)
    
    su_mean_string.append(str(rounded_mean_su))
    bc_mean_string.append(str(rounded_mean_bc))
    

# set labels for plots
labels = ['free',
          'uv-nudged',
          'uv'+char.theta()+'-nudged',
          'circ-adjust',
          'T-adjust',]


# Plot adjustment maps
for j in range(5):
    plt.figure()
    mesh = iplt.pcolormesh(su_maps[j], cmap = 'seismic', vmin = -2, vmax = 2)
    plt.colorbar(mesh, fraction = 0.070, label = r'$\Delta T_{surf}$ / K', orientation = 'horizontal')
    current_map = plt.gca()
    current_map.coastlines(linewidth = 1)
    plt.text(0, -115, 'Mean = ' + su_mean_string[j] + ' K', ha = 'center')
    # plt.tight_layout() # for some reasonforces to top-right corner
    plt.savefig(plot_dir + 'surface_t_adjustment_map_su_'+labels[j], dpi = 300)
    plt.show()
    
    plt.figure()
    mesh = iplt.pcolormesh(bc_maps[j], cmap = 'seismic', vmin = -2, vmax = 2)
    plt.colorbar(mesh, fraction = 0.070, label = r'$\Delta T_{surf}$ / K', orientation = 'horizontal')
    current_map = plt.gca()
    current_map.coastlines(linewidth = 1)
    plt.text(0, -115, 'Mean = ' + bc_mean_string[j] + ' K', ha = 'center')
    # plt.tight_layout() # for some reasonforces to top-right corner
    plt.savefig(plot_dir + 'surface_t_adjustment_map_bc_'+labels[j], dpi = 300)
    plt.show()
    
    
### Final paper figure #######################################################    

import cartopy.crs as ccrs    
plt.tight_layout()
plt.rcParams.update({'font.size': 10})

vert_text = ['free', 'uv-nudged', r'uv$\theta$-nudged']
su_letter = ['a', 'c', 'e']
bc_letter = ['b', 'd', 'f']


    
fig, axs = plt.subplots(nrows=3, ncols=2,
                        subplot_kw={'projection': ccrs.PlateCarree()})

fig.text(0.31,1.01, 'SU', ha = 'center')
fig.text(0.68,1.01, 'BC', ha = 'center')

for count, ax in enumerate(axs[:,0]):
    
    mesh = iplt.pcolormesh(su_maps[count], axes = ax,
                           cmap = 'seismic', vmin = -2, vmax = 2)
    ax.coastlines(resolution = '110m', linewidth = 0.4)

    ax.text(-210, 0, vert_text[count], rotation = 90, va='center')
    ax.text(-180, -116, '(' + su_letter[count] + ')' + '       Mean = ' +
            su_mean_string[count] + ' K', ha = 'left')

for count, ax in enumerate(axs[:,1]):

    mesh = iplt.pcolormesh(bc_maps[count], axes = ax,
                           cmap = 'seismic', vmin = -2, vmax = 2)
    ax.coastlines(resolution = '110m', linewidth = 0.4)

    # ax.text(-210, 0, vert_text[count], rotation = 90, va='center')
    ax.text(-180, -116, '(' + bc_letter[count] + ')' + '       Mean = ' +
            bc_mean_string[count] + ' K', ha = 'left')


cbar_ax = fig.add_axes(rect = [0.15, 0.04, 0.7, 0.05])
fig.colorbar(mesh, cax=cbar_ax, label = r'$\Delta T_{surf}$ / K',
             orientation = 'horizontal')

plt.subplots_adjust(bottom=0.15,
                    left=0,
                    right=1, 
                    top=1, 
                    wspace=-0.45, 
                    hspace=0.25)

plt.savefig(plot_dir + 'nudging_surface_t_adjustment_maps_tesselation',
            dpi = 300, bbox_inches='tight')
plt.show()


    
    
    
    
    
    
    
    
    
