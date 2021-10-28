import plcm, trifacta, s3
import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine

rows = [
    'row_9',
    'row_10',
    'row_11',
    'row_12',
    'row_13',
    'row_14',
    'row_snp'
]

##### Uploading to Trifacta
plcm_date = os.environ.get("DATE")

token = ('eyJ0b2tlbklkIjoiMGI0NjRhZjItZmFjNS00MjczLTkxZmYtZDE2NWQyM2I1OTg1Iiwic2Vjcm'
            'V0IjoiNDlkOTdlOTQ5NDU4ZDAzZTk2OGVjYzM3ZWUyNjUyOWY2YjlhNTQwYjUyY2MyYzljZWYz'
            'ZTU3M2JmZmMwODU5MyJ9')
host='https://trifacta.clinical-data-wranglers.preprod.aws.gel.ac/'

trifacta_client = trifacta.TrifactaClient(host=host, token=token)
flows = trifacta_client.get_flows()

s3_client = s3.S3()
base = os.environ.get("BASE")

for row in rows:
    # Get Flow Id
    flow_0_id = trifacta_client.get_flow_id('0 - Reference Files')
    flow_1_id = trifacta_client.get_flow_id('1 - Preparation')
    flow_2_id = trifacta_client.get_flow_id('2 - Output')
    
    fpath = base + f'/Data/Tables/{plcm_date}/{row}.csv' 

    s3_resp = s3_client.upload_file_to_s3(fpath, '512426816668-data-chapter', 'trifacta/queryResults/shivam.bhatnagar@genomicsengland.co.uk/') 

    # Assuming s3_resp is a json object
    new_id = s3_resp['id']
    old_id = trifacta_client.get_dataset_id_by_name(flow_1_id, row)

    trifacta_client.replace_dataset(flow_1_id, old_id, new_id)


   



