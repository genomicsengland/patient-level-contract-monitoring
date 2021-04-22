#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 16:39:37 2021

@author: shivambhatnagar
"""


import pandas as pd

date = 'March 2021'

fpath = f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM/PLCM_Excel/Dev/{date}/PLCM_v0.xlsx'
#fpath2 = f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM/Data/Bio/{date}/plcm_feb.txt'
df = pd.read_excel(fpath)
#df_tracker = pd.read_csv(fpath2)

#df_tracker = pd.read_table(fpath2, names=['Referral ID'])

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
            
#diff = set(list(df_tracker['Referral ID'])) - set(referrals)

#diff_reverse = set(referrals) - set(list(df_tracker['Referral ID']))


any_null = []
for col in df.columns:
    count = 0
    if 'nan' in [str(x) for x in list(df[col])]:
        any_null.append((col, [str(x) for x in list(df[col])].count('nan')))
        
any_null.sort()
print(any_null)





            
            