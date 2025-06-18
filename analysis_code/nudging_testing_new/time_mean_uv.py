
import sys
sys.path.append('/home/users/nn819853/Documents/python_code')

import diagnostics.radiative_fluxes.fluxes_module as flux_mod
import iris
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input_pp_file', type = str, help = 'pp file containing monthly mean uand v-winds diagnostics')
parser.add_argument('output_name', type = str, help = 'output file name')
args = parser.parse_args()

u_wind_month_mean = iris.load_cube(args.input_pp_file, 'x_wind')
v_wind_month_mean = iris.load_cube(args.input_pp_file, 'y_wind')

u_wind_annual_mean = flux_mod.annual_mean(u_wind_month_mean)
v_wind_annual_mean = flux_mod.annual_mean(v_wind_month_mean)

time_mean_u, time_stdev_u, time_double_SE_u = flux_mod.time_mean_cube(u_wind_annual_mean)
time_mean_v, time_stdev_v, time_double_SE_v = flux_mod.time_mean_cube(v_wind_annual_mean)

cubes = iris.cube.CubeList([time_mean_u, time_stdev_u, time_double_SE_u, time_mean_v, time_stdev_v, time_double_SE_v])

time_mean_u.rename('mean_u_wind')
time_stdev_u.rename('stdev_u_wind')
time_double_SE_u.rename('double_SE_u_wind')
time_mean_v.rename('mean_v_wind')
time_stdev_v.rename('stdev_v_wind')
time_double_SE_v.rename('double_SE_v_wind')

for cube in cubes:
    cube.units = 'm s-1'

iris.save(cubes, args.output_name)
