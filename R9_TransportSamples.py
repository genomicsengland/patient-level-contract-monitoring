#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 11:35:39 2021

@author: shivambhatnagar
"""


import pandas as pd


# Importing the files needed to generate table

date = 'March 2021'

df_biobankall = pd.read_csv(f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM/Tables/{date}/ngis_biobank_all.csv')
df_grecordall = pd.read_csv(f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM/Tables/{date}/ngis_genomicrecord_all.csv')
df_r9tat = pd.read_csv(f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM/Tables/{date}/row_9.csv')

df_join_biobank_r9tat = pd.merge(df_biobankall, df_r9tat, how="left", on="SAMPLE_IDENTIFIER")

df_join_biobankr9tat_grecordall = pd.merge(df_join_biobank_r9tat, df_grecordall, how="left", on="LOCAL_PATIENT_IDENTIFIER_(EXTENDED)")

df_out = df_join_biobankr9tat_grecordall



df_out.rename(columns={"NGIS_REFERRAL_IDENTIFIER_x":"NGIS_REFERRAL_IDENTIFIER"}, inplace=True)
df_out.drop(columns="NGIS_REFERRAL_IDENTIFIER_y", inplace=True)

df_out = df_out.sort_values(by=['NGIS_REFERRAL_IDENTIFIER',  'SAMPLE_IDENTIFIER'])

df_schema = pd.read_excel(r'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM/Data/NHSE Docs/PLCM Examples v2.0. WGS.xlsx',sheet_name='Example 3' )
    
cols = list(df_schema.columns)

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
    plcm_df.to_excel(f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM/Tables/{date}/output/row9_transportsamples.xlsx', index=False)
else:
    pass
    
    






