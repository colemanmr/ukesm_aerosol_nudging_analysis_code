#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 12:48:51 2020

@author: nn819853
"""

import sys
sys.path.append('/home/users/nn819853/Documents/python_code')

import iris
import numpy as np
import matplotlib.pyplot as plt
import diagnostics.file_locations_module as file_loc
import character_shortcuts as char

plot_dir = file_loc.plot_dir + 'net_fluxes/'

sky_type = ['all', 'clear', 'clean', 'clearclean']

for i, sky in enumerate(sky_type):
    filepath = file_loc.diag_dir + 'net_flux/'
    filenames = ['calc_forcing_br793_control_nudging_free_flux_'+sky+'_sky_minus_bv046_su_nudging_free_flux_'+sky+'_sky_1yr_spinup.nc',
                 'calc_forcing_by937_control_nudging_uvt_flux_'+sky+'_sky_minus_by965_su_nudging_uvt_flux_'+sky+'_sky_1yr_spinup.nc',
                 'calc_forcing_bz236_control_nudging_uvt_flux_'+sky+'_sky_minus_bz234_su_nudging_uvt_flux_'+sky+'_sky_1yr_spinup.nc',
                 'calc_forcing_bz237_control_nudging_uvt_flux_'+sky+'_sky_minus_bz235_su_nudging_uvt_flux_'+sky+'_sky_1yr_spinup.nc',
                 'calc_forcing_bz528_control_nudging_uvt_flux_'+sky+'_sky_minus_bz526_su_nudging_uvt_flux_'+sky+'_sky_1yr_spinup.nc',
                 'calc_forcing_bz529_control_nudging_uvt_flux_'+sky+'_sky_minus_bz527_su_nudging_uvt_flux_'+sky+'_sky_1yr_spinup.nc',
                 'calc_forcing_bz531_control_nudging_uv_flux_'+sky+'_sky_minus_bz530_su_nudging_uv_flux_'+sky+'_sky_1yr_spinup.nc',
#                 'calc_forcing_bz380_control_nudging_uvt_flux_'+sky+'_sky_minus_bz381_su_nudging_uvt_flux_'+sky+'_sky_1yr_spinup.nc',
                 ]
    
    no_files = len(filenames)
    forcings = np.zeros((no_files,3,2))
    
    for j, file in enumerate(filenames):
        
#        control_suite = file[13:18]
#        index1 = file.find('_minus_')
#        perturbed_suite = file[index1 + 7: index1 + 12]
#        
#        index2 = file.find('_flux1_')
#        sky_type = file[index2 + 7 : index1 - 5]
        
        sw_cube = iris.load_cube(filepath + file, 'multiannual_area_mean_total_sw_down_forcing')
        lw_cube = iris.load_cube(filepath + file, 'multiannual_area_mean_total_lw_down_forcing')
        net_cube = iris.load_cube(filepath + file, 'multiannual_area_mean_total_net_down_forcing')
        sw_error_cube = iris.load_cube(filepath + file, 'multiannual_area_mean_total_sw_down_forcing_2SE')
        lw_error_cube = iris.load_cube(filepath + file, 'multiannual_area_mean_total_lw_down_forcing_2SE')
        net_error_cube = iris.load_cube(filepath + file, 'multiannual_area_mean_total_net_down_forcing_2SE')
        
        forcings[j, 0, 0] = net_cube.data
        forcings[j, 1, 0] = sw_cube.data
        forcings[j, 2, 0] = lw_cube.data
        forcings[j, 0, 1] = net_error_cube.data
        forcings[j, 1, 1] = sw_error_cube.data
        forcings[j, 2, 1] = lw_error_cube.data
    
    labels = ['Net', 'SW', 'LW']
    
    font = {'size' : 12}
    plt.rc('font', **font)
    
    label_points = np.arange(len(labels))
    width = 0.12
    
    fig, ax = plt.subplots()
    
    ax.bar(label_points - 6*width/2, forcings[0,:,0], width, yerr = forcings[0,:,1], color = 'maroon', label = 'free, n=34')
    ax.bar(label_points - 4*width/2, forcings[5,:,0], width, yerr = forcings[5,:,1], color = 'brown', label = 'uv' + char.theta() + ' nudged, G=1/24, n=4')
    ax.bar(label_points - 2*width/2, forcings[2,:,0], width, yerr = forcings[2,:,1], color = 'firebrick', label = 'uv' + char.theta() + ' nudged, G=1/12, n=4')
    ax.bar(label_points, forcings[1,:,0], width, yerr = forcings[1,:,1], color = 'red', label = 'uv' + char.theta() + ' nudged G=1/6, n=9')
    ax.bar(label_points + 2*width/2, forcings[3,:,0], width, yerr = forcings[3,:,1], color = 'tomato', label = 'uv' + char.theta() + ' nudged, G=1/3, n=4')
    ax.bar(label_points + 4*width/2, forcings[4,:,0], width, yerr = forcings[4,:,1], color = 'lightcoral', label = 'uv' + char.theta() + ' nudged, G=1/1, n=4')
    ax.bar(label_points + 7*width/2, forcings[6,:,0], width, yerr = forcings[6,:,1], color = 'saddlebrown', label = 'uv nudged, G=1/6, n=4')
   
    ax.set_xticks(label_points)
    ax.set_xticklabels(labels)
    ax.set_ylim(-2.2, 1.8)
    plt.legend(fontsize = 'small', ncol = 2)
    ax.text(2,-1.8, sky+' sky', ha = 'center', fontsize = 'large')
#    ax.text(3.3,0.5,'Clear Sky')
#    ax.axvline(x = 2.5, ymin= 0, ymax = 1, color = 'darkgrey', linestyle = '-')
    ax.axhline(y=0, xmin = 0, xmax = 1, color = 'darkgrey', linestyle = ':')
    ax.set_ylabel(u'ERF / W m$^{-2}$')
    plt.tight_layout()
    plt.savefig(plot_dir + 'su_forcing_comparison_bar_chart_varing_G_' + sky + '_sky', dpi = 400)
    plt.show()