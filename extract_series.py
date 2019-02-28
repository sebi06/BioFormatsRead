# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 22:14:48 2019

@author: M1SRH
"""

def calc_series_pylevel(num_series, num_levels, pylevel=0):

    series_per_level = int(num_series/num_levels)
    print('Series per level', series_per_level)
    series_ids = []
    
    if num_levels == 1:
        series_ids = list(range(0, num_series))
        
    if num_levels > 1:
        for p in range(0, series_per_level):
            series_ids.append(p * num_levels + pylevel)
    
    return series_ids

num_series = 8
num_levels = 4
level = 1


series_ids = calc_series_pylevel(num_series, num_levels, pylevel=level)
 
print(series_ids)
    