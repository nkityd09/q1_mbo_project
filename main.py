import boto3
import aws_policies as ap
import aws_s3 as s3
import aws_keypair as kp
import aws_roles as ar
import cdp_env as ce
import configparser
import time
from halo import Halo

# Import Configurations from config.ini 
config = configparser.ConfigParser()
config.read('config.ini')
iam = boto3.client('iam')

#Import Configurations for AWS resources
USERNAME = config.get('NAMES', 'USERNAME_PREFIX')
S3_BUCKET_NAME = config.get('S3', 'S3_BUCKET')
AWS_ACCOUNT_ID = config.get('NAMES', 'AWS_ACCOUNT_ID')
ID_BROKER_ROLE_NAME = config.get('NAMES', 'ID_BROKER_ROLE_NAME')
LOG_ROLE_NAME = config.get('NAMES', 'LOG_ROLE_NAME')
RANGER_AUDIT_ROLE_NAME = config.get('NAMES', 'RANGER_AUDIT_ROLE_NAME')
DATALAKE_ADMIN_ROLE_NAME = config.get('NAMES', 'DATALAKE_ADMIN_ROLE_NAME')
KEYPAIR_NAME = config.get('NAMES', 'KEYPAIR_NAME')
ID_BROKER_ROLE_ARN = "arn:aws:iam::"+AWS_ACCOUNT_ID+":role/"+ID_BROKER_ROLE_NAME
spinner = Halo(text='Creating IAM resources', spinner='simpleDots')

#Import Configuration for CDP Environment
ENV_NAME = config.get('CDP_NAMES','ENV_NAME')
CREDENTIAL_NAME = config.get('CDP_NAMES','CREDENTIAL_NAME')
REGION = config.get('CDP_NAMES','REGION')
CIDR = config.get('CDP_NAMES','CIDR')
DATALAKE_NAME = config.get('CDP_NAMES','DATALAKE_NAME')
DATALAKE_SIZE = config.get('CDP_NAMES','DATALAKE_SIZE')
DATALAKE_RUNTIME = config.get('CDP_NAMES','DATALAKE_RUNTIME')


def main():
    #Create IAM policies
    print("#####")
    print("IAM Policies")
    ap.create_policy(ap.zipped_files)
    #Create S3 Bucket
    print("#####")
    print("S3 Bucket")
    s3.create_bucket(S3_BUCKET_NAME)
    #Create EC2 Keypair
    print("#####")
    print("EC2 KeyPair")
    kp.create_ssh_key_pair(KEYPAIR_NAME)
    #Create IAM Role and Instance Profile
    print("#####")
    print("IAM Roles with Instance Profile")
    ID_BROKER_INSTANCE_PROFILE_ARN = ar.create_iam_role_profile(ID_BROKER_ROLE_NAME, ar.aws_cdp_ec2_role_trust_policy_document)
    LOG_INSTANCE_PROFILE_ARN = ar.create_iam_role_profile(LOG_ROLE_NAME, ar.aws_cdp_ec2_role_trust_policy_document)
    print("#####")
    spinner.start()
    time.sleep(8)
    spinner.stop()
    #Create IAM Role 
    print("IAM Roles")
    RANGER_ROLE_ARN = ar.create_iam_role(RANGER_AUDIT_ROLE_NAME, ar.aws_cdp_idbroker_role_trust_policy_document)
    DATALAKE_ROLE_ARN = ar.create_iam_role(DATALAKE_ADMIN_ROLE_NAME, ar.aws_cdp_idbroker_role_trust_policy_document)
    print("#####")
    print("Attach IAM Policies to IAM Roles")
    #Attach IAM Policy to IAM Roles
    ar.attach_policy(ID_BROKER_ROLE_NAME, ap.policy_dict[USERNAME+'aws_cdp_idbroker_assume_role_policy'], ap.policy_dict[USERNAME+'aws_cdp_log_policy'])
    ar.attach_policy(LOG_ROLE_NAME, ap.policy_dict[USERNAME+'aws_cdp_log_policy'])
    ar.attach_policy(RANGER_AUDIT_ROLE_NAME, ap.policy_dict[USERNAME+'aws_cdp_ranger_audit_s3_policy'], ap.policy_dict[USERNAME+'aws_cdp_bucket_access_policy'], ap.policy_dict[USERNAME+'aws_cdp_backup_policy'])
    ar.attach_policy(DATALAKE_ADMIN_ROLE_NAME, ap.policy_dict[USERNAME+'aws_cdp_datalake_admin_s3_policy'], ap.policy_dict[USERNAME+'aws_cdp_bucket_access_policy'], ap.policy_dict[USERNAME+'aws_cdp_backup_policy'])
    print("#####")
    print("All AWS Resources created successfully")
    #Create CDP Environment ID Broker and DataLake 
    print("#####")
    print("Creating CDP Environment")
    ce.create_env(ENV_NAME, CREDENTIAL_NAME, REGION, KEYPAIR_NAME, S3_BUCKET_NAME, LOG_INSTANCE_PROFILE_ARN, CIDR)
    print("Creating ID_Broker Environment")
    ce.create_id_broker(ENV_NAME, DATALAKE_ROLE_ARN, RANGER_ROLE_ARN)
    print("Creating CDP Datalake Environment")
    ce.create_datalake(DATALAKE_NAME, ENV_NAME, ID_BROKER_INSTANCE_PROFILE_ARN, S3_BUCKET_NAME, DATALAKE_SIZE, DATALAKE_RUNTIME)

if __name__ == "__main__":
    main()    