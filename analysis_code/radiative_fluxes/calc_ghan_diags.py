#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 11:01:51 2021

@author: nn819853
"""

import sys
sys.path.append('/home/users/nn819853/Documents/python_code')

import diagnostics.radiative_fluxes.fluxes_module as flux_mod
import diagnostics.file_locations_module as file_loc
import iris
import argparse
import numpy as np

### Note: have assumed all sims will have 1 year spinup, so spinup not an ### 
### arg in this script; should be changed in flux and forcing scripts ###

# Pass all, clean, clearclean sky forcings for a pair of suites
parser = argparse.ArgumentParser()
parser.add_argument('all_sky_forcing',\
                    type = str,\
                    help = '.nc file of all sky forcing')
parser.add_argument('clean_sky_forcing',\
                    type = str,\
                    help = '.nc file of clean sky forcing')
parser.add_argument('clearclean_sky_forcing',\
                    type = str,\
                    help = '.nc file of clearclean sky forcing')
args = parser.parse_args()

spinup = 1

# Names used for loading forcing cubes
names = [
        'annual_area_meaned_total_sw_down_forcing',
        'annual_area_meaned_total_lw_down_forcing',
        'annual_area_meaned_total_net_down_forcing',
        'multiannual_mean_total_sw_down_forcing',
        'multiannual_mean_total_lw_down_forcing',
        'multiannual_mean_total_net_down_forcing'
        ]

# Load all sky forcing cubes
all_sky_area_sw, all_sky_area_lw, all_sky_area_net, \
all_sky_time_sw, all_sky_time_lw, all_sky_time_net = \
iris.load(args.all_sky_forcing, names)

# Load clean sky forcing cubes
clean_sky_area_sw, clean_sky_area_lw, clean_sky_area_net, \
clean_sky_time_sw, clean_sky_time_lw, clean_sky_time_net = \
iris.load(args.clean_sky_forcing, names)

# Load clearclean sky forcing cubes
clearclean_sky_area_sw, clearclean_sky_area_lw, clearclean_sky_area_net, \
clearclean_sky_time_sw, clearclean_sky_time_lw, clearclean_sky_time_net = \
iris.load(args.clearclean_sky_forcing, names)


#dre_area_sw = all_sky_area_sw - clean_sky_area_sw
#print(all_sky_area_sw, clean_sky_area_sw, dre_area_sw)

########### Direct aerosol effect calcualtions ################

# Calculate annual area meaned forcings for forcing time series plots
dre_area_mean_net_forcing = flux_mod.cube_diff(all_sky_area_net,\
                                           clean_sky_area_net)
dre_area_mean_sw_forcing = flux_mod.cube_diff(all_sky_area_sw,\
                                           clean_sky_area_sw)
dre_area_mean_lw_forcing = flux_mod.cube_diff(all_sky_area_lw,\
                                           clean_sky_area_lw)

#print(dre_area_mean_sw_forcing)

# Calculate time meaned forcing for forcing maps
dre_time_mean_net_forcing = flux_mod.cube_diff(all_sky_time_net,\
                                           clean_sky_time_net)
dre_time_mean_sw_forcing = flux_mod.cube_diff(all_sky_time_sw,\
                                           clean_sky_time_sw)
dre_time_mean_lw_forcing = flux_mod.cube_diff(all_sky_time_lw,\
                                           clean_sky_time_lw)

# Calculate multiannual area meaned overall forcing values
dre_area_time_net_forcing = flux_mod.time_mean_cube(dre_area_mean_net_forcing[spinup:])
dre_area_time_sw_forcing = flux_mod.time_mean_cube(dre_area_mean_sw_forcing[spinup:])
dre_area_time_lw_forcing = flux_mod.time_mean_cube(dre_area_mean_lw_forcing[spinup:])

#print(dre_area_time_sw_forcing)

# Save flux cubes to cubelist
dre_cubes = iris.cube.CubeList([dre_area_mean_sw_forcing, dre_area_mean_lw_forcing, dre_area_mean_net_forcing, 
                            dre_time_mean_sw_forcing, dre_time_mean_lw_forcing, dre_time_mean_net_forcing,
                            dre_area_time_sw_forcing[0], dre_area_time_lw_forcing[0], dre_area_time_net_forcing[0],
                            dre_area_time_sw_forcing[2], dre_area_time_lw_forcing[2], dre_area_time_net_forcing[2]])

########### Cloud effect calcualtions ################

# Calculate annual area meaned forcings for forcing time series plots
cre_area_mean_net_forcing = flux_mod.cube_diff(clean_sky_area_net,\
                                           clearclean_sky_area_net)
cre_area_mean_sw_forcing = flux_mod.cube_diff(clean_sky_area_sw,\
                                           clearclean_sky_area_sw)
cre_area_mean_lw_forcing = flux_mod.cube_diff(clean_sky_area_lw,\
                                           clearclean_sky_area_lw)

# Calculate time meaned forcing for forcing maps
cre_time_mean_net_forcing = flux_mod.cube_diff(clean_sky_time_net,\
                                           clearclean_sky_time_net)
cre_time_mean_sw_forcing = flux_mod.cube_diff(clean_sky_time_sw,\
                                           clearclean_sky_time_sw)
cre_time_mean_lw_forcing = flux_mod.cube_diff(clean_sky_time_lw,\
                                           clearclean_sky_time_lw)

# Calculate multiannual area meaned overall forcing values
cre_area_time_net_forcing = flux_mod.time_mean_cube(cre_area_mean_net_forcing[spinup:])
cre_area_time_sw_forcing = flux_mod.time_mean_cube(cre_area_mean_sw_forcing[spinup:])
cre_area_time_lw_forcing = flux_mod.time_mean_cube(cre_area_mean_lw_forcing[spinup:])

# Save flux cubes to cubelist
cre_cubes = iris.cube.CubeList([cre_area_mean_sw_forcing, cre_area_mean_lw_forcing, cre_area_mean_net_forcing, 
                            cre_time_mean_sw_forcing, cre_time_mean_lw_forcing, cre_time_mean_net_forcing,
                            cre_area_time_sw_forcing[0], cre_area_time_lw_forcing[0], cre_area_time_net_forcing[0],
                            cre_area_time_sw_forcing[2], cre_area_time_lw_forcing[2], cre_area_time_net_forcing[2]])

########################################################

# names to save forcing cubes as
save_names = [
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

# rename cubes to forcing names and set all cube units to W m^-2
for i in np.arange(len(dre_cubes)):
    dre_cubes[i].rename(save_names[i])
    cre_cubes[i].rename(save_names[i])
    
    dre_cubes[i].units = 'W m-2'
    cre_cubes[i].units = 'W m-2'

# Save cubes to a dre and cre file each

diag_dir = file_loc.diag_dir + 'net_flux/'
dre_target = diag_dir + args.all_sky_forcing.replace('all', 'dre')
cre_target = diag_dir + args.all_sky_forcing.replace('all', 'cre')

iris.save(dre_cubes, dre_target)
iris.save(cre_cubes, cre_target)

