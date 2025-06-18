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
        'clearclean', 
        'dre', 
        'cre'
        ]

for i, sky in enumerate(sky_type):
    filepath = file_loc.diag_dir + 'net_flux/'
    filenames = [
                 'calc_forcing_bz529_control_nudging_uvt_flux_'+sky+'_sky_minus_bz527_su_nudging_uvt_flux_'+sky+'_sky_1yr_spinup.nc',
                 'calc_forcing_bz236_control_nudging_uvt_flux_'+sky+'_sky_minus_bz234_su_nudging_uvt_flux_'+sky+'_sky_1yr_spinup.nc',
                 'calc_forcing_by937_control_nudging_uvt_flux_'+sky+'_sky_minus_by965_su_nudging_uvt_flux_'+sky+'_sky_1yr_spinup.nc',
                 'calc_forcing_bz237_control_nudging_uvt_flux_'+sky+'_sky_minus_bz235_su_nudging_uvt_flux_'+sky+'_sky_1yr_spinup.nc',
                 'calc_forcing_bz528_control_nudging_uvt_flux_'+sky+'_sky_minus_bz526_su_nudging_uvt_flux_'+sky+'_sky_1yr_spinup.nc',
                 'calc_forcing_cb108_control_nudging_uvt_flux_'+sky+'_sky_minus_cb109_su_nudging_uvt_flux_'+sky+'_sky_1yr_spinup.nc',
                 'calc_forcing_cb110_control_nudging_uvt_flux_'+sky+'_sky_minus_cb111_su_nudging_uvt_flux_'+sky+'_sky_1yr_spinup.nc',
                 'calc_forcing_ca683_control_nudging_uv_flux_'+sky+'_sky_minus_ca687_su_nudging_uv_flux_'+sky+'_sky_1yr_spinup.nc',
                 'calc_forcing_ca682_control_nudging_uv_flux_'+sky+'_sky_minus_ca686_su_nudging_uv_flux_'+sky+'_sky_1yr_spinup.nc',
                 'calc_forcing_bz531_control_nudging_uv_flux_'+sky+'_sky_minus_bz530_su_nudging_uv_flux_'+sky+'_sky_1yr_spinup.nc',
                 'calc_forcing_ca681_control_nudging_uv_flux_'+sky+'_sky_minus_ca685_su_nudging_uv_flux_'+sky+'_sky_1yr_spinup.nc',
                 'calc_forcing_ca680_control_nudging_uv_flux_'+sky+'_sky_minus_ca684_su_nudging_uv_flux_'+sky+'_sky_1yr_spinup.nc',
                 'calc_forcing_cb349_control_nudging_uv_flux_'+sky+'_sky_minus_cb350_su_nudging_uv_flux_'+sky+'_sky_1yr_spinup.nc',
                 'calc_forcing_cb351_control_nudging_uv_flux_'+sky+'_sky_minus_cb352_su_nudging_uv_flux_'+sky+'_sky_1yr_spinup.nc',
                 ]
    
    no_files = len(filenames)
    forcings = np.zeros((no_files,3,2))
    
    for j, file in enumerate(filenames):
        
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
    
    # calculate uvt nudged minus uv nudged forcing differences for each G  
    no_diffs = int(no_files/2)
    theta_diff = np.zeros([no_diffs,3,2])
    
    for k in range(no_diffs):
        theta_diff[k,:,0] = forcings[k,:,0] - forcings[k+no_diffs,:,0] 
        theta_diff[k,:,1] = forcings[k,:,1] + forcings[k+no_diffs,:,1]
    
    labels = ['Net', 'SW', 'LW']
    
    font = {'size' : 12}
    plt.rc('font', **font)
    
    label_points = np.arange(len(labels))
    width = 0.10
    
    fig, ax = plt.subplots()
    
    ax.bar(label_points - 6*width/2, theta_diff[0,:,0], width, yerr = theta_diff[0,:,1], color = 'brown', label = 'G=1/24, n=4')
    ax.bar(label_points - 4*width/2, theta_diff[1,:,0], width, yerr = theta_diff[1,:,1], color = 'firebrick', label = 'G=1/12, n=4')
    ax.bar(label_points - 2*width/2, theta_diff[2,:,0], width, yerr = theta_diff[2,:,1], color = 'red', label = 'G=1/6, n=9')
    ax.bar(label_points + 0*width/2, theta_diff[3,:,0], width, yerr = theta_diff[3,:,1], color = 'tomato', label = 'G=1/3, n=4')
    ax.bar(label_points + 2*width/2, theta_diff[4,:,0], width, yerr = theta_diff[4,:,1], color = 'lightcoral', label = 'G=1/1, n=4')
    ax.bar(label_points + 4*width/2, theta_diff[5,:,0], width, yerr = theta_diff[5,:,1], color = 'peru', label = 'G=1/6, bl=1, bramp=1, n=4')
    ax.bar(label_points + 6*width/2, theta_diff[6,:,0], width, yerr = theta_diff[6,:,1], color = 'darkorange', label = 'G=1/6, bl=1, bramp=4, n=4')
    
    ax.set_xticks(label_points)
    ax.set_xticklabels(labels)
    ax.set_ylim(-0.4, 0.7)
    plt.legend(fontsize = 'small', ncol = 1, loc = 'upper left')
    ax.text(1.8,0.5, sky+' sky', ha = 'center', fontsize = 'large')
    ax.axhline(y=0, xmin = 0, xmax = 1, color = 'darkgrey', linestyle = ':')
    ax.set_ylabel(u' nudging ' +char.theta()+ ' forcing / W m$^{-2}$')
    plt.tight_layout()
    plt.savefig(plot_dir + 'su_nudging_theta_forcing_bar_chart_varing_G_' + sky + '_sky', dpi = 400)
    plt.show()