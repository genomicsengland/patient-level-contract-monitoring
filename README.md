# patient-level-contract-monitoring
Dataset used to monitor, at a sample level, the activity undertaken through the GMS pipeline. For submission to NHSE.

## Generation 
The PLCM needs to be generated on a monthly basis and submitted via the Arden and Gems CSU using the Data Landing Portal. To generate the excel file, the following steps should be followed in the provided order

_Update Month = 'Month of Submission', e.g. Sep 2021_

### Prep Directories
Create the following folders
- PLCM Root Folder : _PLCM_, the absolute path of this folder should be updated as the _BASE_ in the .env file
In the root folder create the following folders:
- Bio Folder : _Bio_
- Tables Folder : _Tables_
- NHSE Docs Folder : _NHSE Docs_


### Prep Files 
- Hypercare tracker and GMS Samples Tracker - Download from sharepoint and save in _Bio/Month/_
- Hypercare tracker should be saved as : __gms_bio_referral_tracker.csv__
- Referral tracker should be saved as : _Tracker.csv_

### Generate
- Execute `generate_file.py` to create the required prep files

### Trifacta
- Manually upload files to Trifacta flows
- Automation (TO DO)

