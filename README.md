# patient-level-contract-monitoring
Dataset used to monitor, at a sample level, the activity undertaken through the GMS pipeline. For submission to NHSE.

The PLCM needs to be generated on a monthly basis and submitted via the Arden and Gems CSU using the Data Landing Portal. To generate the excel file, the following steps should be followed in the provided order

### Usage
- Create a `.env` file in the root of the project. The required variables are detailed in the `dotenv` file.
  - Update Month = 'Month of Submission', e.g. Sep 2021
  - Update BASE as detailed in the `Prep Directories` section
  - Make sure the connection strings for biobank and genomic record and up to date and in the required format
- Export all environment variables from the .env file
  - mac : `export $(grep -v '^#' .env | xargs)`
  - linux : `export $(grep -v '^#' .env | xargs -d '\n')`
  
- Create the required directories as detailed in the `Prep Directories` section
- Download the required files as detailed in the `Prep Files` section
- Execute `python generate_file.py` to create the required files
- Upload the following files to trifacta 
    - 1 - Create Row Data
      - row_12.csv
      - row_13.csv
      - row_14.csv
      - row_snp.csv
    - 0 - Reference Files
      - HyperCareAggregate.csv

### Prep Directories
Create the following folders
- PLCM Root Folder : _PLCM_, the absolute path of this folder should be updated as the _BASE_ in the .env file
#### In the root folder create the following:
- Data Parent Folder: _Data_
#### In the Data folder create the following sub-folders:
- Bio Folder : _Bio_
- Tables Folder : _Tables_
- NHSE Docs Folder : _NHSE Docs_

### Prep Files 
- Download gms_bio_referral_tracker.csv and GMS Sample Tracker.csv - Download from sharepoint and save in _Bio/Month/_
- gms_bio_referral_tracker.csv should be saved as : __gms_bio_referral_tracker.csv__
- GMS Sample Tracker.csv should be saved as : _Tracker.csv_




