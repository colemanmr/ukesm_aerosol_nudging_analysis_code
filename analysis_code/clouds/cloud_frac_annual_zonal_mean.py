#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 11:13:57 2021

@author: nn819853
"""

"""
Script to determine annually averaged zonal mean cloud fractions (00266)
from monthly mean cloud fraction diagnostic output, and save as .nc files
for further analysis
"""

import sys
sys.path.append('/home/users/nn819853/Documents/python_code')

import iris
import diagnostics.radiative_fluxes.fluxes_module as flux_mod
import argparse 

parser = argparse.ArgumentParser()
parser.add_argument('diag_file', type = str, \
                    help = 'pp file containing monthly mean cloud diagnostics')
args = parser.parse_args()

# load cloud fraction diag file
cube = iris.load_cube(args.diag_file, \
                      'cloud_volume_fraction_in_atmosphere_layer')

# ensure only full years included in averaging
annual_mean = flux_mod.annual_mean(cube)

# remove spinup (1 year)
annual_mean_no_spin = annual_mean[1:,:,:,:]

# determine annual zonal mean
annual_zonal_mean = annual_mean_no_spin.collapsed('longitude', iris.analysis.MEAN)

# rename cube
annual_zonal_mean.rename('annual_zonal_mean_cloud_volume_fraction_in_atmosphere_layer')

# save annual zonal mean cube
suite_id = args.diag_file[11:16]
target = 'cloud_frac_annual_zonal_mean_' + suite_id 
# target = 'test_name.nc'
iris.save(annual_zonal_mean, target)