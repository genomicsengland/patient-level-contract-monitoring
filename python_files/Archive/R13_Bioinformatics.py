#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 12:23:20 2021

@author: shivambhatnagar


"""

import pandas as pd

date = 'Jul 2021'

# Importing the files needed to generate table
df_biobankall = pd.read_csv(f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM Dev/Tables/{date}/ngis_biobank_all.csv')
df_grecordall = pd.read_csv(f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM Dev/Tables/{date}/ngis_genomicrecord_all.csv')
df_r13tat = pd.read_csv(f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM Dev/Tables/{date}/row_13.csv')

df_join_biobank_r13tat = pd.merge(df_biobankall, df_r13tat, how="left", on="SAMPLE_IDENTIFIER")

df_join_biobankr13tat_grecordall = pd.merge(df_join_biobank_r13tat, df_grecordall, how="left", on="LOCAL_PATIENT_IDENTIFIER_(EXTENDED)")

df_out = df_join_biobankr13tat_grecordall



df_out.rename(columns={"NGIS_REFERRAL_IDENTIFIER_x":"NGIS_REFERRAL_IDENTIFIER"}, inplace=True)
df_out.drop(columns="NGIS_REFERRAL_IDENTIFIER_y", inplace=True)

df_out = df_out.sort_values(by=['NGIS_REFERRAL_IDENTIFIER',  'SAMPLE_IDENTIFIER'])

df_schema = pd.read_excel(r'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM Dev/Data/NHSE Docs/Specification/Schema_202122.xlsx',sheet_name='Specification')
    
cols = list(df_schema['Data Element'])
cols = [x.replace(' ', '_', 10) for x in cols]

plcm_dict = {}

            
    
    


for x in cols:
    if x in df_out.columns:
        plcm_dict[x] = df_out[x]
    else:
        plcm_dict[x] = 'TO DO'
    

        
        
plcm_df = pd.DataFrame(plcm_dict)
plcm_df.drop_duplicates(inplace=True)

x= input('Write out? y/n')

if x.lower() == 'y':        
    plcm_df.to_excel(f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM Dev/Tables/{date}/output/row13_bioinformatics.xlsx', index=False)
else:
    pass
    