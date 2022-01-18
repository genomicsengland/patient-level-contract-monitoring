import os 
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from dotenv import load_dotenv
import importlib 
import pandas as pd
import sqlalchemy
from python_files import bio

basedir = os.path.abspath(os.path.dirname(__file__))  ## Change to correct file path
load_dotenv(os.path.join(basedir, "..", ".env"))

class PLCM:

    def __init__(self, date: str):
        self.date = date
        self.base = os.environ.get("BASE")
        self.gms_path = '/Data/Bio/'
        self.table_path = '/Data/Tables/'
        self.nhse_path = '/Data/NHSE Docs/'

    def create_gms_tracker_file(self) -> None:
        """Creates the aggregated gms_tracker and write out a file."""
        path = self.base+self.gms_path+self.date
        fpath1 = path+"/gms_bio_referral_tracker.csv"
        fpath2 = path+"/Tracker.csv"

        df_hypercare = pd.read_csv(fpath1)
        df_tracker = pd.read_csv(fpath2)
        df_tracker = df_tracker[['Referral ID', 'Sample ID']]
        df_out = df_hypercare.merge(df_tracker)
        df_out.to_csv(path + '/HyperCareAggregate.csv', index=False)

    def create_row_file(self, row_name:str) -> None:
        """To Deprecate: Takes in a row name and creates an excel file written to the desired location."""
        path = self.base+self.table_path+self.date+'/'
        spec_path = self.base+self.nhse_path
        out_path = self.base + '/Data/Tables/' + self.date + f'/output/{row_name}.xlsx'
        self.out_path = out_path

        df_biobankall = pd.read_csv(path + 'ngis_biobank_all.csv')
        df_grecordall = pd.read_csv(path + 'ngis_genomicrecord_all.csv')
        df_1 = pd.read_csv(path + row_name + '.csv')

        df_2 = pd.merge(df_biobankall, df_1, how="left", on="SAMPLE_IDENTIFIER")

        df_3 = pd.merge(df_2, df_grecordall, how="left", on="LOCAL_PATIENT_IDENTIFIER_(EXTENDED)")

        df_out = df_3

        df_out.rename(columns={"NGIS_REFERRAL_IDENTIFIER_x":"NGIS_REFERRAL_IDENTIFIER"}, inplace=True)
        df_out.drop(columns="NGIS_REFERRAL_IDENTIFIER_y", inplace=True)

        df_out = df_out.sort_values(by=['NGIS_REFERRAL_IDENTIFIER',  'SAMPLE_IDENTIFIER'])

        # Updates to 2021/22 Spec
        df_schema = pd.read_excel(spec_path + '/Specification/Schema_202122.xlsx',sheet_name='Specification')
            
        cols = list(df_schema['Data Element'])
        cols = [x.replace(' ', '_', 10) for x in cols]

        plcm_dict = {}       

        for x in cols:
            if x in df_out.columns:
                plcm_dict[x] = df_out[x]
            else:
                plcm_dict[x] = 'TO DO'
        
        plcm_df = pd.DataFrame(plcm_dict)
        plcm_df.drop_duplicates(inplace=True)
        plcm_df.to_excel(out_path, index=False)

    def execute_bio_file(self) -> None:
        """Takes in a file and executes it."""
        bio.main()

    def db_to_csv(self, sql_path: str, engine: sqlalchemy.engine, path: str) -> None:
        """Reads in a sql file and writes out a file to a given location."""
        file = open(SCRIPT_DIR+'/..'+'/sql/'+sql_path)
        with engine.connect() as conn:
            query = sqlalchemy.text(file.read())
            resultproxy = conn.execute(query)

        df_dict = [
            {column: value for column, value in rowproxy.items()}
            for rowproxy in resultproxy
        ]
        df = pd.DataFrame(df_dict)

        out_path = self.base + path + self.date + '/' + str(sql_path.split('.')[0]) + '.csv'

        df.to_csv(out_path, index=False)
    def create_dirs(self):
        """Create the required folders to store and generate PLCM."""
        # Create Data Folder
        try:
            os.makedirs(self.base + '/Data/')
        except FileExistsError:
            print('Data Directory Exists, continuing...')

        # Create Bio and Tables Folders
        folders = ['Bio', 'Tables', 'NHSE Docs']
        for f in folders:
            try:
                os.makedirs(self.base+f'/Data/{f}/'+self.date)
            except FileExistsError:
                print(f'{f} folder already exist')






        

    


