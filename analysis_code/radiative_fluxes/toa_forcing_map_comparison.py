#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 10:29:27 2020

@author: nn819853
"""

import sys
sys.path.append('/home/users/nn819853/Documents/python_code')

import numpy as np
import iris
import iris.plot as iplt
import matplotlib.pyplot as plt
import diagnostics.file_locations_module as file_loc


# Set forcing input filenames (free, uv, uvt templates)
filename1 = 'calc_forcing_br793_control_nudging_free_flux_all_sky_minus_ce067_bc_nudging_free_flux_all_sky_1yr_spinup.nc'
filename2 = 'calc_forcing_cb349_control_nudging_uv_flux_all_sky_minus_ce304_bc_nudging_uv_flux_all_sky_1yr_spinup.nc'
# filename2 = 'calc_forcing_cb108_control_nudging_uvt_flux_all_sky_minus_ce303_bc_nudging_uvt_flux_all_sky_1yr_spinup.nc'

filepath = file_loc.diag_dir + 'net_flux/'

forcing_input1 = filepath + filename1
forcing_input2 = filepath + filename2


# Load net, sw, and lw time meaned TOA forcing cubes
names = [
        'multiannual_mean_total_sw_down_forcing',
        'multiannual_mean_total_lw_down_forcing',
        'multiannual_mean_total_net_down_forcing',
        ]

time_sw_forcing1, time_lw_forcing1, time_net_forcing1,\
 = iris.load(forcing_input1, names)
 
time_sw_forcing2, time_lw_forcing2, time_net_forcing2,\
 = iris.load(forcing_input2, names) 
 
 
# Calculate delta forcings
sw_diff = time_sw_forcing1 - time_sw_forcing2
lw_diff = time_lw_forcing1 - time_lw_forcing2
net_diff = time_net_forcing1 - time_net_forcing2


# for deciding vmin, vmax
# print(np.min((sw_diff.data, lw_diff.data, net_diff.data)))
# print(np.max((sw_diff.data, lw_diff.data, net_diff.data)))


##################################
# Set target for saving files
plot_dir = file_loc.plot_dir + 'net_fluxes/'

diff1_cont = filename1[13:18]
index1 = filename1.find('_minus_')
diff1_pert = filename1[index1 + 7: index1 + 12]

diff2_cont = filename2[13:18]
index2 = filename2.find('_minus_')
diff2_pert = filename2[index2 + 7: index2 + 12]


index3 = filename1.find('_sky_')
index4 = filename1.find('_flux_')
diff1_sky = filename1[index4 + 6: index3]

index5 = filename2.find('_sky_')
index6 = filename2.find('_flux_')
diff2_sky = filename2[index6 + 6: index5]

name = diff1_cont + '-' + diff1_pert + '_' + diff1_sky + '_sky_minus_' +\
diff2_cont + '-' + diff2_pert + '_' + diff2_sky + '_sky'

target = plot_dir + name
##################################


#!! change color scheme to better for color blindness!!! !!#
# Plot net forcing delta map
plt.figure()
mesh = iplt.pcolormesh(net_diff, cmap = 'seismic', vmin = -10, vmax = 10)
plt.colorbar(mesh, fraction = 0.068, label = u' W m$^{-2}$', orientation = 'horizontal')
current_map = plt.gca()
current_map.coastlines(linewidth = 1)
# plt.title(name, fontsize = 'medium')
# plt.tight_layout()
plt.savefig(target + '_multiannual_mean_forcing_diff_map_net', dpi = 300)
plt.show()


# Plot sw forcing delta map
plt.figure()
mesh = iplt.pcolormesh(sw_diff, cmap = 'seismic', vmin = -10, vmax = 10)
plt.colorbar(mesh, fraction = 0.068, label = u' W m$^{-2}$', orientation = 'horizontal')
current_map = plt.gca()
current_map.coastlines(linewidth = 1)
# plt.title(name, fontsize = 'medium')
# plt.tight_layout()
plt.savefig(target + '_multiannual_mean_forcing_diff_map_sw', dpi = 300)
plt.show()


# Plot lw forcing delta map
plt.figure()
mesh = iplt.pcolormesh(lw_diff, cmap = 'seismic', vmin = -10, vmax = 10)
plt.colorbar(mesh, fraction = 0.068, label = u' W m$^{-2}$', orientation = 'horizontal')
current_map = plt.gca()
current_map.coastlines(linewidth = 1)
# plt.title(name, fontsize = 'medium')
# plt.tight_layout()
plt.savefig(target + '_multiannual_mean_forcing_diff_map_lw', dpi = 300)
plt.show()