import pandas as pd
import os 

date = 'Aug 2021'
base = os.environ.get("BASE")
bio_path = '/Data/Bio/'
fpath1 = bio_path + date + 'gms_bio_referral_tracker.csv'
fpath2 = bio_path + date + 'Tracker.csv'

df_hypercare = pd.read_csv(fpath1)
df_tracker = pd.read_csv(fpath2)
df_tracker = df_tracker[['Referral ID', 'Sample ID']]
df_out = df_hypercare.merge(df_tracker)
df_out.to_csv(base + bio_path + date + 'HyperCareAggregate.csv', index=False)

