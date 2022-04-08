import boto3
import json
import aws_policies as ap
import aws_s3 as s3
import aws_keypair as kp
import aws_roles as ar
import configparser
import time
from halo import Halo

config = configparser.ConfigParser()
config.read('config.ini')
iam = boto3.client('iam')

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

def main():
    print("#####")
    print("IAM Policies")
    ap.create_policy(ap.zipped_files)
    print("#####")
    print("S3 Bucket")
    s3.create_bucket(S3_BUCKET_NAME)
    print("#####")
    print("EC2 KeyPair")
    kp.create_ssh_key_pair(KEYPAIR_NAME)
    print("#####")
    print("IAM Roles with Instance Profile")
    ar.create_iam_role_profile(ID_BROKER_ROLE_NAME, ar.aws_cdp_ec2_role_trust_policy_document)
    ar.create_iam_role_profile(LOG_ROLE_NAME, ar.aws_cdp_ec2_role_trust_policy_document)
    print("#####")
    spinner.start()
    time.sleep(8)
    spinner.stop()
    print("IAM Roles")
    ar.create_iam_role(RANGER_AUDIT_ROLE_NAME, ar.aws_cdp_idbroker_role_trust_policy_document)
    ar.create_iam_role(DATALAKE_ADMIN_ROLE_NAME, ar.aws_cdp_idbroker_role_trust_policy_document)
    print("#####")
    print("Attach IAM Policies to IAM Roles")
    ar.attach_policy(ID_BROKER_ROLE_NAME, ap.policy_dict[USERNAME+'aws_cdp_idbroker_assume_role_policy'], ap.policy_dict[USERNAME+'aws_cdp_log_policy'])
    ar.attach_policy(LOG_ROLE_NAME, ap.policy_dict[USERNAME+'aws_cdp_log_policy'])
    ar.attach_policy(RANGER_AUDIT_ROLE_NAME, ap.policy_dict[USERNAME+'aws_cdp_ranger_audit_s3_policy'], ap.policy_dict[USERNAME+'aws_cdp_bucket_access_policy'], ap.policy_dict[USERNAME+'aws_cdp_backup_policy'])
    ar.attach_policy(DATALAKE_ADMIN_ROLE_NAME, ap.policy_dict[USERNAME+'aws_cdp_datalake_admin_s3_policy'], ap.policy_dict[USERNAME+'aws_cdp_bucket_access_policy'], ap.policy_dict[USERNAME+'aws_cdp_backup_policy'])
    print("#####")
    print("All Resources created successfully")
if __name__ == "__main__":
    main()    