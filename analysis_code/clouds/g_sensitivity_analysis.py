#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 14:14:26 2020

@author: nn819853
"""

import sys
sys.path.append('/home/users/nn819853/Documents/python_code')

import iris
import matplotlib.pyplot as plt
import iris.quickplot as qplt
import iris.plot as iplt
import numpy as np
import diagnostics.file_locations_module as file_loc
import diagnostics.radiative_fluxes.fluxes_module as flux_mod

file_dir = file_loc.diag_dir + 'cloud_diags/'

suites = ['br793', 'bv046', 'by937', 'by965']
cube_array = []

for suite_id in suites: 
    filename = 'cloud_frac_'+suite_id+'_apm.pp'
    filepath = file_dir + filename
    
    cube = iris.load_cube(filepath)
    cube_array.append(cube[12:]) # remove first year spinup
    
time_means = []

# ensure only full years included in averaging
for cube in cube_array:
    annual_mean = flux_mod.annual_mean(cube)
    
    time_mean = annual_mean.collapsed('time', iris.analysis.MEAN)
    time_means.append(time_mean)
    
column_means = []
zonal_means = []

for cube in time_means:
    column_mean = cube.collapsed('model_level_number', iris.analysis.MEAN)
    column_means.append(column_mean)
    
    zonal_mean = cube.collapsed('longitude', iris.analysis.MEAN)
    zonal_means.append(zonal_mean[:63])
    
column_free_cloud_pert = column_means[0] - column_means[1]
column_nudging_uvt_cloud_pert = column_means[2] - column_means[3]
zonal_free_cloud_pert = zonal_means[0] - zonal_means[1]
zonal_nudging_uvt_cloud_pert = zonal_means[2] - zonal_means[3]

plot_dir = file_loc.plot_dir + 'cloud_frac/'
#
#plt.figure()
#qplt.pcolormesh(column_free_cloud_pert)
##plt.legend()
#plt.savefig(plot_dir+'nudging_free_su_cloud_frac_adjustment_column', dpi = 400)
#plt.show()
#
#plt.figure()
#qplt.pcolormesh(column_nudging_uvt_cloud_pert)
##plt.legend()
#plt.savefig(plot_dir+'nudging_uvt_G_6hr_su_cloud_frac_adjustment_column', dpi = 400)
#plt.show()

plt.figure()
qplt.pcolormesh(zonal_free_cloud_pert, cmap='seismic', vmin=-0.02, vmax=0.02)
#plt.legend()
#plt.savefig(plot_dir+'nudging_free_su_cloud_frac_adjustment_zonal', dpi = 400)
plt.show()

plt.figure()
qplt.pcolormesh(zonal_nudging_uvt_cloud_pert, cmap='seismic', vmin=-0.02, vmax=0.02)
#plt.legend()
#plt.savefig(plot_dir+'nudging_uvt_G_6hr_su_cloud_frac_adjustment_zonal', dpi = 400)
plt.show()


#diff_column_cloud_frac = column_nudging_uvt_cloud_pert - column_free_cloud_pert
#diff_zonal_cloud_frac = zonal_nudging_uvt_cloud_pert - zonal_free_cloud_pert
#
#plt.figure()
#qplt.pcolormesh(diff_column_cloud_frac)
##plt.legend()
#plt.savefig(plot_dir+'nudging_uvt_G_6hr_su_minus_nudging_free_su_cloud_frac_adjustment_column_diff', dpi = 400)
#plt.show()
#
#plt.figure()
#qplt.pcolormesh(diff_zonal_cloud_frac)
##plt.legend()
#plt.savefig(plot_dir+'nudging_uvt_G_6hr_su_minus_nudging_free_su_cloud_frac_adjustment_zonal_diff', dpi = 400)
#plt.show()