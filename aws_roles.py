import boto3
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
iam = boto3.client('iam')

# Global Variables

AWS_ACCOUNT_ID = config.get('NAMES', 'AWS_ACCOUNT_ID')
ID_BROKER_ROLE_NAME = config.get('NAMES', 'ID_BROKER_ROLE_NAME')
ID_BROKER_ROLE_ARN = "arn:aws:iam::"+AWS_ACCOUNT_ID+":role/"+ID_BROKER_ROLE_NAME

# AWS Policies

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

# Function to create IAM role and profile

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
    print(" ")
    print("Created IAM Role -> ", create_role["Role"]["RoleName"])
    print("Created IAM Profile -> ", create_profile["InstanceProfile"]["InstanceProfileName"])
    print(" ")
    
    return create_profile["InstanceProfile"]["Arn"]

# Function to create only IAM role 

def create_iam_role(role_name, policy_name):
    create_role = iam.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(policy_name)
    )
    print(" ")
    print("Created IAM Role -> ", create_role["Role"]["RoleName"])
    print(" ")
    return create_role["Role"]["Arn"]

# Function to attach IAM Policy to IAM Role

def attach_policy(role_name, *role_arn):
    for role_arn in role_arn:
        attach_role = iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn=role_arn
        )
        print(" ")
        print("Attached IAM Policy:-",role_arn,"to IAM Role:-",role_name)
        print(" ")
    