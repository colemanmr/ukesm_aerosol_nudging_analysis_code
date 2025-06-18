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
    filenames = ['calc_forcing_br793_control_nudging_free_flux_'+sky+'_sky_minus_bv046_su_nudging_free_flux_'+sky+'_sky_1yr_spinup.nc',
                 'calc_forcing_bz529_control_nudging_uvt_flux_'+sky+'_sky_minus_bz527_su_nudging_uvt_flux_'+sky+'_sky_1yr_spinup.nc',
                 'calc_forcing_bz236_control_nudging_uvt_flux_'+sky+'_sky_minus_bz234_su_nudging_uvt_flux_'+sky+'_sky_1yr_spinup.nc',
                 'calc_forcing_by937_control_nudging_uvt_flux_'+sky+'_sky_minus_by965_su_nudging_uvt_flux_'+sky+'_sky_1yr_spinup.nc',
                 'calc_forcing_bz237_control_nudging_uvt_flux_'+sky+'_sky_minus_bz235_su_nudging_uvt_flux_'+sky+'_sky_1yr_spinup.nc',
                 'calc_forcing_bz528_control_nudging_uvt_flux_'+sky+'_sky_minus_bz526_su_nudging_uvt_flux_'+sky+'_sky_1yr_spinup.nc',
                 'calc_forcing_ca683_control_nudging_uv_flux_'+sky+'_sky_minus_ca687_su_nudging_uv_flux_'+sky+'_sky_1yr_spinup.nc',
                 'calc_forcing_ca682_control_nudging_uv_flux_'+sky+'_sky_minus_ca686_su_nudging_uv_flux_'+sky+'_sky_1yr_spinup.nc',
                 'calc_forcing_bz531_control_nudging_uv_flux_'+sky+'_sky_minus_bz530_su_nudging_uv_flux_'+sky+'_sky_1yr_spinup.nc',
                 'calc_forcing_ca681_control_nudging_uv_flux_'+sky+'_sky_minus_ca685_su_nudging_uv_flux_'+sky+'_sky_1yr_spinup.nc',
                 'calc_forcing_ca680_control_nudging_uv_flux_'+sky+'_sky_minus_ca684_su_nudging_uv_flux_'+sky+'_sky_1yr_spinup.nc',
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
    width = 0.08
    
    fig, ax = plt.subplots()
    
    ax.bar(label_points - 11*width/2, forcings[0,:,0], width, yerr = forcings[0,:,1], color = 'black', label = 'free, n=34')
    ax.bar(label_points - 8*width/2, forcings[1,:,0], width, yerr = forcings[1,:,1], color = 'brown', label = 'uv' + char.theta() + ', G=1/24, n=4')
    ax.bar(label_points - 6*width/2, forcings[2,:,0], width, yerr = forcings[2,:,1], color = 'firebrick', label = 'uv' + char.theta() + ', G=1/12, n=4')
    ax.bar(label_points - 4*width/2, forcings[3,:,0], width, yerr = forcings[3,:,1], color = 'red', label = 'uv' + char.theta() + ', G=1/6, n=9')
    ax.bar(label_points - 2*width/2, forcings[4,:,0], width, yerr = forcings[4,:,1], color = 'tomato', label = 'uv' + char.theta() + ', G=1/3, n=4')
    ax.bar(label_points + 0*width/2, forcings[5,:,0], width, yerr = forcings[5,:,1], color = 'lightcoral', label = 'uv' + char.theta() + ', G=1/1, n=4')
    ax.bar(label_points + 3*width/2, forcings[6,:,0], width, yerr = forcings[6,:,1], color = 'midnightblue', label = 'uv, G=1/24, n=4')
    ax.bar(label_points + 5*width/2, forcings[7,:,0], width, yerr = forcings[7,:,1], color = 'mediumblue', label = 'uv, G=1/12, n=4')
    ax.bar(label_points + 7*width/2, forcings[8,:,0], width, yerr = forcings[8,:,1], color = 'royalblue', label = 'uv, G=1/6, n=4')
    ax.bar(label_points + 9*width/2, forcings[9,:,0], width, yerr = forcings[9,:,1], color = 'cornflowerblue', label = 'uv, G=1/3, n=4')
    ax.bar(label_points + 11*width/2, forcings[10,:,0], width, yerr = forcings[10,:,1], color = 'lightsteelblue', label = 'uv, G=1/1, n=4')
    
    ax.set_xticks(label_points)
    ax.set_xticklabels(labels)
    ax.set_ylim(-2.2, 1.8)
    plt.legend(fontsize = 'x-small', ncol = 2, loc = 'upper left')
    ax.text(2,-1.8, sky+' sky', ha = 'center', fontsize = 'large')
    ax.axhline(y=0, xmin = 0, xmax = 1, color = 'darkgrey', linestyle = ':')
    ax.set_ylabel(u'ERF / W m$^{-2}$')
    plt.tight_layout()
    plt.savefig(plot_dir + 'su_forcing_comparison_bar_chart_varing_G_' + sky + '_sky', dpi = 400)
    plt.show()