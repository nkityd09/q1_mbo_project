import boto3
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
ec2 = boto3.client('ec2')

def create_ssh_key_pair(key_pair_name):
    key_pair = ec2.create_key_pair(
        KeyName = key_pair_name
    )

    return key_pair

##### Rough Code #####