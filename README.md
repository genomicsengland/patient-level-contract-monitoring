# patient-level-contract-monitoring
Dataset used to monitor, at a sample level, the activity undertaken through the GMS pipeline. For submission to NHSE.

The PLCM needs to be generated on a monthly basis and submitted via the Arden and Gems CSU using the Data Landing Portal. To generate the excel file, the following steps should be followed in the provided order

### Usage
#### Project Setup
- Create a `.env` file in the root of the project. The required variables are detailed in the `dotenv` file.
  - Update Month = 'Month of Submission', e.g. Sep 2021
  - Update BASE as detailed in the `Prep Directories` section
  - Make sure the connection strings for biobank and genomic record and up to date and in the required format
- Export all environment variables from the .env file
  - mac : `export $(grep -v '^#' .env | xargs)`
  - linux : `export $(grep -v '^#' .env | xargs -d '\n')`
- Create the required directories as detailed in the `Prep Directories` section
- Download the required files as detailed in the `Prep Files` section

#### Python
- Setup and activate a virtual environment 
  - `python -m venv venv`
  - Activate venv - Windows - `.\venv\Scripts\activate`
  - Activate venv - Mac/Linux - `source venv/bin/activate`
- Install requirements - `pip install -r requirements.txt`
- Execute `python generate_file.py` to create the required files

#### Trifacta 
- Access Trifacta Prod - https://trifacta.clinical-data-wranglers.prod.aws.gel.ac/home
- Upload the following files to the following trifacta flows 
    - `1 - Create Row Data`
      - row_12.csv
      - row_13.csv
      - row_14.csv
      - row_snp.csv
    - `0 - Reference Files`
      - HyperCareAggregate.csv
- DBS Trace File - Run the _PLCM_To_Trace_ output in the `2 - Output` flow
  - Update the value of the run-time parameter `Financial Month - Submission` = Current Financial Month
  - Once the flow has run, notify EDS that the dbs trace is ready
- Once the dbs response file has been returned, replace the dbs file in `2 - Output` flow
- Run the `PLCM_Out` output in `2 - Output` flow
  - Set the file format to dos (should be default in windows)
  - Rename the file to `8J834_GENERIC_GENOMICS_TESTING_REPORTING_NHSE2223`
- Submit the file via the data landing portal

### Prep Directories
Create the following directories
- `PLCM` - PLCM Root Directory : the absolute path of this folder should be updated as the `BASE` in the .env file
- `PLCM/Data` - Data Directory : this is a sub-directory under `PLCM`
- `PLCM/Bio` - Bioinformatics Directory : this is a sub-directory under `PLCM`
- `PLCM/NHSE Docs` - NHSE Docs Directory : this is a sub-directory under `PLCM`

### Prep Files 
- The following files need to be downloaded from https://genomicsenglandltd.sharepoint.com.mcas.ms/sites/log/Shared%20Documents/Forms/AllItems.aspx?viewid=3b321a09%2D3809%2D4096%2Daf63%2D37f46f69c115&id=%2Fsites%2Flog%2FShared%20Documents%2FGMS%20tracking
- The files must be downloaded to the `PLCM/Bio/Month` directory where Month is replaced by the value as detailed in the `.env` file
- `gms_bio_referral_tracker.csv` - should be saved as - `gms_bio_referral_tracker.csv`
- `GMS Sample Tracker.csv` - should be saved as - `Tracker.csv`




