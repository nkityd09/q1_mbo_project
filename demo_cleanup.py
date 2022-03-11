import boto3
import json
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
iam = boto3.client('iam')
s3 = boto3.client('s3')

USERNAME = config.get('NAMES', 'USERNAME_PREFIX')
ID_BROKER_ROLE_NAME=config.get('NAMES', 'ID_BROKER_ROLE_NAME')
LOG_ROLE_NAME=config.get('NAMES', 'LOG_ROLE_NAME')
RANGER_AUDIT_ROLE_NAME=config.get('NAMES', 'RANGER_AUDIT_ROLE_NAME')
DATALAKE_ADMIN_ROLE_NAME=config.get('NAMES', 'DATALAKE_ADMIN_ROLE_NAME')
AWS_ACCOUNT_ID=config.get('NAMES', 'AWS_ACCOUNT_ID')
S3_BUCKET_NAME = config.get('S3', 'S3_BUCKET')

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

policy_names= ["arn:aws:iam::268282262010:policy/ankity_boto3_aws_cdp_log_policy", "arn:aws:iam::268282262010:policy/ankity_boto3_aws_cdp_idbroker_assume_role_policy", "arn:aws:iam::268282262010:policy/ankity_boto3_aws_cdp_ranger_audit_s3_policy", "arn:aws:iam::268282262010:policy/ankity_boto3_aws_cdp_datalake_admin_s3_policy", "arn:aws:iam::268282262010:policy/ankity_boto3_aws_cdp_bucket_access_policy", "arn:aws:iam::268282262010:policy/ankity_boto3_aws_cdp_backup_policy"]


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



def detach_policy(role_name, role_arn):
    response = iam.detach_role_policy(
        RoleName=role_name,
        PolicyArn=role_arn
    )        

def delete_s3_bucket(bucket_name):
    response = s3.delete_bucket(
    Bucket=bucket_name
    )

# detach_policy(ID_BROKER_ROLE_NAME, policy_dict[USERNAME+"aws_cdp_idbroker_assume_role_policy"])
# detach_policy(ID_BROKER_ROLE_NAME, policy_dict[USERNAME+'aws_cdp_log_policy'])
# detach_policy(LOG_ROLE_NAME, policy_dict[USERNAME+'aws_cdp_log_policy'])
# detach_policy(RANGER_AUDIT_ROLE_NAME, policy_dict[USERNAME+'aws_cdp_ranger_audit_s3_policy'])
# detach_policy(RANGER_AUDIT_ROLE_NAME, policy_dict[USERNAME+'aws_cdp_bucket_access_policy'])
# detach_policy(RANGER_AUDIT_ROLE_NAME, policy_dict[USERNAME+'aws_cdp_backup_policy'])
# detach_policy(DATALAKE_ADMIN_ROLE_NAME, policy_dict[USERNAME+'aws_cdp_datalake_admin_s3_policy'])
# detach_policy(DATALAKE_ADMIN_ROLE_NAME, policy_dict[USERNAME+'aws_cdp_bucket_access_policy'])
# detach_policy(DATALAKE_ADMIN_ROLE_NAME, policy_dict[USERNAME+'aws_cdp_backup_policy'])

# cleanup()
# cleanup_roles_profiles(ID_BROKER_ROLE_NAME)
# cleanup_roles_profiles(LOG_ROLE_NAME)
# cleanup_roles(RANGER_AUDIT_ROLE_NAME)
# cleanup_roles(DATALAKE_ADMIN_ROLE_NAME)
# #TODO: Add delete keypair function
delete_s3_bucket(S3_BUCKET_NAME) #TODO: Make bucket empty before deleting