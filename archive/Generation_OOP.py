#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 24 16:25:28 2021

@author: shivambhatnagar
"""

import pandas as pd
import datetime as dt
import date 
import math


class PLCM():

    def empty_plcm_df(self):
        
        """
        Generates an empty pandas dataframe with the correct columns from the spec
        
        """
        
        df_schema = pd.read_excel(r'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM Dev/Data/NHSE Docs/Specification/Schema_202122.xlsx',
                                  sheet_name='Specification')
        cols = [x.replace(' ', '_', 10) for x in list(df_schema['Data Element'])]
        for c in cols:
            self.plcm_dict[c] = []
            
        self.plcm_df = pd.DataFrame(self.plcm_dict)
    
    
    def __init__(self, file_path, stage):
        self.file_path = file_path
        self.plcm_dict = {}
        self.empty_plcm_df()    
        self.stage = stage
        

        
    def fill_stage(self):
        df = pd.read_excel(self.file_path)
        for col in df.columns:
            self.plcm_df[col] = df[col]
            
    def all_stage(self):
        # Birth Date
        self.plcm_df['PERSON_BIRTH_DATE'] = self.plcm_df['PERSON_BIRTH_DATE'].apply(lambda x: str(x).split()[0])
        self.plcm_df['PERSON_BIRTH_DATE'] = self.plcm_df['PERSON_BIRTH_DATE'].apply(lambda x: dt.date(int(x.split('-')[0]), int(x.split('-')[1]), int(x.split('-')[2])))
        
        # Age
        self.plcm_df['AGE_AT_ACTIVITY_DATE_(CONTRACT_MONITORING)'] = date.today() - self.plcm_df['PERSON_BIRTH_DATE']
        self.plcm_df['AGE_AT_ACTIVITY_DATE_(CONTRACT_MONITORING)'] = self.plcm_df['AGE_AT_ACTIVITY_DATE_(CONTRACT_MONITORING)'].apply(lambda x: math.floor(x.days/365.2425))
        
# =============================================================================
# plcm_df['PERSON_BIRTH_DATE'] = plcm_df['PERSON_BIRTH_DATE'].apply(lambda x: str(x).split()[0])
# plcm_df['PERSON_BIRTH_DATE'] = plcm_df['PERSON_BIRTH_DATE'].apply(lambda x: dt.date(int(x.split('-')[0]), int(x.split('-')[1]), int(x.split('-')[2])))
# =============================================================================
        
        all = {}
            
        for k,v in all.items():
            self.plcm_df.loc[self.plcm_df['LOCAL_POINT_OF_DELIVERY_CODE'] == self.stage, self.plcm_df[k]] = v
    
    def custom_stage(self):
        
        custom = {'TESTTRASAM':{}, 
                #  'TESTPLATE':{},
                  'TESTTRAPLATE':{},
                  'TESTTEST':{},
                  'TESTBIOINFO':{},
                  'TESTDSS':{}}
        
        for k,v in custom[self.stage].items():
            self.plcm_df.loc[self.plcm_df['LOCAL_POINT_OF_DELIVERY_CODE'] == self.stage, self.plcm_df[k]] = v
    
# Orchestration

trasample = PLCM(r'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM Dev/Tables/April 2021/output/row9_transportsamples.xlsx')
traplate = PLCM(r'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM Dev/Tables/April 2021/output/row11_transportplate.xlsx')
        
        
        
        
        

        
    
    
    