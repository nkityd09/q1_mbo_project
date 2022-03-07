import boto3
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
s3 = boto3.client("s3")
S3_BUCKET_NAME = config.get('S3', 'S3_BUCKET')


def create_bucket(bucket_name):
    response = s3.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': 'us-east-2'
        }
    )

#create_bucket(S3_BUCKET_NAME)    
