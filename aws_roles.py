import boto3
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
iam = boto3.client('iam')

AWS_ACCOUNT_ID = config.get('NAMES', 'AWS_ACCOUNT_ID')
ID_BROKER_ROLE_NAME = config.get('NAMES', 'ID_BROKER_ROLE_NAME')
ID_BROKER_ROLE_ARN = "arn:aws:iam::"+AWS_ACCOUNT_ID+":role/"+ID_BROKER_ROLE_NAME

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
			"AWS": ID_BROKER_ROLE_ARN
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
    create_role = iam.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(policy_name)
    )
    return create_role

def attach_policy(role_name, *role_arn):
    for role_arn in role_arn:
        attach_role = iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn=role_arn
        )
    