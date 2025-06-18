import iris
import numpy as np
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('input_pp_file', type = str, help = 'pp file containing monthly mean tropopause height diagnostic')
parser.add_argument('output_name', type = str, help = 'output file name')
args = parser.parse_args()


cube = iris.load_cube(args.input_pp_file)

# Mean over time
time_mean_cube = cube.collapsed('time', iris.analysis.MEAN)
   
lon_mean_cube = time_mean_cube.collapsed('longitude', iris.analysis.MEAN)

lon_mean_cube.rename('time_longitude_mean_tropopoause_height')

iris.save(lon_mean_cube, args.output_name)
