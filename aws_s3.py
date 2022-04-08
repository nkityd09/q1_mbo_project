import boto3
import json
import configparser

s3 = boto3.client("s3")

def create_bucket(bucket_name):
    response = s3.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': 'us-east-2'
        }
    )
    print(" ")
    print("Created S3 Bucket -> ",response["Location"])
    print(" ")


