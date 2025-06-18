#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 14:35:24 2021

@author: nn819853
"""

import sys
sys.path.append('/home/users/nn819853/Documents/python_code')

# import diagnostics.radiative_fluxes.fluxes_module as flux_mod
import diagnostics.file_locations_module as file_loc
import numpy as np
import matplotlib.pyplot as plt
import cf


diag_loc = file_loc.diag_dir + 'nudging_testing_post_mc4/theta_inc_diags/'

# filename = diag_loc + 'month_mean_nudge_inc_theta_cb108.pp'
filename = diag_loc + 'hourly_other_inc_theta_cb108_2014_fb_28_29.pp'
filename2 = diag_loc + 'hourly_other_inc_theta_cb108_2014_01_01-02.pp'


# filename = file_loc.diag_dir +\
#     'net_flux/br793_net_flux_control_nudging_free.pp'

# fields = cf.read(filename, um = {'fmt': 'PP', 'version': 11.1})
fields1 = cf.read(diag_loc + 'hourly_other_inc_theta_cb108_2014_01_01-02.pp')
# fields2 = cf.read(filename2)



