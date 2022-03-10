import boto3
import json
import aws_policies as ap
import aws_s3 as s3
import aws_keypair as kp
import configparser

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

aws_cdp_ec2_role_trust_policy_document = {
	"Version": "2012-10-17",
	"Statement": [{
		"Effect": "Allow",
		"Principal": {
			"Service": "ec2.amazonaws.com"
		},
		"Action": "sts:AssumeRole"
	}]
}
aws_cdp_idbroker_role_trust_policy_document = {
	"Version": "2012-10-17",
	"Statement": [{
		"Effect": "Allow",
		"Principal": {
			"AWS": "arn:aws:iam::"+AWS_ACCOUNT_ID+":role/"+ID_BROKER_ROLE_NAME
		},
		"Action": "sts:AssumeRole"
	}]
}

def create_iam_role_profile(role_name, policy_name):
    create_role = iam.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(policy_name)
    )

    create_profile = iam.create_instance_profile(
        InstanceProfileName=role_name
    )

    add_role_to_profile = iam.add_role_to_instance_profile(
    InstanceProfileName=role_name,
    RoleName=role_name
    )
    return create_role, create_profile, add_role_to_profile

def create_iam_role(role_name, policy_name):
    response = iam.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(policy_name)
    )
    return response

def generate_policy_arn(account_id):
    policy_arns = []
    for i in range(len(ap.policy_names)):
        policy_arns.append("arn:aws:iam::"+account_id+":policy/"+ap.policy_names[i])
    return policy_arns

policy_arns = generate_policy_arn(AWS_ACCOUNT_ID)
policy_dict = {}

for i in range(len(policy_arns)):
    policy_dict[ap.policy_names[i]] = policy_arns[i]


def attach_policy(role_name, *role_arn):
    for role_arn in role_arn:
        response = iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn=role_arn
        )
    

s3.create_bucket(S3_BUCKET_NAME)
kp.create_ssh_key_pair(KEYPAIR_NAME)
create_iam_role_profile(ID_BROKER_ROLE_NAME, aws_cdp_ec2_role_trust_policy_document)
create_iam_role_profile(LOG_ROLE_NAME, aws_cdp_ec2_role_trust_policy_document)
create_iam_role(RANGER_AUDIT_ROLE_NAME, aws_cdp_idbroker_role_trust_policy_document)
create_iam_role(DATALAKE_ADMIN_ROLE_NAME, aws_cdp_idbroker_role_trust_policy_document)
attach_policy(ID_BROKER_ROLE_NAME, policy_dict[USERNAME+'aws_cdp_idbroker_assume_role_policy'],policy_dict[USERNAME+'aws_cdp_log_policy'])
attach_policy(LOG_ROLE_NAME, policy_dict[USERNAME+'aws_cdp_log_policy'])
attach_policy(RANGER_AUDIT_ROLE_NAME, policy_dict[USERNAME+'aws_cdp_ranger_audit_s3_policy'],policy_dict[USERNAME+'aws_cdp_bucket_access_policy'],policy_dict[USERNAME+'aws_cdp_backup_policy'])
attach_policy(DATALAKE_ADMIN_ROLE_NAME, policy_dict[USERNAME+'aws_cdp_datalake_admin_s3_policy'],policy_dict[USERNAME+'aws_cdp_bucket_access_policy'],policy_dict[USERNAME+'aws_cdp_backup_policy'])


#####Rough Code#####

# def generate_policy_dict(ap.policy_documents, policy_arns):
#     policy_dict = {}
#     for i in ap.policy_documents():
#         policy_dict[i] = policy_arns[i] # Wll not work 



# response = iam.attach_role_policy(
#             RoleName = role_name
#             PolicyArn = 
#         )
