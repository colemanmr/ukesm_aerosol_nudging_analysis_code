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

sky_type = [
        'all', 
        'clear', 
        'clean', 
        'clearclean'
        ]

for i, sky in enumerate(sky_type):
    filepath = file_loc.diag_dir + 'net_flux/'
    filenames = [
            'br793_4years_net_flux_control_nudging_free_calc_fluxes_'+sky+'_sky_1yr_spinup.nc',
            'bz529_net_flux_control_nudging_uvt_calc_fluxes_'+sky+'_sky_1yr_spinup.nc',
            'bz236_net_flux_control_nudging_uvt_calc_fluxes_'+sky+'_sky_1yr_spinup.nc',
            'by937_net_flux_control_nudging_uvt_calc_fluxes_'+sky+'_sky_1yr_spinup.nc',
            'bz237_net_flux_control_nudging_uvt_calc_fluxes_'+sky+'_sky_1yr_spinup.nc',
            'bz528_net_flux_control_nudging_uvt_calc_fluxes_'+sky+'_sky_1yr_spinup.nc',
            'cb108_net_flux_control_nudging_uvt_calc_fluxes_'+sky+'_sky_1yr_spinup.nc',
            'cb110_net_flux_control_nudging_uvt_calc_fluxes_'+sky+'_sky_1yr_spinup.nc',
#            'ca683_net_flux_control_nudging_uv_calc_fluxes_'+sky+'_sky_1yr_spinup.nc',
#            'ca682_net_flux_control_nudging_uv_calc_fluxes_'+sky+'_sky_1yr_spinup.nc',
#            'bz531_net_flux_control_nudging_uv_calc_fluxes_'+sky+'_sky_1yr_spinup.nc',
#            'ca681_net_flux_control_nudging_uv_calc_fluxes_'+sky+'_sky_1yr_spinup.nc',
#            'ca680_net_flux_control_nudging_uv_calc_fluxes_'+sky+'_sky_1yr_spinup.nc',
#            'cb349_net_flux_control_nudging_uv_calc_fluxes_'+sky+'_sky_1yr_spinup.nc',
#            'cb351_net_flux_control_nudging_uv_calc_fluxes_'+sky+'_sky_1yr_spinup.nc',
            ]
    
    no_files = len(filenames)
    fluxes = np.zeros((no_files,3,2))
    flux_error = np.zeros((no_files,3,2))
    
    for j, file in enumerate(filenames):
        
#        control_suite = file[13:18]
#        index1 = file.find('_minus_')
#        perturbed_suite = file[index1 + 7: index1 + 12]
#        
#        index2 = file.find('_flux1_')
#        sky_type = file[index2 + 7 : index1 - 5]
        
        sw_cube = iris.load_cube(filepath + file, 'multiannual_area_mean_total_sw_down_flux')
        lw_cube = iris.load_cube(filepath + file, 'multiannual_area_mean_total_lw_down_flux')
        net_cube = iris.load_cube(filepath + file, 'multiannual_area_mean_total_net_down_flux')
        sw_error_cube = iris.load_cube(filepath + file, 'multiannual_area_mean_total_sw_down_flux_2SE')
        lw_error_cube = iris.load_cube(filepath + file, 'multiannual_area_mean_total_lw_down_flux_2SE')
        net_error_cube = iris.load_cube(filepath + file, 'multiannual_area_mean_total_net_down_flux_2SE')
        
        fluxes[j, 0, 0] = net_cube.data
        fluxes[j, 1, 0] = sw_cube.data
        fluxes[j, 2, 0] = lw_cube.data
        fluxes[j, 0, 1] = net_error_cube.data
        fluxes[j, 1, 1] = sw_error_cube.data
        fluxes[j, 2, 1] = lw_error_cube.data
        
        # Calculate error: control_flux - free_control_flux 
        flux_error[j, :, 0] = fluxes[j, :, 0] - fluxes[0, :, 0]
        flux_error[j, :, 1] = fluxes[j, :, 1] + fluxes[0, :, 1]
        #!! redo with errors calculated on individual year diff stdev !!#
    
    labels = ['Net',
#              'SW', 
#              'LW'
              ]
    
    font = {'size' : 12}
    plt.rc('font', **font)
    
    label_points = np.arange(len(labels))
    width = 0.06
    
    fig, ax = plt.subplots()
    
