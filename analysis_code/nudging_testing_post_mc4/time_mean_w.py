
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

w_wind_month_mean = iris.load_cube(args.input_pp_file, 'upward_air_velocity')

w_wind_annual_mean = flux_mod.annual_mean(w_wind_month_mean)

time_mean_w, time_stdev_w, time_double_SE_w = flux_mod.time_mean_cube(w_wind_annual_mean)

cubes = iris.cube.CubeList([time_mean_w, time_stdev_w, time_double_SE_w])

time_mean_w.rename('mean_w_wind')
time_stdev_w.rename('stdev_w_wind')
time_double_SE_w.rename('double_SE_w_wind')

for cube in cubes:
    cube.units = 'm s-1'

iris.save(cubes, args.output_name)
