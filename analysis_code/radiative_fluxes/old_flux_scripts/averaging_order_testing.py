#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 10:35:41 2021

@author: nn819853
"""

import iris
import diagnostics.file_locations_module as file_loc
import diagnostics.radiative_fluxes.fluxes_module as flux_mod

diag_dir = file_loc.diag_dir + 'net_flux/'

cont = diag_dir + 'by937_net_flux_control_nudging_uvt_calc_fluxes_all_sky_1yr_spinup.nc'
pert = diag_dir + 'by965_net_flux_su_nudging_uvt_calc_fluxes_all_sky_1yr_spinup.nc'

spinup = 1

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

# Load control fluxes to cubes
control_area_sw, control_area_lw, control_area_net, \
control_time_sw, control_time_lw, control_time_net, \
control_area_time_sw, control_area_time_lw, control_area_time_net, \
control_area_time_double_se_sw, control_area_time_double_se_lw, control_area_time_double_se_net = \
iris.load(cont, names)

# Load perturbed fluxes to cubes
perturbed_area_sw, perturbed_area_lw, perturbed_area_net, \
perturbed_time_sw, perturbed_time_lw, perturbed_time_net, \
perturbed_area_time_sw, perturbed_area_time_lw, perturbed_area_time_net, \
perturbed_area_time_double_se_sw, perturbed_area_time_double_se_lw, perturbed_area_time_double_se_net = \
iris.load(pert, names)

######## Method 1 #########

# Calculate annual area meaned forcings for forcing time series plots
area_mean_net_forcing = flux_mod.cube_diff(control_area_net,\
                                           perturbed_area_net)
area_mean_sw_forcing = flux_mod.cube_diff(control_area_sw,\
                                           perturbed_area_sw)
area_mean_lw_forcing = flux_mod.cube_diff(control_area_lw,\
                                           perturbed_area_lw)

## Calculate time meaned forcing for forcing maps
#time_mean_net_forcing = flux_mod.cube_diff(control_time_net,\
#                                           perturbed_time_net)
#time_mean_sw_forcing = flux_mod.cube_diff(control_time_sw,\
#                                           perturbed_time_sw)
#time_mean_lw_forcing = flux_mod.cube_diff(control_time_lw,\
#                                           perturbed_time_lw)
##!! FIX: This should really exclude the spinup which currently doesn't!!! !!#

# Claculate multiannual area meaned overall forcing values
area_time_net_forcing1 = flux_mod.time_mean_cube(area_mean_net_forcing[spinup:])
area_time_sw_forcing1 = flux_mod.time_mean_cube(area_mean_sw_forcing[spinup:])
area_time_lw_forcing1 = flux_mod.time_mean_cube(area_mean_lw_forcing[spinup:])

####### Method 2 #########

area_time_net_forcing2 = control_area_time_net - perturbed_area_time_net
area_time_sw_forcing2 = control_area_time_sw - perturbed_area_time_sw
area_time_lw_forcing2 = control_area_time_lw - perturbed_area_time_lw