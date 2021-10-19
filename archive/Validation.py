#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 16:39:37 2021

@author: shivambhatnagar
"""


import pandas as pd

date = 'Jun 2021'

fpath = f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM Dev/PLCM_Excel/Dev/{date}/PLCM_v0.xlsx'
fpath2 = f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM Dev/Data/Bio/{date}/Tracker_val.csv'
df = pd.read_excel(fpath)
df_tracker = pd.read_csv(fpath2)

# Number Checks

referrals = list(set(list(df['NGIS_REFERRAL_IDENTIFIER'])))

ref_samp = {}
out_dict = {}

for ref in referrals:
    ref_samp[ref] = []
    out_dict[ref] = []

for ref in referrals:
    ref_samp[ref].append(df.loc[df['NGIS_REFERRAL_IDENTIFIER']==ref, ['SAMPLE_IDENTIFIER']])

for k,v in ref_samp.items():
    out_dict[k].append(list(set(list(v[0]['SAMPLE_IDENTIFIER']))))
    
num_samples = 0

for k,v in out_dict.items():
    for el in v:
        for s in el:            
            num_samples += 1
            
# Referrals in Tracker not in PLCM
            
diff = set(list(df_tracker['Referral ID'])) - set(referrals)

# Referrals in PLCM not in Tracker

diff_reverse = set(referrals) - set(list(df_tracker['Referral ID']))


# Null Checks
any_null = []
for col in df.columns:
    count = 0
    if 'nan' in [str(x) for x in list(df[col])]:
        any_null.append((col, [str(x) for x in list(df[col])].count('nan')))
        
any_null.sort()


# Schema Checks
df_schema = pd.read_excel(r'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM Dev/Data/NHSE Docs/Specification/Schema_202122.xlsx',sheet_name='Specification')
    
cols = list(df_schema['Data Element'])
cols = [x.replace(' ', '_', 10) for x in cols]

col_diff = set(df.columns) - set(cols)


# Reporting
flag = True

print(f'There are {len(referrals)} referrals in this submission and {num_samples} samples')

if diff:
    print(f'There are {len(diff)} referrals in the tracker and not in the PLCM, speak to Jonny')
    flag = False
elif diff_reverse:
    print(f'There are {len(diff_reverse)} referrals in the PLCM and not in the Tracker, speak to Jonny')
    flag = False
else:
    print('There are no differences between the samples tracker and PLCM')
    

if col_diff:
    print(f'There are {len(col_diff)} columns that dont have the correct name as in the specification')
    flag = False
else:
    print('The schema is correct')
    
if flag == True:
    print('Ready to submit')
else:
    print('File not ready to submit, needs changes')







            
            