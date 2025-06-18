#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 17 15:11:36 2021

@author: nn819853
"""

import sys
sys.path.append('/home/users/nn819853/Documents/python_code')

# import diagnostics.radiative_fluxes.fluxes_module as flux_mod
import diagnostics.file_locations_module as file_loc
# import numpy as np
import iris
# import iris.plot as iplt
# import matplotlib.pyplot as plt

import datetime
from iris.time import PartialDateTime
import cftime


diag_loc = file_loc.diag_dir + 'nudging_testing_post_mc4/theta_inc_diags/'

# filename = diag_loc + 'month_mean_nudge_inc_theta_cb108.pp'
filename = diag_loc + 'hourly_other_inc_theta_cb108_2014_fb_28_29.pp'

# cube = iris.load_cube(filename)


# import iris.fileformats.pp as ipp

# fields = ipp.load(filename)

# fields = list(fields)

# for f in fields:
#     f.lbtim.ic = 2

# print('lbyr\tlbmon\tlbdat\tlbyrd\tlbmond\tlbdatd')
# for f in fields:
#     print('{f.lbyr}\t{f.lbmon}\t{f.lbdat}\t'
#           '{f.lbyrd}\t{f.lbmond}\t{f.lbdatd}'.format(f=f))

# ipp.save_fields(fields, 'test.pp')

    










start = cftime.Datetime360Day(2014, 2, 28, 0)
end = cftime.Datetime360Day(2014, 2, 28, 23)

time_selection = iris.Constraint(time = lambda c: start <= c.point <= end)
iris.load_cube(filename, time_selection)

# pdt1 = PartialDateTime(year = 2014, month = 2, day = 29)
# pdt2 = PartialDateTime(year = 2014, month = 2, day = 30)
# dt = datetime.datetime.strptime('20140229T0000Z', '%Y%m%dT%H%MZ')

# date_constraint = iris.Constraint(time = pdt)
# cube = iris.load_cube(filename, date_constraint)

# st_swithuns_daterange_07 = iris.Constraint(
#     time=lambda cell: pdt1 <= cell.point < pdt2)
# within_st_swithuns_07 = iris.load_cubes(filename, st_swithuns_daterange_07)


