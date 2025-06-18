#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 11:51:43 2020

@author: nn819853
"""

import diagnostics.radiative_fluxes.fluxes_module as flux_mod
import diagnostics.file_locations_module as file_loc
import iris
import argparse
import numpy as np

#!!! Need to constrain end number of years !!!#

# Allow pp file with toa fluxes and spinup to be passed as argument to script
parser = argparse.ArgumentParser()
parser.add_argument('input_pp_file',\
                    type = str,\
                    help = 'pp file of diags to calculate toa fluxes')
parser.add_argument('spinup',\
                    type = int,\
                    help = 'number of years spinup')
args = parser.parse_args()

# Write list of skytypes for loop below
sky_type_list = ['all', 'clear', 'clean', 'clearclean']

for sky_type_type in sky_type_list:
    
    # Calculate toa flux annual area means, multiannual mean and overall mean
    area_sw, area_lw, area_net,\
    time_sw, time_lw, time_net,\
    area_time_sw, area_time_lw, area_time_net = \
    flux_mod.toa_flux(args.input_pp_file, sky_type = sky_type_type, \
                      spinup_years = args.spinup) 
    
#    area_sw.rename('annual_area_meaned_total_sw_down_flux')
#    area_lw.rename('annual_area_meaned_total_lw_down_flux')
#    area_net.rename('annual_area_meaned_total_net_down_flux')
#    
#    time_sw[0].rename('multiannual_mean_total_sw_down_flux')
#    time_lw[0].rename('multiannual_mean_total_lw_down_flux')
#    time_net[0].rename('multiannual_mean_total_net_down_flux')
#    
#    area_time_sw[0].rename('multiannual_area_mean_total_sw_down_flux')
#    area_time_lw[0].rename('multiannual_area_mean_total_lw_down_flux')
#    area_time_net[0].rename('multiannual_area_mean_total_net_down_flux')
#    
#    area_time_sw[2].rename('multiannual_area_mean_total_sw_down_flux_2SE')
#    area_time_lw[2].rename('multiannual_area_mean_total_lw_down_flux_2SE')
#    area_time_net[2].rename('multiannual_area_mean_total_net_down_flux_2SE')
    
    # Save flux cubes to cubelist
    cubes = iris.cube.CubeList([area_sw, area_lw, area_net, 
                                time_sw[0], time_lw[0], time_net[0],
                                #time_sw[2], time_lw[2], time_net[2],
                                area_time_sw[0], area_time_lw[0], area_time_net[0],
                                area_time_sw[2], area_time_lw[2], area_time_net[2]])
    
    # Rename cubes to make loading them elsewhere easier
    names = [
            'annual_area_meaned_total_sw_down_flux',
            'annual_area_meaned_total_lw_down_flux',
            'annual_area_meaned_total_net_down_flux',
            'multiannual_mean_total_sw_down_flux',
            'multiannual_mean_total_lw_down_flux',
            'multiannual_mean_total_net_down_flux',
            'multiannual_area_mean_total_sw_down_flux',
            'multiannual_area_mean_total_lw_down_flux',
            'multiannual_area_mean_total_net_down_flux',
            'multiannual_area_mean_total_sw_down_flux_2SE',
            'multiannual_area_mean_total_lw_down_flux_2SE',
            'multiannual_area_mean_total_net_down_flux_2SE'
            ]
    
    for i in np.arange(len(cubes)):
        cubes[i].rename(names[i])
    
    # Set all cube units to W m^-2
    for cube in cubes:
        cube.units = 'W m-2'
            
    # Write cubes to .nc file
    diag_dir = file_loc.diag_dir + 'net_flux/'
    target = diag_dir + args.input_pp_file[:-3] + '_calc_fluxes_' \
    + sky_type_type + '_sky_' + str(args.spinup) + 'yr_spinup.nc'
    iris.save(cubes, target)