import boto3
import json
import configparser
import time
import cdp_env as ce
from halo import Halo
config = configparser.ConfigParser()
config.read('config.ini')
iam = boto3.client('iam')
s3 = boto3.client('s3')
s3_resource = boto3.resource('s3')
ec2 = boto3.client('ec2')

USERNAME = config.get('NAMES', 'USERNAME_PREFIX')
ID_BROKER_ROLE_NAME=config.get('NAMES', 'ID_BROKER_ROLE_NAME')
LOG_ROLE_NAME=config.get('NAMES', 'LOG_ROLE_NAME')
RANGER_AUDIT_ROLE_NAME=config.get('NAMES', 'RANGER_AUDIT_ROLE_NAME')
DATALAKE_ADMIN_ROLE_NAME=config.get('NAMES', 'DATALAKE_ADMIN_ROLE_NAME')
AWS_ACCOUNT_ID=config.get('NAMES', 'AWS_ACCOUNT_ID')
S3_BUCKET_NAME = config.get('S3', 'S3_BUCKET')
KEYPAIR_NAME = config.get('NAMES', 'KEYPAIR_NAME')
ENV_NAME = config.get('CDP_NAMES','ENV_NAME')
DATALAKE_NAME = config.get('CDP_NAMES','DATALAKE_NAME')
spinner = Halo(text='Deleting CDP Env', spinner='simpleDots')

#TODO: Change name of below variable
policy_names_= [USERNAME+"aws_cdp_log_policy", USERNAME+"aws_cdp_idbroker_assume_role_policy", USERNAME+"aws_cdp_ranger_audit_s3_policy", USERNAME+"aws_cdp_datalake_admin_s3_policy", USERNAME+"aws_cdp_bucket_access_policy", USERNAME+"aws_cdp_backup_policy"]

def cleanup_roles_profiles(rolename):
    remove_role_to_profile = iam.remove_role_from_instance_profile(
    InstanceProfileName=rolename,
    RoleName=rolename
    )
    
    response = iam.delete_instance_profile(
        InstanceProfileName=rolename
    )

    response = iam.delete_role(
        RoleName = rolename
    )

    

def cleanup_roles(rolename):
    response = iam.delete_role(
        RoleName = rolename
    )

# response = iam.delete_policy(
#     PolicyArn='arn:aws:iam::268282262010:policy/aws_cdp_log_policy_ankit_boto3'
# )

policy_names= ["arn:aws:iam::268282262010:policy/"+USERNAME+"aws_cdp_log_policy", "arn:aws:iam::268282262010:policy/"+USERNAME+"aws_cdp_idbroker_assume_role_policy", "arn:aws:iam::268282262010:policy/"+USERNAME+"aws_cdp_ranger_audit_s3_policy", "arn:aws:iam::268282262010:policy/"+USERNAME+"aws_cdp_datalake_admin_s3_policy", "arn:aws:iam::268282262010:policy/"+USERNAME+"aws_cdp_bucket_access_policy", "arn:aws:iam::268282262010:policy/"+USERNAME+"aws_cdp_backup_policy"]


def cleanup():
    for i in policy_names:
        response = iam.delete_policy(
        PolicyArn=i
        )

def generate_policy_arn(account_id):
    policy_arns = []
    for i in range(len(policy_names)):
        policy_arns.append("arn:aws:iam::"+account_id+":policy/"+policy_names_[i])
    return policy_arns

policy_arns = generate_policy_arn(AWS_ACCOUNT_ID)

policy_dict = {}

for i in range(len(policy_arns)):
    policy_dict[policy_names_[i]] = policy_arns[i]



def detach_policy(role_name, *role_arn):
    for role_arn in role_arn:
        response = iam.detach_role_policy(
            RoleName=role_name,
            PolicyArn=role_arn
        )        

def delete_s3_bucket(bucket_name):
    bucket = s3_resource.Bucket(bucket_name)
    bucket.objects.all().delete()
    response = s3.delete_bucket(
    Bucket=bucket_name
    )

def delete_ssh_key_pair(key_pair_name):
    key_pair = ec2.delete_key_pair(
        KeyName = key_pair_name
    )

ce.delete_datalake(DATALAKE_NAME)
spinner.start()
time.sleep(1200)
spinner.stop()
ce.delete_env(ENV_NAME)
spinner.start()
time.sleep(300)
spinner.stop()
detach_policy(ID_BROKER_ROLE_NAME, policy_dict[USERNAME+"aws_cdp_idbroker_assume_role_policy"], policy_dict[USERNAME+'aws_cdp_log_policy'])
detach_policy(LOG_ROLE_NAME, policy_dict[USERNAME+'aws_cdp_log_policy'])
detach_policy(RANGER_AUDIT_ROLE_NAME, policy_dict[USERNAME+'aws_cdp_ranger_audit_s3_policy'], policy_dict[USERNAME+'aws_cdp_bucket_access_policy'], policy_dict[USERNAME+'aws_cdp_backup_policy'])
detach_policy(DATALAKE_ADMIN_ROLE_NAME, policy_dict[USERNAME+'aws_cdp_datalake_admin_s3_policy'], policy_dict[USERNAME+'aws_cdp_bucket_access_policy'], policy_dict[USERNAME+'aws_cdp_backup_policy'])

cleanup()
cleanup_roles_profiles(ID_BROKER_ROLE_NAME)
cleanup_roles_profiles(LOG_ROLE_NAME)
cleanup_roles(RANGER_AUDIT_ROLE_NAME)
cleanup_roles(DATALAKE_ADMIN_ROLE_NAME)
delete_ssh_key_pair(KEYPAIR_NAME)
delete_s3_bucket(S3_BUCKET_NAME)
