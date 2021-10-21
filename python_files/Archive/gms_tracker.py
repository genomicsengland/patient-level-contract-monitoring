import pandas as pd

date = 'Aug 2021'

fpath1 = f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/Other/PLCM Dev/Data/Bio/{date}/gms_bio_referral_tracker.csv'
fpath2 = f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/Other/PLCM Dev/Data/Bio/{date}/Tracker.csv'

df_hypercare = pd.read_csv(fpath1)
df_tracker = pd.read_csv(fpath2)
df_tracker = df_tracker[['Referral ID', 'Sample ID']]
df_out = df_hypercare.merge(df_tracker)
df_out.to_csv(f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/Other/PLCM Dev/Data/Bio/{date}/HyperCareAggregate.csv', index=False)

