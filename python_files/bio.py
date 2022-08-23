#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 14:56:41 2021

@author: shivambhatnagar
"""
# %% Generating Bio Rows

import pandas as pd
import os 



def main():

    date = os.environ.get("DATE")
    base = os.environ.get("BASE")
    fpath = base + '/Data/Bio/' + date + '/HyperCareAggregate.csv'
    fpath2 = base + '/Data/Tables/' + date + '/ngis_snp_referring_glh.csv'
    biobank_path = base + '/Data/Tables/' + date + '/ngis_biobank_all.csv'
    df_biobankall = pd.read_csv(biobank_path)
    df_hypercare = pd.read_csv(fpath)
    df_ods = pd.read_csv(fpath2)

    sample_id_list = list(df_biobankall['SAMPLE_IDENTIFIER'])

    def get_dict(df, col, sample_ids):
        empty = {}
        
        for i in sample_ids:
            if i in list(df_hypercare['Sample ID']):
                
                temp = df.loc[df['Sample ID'] == i, col].iloc[0]
        
                empty[i] = temp
            else:
                pass
            
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


    df_r12['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'] = pd.to_datetime(df_r12['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'], format="%d/%b/%Y %H:%M", errors='coerce')

    # Activity end date

    end_date = {}

    end_date = get_dict(df_hypercare, 'bio_pipeline_start', sample_id_list)

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

    # %% SNP Check

    # Referral ID, Sample ID as base
    df_rsnp = df_biobankall[['NGIS_REFERRAL_IDENTIFIER','SAMPLE_IDENTIFIER']]

    # Activity start date
    start_date  ={}
    start_date = get_dict(df_hypercare, 'snp_check_pending_date', sample_id_list)

    for k,v in start_date.items():
        if str(v) != 'nan':
            start_date[k] = v[:v.rfind(':')]

    df_rsnp['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'] = ''

    for k,v in start_date.items():
        df_rsnp['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'].loc[df_rsnp['SAMPLE_IDENTIFIER'] == k] = v

    ## NEED TO CHANGE FORMAT OF DATES FROM d/h/y H:M:S to d/h/y H:M

    df_rsnp['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'] = pd.to_datetime(df_rsnp['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'], format="%d/%m/%Y %H:%M", errors='coerce')

    # Activity end date
    end_date = {}

    end_date = get_dict(df_hypercare, 'snp_check_pass_date', sample_id_list)

    for k,v in end_date.items():
        if str(v) != 'nan':
            end_date[k] = v[:v.rfind(':')]

    df_rsnp['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'] = ''

    for k,v in end_date.items():
        df_rsnp['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'].loc[df_rsnp['SAMPLE_IDENTIFIER'] == k] = v

    df_rsnp['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'] = pd.to_datetime(df_rsnp['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'], format="%d/%m/%Y %H:%M", errors='coerce')


    # Turnaround time

    df_rsnp['TURNAROUND_TIME_(CALENDAR_DAYS)'] = df_rsnp['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'] - df_rsnp['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)']

    # Turnaround time standard

    df_rsnp['TURNAROUND_TIME_STANDARD_(CALENDAR_DAYS)'] = 'X'

    # Compliant with TAT

    df_rsnp['COMPLIANT_WITH_TURNAROUND_TIME_STANDARD'] = 'X'

    ods_ref = dict(zip(list(df_ods['referral_id']), list(df_ods['ods'])))

    df_rsnp['ORGANISATION_IDENTIFIER_(CODE_OF_SUBMITTING_ORGANISATION)'] = '8J834'
    df_rsnp['ORGANISATION_IDENTIFIER_(CODE_OF_COMMISSIONED_ORGANISATION)'] = '8J834'
    df_rsnp['ORGANISATION_IDENTIFIER_(CODE_OF_SERVICE_PROVIDER)'] =  'GLH ODS'
    df_rsnp['ORGANISATION_IDENTIFIER_(CODE_OF_SERVICE)'] =  'GLH ODS'
    df_rsnp['LOCAL_POINT_OF_DELIVERY_CODE'] = 'TESTSNP'

    for k,v in ods_ref.items():
        df_rsnp.loc[df_rsnp['NGIS_REFERRAL_IDENTIFIER'] == k, ['ORGANISATION_IDENTIFIER_(CODE_OF_SERVICE_PROVIDER)']] =  v
        df_rsnp.loc[df_rsnp['NGIS_REFERRAL_IDENTIFIER'] == k, ['ORGANISATION_IDENTIFIER_(CODE_OF_SERVICE)']] =  v







    # %% Row 13 - Bioinformatics

    #### Phase 1 (Bio start to SNP Check start)

    # Referral ID, Sample ID as base
    df_r13_p1 = df_biobankall[['NGIS_REFERRAL_IDENTIFIER','SAMPLE_IDENTIFIER']]



    # Activity start date
    start_date  ={}
    start_date = get_dict(df_hypercare, 'bio_pipeline_start', sample_id_list)

    for k,v in start_date.items():
        if str(v) != 'nan':
            start_date[k] = v[:v.rfind(':')]

    df_r13_p1['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'] = ''

    for k,v in start_date.items():
        df_r13_p1['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'].loc[df_r13_p1['SAMPLE_IDENTIFIER'] == k] = v

    df_r13_p1['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'] = pd.to_datetime(df_r13_p1['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'], format="%d/%m/%Y %H:%M", errors='coerce')

    # Activity end date
    end_date = {}

    end_date = get_dict(df_hypercare, 'snp_check_pending_date', sample_id_list)

    for k,v in end_date.items():
        if str(v) != 'nan':
            end_date[k] = v[:v.rfind(':')]

    df_r13_p1['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'] = ''

    for k,v in end_date.items():
        df_r13_p1['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'].loc[df_r13_p1['SAMPLE_IDENTIFIER'] == k] = v

    df_r13_p1['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'] = pd.to_datetime(df_r13_p1['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'], format="%d/%m/%Y %H:%M", errors='coerce')

    df_r13_p1['TURNAROUND_TIME_(CALENDAR_DAYS)'] = df_r13_p1['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'] - df_r13_p1['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)']

    ### Phase 2 (Snp Check End to Dispatched to congenica)

    # Referral ID, Sample ID as base
    df_r13_p2 = df_biobankall[['NGIS_REFERRAL_IDENTIFIER','SAMPLE_IDENTIFIER']]



    # Activity start date
    start_date  ={}
    start_date = get_dict(df_hypercare, 'snp_check_pass_date', sample_id_list)

    for k,v in start_date.items():
        if str(v) != 'nan':
            start_date[k] = v[:v.rfind(':')]

    df_r13_p2['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'] = ''

    for k,v in start_date.items():
        df_r13_p2['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'].loc[df_r13_p2['SAMPLE_IDENTIFIER'] == k] = v

    df_r13_p2['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'] = pd.to_datetime(df_r13_p2['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'], format="%d/%m/%Y %H:%M", errors='coerce')

    # Activity end date
    end_date = {}

    end_date = get_dict(df_hypercare, 'dispatched_to_congenica_date', sample_id_list)

    for k,v in end_date.items():
        if str(v) != 'nan':
            end_date[k] = v[:v.rfind(':')]

    df_r13_p2['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'] = ''

    for k,v in end_date.items():
        df_r13_p2['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'].loc[df_r13_p2['SAMPLE_IDENTIFIER'] == k] = v

    df_r13_p2['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'] = pd.to_datetime(df_r13_p2['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'], format="%d/%m/%Y %H:%M", errors='coerce')

    df_r13_p2['TURNAROUND_TIME_(CALENDAR_DAYS)'] = df_r13_p2['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'] - df_r13_p2['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)']



    ### Combine
    df_r13 = df_biobankall[['NGIS_REFERRAL_IDENTIFIER','SAMPLE_IDENTIFIER']]

    # Activity start date
    start_date  ={}
    start_date = get_dict(df_hypercare, 'bio_pipeline_start', sample_id_list)

    for k,v in start_date.items():
        if str(v) != 'nan':
            start_date[k] = v[:v.rfind(':')]

    df_r13['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'] = ''

    for k,v in start_date.items():
        df_r13['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'].loc[df_r13['SAMPLE_IDENTIFIER'] == k] = v

    df_r13['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'] = pd.to_datetime(df_r13['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'], format="%d/%m/%Y %H:%M", errors='coerce')

    # Activity end date
    end_date = {}

    end_date = get_dict(df_hypercare, 'dispatched_to_congenica_date', sample_id_list)

    for k,v in end_date.items():
        if str(v) != 'nan':
            end_date[k] = v[:v.rfind(':')]

    df_r13['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'] = ''

    for k,v in end_date.items():
        df_r13['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'].loc[df_r13['SAMPLE_IDENTIFIER'] == k] = v

    df_r13['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'] = pd.to_datetime(df_r13['ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)'], format="%d/%m/%Y %H:%M", errors='coerce')


    # Turnaround time

    df_r13['TURNAROUND_TIME_(CALENDAR_DAYS)'] = df_r13_p1['TURNAROUND_TIME_(CALENDAR_DAYS)'] - df_r13_p2['TURNAROUND_TIME_(CALENDAR_DAYS)']


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
    start_date = get_dict(df_hypercare, 'dispatched_to_congenica_date', sample_id_list)

    for k,v in start_date.items():
        if str(v) != 'nan':
            start_date[k] = v[:v.rfind(':')]

    df_r14['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'] = ''

    for k,v in start_date.items():
        df_r14['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'].loc[df_r14['SAMPLE_IDENTIFIER'] == k] = v

    df_r14['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'] = pd.to_datetime(df_r14['ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)'], format="%d/%m/%Y %H:%M", errors='coerce')

    # Activity end date
    end_date = {}
    end_date = get_dict(df_hypercare, 'returned_date', sample_id_list)


    for k,v in end_date.items():
        if str(v) != 'nan':
            end_date[k] = v[:v.rfind(':')]


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
    out_path = base + '/Data/Tables/' + date + '/'
    df_r12.to_csv(out_path + 'row_12_v2.csv', index=False)
    df_rsnp.to_csv(out_path + 'row_snp.csv', index=False)
    df_r13.to_csv(out_path + 'row_13.csv', index=False)
    df_r14.to_csv(out_path + 'row_14.csv', index=False)











    
    

