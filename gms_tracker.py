import pandas as pd

date = 'March 2021'

fpath1 = f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM/Data/Bio/{date}/bio_gms_hypercare_tracker.csv'
fpath2 = f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM/Data/Bio/{date}/Tracker.csv'

df_hypercare = pd.read_csv(fpath1)
df_hypercare.rename(columns={str(list(df_hypercare.columns)[0]):'Referral ID'}, inplace=True)
df_tracker = pd.read_csv(fpath2)
df_tracker = df_tracker[['Referral ID', 'Sample ID']]
df_out = df_hypercare.merge(df_tracker)
#df_out.to_csv(f'/Users/shivambhatnagar/OneDrive - Genomics England Ltd/Genomics England/PLCM/Data/Bio/{date}/HyperCareAggregate.csv', index=False)