#    ax.bar(label_points - 11*width/2, flux_error[0,0,0], width, yerr = flux_error[0,0,1], color = 'black', label = 'free, n=34')
    ax.bar(label_points - 15*width/2, flux_error[1,0,0], width, yerr = flux_error[1,0,1], color = 'brown', label = 'uv' + char.theta() + ', G=1/24')
    ax.bar(label_points - 13*width/2, flux_error[2,0,0], width, yerr = flux_error[2,0,1], color = 'firebrick', label = 'uv' + char.theta() + ', G=1/12')
    ax.bar(label_points - 11*width/2, flux_error[3,0,0], width, yerr = flux_error[3,0,1], color = 'red', label = 'uv' + char.theta() + ', G=1/6')
    ax.bar(label_points - 9*width/2, flux_error[4,0,0], width, yerr = flux_error[4,0,1], color = 'tomato', label = 'uv' + char.theta() + ', G=1/3')
    ax.bar(label_points - 7*width/2, flux_error[5,0,0], width, yerr = flux_error[5,0,1], color = 'lightcoral', label = 'uv' + char.theta() + ', G=1/1')
    
    ax.bar(label_points - 4*width/2, flux_error[6,0,0], width, yerr = flux_error[6,0,1], color = 'peru', label = 'uv' + char.theta() + ', G=1/6, bl=1, ramp=1')
    ax.bar(label_points - 2*width/2, flux_error[7,0,0], width, yerr = flux_error[7,0,1], color = 'darkorange', label = 'uv' + char.theta() + ', G=1/6, bl=1, ramp=4')
    
#    ax.bar(label_points + 1*width/2, flux_error[8,0,0], width, yerr = flux_error[8,0,1], color = 'midnightblue', label = 'uv, G=1/24, n=4')
#    ax.bar(label_points + 3*width/2, flux_error[9,0,0], width, yerr = flux_error[9,0,1], color = 'mediumblue', label = 'uv, G=1/12, n=4')
#    ax.bar(label_points + 5*width/2, flux_error[10,0,0], width, yerr = flux_error[10,0,1], color = 'royalblue', label = 'uv, G=1/6, n=4')
#    ax.bar(label_points + 7*width/2, flux_error[11,0,0], width, yerr = flux_error[11,0,1], color = 'cornflowerblue', label = 'uv, G=1/3, n=4')
#    ax.bar(label_points + 9*width/2, flux_error[12,0,0], width, yerr = flux_error[12,0,1], color = 'lightsteelblue', label = 'uv, G=1/1, n=4')
#    
#    ax.bar(label_points + 12*width/2, flux_error[13,0,0], width, yerr = flux_error[13,0,1], color = 'indigo', label = 'uv, G=1/6, bl=1, ramp=1, n=4')
#    ax.bar(label_points + 14*width/2, flux_error[14,0,0], width, yerr = flux_error[14,0,1], color = 'darkviolet', label = 'uv, G=1/6, bl=1, ramp=4, n=4')
    # note to self: I have checked the order of these (and initial cube loads order) and they are defo correct!
    
    ax.set_xticks([])
    ax.set_xticklabels([])
    ax.set_ylim(-1.5, 8)
    plt.legend(fontsize = 'small', ncol = 1, loc = 'upper left')
    ax.text(-0.3,-1.1, sky+' sky', ha = 'left', fontsize = 'large')
    ax.axhline(y=0, xmin = 0, xmax = 1, color = 'darkgrey', linestyle = ':')
    ax.set_ylabel(u'TOA Flux error / W m$^{-2}$')
    plt.tight_layout()
    plt.savefig(plot_dir + 'control_flux_error_comparison_net_only_varying_G_' + sky + '_sky', dpi = 400)
    plt.show()
    