#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 12:09:54 2021

@author: shivambhatnagar
"""

import pandas as pd


import numpy as np

import datetime as dt

from datetime import *

import math

d = 'Jul 2021'


fpath1 = f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM Dev/Tables/{d}/output/row9_transportsamples.xlsx'
fpath2 = f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM Dev/Tables/{d}/output/row10_sampleplating.xlsx'
fpath3 = f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM Dev/Tables/{d}/output/row11_transportplate.xlsx'
fpath4 = f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM Dev/Tables/{d}/output/row12_testing.xlsx'
fpath5 = f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM Dev/Tables/{d}/output/row13_bioinformatics.xlsx'
fpath6 = f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM Dev/Tables/{d}/output/row_snp.xlsx'
fpath7 = f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM Dev/Tables/{d}/output/row14_dss.xlsx'

df_r9 = pd.read_excel(fpath1)
df_r10 = pd.read_excel(fpath2)
df_r11 = pd.read_excel(fpath3)
df_r12 = pd.read_excel(fpath4)
df_r13 = pd.read_excel(fpath5)
df_rsnp = pd.read_excel(fpath6)
df_r14 = pd.read_excel(fpath7)

df_list = [df_r9,df_r10, df_r11, df_r12, df_r13, df_rsnp, df_r14]

order = 1

for df in df_list:
    df['SORT'] = order
    order += 1
    
    
plcm_df = pd.concat(df_list)

# Adding Information that is common to all
cols_list = []

for col in plcm_df.columns:
    if list(plcm_df.loc[0, col][0])[0] == 'TO DO':
        cols_list.append(col)

 



# %% Data Quality Checks


# DOB : PERSON_BIRTH_DATE - Convert to just date

plcm_df['PERSON_BIRTH_DATE'] = plcm_df['PERSON_BIRTH_DATE'].apply(lambda x: str(x).split()[0])
plcm_df['PERSON_BIRTH_DATE'] = plcm_df['PERSON_BIRTH_DATE'].apply(lambda x: dt.date(int(x.split('-')[0]), int(x.split('-')[1]), int(x.split('-')[2])))

# AGE_AT_ACTIVITY_DATE_(CONTRACT_MONITORING) : Convert AGE to YEARS (CHECK SPEC)

plcm_df['AGE_AT_ACTIVITY_DATE_(CONTRACT_MONITORING)'] = date.today() - plcm_df['PERSON_BIRTH_DATE']
plcm_df['AGE_AT_ACTIVITY_DATE_(CONTRACT_MONITORING)'] = plcm_df['AGE_AT_ACTIVITY_DATE_(CONTRACT_MONITORING)'].apply(lambda x: math.floor(x.days/365.2425))

# Activity start and end - right format : ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)
plcm_df['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'] = [str(x) +' 00:00:00' if len(str(x).split()) < 2 and str(x) != 'nan' else x for x in plcm_df['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)']]

start_dt = [pd.to_datetime(x) for x in plcm_df['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)']]
plcm_df['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'] = start_dt
end_dt = [pd.to_datetime(x)for x in plcm_df['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)']]
plcm_df['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'] = end_dt

# Filtering out dates
plcm_df = plcm_df[plcm_df['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'] < dt.datetime(2021, 8, 1, 0,0,0)]
plcm_df = plcm_df[plcm_df['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'] < dt.datetime(2021, 8, 1,0,0,0)]

# TAT - CONVERT to WORKING DAYS TO DO

np_start = list(plcm_df['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'])

np_end = list(plcm_df['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'])


np_stage = [x for x in plcm_df['LOCAL_POINT_OF_DELIVERY_CODE']]

def wdays(startdt, enddt):
    delta = enddt - startdt       # as timedelta
    wdays = []
    for i in range(delta.days + 1):
        day = startdt + timedelta(days=i)
        if not day.strftime("%A") in ['Saturday', 'Sunday']:
            wdays.append(day)
    return len(wdays)

np_diff = []
for x in range(len(np_start)):      
    if np_stage[x] != 'TESTTEST' and np_stage[x] != 'TESTBIOINFO':       
        if str(np_start[x]) == 'NaT' or str(np_end[x]) == 'NaT':
            np_diff.append('nan')
        else:
            # Getting dates into UTF Datetime
            start = np_start[x]
            end = np_end[x]
            start_f = str(start).split()[0]
            end_f = str(end).split()[0]
            start_dt = dt.datetime(int(start_f.split('-')[0]), int(start_f.split('-')[1]),int(start_f.split('-')[2]))
            end_dt = dt.datetime(int(end_f.split('-')[0]), int(end_f.split('-')[1]),int(end_f.split('-')[2]))
            # Getting working_days
            work_days = wdays(start_dt, end_dt)
            np_diff.append(work_days)
    if np_stage[x] == 'TESTTEST':
        ddiff = np_end[x] - np_start[x]
        np_diff.append(ddiff.days)


# =============================================================================
# plcm_df.loc[plcm_df['LOCAL_POINT_OF_DELIVERY_CODE'] == 'TESTTEST', 'TURNAROUND_TIME_(CALENDAR_DAYS)'] = plcm_df.loc[plcm_df['LOCAL_POINT_OF_DELIVERY_CODE'] == 'TESTTEST', 'ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'] - plcm_df.loc[plcm_df['LOCAL_POINT_OF_DELIVERY_CODE'] == 'TESTTEST', 'ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)']
#           
#     
# plcm_df.loc[plcm_df['LOCAL_POINT_OF_DELIVERY_CODE'] not in ['TESTTEST', 'TESTBIOINFO'], 'TURNAROUND_TIME_(CALENDAR_DAYS)'] = np.busday_count(plcm_df.loc[plcm_df['LOCAL_POINT_OF_DELIVERY_CODE'] == 'TESTTEST', 'ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'] , plcm_df.loc[plcm_df['LOCAL_POINT_OF_DELIVERY_CODE'] == 'TESTTEST', 'ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'])
# 
# =============================================================================


plcm_df['TURNAROUND_TIME_(CALENDAR_DAYS)'] = np_diff
plcm_df.loc[(plcm_df['SAMPLE_IDENTIFIER'] == 1046785524) & (plcm_df['LOCAL_POINT_OF_DELIVERY_CODE'] == 'TESTTRASAM'),['TURNAROUND_TIME_(CALENDAR_DAYS)']] = 3
 
# Adding Blanks
plcm_df['DECEASED_INDICATOR']  = ''
plcm_df['SAMPLE_PLATING_QUALITY_CONTROL']  = ''
plcm_df['ORGANISATION_IDENTIFIER_(CODE_OF_HISTOPATHOLOGY_LABORATORY_ENTITY)'] = ''
plcm_df['GENOMIC_TEST_CODE_(SNOMED_CT_DM+D)'] = ''
plcm_df['LOCAL_REPORT_IDENTIFIER'] = ''
plcm_df['REPORT_COMPLEXITY_CODE'] = ''
plcm_df['TEST_OUTCOME_CODE'] = ''
plcm_df['HOSPITAL_PROVIDER_SPELL_IDENTIFIER'] = ''
plcm_df['OUT-PATIENT_ATTENDANCE_IDENTIFIER'] = ''
# No NHS Number match
plcm_df['ORGANISATION_IDENTIFIER_(GP_PRACTICE_RESPONSIBILITY)'] = ''
plcm_df['GENERAL_MEDICAL_PRACTICE_CODE_(PATIENT_REGISTRATION)'] = ''


# Quality score for sequencing

plcm_df['QUALITY_SCORE_FOR_SEQUENCING'] = ''

# COMMISSIONED_SERVICE_CATEGORY_CODE, SERVICE CODE
plcm_df['COMMISSIONED_SERVICE_CATEGORY_CODE'] = 21
plcm_df['SERVICE_CODE'] = 'NCBPS20Z'

plcm_df['ETHNIC_CATEGORY'] = plcm_df['ETHNIC_CATEGORY'].apply(lambda x: 'Z-Not Known' if str(x) == 'nan' else x)
plcm_df['ETHNIC_CATEGORY'] = plcm_df['ETHNIC_CATEGORY'].apply(lambda x: (x.split('-')[0]).strip())

# TAT Standards --- HERE
#disease_area
fpath6 = f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM Dev/Tables/{d}/ngis_diseasearea_all.csv'
df_da = pd.read_csv(fpath6)

plcm_df = plcm_df.merge(df_da, how='inner', left_on='SAMPLE_IDENTIFIER', right_on='dispatched_sample_lsid')

plcm_df.drop(columns=['dispatched_sample_lsid'], inplace=True)

# R12, CA: 42 CD, RD: 28 CD # CONFIRM WITH AFSHAAN

plcm_df.loc[(plcm_df['LOCAL_POINT_OF_DELIVERY_CODE'] == 'TESTTEST') & (plcm_df['disease_area'] == 'Cancer'), ['TURNAROUND_TIME_STANDARD_(CALENDAR_DAYS)']] = 42
plcm_df.loc[(plcm_df['LOCAL_POINT_OF_DELIVERY_CODE'] == 'TESTTEST') & (plcm_df['disease_area'] != 'Cancer'), ['TURNAROUND_TIME_STANDARD_(CALENDAR_DAYS)']] = 28


# R13, CA: 4WD, RD: 3WD

plcm_df.loc[(plcm_df['LOCAL_POINT_OF_DELIVERY_CODE'] == 'TESTBIOINFO') & (plcm_df['disease_area'] == 'Cancer'), ['TURNAROUND_TIME_STANDARD_(CALENDAR_DAYS)']] = 4
plcm_df.loc[(plcm_df['LOCAL_POINT_OF_DELIVERY_CODE'] == 'TESTBIOINFO') & (plcm_df['disease_area'] != 'Cancer'), ['TURNAROUND_TIME_STANDARD_(CALENDAR_DAYS)']] = 3

plcm_df.loc[(plcm_df['LOCAL_POINT_OF_DELIVERY_CODE'] == 'TESTSNP'), ['TURNAROUND_TIME_STANDARD_(CALENDAR_DAYS)']] = 0


# R14, 1 WD for both

plcm_df.loc[plcm_df['LOCAL_POINT_OF_DELIVERY_CODE'] == 'TESTDSS', 'TURNAROUND_TIME_STANDARD_(CALENDAR_DAYS)'] = 1



# TAT Compliance
plcm_df['COMPLIANT_WITH_TURNAROUND_TIME_STANDARD'] = plcm_df['TURNAROUND_TIME_(CALENDAR_DAYS)'] <= plcm_df['TURNAROUND_TIME_STANDARD_(CALENDAR_DAYS)']

# Change compliance TAT to Y, N
plcm_df['COMPLIANT_WITH_TURNAROUND_TIME_STANDARD'] = plcm_df['COMPLIANT_WITH_TURNAROUND_TIME_STANDARD'].apply(lambda x : 'Y' if x == True else 'N')

## Compliance set to '' for TESTSNP rows
plcm_df.loc[plcm_df['LOCAL_POINT_OF_DELIVERY_CODE'] == 'TESTSNP', ['TURNAROUND_TIME_STANDARD_(CALENDAR_DAYS)','COMPLIANT_WITH_TURNAROUND_TIME_STANDARD']] = ''

# Sample Category Code Apply Logic

plcm_df.loc[(plcm_df['DNA_CONCENTRATION'] >= 20) & (plcm_df['DNA_CONCENTRATION'] <= 100) & (plcm_df['SAMPLE_VOLUME'] >= 100), ['SAMPLE_CATEGORY_CODE']] = 1 # Standard Input
plcm_df.loc[(plcm_df['SAMPLE_VOLUME'] < 100), ['SAMPLE_CATEGORY_CODE']] = 2 # Low Volume Input
plcm_df.loc[(plcm_df['DNA_CONCENTRATION'] < 20), ['SAMPLE_CATEGORY_CODE']] = 1 # Low Concentration Input


# Financial Month and Year --- HERE
fin_month = {1:'Jan', 2:'Feb', 3:'Mar', 4: 'Apr', 5: 'May', 6: 'Jun' , 7: 'Jul', 11:'Nov', 12:'Dec'}
fin_month_2 = {'Nov' : 8, 'Dec' : 9, 'Jan' : 10, 'Feb' : 11, 'Mar':12, 'Apr': 1, 'May': 2, 'Jun': 3, 'Jul': 4}

plcm_df['FINANCIAL_MONTH'] = plcm_df['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'].apply(lambda x: x.month)
plcm_df['FINANCIAL_MONTH'] = plcm_df['FINANCIAL_MONTH'].apply(lambda x: fin_month[x])
plcm_df['FINANCIAL_MONTH'] = plcm_df['FINANCIAL_MONTH'].apply(lambda x: fin_month_2[x])


plcm_df.loc[(~plcm_df['FINANCIAL_MONTH'].isin([1,2,3,4])), ['FINANCIAL_YEAR']] = 202021
plcm_df.loc[(plcm_df['FINANCIAL_MONTH'].isin([1,2,3,4])), ['FINANCIAL_YEAR']] = 202122

# Keep only files in the current calendar year
plcm_df = plcm_df[plcm_df['FINANCIAL_YEAR'] == 202122]


#Specification Checks and final mapping
plcm_df['ETHNIC_CATEGORY'] = plcm_df['ETHNIC_CATEGORY'].apply(lambda x: 'Z' if x == 'Not known' else x)


def sample_func(x):
    if x == 'Normal or Germline sample':
        return 1
    elif x == 'Liquid tumour sample':
        return 2
    elif x == 'Solid tumour sample':
        return 3
    else:
        return 4   
    

plcm_df['SAMPLE_TYPE_CODE'] = plcm_df['SAMPLE_TYPE_CODE'].apply(sample_func)


# Manual Setting of service code to same as service provider
plcm_df['ORGANISATION_SITE_IDENTIFIER_(OF_SERVICE)'] = plcm_df['ORGANISATION_IDENTIFIER_(CODE_OF_SERVICE_PROVIDER)']

plcm_df.drop(columns=['disease_area'], inplace=True)

plcm_df.sort_values(by=['NGIS_REFERRAL_IDENTIFIER','SORT'], inplace=True)

# Delete SORT
plcm_df.drop(columns=['SORT'], inplace=True)
plcm_df.drop_duplicates(inplace=True)


plcm_df.to_excel(f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM Dev/PLCM_Excel/Dev/{d}/PLCM_Trifacta.xlsx', index=False)











