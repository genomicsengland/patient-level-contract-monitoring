import boto3
import logging 
import pandas as pd 



class S3:

    def __init__(self, logger=None):
        """Module to connect to s3."""
        aws_logger = logging.getLogger('aws_logger')
        aws_logger.setLevel(logging.INFO)
        self.logger = logger or aws_logger
        self.s3_client = boto3.resource(
            's3',
            aws_access_key_id='AKIAZZ6RHY6DOHLPBJTF',
            aws_secret_access_key='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',
        )

    def upload_file_to_s3(self, source_file_name: str, destination_s3_bucket: str, destination_s3_path: str):
        """Takes a local flat file and uploads to S3."""
        response = self.s3_client.Bucket(destination_s3_bucket).upload_file(source_file_name, 
        destination_s3_path)

        return response

    
    
        
