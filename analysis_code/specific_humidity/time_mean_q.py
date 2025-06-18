#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 20 15:06:33 2021

@author: nn819853
"""

import sys
sys.path.append('/home/users/nn819853/Documents/python_code')

import diagnostics.radiative_fluxes.fluxes_module as flux_mod
import iris
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input_pp_file', type = str, help = 'pp file containing monthly mean  diagnostic')
parser.add_argument('output_name', type = str, help = 'output file name')
args = parser.parse_args()

month_means_cube = iris.load_cube(args.input_pp_file)

annual_means_cube = flux_mod.annual_mean(month_means_cube)

time_mean, time_stdev, time_double_SE = flux_mod.time_mean_cube(annual_means_cube)

cubes = iris.cube.CubeList([time_mean, time_stdev, time_double_SE])

time_mean.rename('time_mean_q')
time_stdev.rename('time_stdev_q')
time_double_SE.rename('time_double_SE_q')

for cube in cubes:
    cube.units = 'kg kg-1'

iris.save(cubes, args.output_name)