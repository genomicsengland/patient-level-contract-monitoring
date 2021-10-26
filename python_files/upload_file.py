import plcm, trifacta
import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine


##### Uploading to Trifacta
plcm_date = os.environ.get("DATE")
plcm = plcm.PLCM(plcm_date)
plcm.create_gms_tracker_file()

token = ('eyJ0b2tlbklkIjoiMGI0NjRhZjItZmFjNS00MjczLTkxZmYtZDE2NWQyM2I1OTg1Iiwic2Vjcm'
            'V0IjoiNDlkOTdlOTQ5NDU4ZDAzZTk2OGVjYzM3ZWUyNjUyOWY2YjlhNTQwYjUyY2MyYzljZWYz'
            'ZTU3M2JmZmMwODU5MyJ9')
host='https://trifacta.clinical-data-wranglers.preprod.aws.gel.ac/'

trifacta_client = trifacta.TrifactaClient(host=host, token=token)
flows = trifacta_client.get_flows()
print(flows)

for row in rows:
    base = os.environ.get("BASE")
    fpath = base + f'/Data/Tables/{plcm_date}/{row}.csv' 

    new_id = trifacta_client.upload_dataset(fpath, row)

    # Get Flow Id
    flow_0_id = trifacta_client.get_flow_id('0 - Reference Files')
    flow_1_id = trifacta_client.get_flow_id('1 - Preparation')
    flow_2_id = trifacta_client.get_flow_id('2 - Output')

    trifacta_client.replace_dataset(flow_1_id, 14910, new_id)


   



