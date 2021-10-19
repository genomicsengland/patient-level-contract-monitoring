#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 24 10:17:46 2021

@author: shivambhatnagar
"""

import pandas as pd


class PLCM_Validation():   
    
    
    def __init__(self, file_date, file_path):
        self.file_date = file_date
        self.file_path = file_path
        try:            
            self.plcm_df = pd.read_excel(self.file_path)
        except:
            self.plcm_df = pd.read_csv(self.file_path)

        self.submit = {}
        
    def get_tracker(self):
        tracker_df = pd.read_csv(f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM Dev/Data/Bio/{self.file_date}/Tracker_val.csv')    
        return tracker_df
    
    def get_schema(self):
        df = pd.read_excel(r'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM Dev/Data/NHSE Docs/Specification/Schema_202122.xlsx',sheet_name='Specification')
        return df
      
    def schema_check(self):
        df_schema = self.get_schema()
        self.schema = [x.replace(' ', '_', 10) for x in list(df_schema['Data Element'])]        
        if set(self.plcm_df.columns) == set(self.schema):
            self.submit['schema_check'] = {'Pass':True}
        else:
            self.submit['schema_check'] = {'Pass':False}
            
    def samples_check(self):
        tracker_df = self.get_tracker()
        
        referrals = list(set(list(self.plcm_df['NGIS_REFERRAL_IDENTIFIER'])))

        ref_samp = {}
        out_dict = {}
        
        for ref in referrals:
            ref_samp[ref] = []
            out_dict[ref] = []
        
        for ref in referrals:
            ref_samp[ref].append(self.plcm_df.loc[self.plcm_df['NGIS_REFERRAL_IDENTIFIER']==ref, ['SAMPLE_IDENTIFIER']])
        
        for k,v in ref_samp.items():
            out_dict[k].append(list(set(list(v[0]['SAMPLE_IDENTIFIER']))))
            
        num_samples = 0
        
        for k,v in out_dict.items():
            for el in v:
                for s in el:            
                    num_samples += 1
                    
        self.num_referrals = len(referrals)
        self.num_samples = num_samples
        
        diff = set(list(tracker_df['Referral ID'])) - set(referrals)

        diff_reverse = set(referrals) - set(list(tracker_df['Referral ID']))

        
        if diff:            
            self.submit['samples_check'] = {'Pass':False, 'tracker_plcm' : diff}
        elif diff_reverse:
            self.submit['samples_check'] = {'Pass':False, 'plcm_tracker': diff_reverse}
        else:
            self.submit['samples_check'] = {'Pass':True}
        
    def validate(self):
        self.schema_check()
        self.samples_check()
        flag = True
        
        for k in self.submit.keys():
            if self.submit[k]['Pass'] != True:
                flag = False                
            else:
            
                pass

        self.submit['Samples'] = self.num_samples
        self.submit['Referrals'] = self.num_referrals
            
        if flag == True:
            print('Ready to submit', self.submit)
        else:
            print('Needs fixing', self.submit)
            
        
        
            
plcm = PLCM_Validation('Jun 2021', r'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM Dev/PLCM_Excel/Dev/Jun 2021/PLCM_V0.csv')
plcm.validate()
          
        
        
        
        
    
