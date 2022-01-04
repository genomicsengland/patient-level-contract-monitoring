"""
Control Interface for PLCM functions
"""
import logging
import fire
import os
from python_files import plcm, bio
from sqlalchemy import create_engine


LOGGER = logging.getLogger(__name__)

class RunPLCM:
    class Prepare:

        def __init__(self):
            self.plcm_instance = plcm.PLCM('Nov 2021')
            self.ngis_biobank_engine = create_engine(
                        'postgresql+psycopg2://ngis_data_quality:QXW45Kiv7BrZgruLREZGzd7dO92s91KQ@10.1.30.104/ngis_biobank_prod'
                    )
            self.ngis_gr_engine = create_engine(
                        'postgresql+psycopg2://ngis_data_quality:QXW45Kiv7BrZgruLREZGzd7dO92s91KQ@10.1.30.104/ngis_genomicrecord_prod'
                    )

        def dirs(self):
            """Creates the required directories for a local PLCM run."""
            LOGGER.info("creating required PLCM directories")            
            self.plcm_instance.create_dirs()

        def create_gms_tracker_file(self):
            """Creates the gms tracker file."""
            LOGGER.info("creating GMS Tracker")
            self.plcm_instance.create_gms_tracker_file()

        def run_sql(self):
            """Iterates through SQL folder and executes all sql queries."""
            LOGGER.info("Running SQL Scripts")
            sql_files = os.listdir('sql/')
            for sq in sql_files:
                engine = self.ngis_biobank_engine
                if 'genomicrecord' in sq:
                    engine = self.ngis_gr_engine
                self.plcm_instance.db_to_csv(sq, engine, '/Data/Tables/')

        def run_bio(self):
            """Runs the bio files."""
            LOGGER.info("Running bio file setup")
            self.plcm_instance.execute_bio_file()


if __name__ == '__main__':
    """Build the fire interface."""
    fire.Fire(RunPLCM)

