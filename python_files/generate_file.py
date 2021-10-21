import plcm, trifacta
import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine

plcm_date = os.environ.get("DATE")

# # Create Required Directories
# prep_plcm = plcm.PLCM(plcm_date)
# prep_plcm.create_dirs()


# Create all non-bio prep files
# Hypercare tracker
"""
Requires 2 files as input
a) gms_bio_referral_tracker.csv
b) Tracker.csv
"""


p0 = plcm.PLCM(plcm_date)
p0.create_gms_tracker_file()

"""
Iterates through sql folder and executes all the sql queries and writes out to csv files
"""

sql_files = os.listdir('sql/')

ngis_biobank_engine = create_engine(
            'postgresql+psycopg2://ngis_data_quality:QXW45Kiv7BrZgruLREZGzd7dO92s91KQ@10.1.30.104/ngis_biobank_prod'
        )
ngis_gr_engine = create_engine(
            'postgresql+psycopg2://ngis_data_quality:QXW45Kiv7BrZgruLREZGzd7dO92s91KQ@10.1.30.104/ngis_genomicrecord_prod'
        )

for sq in sql_files:
    engine = ngis_biobank_engine
    if 'genomicrecord' in sq:
        engine = ngis_gr_engine
    p1 = plcm.PLCM(plcm_date)
    p1.db_to_csv(sq, engine, '/Data/Tables/')

"""
Create Bio Files
"""
p2 = plcm.PLCM(plcm_date)
p2.execute_bio_file()






###### Uploading to Trifacta
# plcm_date = os.environ.get("DATE")
# plcm = plcm.PLCM(plcm_date)
# plcm.create_gms_tracker_file()

# token = ('eyJ0b2tlbklkIjoiMGI0NjRhZjItZmFjNS00MjczLTkxZmYtZDE2NWQyM2I1OTg1Iiwic2Vjcm'
#             'V0IjoiNDlkOTdlOTQ5NDU4ZDAzZTk2OGVjYzM3ZWUyNjUyOWY2YjlhNTQwYjUyY2MyYzljZWYz'
#             'ZTU3M2JmZmMwODU5MyJ9')
# host='https://trifacta.clinical-data-wranglers.preprod.aws.gel.ac/'

# trifacta_client = trifacta.TrifactaClient(host=host, token=token)
# flows = trifacta_client.get_flows()
# print(flows)

# for row in rows:
#     base = os.environ.get("BASE")
#     fpath = base + f'/Data/Tables/{plcm_date}/{row}.csv' 

#     new_id = trifacta_client.upload_dataset(fpath, row)

#     # Get Flow Id
#     flow_0_id = trifacta_client.get_flow_id('0 - Reference Files')
#     flow_1_id = trifacta_client.get_flow_id('1 - Preparation')
#     flow_2_id = trifacta_client.get_flow_id('2 - Output')

#     trifacta_client.replace_dataset(flow_1_id, 14910, new_id)


   



