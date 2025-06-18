#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 16:44:15 2021

@author: nn819853
"""

"""
Script to determine cloud fraction (00266) adjustment between control and
perturbed suites, including error estimation, and plotting cross section
"""

import sys
sys.path.append('/home/users/nn819853/Documents/python_code')

import iris
import numpy as np
import diagnostics.file_locations_module as file_loc
import diagnostics.radiative_fluxes.fluxes_module as flux_mod
import iris.plot as iplt
import iris.quickplot as qplt
import matplotlib.pyplot as plt
import character_shortcuts as char


# Assign diag and plot directories
diag_dir = file_loc.diag_dir + 'cloud_diags/'
plot_dir = file_loc.plot_dir + 'clouds/'


# load control and perturbed cubes - CAN CHANGE
cont_suite = 'by937'
pert_suite = 'by965'

cont_file = 'cloud_frac_annual_zonal_mean_' + cont_suite + '.nc'
pert_file = 'cloud_frac_annual_zonal_mean_' + pert_suite + '.nc'

cont_cube = iris.load_cube(diag_dir + cont_file,\
          'annual_zonal_mean_cloud_volume_fraction_in_atmosphere_layer')
pert_cube = iris.load_cube(diag_dir + pert_file,\
          'annual_zonal_mean_cloud_volume_fraction_in_atmosphere_layer')


# Dfiference control and pert cubes
diff = cont_cube - pert_cube


# Time mean difference cube to determine uncertainty
adjustment, adjustment_stdev, adjustment_double_se =\
flux_mod.time_mean_cube(diff)


# Change units of level height to km
adjustment.coord('level_height').convert_units('km')

# Adjust plottign variables
font = {'size' : 12}
plt.rc('font', **font)


#Set target for plot saving
target = plot_dir + 'cloud_frac_zonal_time_mean_adjustment_' + cont_suite + '_minus_' + pert_suite + '_paper_plot'


# Plot zonal mean cross section
plt.figure()
mesh = iplt.pcolormesh(adjustment[0:63],
                       coords = ['latitude', 'level_height'],
                       cmap = 'seismic',
                       vmin = -0.02,
                       vmax = 0.02)
plt.colorbar(mesh,
             fraction = 0.070,
             label = 'Cloud volume fraction adjustment',
             orientation = 'horizontal',
             ticks = [-0.02,-0.01,0,0.01,0.02])
plt.ylabel('Altitude / km')
plt.xlabel('Latitude')
plt.savefig(target, dpi = 300)
plt.show()


###OLD METHOD###

########## Temp extraction of values from cube ###########
# lat = adjustment.coord('latitude').points
# heights = adjustment.coord('level_height').points
# cloud_adjustment = adjustment.data
##########################################################

# plt.figure()
# # mesh = iplt.pcolormesh(adjustment[:65], cmap='seismic', vmin=-0.02, vmax=0.02)
# mesh = plt.pcolormesh(lat, heights, cloud_adjustment, cmap='seismic', vmin=-0.02, vmax=0.02)
# plt.colorbar(mesh, shrink = 0.9, label = 'Cloud volume fraction adjustment', \
#               orientation = 'horizontal', ticks = [-0.02, -0.01, 0, 0.01, 0.02])
# plt.ylabel('Altitude / m')
# plt.xlabel('Latitude')
# plt.ylim(0,28000)
# plt.title('Zonal time mean cloud adjustment: nudging uv G=1/6 BC cont-pert', \
#           fontsize = 'medium')
# plt.tight_layout()
# plt.savefig(target, dpi = 400)
# plt.show()

################


###Comtourf Method###
## Set levels to an array to also set vmin and vmax :) (thanks Jake!)
# plt.figure()
# contour_levels = np.linspace(-0.019, 0.019, num = 20)
# mesh = iplt.contourf(adjustment[:65], levels=contour_levels, cmap='seismic')
# #contour = iplt.contour(adjustment_double_se[:65])
# #plt.clabel(contour, inline=False)
# plt.colorbar(mesh, shrink = 0.9, label = 'Cloud volume fraction adjustment', \
#             orientation = 'horizontal')
# plt.show()


