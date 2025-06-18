#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 11:21:16 2021

@author: nn819853
"""

import sys
sys.path.append('/home/users/nn819853/Documents/python_code')

import numpy as np
import matplotlib.pyplot as plt
import iris
import iris.plot as iplt
import iris.quickplot as qplt
import diagnostics.radiative_fluxes.fluxes_module as flux_mod
import diagnostics.file_locations_module as file_loc
import iris.analysis
import character_shortcuts as char


data_dir = file_loc.diag_dir + 'nudging_testing_post_mc4/uv_pres_lev/'
plot_dir = file_loc.plot_dir + 'nudging_testing_post_mc4/uv_vector/'

# Change these to change suites used
cont = 'by937'
pert = 'by965'

# Choose cont error or adjustment
diff_type = 'adjustment'
# diff_type = 'cont_error'

# Choose nudging type for plot title
# nudging_type = 'free'
# nudging_type = 'uv' + char.theta() + '-nudged (G=1/6, bl=10, r=4)'
nudging_type = 'uv-nudged (G=1/6, bl=10, r=4)'

# Set species (for figure titles and filenames only)
species = 'SU' # set to '' for cont error


# load free u-wind v-wind and heavyside fraction time means
cont_cubes = iris.load(data_dir + 'uv_pres_lev_time_mean_'+cont+'.pp') # use for adjustment
pert_cubes = iris.load(data_dir + 'uv_pres_lev_time_mean_'+pert+'.pp')
# cont_cubes = iris.load(data_dir + 'uv_pres_lev_time_mean_'+cont+'_2015-2018.pp') # use for cont error


# load cont and pert cubes for heavyside function and u and v on p levels
cont_heavy = cont_cubes[3]
cont_u_raw = cont_cubes[5]
cont_v_raw = cont_cubes[7]

pert_heavy = pert_cubes[3]
pert_u_raw = pert_cubes[5]
pert_v_raw = pert_cubes[7]

# check right cubes loaded
print(np.max(cont_heavy.data)) # should be 1
print(np.min(cont_u_raw.data)) # should be <0
print(np.min(cont_v_raw.data)) # should be <0

print(np.max(pert_heavy.data)) # should be 1
print(np.min(pert_u_raw.data)) # should be <0
print(np.min(pert_v_raw.data)) # should be <0


# Normalise u and v by heavyside function
cont_u = cont_u_raw * cont_heavy
cont_v = cont_v_raw * cont_heavy

pert_u = pert_u_raw * pert_heavy
pert_v = pert_v_raw * pert_heavy


# take diff - (adjustment or cont error)
diff_u = cont_u - pert_u
diff_v = cont_v - pert_v


# determine magnitude of horizontal wind speed
speed = (diff_u ** 2 + diff_v ** 2) ** 0.5
speed.rename("windspeed")


# take only a selection of lat-lon points for plottign arrows
diff_u_step = diff_u[:,::9,::9]
diff_v_step = diff_v[:,::9,::9]###


# extract lat, lon and u and v values for plottign arrows
x = diff_u_step.coord('longitude').points
y = diff_u_step.coord("latitude").points
u = diff_u_step.data
v = diff_v_step.data


# plottign settings
# set figure font size
font = {'size' : 12}
plt.rc('font', **font)

# set filename for saving fig
target = plot_dir + 'horizontal_wind_'+diff_type+'_vector_map_'+cont+'-'+pert


# select levels for map plots and loop over for plotting
levels = [5,13,18,27,30,33]

for level in levels:
    
    # get pressure level for savefig filename
    pressure = speed[level].coord('pressure').points[0]
    
    # plot
    plt.figure()
    
    # Plot the wind speed as a colormesh plot
    mesh = iplt.pcolormesh(speed[level], cmap = 'viridis', vmin = 0, vmax = 2)
    plt.colorbar(mesh, fraction = 0.07, 
                 label = u'$\Delta$ horizontal windspeed', 
                 orientation = 'horizontal', extend = 'max', 
                 # ticks = [0,0.5,1,1.5,2]
                 ticks = [0, 0.25, 0.5, 0.75, 1]
                 )
    
    # Add arrows to show the wind vectors
    plt.quiver(x, y, u[level], v[level], pivot="middle", scale = 15)
    
    # add coastlines
    current_map = plt.gca()
    current_map.coastlines(linewidth = 1)
    
    # add title and save figure
    plt.title(nudging_type+' '+species+'\n horizontal wind '+diff_type+' ' +str(int(pressure))+' hPa')
    plt.savefig(target + '_'+str(int(pressure))+'_hPa')
    plt.show()


# # set figure font size
# font = {'size' : 12}
# plt.rc('font', **font)