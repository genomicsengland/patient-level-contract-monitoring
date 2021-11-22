import plcm, trifacta
import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine

plcm_date = os.environ.get("DATE")

# # Create Required Directories
prep_plcm = plcm.PLCM(plcm_date)
prep_plcm.create_dirs()


# Create all non-bio prep files
# Hypercare tracker
"""
Requires 2 files as input
a) gms_bio_referral_tracker.csv
b) Tracker.csv
"""

print('Creating gms_tracker_file')
p0 = plcm.PLCM(plcm_date)
p0.create_gms_tracker_file()

"""
Iterates through sql folder and executes all the sql queries and writes out to csv files
"""
print('Running SQL Scripts')
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
print('Running Bio Files')
p2 = plcm.PLCM(plcm_date)
p2.execute_bio_file()






