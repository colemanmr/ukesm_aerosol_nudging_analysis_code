#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 10:32:32 2021

@author: nn819853
"""

import sys
sys.path.append('/home/users/nn819853/Documents/python_code')

import diagnostics.radiative_fluxes.fluxes_module as flux_mod
import iris
import numpy as np
import argparse

input_file = '/storage/silver/scenario/nn819853/diags/nudging_testing_post_mc4/uv_pres_lev/uv_pres_lev_mon_mean_br793.pp'

month_mean = iris.load(input_file)

heavy = month_mean[0]
u = month_mean[4]
v = month_mean[8]


heavy_annua_mean = flux_mod.annual_mean(heavy[:48])
u_annua_mean = flux_mod.annual_mean(u[:48])
v_annua_mean = flux_mod.annual_mean(v[:48])


time_mean_heavy, time_stdev_heavy, time_double_SE_heavy = flux_mod.time_mean_cube(heavy_annua_mean)
time_mean_u, time_stdev_u, time_double_SE_u = flux_mod.time_mean_cube(u_annua_mean)
time_mean_v, time_stdev_v, time_double_SE_v = flux_mod.time_mean_cube(v_annua_mean)

cubes = iris.cube.CubeList([time_mean_heavy, time_stdev_heavy, time_double_SE_heavy,
                            time_mean_u, time_stdev_u, time_double_SE_u,
                            time_mean_v, time_stdev_v, time_double_SE_v])


time_mean_heavy.rename('mean_heavyside')
time_stdev_heavy.rename('stdev_heavyside')
time_double_SE_heavy.rename('double_SE_heavyside')

time_mean_u.rename('mean_u_wind')
time_stdev_u.rename('stdev_u_wind')
time_double_SE_u.rename('double_SE_u_wind')

time_mean_v.rename('mean_v_wind')
time_stdev_v.rename('stdev_v_wind')
time_double_SE_v.rename('double_SE_v_wind')


wind_cubes = iris.cube.CubeList([time_mean_u, time_stdev_u, time_double_SE_u, time_mean_v, time_stdev_v, time_double_SE_v])
for cube in wind_cubes:
    cube.units = 'm s-1'


cubes = iris.cube.CubeList([time_mean_u, time_stdev_u, time_double_SE_u, 
                            time_mean_v, time_stdev_v, time_double_SE_v, 
                            time_mean_heavy, time_stdev_heavy, time_double_SE_heavy])


iris.save(cubes, '/storage/silver/scenario/nn819853/diags/nudging_testing_post_mc4/uv_pres_lev/uv_pres_lev_time_mean_br793_2015-2018.pp')