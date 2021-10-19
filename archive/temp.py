#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 11:46:44 2021

@author: shivambhatnagar
"""

import pandas as pd

fpath = r'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM Dev/PLCM_Excel/For Submission/Jun 2021/8J834_GENERIC_GENOMICS_TESTING_REPORTING_NHSE2021.csv'

df = pd.read_csv(fpath)

df_old = df

snp_dict = {}

for ref in set(df['SHARED_REFERRAL_IDENTIFIER']):
    df_temp = df.loc[df['SHARED_REFERRAL_IDENTIFIER'] == ref]
    try:        
        snp_dict[ref] = list(df_temp.loc[df_temp['LOCAL_POINT_OF_DELIVERY_CODE'] == 'TESTSNP', 'TURNAROUND_TIME_(CALENDAR_DAYS)'])[0]
    except:
        snp_dict[ref] = ''
    
for ref in set(df['SHARED_REFERRAL_IDENTIFIER']):
    if snp_dict[ref] != '':
        df.loc[(df['LOCAL_POINT_OF_DELIVERY_CODE'] == 'TESTBIOINFO') & (df['SHARED_REFERRAL_IDENTIFIER'] == ref), 'TURNAROUND_TIME_(CALENDAR_DAYS)'] = df.loc[(df['LOCAL_POINT_OF_DELIVERY_CODE'] == 'TESTBIOINFO') & (df['SHARED_REFERRAL_IDENTIFIER'] == ref), 'TURNAROUND_TIME_(CALENDAR_DAYS)'] - snp_dict[ref]
        
   
    
if df.equals(df_old) == True:
    print('no change')
else:
    print('change')