
import sys
sys.path.append('/home/users/nn819853/Documents/python_code')

import diagnostics.radiative_fluxes.fluxes_module as flux_mod
import iris
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input_pp_file', type = str, help = 'pp file containing monthly mean theta diagnostic')
parser.add_argument('output_name', type = str, help = 'output file name')
args = parser.parse_args()

month_means_cube = iris.load_cube(args.input_pp_file)

annual_means_cube = flux_mod.annual_mean(month_means_cube)

time_mean_theta, time_stdev_theta, time_double_SE_theta = flux_mod.time_mean_cube(annual_means_cube)

cubes = [time_mean_theta, time_stdev_theta, time_double_SE_theta]

iris.save(cubes, args.output_name)
