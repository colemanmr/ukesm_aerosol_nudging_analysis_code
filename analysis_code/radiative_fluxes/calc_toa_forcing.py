#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 17:17:32 2020

@author: nn819853
"""

import sys
sys.path.append('/home/users/nn819853/Documents/python_code')

import diagnostics.radiative_fluxes.fluxes_module as flux_mod
import diagnostics.file_locations_module as file_loc
import iris
import argparse
import numpy as np

#!! Note: this won't work if have different number of years in simulations !!#
#!! Perhaps best to do this in another script, as not sure how to do time series !!#
#!! plots otherwise !!#

# Pass two .nc calc_flux files with toa fluxes and spinup specified to script
parser = argparse.ArgumentParser()
parser.add_argument('control_fluxes',\
                    type = str,\
                    help = '.nc file of control toa fluxes to calculate forcing')
parser.add_argument('perturbed_fluxes',\
                    type = str,\
                    help = '.nc file of perturbed toa fluxes to calculate forcing')
parser.add_argument('end_year',\
                    type = int,\
                    help = 'last year to include for time and time_area means')
args = parser.parse_args()

# Cube names for calc flux .nc files
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
##! doesnt need to read the multi annual area mean values !##

# Read spinup from filenames and check same
index1 = args.control_fluxes.find('yr_spinup')
spinup_cont = args.control_fluxes[index1 - 1]

index2 = args.perturbed_fluxes.find('yr_spinup')
spinup_pert = args.perturbed_fluxes[index2 - 1]

if spinup_cont == spinup_pert:
    spinup = int(spinup_cont)
    ##! not sure needs to check spinup is same really? !##
# spinup = 1 # test cf-env

# Load control fluxes to cubes
control_area_sw, control_area_lw, control_area_net, \
control_time_sw, control_time_lw, control_time_net, \
control_area_time_sw, control_area_time_lw, control_area_time_net, \
control_area_time_double_se_sw, control_area_time_double_se_lw, control_area_time_double_se_net = \
iris.load(args.control_fluxes, names)
##! doesnt need to read the multi annual area mean values !##

# Load perturbed fluxes to cubes
perturbed_area_sw, perturbed_area_lw, perturbed_area_net, \
perturbed_time_sw, perturbed_time_lw, perturbed_time_net, \
perturbed_area_time_sw, perturbed_area_time_lw, perturbed_area_time_net, \
perturbed_area_time_double_se_sw, perturbed_area_time_double_se_lw, perturbed_area_time_double_se_net = \
iris.load(args.perturbed_fluxes, names)
##! doesnt need to read the multi annual area mean values !##

# Calculate annual area meaned forcings for forcing time series plots
area_mean_net_forcing = flux_mod.cube_diff(control_area_net[:args.end_year],\
                                           perturbed_area_net[:args.end_year])
area_mean_sw_forcing = flux_mod.cube_diff(control_area_sw[:args.end_year],\
                                           perturbed_area_sw[:args.end_year])
area_mean_lw_forcing = flux_mod.cube_diff(control_area_lw[:args.end_year],\
                                           perturbed_area_lw[:args.end_year])

# Calculate time meaned forcing for forcing maps
time_mean_net_forcing = flux_mod.cube_diff(control_time_net,\
                                           perturbed_time_net)
time_mean_sw_forcing = flux_mod.cube_diff(control_time_sw,\
                                           perturbed_time_sw)
time_mean_lw_forcing = flux_mod.cube_diff(control_time_lw,\
                                           perturbed_time_lw)

# Claculate multiannual area meaned overall forcing values
area_time_net_forcing = flux_mod.time_mean_cube(area_mean_net_forcing[spinup:args.end_year])
area_time_sw_forcing = flux_mod.time_mean_cube(area_mean_sw_forcing[spinup:args.end_year])
area_time_lw_forcing = flux_mod.time_mean_cube(area_mean_lw_forcing[spinup:args.end_year])

# Save flux cubes to cubelist
cubes = iris.cube.CubeList([area_mean_sw_forcing, area_mean_lw_forcing, area_mean_net_forcing, 
                            time_mean_sw_forcing, time_mean_lw_forcing, time_mean_net_forcing,
                            area_time_sw_forcing[0], area_time_lw_forcing[0], area_time_net_forcing[0],
                            area_time_sw_forcing[2], area_time_lw_forcing[2], area_time_net_forcing[2]])

# names to save forcing cubes as
names = [
        'annual_area_meaned_total_sw_down_forcing',
        'annual_area_meaned_total_lw_down_forcing',
        'annual_area_meaned_total_net_down_forcing',
        'multiannual_mean_total_sw_down_forcing',
        'multiannual_mean_total_lw_down_forcing',
        'multiannual_mean_total_net_down_forcing',
        'multiannual_area_mean_total_sw_down_forcing',
        'multiannual_area_mean_total_lw_down_forcing',
        'multiannual_area_mean_total_net_down_forcing',
        'multiannual_area_mean_total_sw_down_forcing_2SE',
        'multiannual_area_mean_total_lw_down_forcing_2SE',
        'multiannual_area_mean_total_net_down_forcing_2SE'
        ]

# rename cubes to forcing names
for i in np.arange(len(cubes)):
    cubes[i].rename(names[i])

# Set all cube units to W m^-2
for cube in cubes:
    cube.units = 'W m-2'

# Write cubes to .nc file
cont_suite_id = args.control_fluxes[:5]
pert_suite_id = args.perturbed_fluxes[:5]

cont_sky_end_index = args.control_fluxes.find('_sky_')
cont_sky_start_index = args.control_fluxes.find('_fluxes_')
cont_sky = args.control_fluxes[cont_sky_start_index + 8: cont_sky_end_index]

pert_sky_end_index = args.perturbed_fluxes.find('_sky_')
pert_sky_start_index = args.perturbed_fluxes.find('_fluxes_')
pert_sky = args.perturbed_fluxes[pert_sky_start_index + 8: pert_sky_end_index]

cont_type_end_index = args.control_fluxes.find('_calc_fluxes_')
cont_type = args.control_fluxes[15:cont_type_end_index]

pert_type_end_index = args.perturbed_fluxes.find('_calc_fluxes_')
pert_type = args.perturbed_fluxes[15:pert_type_end_index]

diag_dir = file_loc.diag_dir + 'net_flux/'
target = diag_dir + 'calc_forcing_' + \
cont_suite_id + '_' + cont_type + '_flux_' + cont_sky + '_sky_' + \
'minus_' + \
pert_suite_id + '_' + pert_type + '_flux_' + pert_sky + '_sky_' + \
spinup_cont + 'yr_spinup.nc'
# target = diag_dir + 'calc_forcing_bz236-bz234_test_all_sky.nc' # test cf-env
iris.save(cubes, target)

#!! maybe add print statements for some values so can check output sensible on command line !##
