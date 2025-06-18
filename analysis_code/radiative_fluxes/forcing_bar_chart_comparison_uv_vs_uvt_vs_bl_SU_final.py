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
        # 'clear', 
        # 'clean', 
        'clearclean', 
        'dre', 
        'cre'
        ]

for i, sky in enumerate(sky_type):
    filepath = file_loc.diag_dir + 'net_flux/'
    filenames = ['calc_forcing_br793_control_nudging_free_flux_'+sky+'_sky_minus_bv046_su_nudging_free_flux_'+sky+'_sky_1yr_spinup.nc',
                 # 'calc_forcing_bz529_control_nudging_uvt_flux_'+sky+'_sky_minus_bz527_su_nudging_uvt_flux_'+sky+'_sky_1yr_spinup.nc',
                 # 'calc_forcing_bz236_control_nudging_uvt_flux_'+sky+'_sky_minus_bz234_su_nudging_uvt_flux_'+sky+'_sky_1yr_spinup.nc',
                 # 'calc_forcing_by937_control_nudging_uvt_flux_'+sky+'_sky_minus_by965_su_nudging_uvt_flux_'+sky+'_sky_1yr_spinup.nc',
                 # 'calc_forcing_bz237_control_nudging_uvt_flux_'+sky+'_sky_minus_bz235_su_nudging_uvt_flux_'+sky+'_sky_1yr_spinup.nc',
                 # 'calc_forcing_bz528_control_nudging_uvt_flux_'+sky+'_sky_minus_bz526_su_nudging_uvt_flux_'+sky+'_sky_1yr_spinup.nc',
                 'calc_forcing_cb108_control_nudging_uvt_flux_'+sky+'_sky_minus_cb109_su_nudging_uvt_flux_'+sky+'_sky_1yr_spinup.nc',
                 # 'calc_forcing_cb110_control_nudging_uvt_flux_'+sky+'_sky_minus_cb111_su_nudging_uvt_flux_'+sky+'_sky_1yr_spinup.nc',
                 # 'calc_forcing_ca683_control_nudging_uv_flux_'+sky+'_sky_minus_ca687_su_nudging_uv_flux_'+sky+'_sky_1yr_spinup.nc',
                 # 'calc_forcing_ca682_control_nudging_uv_flux_'+sky+'_sky_minus_ca686_su_nudging_uv_flux_'+sky+'_sky_1yr_spinup.nc',
                 # 'calc_forcing_bz531_control_nudging_uv_flux_'+sky+'_sky_minus_bz530_su_nudging_uv_flux_'+sky+'_sky_1yr_spinup.nc',
                 # 'calc_forcing_ca681_control_nudging_uv_flux_'+sky+'_sky_minus_ca685_su_nudging_uv_flux_'+sky+'_sky_1yr_spinup.nc',
                 # 'calc_forcing_ca680_control_nudging_uv_flux_'+sky+'_sky_minus_ca684_su_nudging_uv_flux_'+sky+'_sky_1yr_spinup.nc',
                 'calc_forcing_cb349_control_nudging_uv_flux_'+sky+'_sky_minus_cb350_su_nudging_uv_flux_'+sky+'_sky_1yr_spinup.nc',
                 # 'calc_forcing_cb351_control_nudging_uv_flux_'+sky+'_sky_minus_cb352_su_nudging_uv_flux_'+sky+'_sky_1yr_spinup.nc',
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
    
    # labels = ['Net', 'SW', 'LW']
    
    # font = {'size' : 12}
    # plt.rc('font', **font)
    
    # label_points = np.arange(len(labels))
    # width = 0.055
    
    # fig, ax = plt.subplots()
    
    # ax.bar(label_points - 18*width/2, forcings[0,:,0], width, yerr = forcings[0,:,1], color = 'black', label = 'free, n=34')
    
    # ax.bar(label_points - 15*width/2, forcings[1,:,0], width, yerr = forcings[1,:,1], color = 'brown', label = 'uv' + char.theta() + ', G=1/24, n=4')
    # ax.bar(label_points - 13*width/2, forcings[2,:,0], width, yerr = forcings[2,:,1], color = 'firebrick', label = 'uv' + char.theta() + ', G=1/12, n=4')
    # ax.bar(label_points - 11*width/2, forcings[3,:,0], width, yerr = forcings[3,:,1], color = 'red', label = 'uv' + char.theta() + ', G=1/6, n=9')
    # ax.bar(label_points - 9*width/2, forcings[4,:,0], width, yerr = forcings[4,:,1], color = 'tomato', label = 'uv' + char.theta() + ', G=1/3, n=4')
    # ax.bar(label_points - 7*width/2, forcings[5,:,0], width, yerr = forcings[5,:,1], color = 'lightcoral', label = 'uv' + char.theta() + ', G=1/1, n=4')
    
    # ax.bar(label_points - 4*width/2, forcings[6,:,0], width, yerr = forcings[6,:,1], color = 'peru', label = 'uv' + char.theta() + ', G=1/6, bl=1, ramp=1, n=4')
    # ax.bar(label_points - 2*width/2, forcings[7,:,0], width, yerr = forcings[7,:,1], color = 'darkorange', label = 'uv' + char.theta() + ', G=1/6, bl=1, ramp=4, n=4')
    
    # ax.bar(label_points + 1*width/2, forcings[8,:,0], width, yerr = forcings[8,:,1], color = 'midnightblue', label = 'uv, G=1/24, n=4')
    # ax.bar(label_points + 3*width/2, forcings[9,:,0], width, yerr = forcings[9,:,1], color = 'mediumblue', label = 'uv, G=1/12, n=4')
    # ax.bar(label_points + 5*width/2, forcings[10,:,0], width, yerr = forcings[10,:,1], color = 'royalblue', label = 'uv, G=1/6, n=4')
    # ax.bar(label_points + 7*width/2, forcings[11,:,0], width, yerr = forcings[11,:,1], color = 'cornflowerblue', label = 'uv, G=1/3, n=4')
    # ax.bar(label_points + 9*width/2, forcings[12,:,0], width, yerr = forcings[12,:,1], color = 'lightsteelblue', label = 'uv, G=1/1, n=4')
    
    # ax.bar(label_points + 12*width/2, forcings[13,:,0], width, yerr = forcings[13,:,1], color = 'indigo', label = 'uv, G=1/6, bl=1, ramp=1, n=4')
    # ax.bar(label_points + 14*width/2, forcings[14,:,0], width, yerr = forcings[14,:,1], color = 'darkviolet', label = 'uv, G=1/6, bl=1, ramp=4, n=4')
    
    # # note to self: I have checked the order of these (and initial cube loads order) and they are defo correct!
    
    # ax.set_xticks(label_points)
    # ax.set_xticklabels(labels)
    # ax.set_ylim(-2.2, 3)
    # plt.legend(fontsize = 'x-small', ncol = 2, loc = 'upper left')
    # ax.text(2,-1.8, sky+' sky', ha = 'center', fontsize = 'large')
    # ax.axhline(y=0, xmin = 0, xmax = 1, color = 'darkgrey', linestyle = ':')
    # ax.set_ylabel(u'ERF / W m$^{-2}$')
    # plt.tight_layout()
    # plt.savefig(plot_dir + 'su_forcing_comparison_bar_chart_varing_G_' + sky + '_sky', dpi = 400)
    # plt.show()
    
    
    ##### Forcing diffs calculations #####
    
    adjust_rounding = 2
    uncertainty_rounding = 2
    
    # ERF = free
    net_erf = np.round( forcings[0,0,0] ,adjust_rounding)
    net_erf_error = np.round( forcings[0,0,1] ,uncertainty_rounding)
    sw_erf = np.round( forcings[0,1,0] ,adjust_rounding)
    sw_erf_error = np.round( forcings[0,1,1] ,uncertainty_rounding)
    lw_erf = np.round( forcings[0,2,0] ,adjust_rounding)
    lw_erf_error = np.round( forcings[0,2,1] ,uncertainty_rounding)
    
    
    # uv-nudged
    net_uv_nudged = np.round( forcings[2,0,0] ,adjust_rounding)
    net_uv_nudged_error = np.round( forcings[2,0,1] ,uncertainty_rounding)
    sw_uv_nudged = np.round( forcings[2,1,0] ,adjust_rounding)
    sw_uv_nudged_error = np.round( forcings[2,1,1] ,uncertainty_rounding)
    lw_uv_nudged = np.round( forcings[2,2,0] ,adjust_rounding)
    lw_uv_nudged_error = np.round( forcings[2,2,1] ,uncertainty_rounding)
    

    # uvt-nudged
    net_uvt_nudged = np.round( forcings[1,0,0] ,adjust_rounding)
    net_uvt_nudged_error = np.round( forcings[1,0,1] ,uncertainty_rounding)
    sw_uvt_nudged = np.round( forcings[1,1,0] ,adjust_rounding)
    sw_uvt_nudged_error = np.round( forcings[1,1,1] ,uncertainty_rounding)
    lw_uvt_nudged = np.round( forcings[1,2,0] ,adjust_rounding)
    lw_uvt_nudged_error = np.round( forcings[1,2,1] ,uncertainty_rounding)
    
    
    # Circulation adjustment = free - uv nudged
    net_circ_adjust = np.round( forcings[0,0,0] - forcings [2,0,0] ,adjust_rounding)
    net_circ_adjust_error = np.round( forcings[0,0,1] + forcings [2,0,1] ,uncertainty_rounding)
    sw_circ_adjust = np.round( forcings[0,1,0] - forcings [2,1,0] ,adjust_rounding)
    sw_circ_adjust_error = np.round( forcings[0,1,1] + forcings [2,1,1] ,uncertainty_rounding)
    lw_circ_adjust = np.round( forcings[0,2,0] - forcings [2,2,0] ,adjust_rounding)
    lw_circ_adjust_error = np.round( forcings[0,2,1] + forcings [2,2,1] ,uncertainty_rounding)
    
    
    # T adjustment = uv nudged - uvtheta nudged 
    net_T_adjust = np.round( forcings[2,0,0] - forcings [1,0,0] ,adjust_rounding)
    net_T_adjust_error = np.round( forcings[2,0,1] + forcings [1,0,1] ,uncertainty_rounding)
    sw_T_adjust = np.round( forcings[2,1,0] - forcings [1,1,0] ,adjust_rounding)
    sw_T_adjust_error = np.round( forcings[2,1,1] + forcings [1,1,1] ,uncertainty_rounding)
    lw_T_adjust = np.round( forcings[2,2,0] - forcings [1,2,0] ,adjust_rounding)
    lw_T_adjust_error = np.round( forcings[2,2,1] + forcings [1,2,1] ,uncertainty_rounding)
    
    erf = [net_erf, sw_erf, lw_erf]
    erf_error = [net_erf_error, sw_erf_error, lw_erf_error]
    
    circ_adjust = [net_circ_adjust, sw_circ_adjust, lw_circ_adjust]
    circ_adjust_error = [net_circ_adjust_error, sw_circ_adjust_error, lw_circ_adjust_error]
    
    T_adjust = [net_T_adjust, sw_T_adjust, lw_T_adjust]
    T_adjust_error = [net_T_adjust_error, sw_T_adjust_error, lw_T_adjust_error]


    print('\n%%% ',sky,' %%%')
    
    print('\nerf: ')
    print('net: ', net_erf, ' +/-', net_erf_error)
    print('sw: ', sw_erf, ' +/-', sw_erf_error)
    print('lw: ', lw_erf, ' +/-', lw_erf_error)
    
    print('\nuv-nudged: ')
    print('net: ', net_uv_nudged, ' +/-', net_uv_nudged_error)
    print('sw: ', sw_uv_nudged, ' +/-', sw_uv_nudged_error)
    print('lw: ', lw_uv_nudged, ' +/-', lw_uv_nudged_error)

    print('\nuvt-nudged: ')
    print('net: ', net_uvt_nudged, ' +/-', net_uvt_nudged_error)
    print('sw: ', sw_uvt_nudged, ' +/-', sw_uvt_nudged_error)
    print('lw: ', lw_uvt_nudged, ' +/-', lw_uvt_nudged_error)

    print('\nCirculation adjustment: ')
    print('net: ', net_circ_adjust, ' +/-', net_circ_adjust_error)
    print('sw: ', sw_circ_adjust, ' +/-', sw_circ_adjust_error)
    print('lw: ', lw_circ_adjust, ' +/-', lw_circ_adjust_error)
    
    print('\nT adjustment: ')
    print('net: ', net_T_adjust, ' +/-', net_T_adjust_error)
    print('sw: ', sw_T_adjust, ' +/-', sw_T_adjust_error)
    print('lw: ', lw_T_adjust, ' +/-', lw_T_adjust_error)
    
    
        
    labels = ['Net', 'SW', 'LW']
    
    font = {'size' : 12}
    plt.rc('font', **font)
    
    label_points = np.arange(len(labels))
    width = 0.2
    
    fig, ax = plt.subplots()
    
    ax.bar(label_points - 2.5*width/2, erf, width, yerr = erf_error, color = 'indigo', capsize = 4, label = 'ERF')
    ax.bar(label_points - 0*width/2, circ_adjust, width, yerr = circ_adjust_error, color = 'darkviolet', capsize = 4, label = 'Circulation adjustment')
    ax.bar(label_points + 2.5*width/2, T_adjust, width, yerr = T_adjust_error, color = 'thistle', capsize = 4, label = 'T adjustment')
    
    ax.set_xticks(label_points)
    ax.set_xticklabels(labels)
    ax.set_ylim(-2, 1)
    plt.legend(fontsize = 'medium', ncol = 1, loc = 'lower right')
    ax.text(2.35,0.75, 'SU: '+sky+' sky', ha = 'right', fontsize = 'large')
    ax.axhline(y=0, xmin = 0, xmax = 1, color = 'darkgrey', linestyle = ':')
    ax.set_ylabel(u'Radiative forcing / W m$^{-2}$')
    plt.tight_layout()
    plt.savefig(plot_dir + 'su_forcing_erf_T_circ_adjust_bar_chart_' + sky + '_sky', dpi = 300)
    plt.show()