# patient-level-contract-monitoring
Dataset used to monitor, at a sample level, the activity undertaken through the GMS pipeline. For submission to NHSE.

## Generation 
The PLCM needs to be generated on a monthly basis and submitted via the Arden and Gems CSU using the Data Landing Portal. To generate the excel file, the following steps should be followed in the provided order

_Update Month = 'Month of Submission', e.g. March 2021_

**All folders should have the month added to the end e.g. Folder A_March**

### Prep Directories
Create the following folders
- Folder A : Stores the bio source files, update folder path in gms_tracker.py
- Folder B : Stores all the _Prep Files_ below in here, update folder path in all files
- Folder C : Stores all the _Prep Files - Stage 2_ in here, update folder path in all files
- Folder D : Stores the output PLCM to be tested, upadte in Aggregate.py

### Prep Files 
- Hypercare tracker and samples tracker - Sharepoint
- SQL Extracts of the following tables - Genrated using the source_script in the tables below

| file_name     | source_script |
| ------------- |:-------------:|
| ngis_biobank_all.csv      | ngis_biobank_all.sql |
| ngis_genomicrecord_all.csv     | ngis_genomicrecord_all.sql     |
| ngis_diseasearea_all.csv | ngis_biobank_all.sql      |
| ow_9.csv | row_9_specific.sql     |
| row_11.csv | row_11_specific.sql      |

### Prep Files - Stage 2
- gms_tracker.py
- R9_TransportSamples.py
- R11_TransportPlate.py
- R_12_13_14.py
- R12_Testing.py
- R13_Bioinformatics.py
- R14_Dss.py

### Generation
- Aggregate.py
