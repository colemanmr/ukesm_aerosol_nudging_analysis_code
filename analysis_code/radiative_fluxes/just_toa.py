#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 23:18:16 2020

@author: nn819853
"""

import iris
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input_pp_file', type = str, help = 'pp file containing diags on levels to extract TOA from')
args = parser.parse_args()

index1 = args.input_pp_file.find('and')
index2 = args.input_pp_file.find('ap4')
target = args.input_pp_file[:index1 - 7] + args.input_pp_file[index2 + 3 :]

diag_names = ['m01s01i517', \
              'm01s02i517', \
              'm01s01i519', \
              'm01s02i519']

clean_sw_up, clean_lw_up, clear_clean_sw_up, clear_clean_lw_up = \
iris.load(args.input_pp_file)

toa_clean_sw_up = clean_sw_up[:,-1,:,:]
toa_clean_lw_up = clean_lw_up[:,-1,:,:]
toa_clear_clean_sw_up = clear_clean_sw_up[:,-1,:,:]
toa_clear_clean_lw_up = clear_clean_lw_up[:,-1,:,:]

cubes = toa_clean_sw_up, toa_clean_lw_up, \
toa_clear_clean_sw_up, toa_clear_clean_lw_up

iris.save(cubes, target, append=True)
