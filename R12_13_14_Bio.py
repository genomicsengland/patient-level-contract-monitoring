#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 14:56:41 2021

@author: shivambhatnagar
"""

import pandas as pd

# %% Generating Bio Rows

date = 'March 2021'

fpath = f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM/Data/Bio/{date}/HyperCareAggregate.csv'
df_biobankall = pd.read_csv(f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM/Tables/{date}/ngis_biobank_all.csv')
df_grecordall = pd.read_csv(f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM/Tables/{date}/ngis_genomicrecord_all.csv')
df_hypercare = pd.read_csv(fpath)
sample_id_list = list(df_biobankall['SAMPLE_IDENTIFIER'])

def get_dict(df, col, sample_ids):
    empty = {}
    
    for i in sample_ids:
        if i in list(df_hypercare['Sample ID']):
            
            temp = df.loc[df['Sample ID'] == i, col].iloc[0]
    
            empty[i] = temp
        else:
            print(i, 'ID not in gms tracker')
        
    return empty

# %% Row 12 - Testing

# Referral ID, Sample ID as base
df_r12 = df_biobankall[['NGIS_REFERRAL_IDENTIFIER','SAMPLE_IDENTIFIER']]

# Activity start date
start_date = {}
start_date = get_dict(df_hypercare, 'Arrived at Illumina', sample_id_list)

df_r12['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'] = ''

for k,v in start_date.items():
    if str(v) != 'nan':
        df_r12['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'].loc[df_r12['SAMPLE_IDENTIFIER'] == k] = str(v) + ' ' + '00:00'
        
    
df_r12['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'] = pd.to_datetime(df_r12['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'], format="%d/%m/%Y %H:%M", errors='coerce')



# Activity end date

end_date = {}

end_date = get_dict(df_hypercare, 'Seq Arrived at GEL', sample_id_list)

df_r12['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'] = ''

for k,v in end_date.items():    
    df_r12['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'].loc[df_r12['SAMPLE_IDENTIFIER'] == k] = str(v)[:16]

    

df_r12['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'] = pd.to_datetime(df_r12['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'], format="%d/%m/%Y %H:%M", errors='coerce')



# Turnaround time

df_r12['TURNAROUND_TIME_(CALENDAR_DAYS)'] = df_r12['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'] - df_r12['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)']



# Turnaround time standard

df_r12['TURNAROUND_TIME_STANDARD_(CALENDAR_DAYS)'] = 'X'

# Compliant with TAT

df_r12['COMPLIANT_WITH_TURNAROUND_TIME_STANDARD'] = 'X'


df_r12['ORGANISATION_IDENTIFIER_(CODE_OF_SUBMITTING_ORGANISATION)'] = '8J834'
df_r12['ORGANISATION_IDENTIFIER_(CODE_OF_COMMISSIONED_ORGANISATION)'] = '8J834'
df_r12['ORGANISATION_IDENTIFIER_(CODE_OF_SERVICE_PROVIDER)'] = '8JP17'
df_r12['ORGANISATION_IDENTIFIER_(CODE_OF_SERVICE)'] = '8JP17'
df_r12['LOCAL_POINT_OF_DELIVERY_CODE'] = 'TESTTEST'

# %% Row 13 - Bioinformatics

# Referral ID, Sample ID as base
df_r13 = df_biobankall[['NGIS_REFERRAL_IDENTIFIER','SAMPLE_IDENTIFIER']]

# Activity start date
start_date  ={}
start_date = get_dict(df_hypercare, 'Seq Arrived at GEL', sample_id_list)

df_r13['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'] = ''

for k,v in start_date.items():    
    df_r13['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'].loc[df_r13['SAMPLE_IDENTIFIER'] == k] = v
    
df_r13['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'] = pd.to_datetime(df_r13['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'], format="%d/%m/%Y %H:%M", errors='coerce')

# Activity end date
end_date = {}

end_date = get_dict(df_hypercare, 'Arrived in Portal', sample_id_list)

df_r13['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'] = ''

for k,v in end_date.items():    
    df_r13['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'].loc[df_r13['SAMPLE_IDENTIFIER'] == k] = v
    
df_r13['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'] = pd.to_datetime(df_r13['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'], format="%d/%m/%Y %H:%M", errors='coerce')


# Turnaround time

df_r13['TURNAROUND_TIME_(CALENDAR_DAYS)'] = df_r13['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'] - df_r13['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)']

# Turnaround time standard

df_r13['TURNAROUND_TIME_STANDARD_(CALENDAR_DAYS)'] = 'X'

# Compliant with TAT

df_r13['COMPLIANT_WITH_TURNAROUND_TIME_STANDARD'] = 'X'


df_r13['ORGANISATION_IDENTIFIER_(CODE_OF_SUBMITTING_ORGANISATION)'] = '8J834'
df_r13['ORGANISATION_IDENTIFIER_(CODE_OF_COMMISSIONED_ORGANISATION)'] = '8J834'
df_r13['ORGANISATION_IDENTIFIER_(CODE_OF_SERVICE_PROVIDER)'] = '8J834'
df_r13['ORGANISATION_IDENTIFIER_(CODE_OF_SERVICE)'] = '8J834'
df_r13['LOCAL_POINT_OF_DELIVERY_CODE'] = 'TESTBIOINFO'

# %% Row 14 - Decision Support

# Referral ID, Sample ID as base
df_r14 = df_biobankall[['NGIS_REFERRAL_IDENTIFIER','SAMPLE_IDENTIFIER']]

# Activity start date
start_date = {}
start_date = get_dict(df_hypercare, 'Dispatched to Congenica', sample_id_list)

df_r14['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'] = ''

for k,v in start_date.items():    
    df_r14['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'].loc[df_r14['SAMPLE_IDENTIFIER'] == k] = v
    
df_r14['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'] = pd.to_datetime(df_r14['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'], format="%d/%m/%Y %H:%M", errors='coerce')

# Activity end date
end_date = {}
end_date = get_dict(df_hypercare, 'Returned Date', sample_id_list)

df_r14['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'] = ''

for k,v in end_date.items():    
    df_r14['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'].loc[df_r14['SAMPLE_IDENTIFIER'] == k] = v
    
df_r14['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'] = pd.to_datetime(df_r14['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'], format="%d/%m/%Y %H:%M", errors='coerce')


# Turnaround time

df_r14['TURNAROUND_TIME_(CALENDAR_DAYS)'] = df_r14['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'] - df_r14['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)']

# Turnaround time standard

df_r14['TURNAROUND_TIME_STANDARD_(CALENDAR_DAYS)'] = 'X'

# Compliant with TAT

df_r14['COMPLIANT_WITH_TURNAROUND_TIME_STANDARD'] = 'X'

# Identifiers


df_r14['ORGANISATION_IDENTIFIER_(CODE_OF_SUBMITTING_ORGANISATION)'] = '8J834'
df_r14['ORGANISATION_IDENTIFIER_(CODE_OF_COMMISSIONED_ORGANISATION)'] = '8J834'
df_r14['ORGANISATION_IDENTIFIER_(CODE_OF_SERVICE_PROVIDER)'] = '8J885'
df_r14['ORGANISATION_IDENTIFIER_(CODE_OF_SERVICE)'] = '8J885'
df_r14['LOCAL_POINT_OF_DELIVERY_CODE'] = 'TESTDSS'


# %% Writing out to dataframes
df_r12.to_csv(f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM/Tables/{date}/row_12.csv', index=False)
df_r13.to_csv(f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM/Tables/{date}/row_13.csv', index=False)
df_r14.to_csv(f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM/Tables/{date}/row_14.csv', index=False)










    
    

