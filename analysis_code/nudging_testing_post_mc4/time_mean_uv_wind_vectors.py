
import sys
sys.path.append('/home/users/nn819853/Documents/python_code')

import diagnostics.radiative_fluxes.fluxes_module as flux_mod
import iris
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input_pp_file', type = str, help = 'pp file containing monthly mean u and v-winds and heavyside diagnostics on p levels')
parser.add_argument('output_name', type = str, help = 'output file name')
args = parser.parse_args()

in_cubes = iris.load(args.input_pp_file)
# in_cubes = iris.load('/storage/silver/scenario/nn819853/diags/nudging_testing_post_mc4/uv_pres_lev/uv_pres_lev_mon_mean_br793.pp')

heavyside = in_cubes[0]
u_wind = in_cubes[4]
v_wind = in_cubes[8]


heavyside_annual_mean = flux_mod.annual_mean(heavyside)
u_wind_annual_mean = flux_mod.annual_mean(u_wind)
v_wind_annual_mean = flux_mod.annual_mean(v_wind)

time_mean_heavy, time_stdev_heavy, time_double_SE_heavy = flux_mod.time_mean_cube(heavyside_annual_mean)
time_mean_u, time_stdev_u, time_double_SE_u = flux_mod.time_mean_cube(u_wind_annual_mean)
time_mean_v, time_stdev_v, time_double_SE_v = flux_mod.time_mean_cube(v_wind_annual_mean)


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

iris.save(cubes, args.output_name)