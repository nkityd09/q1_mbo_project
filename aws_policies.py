import boto3
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
iam = boto3.client('iam')

#####Global Variables#####

#TODO: Ensure bucket name is setup correctly in all policies and 
LOGS_BUCEKT=config.get('S3', 'S3_BUCKET_ARN')
LOGS_LOCATION_BASE=config.get('S3', 'S3_BUCKET_ARN')
USERNAME = config.get('NAMES', 'USERNAME_PREFIX')  # Username will be appended to all policy names


#####AWS Policies#####

aws_cdp_log_policy_document = {
	"Version": "2012-10-17",
	"Statement": [{
			"Effect": "Allow",
			"Action": [
				"s3:ListBucket"
			],
			"Resource": LOGS_BUCEKT
		},
		{
			"Effect": "Allow",
			"Action": [
				"s3:AbortMultipartUpload",
				"s3:ListMultipartUploadParts",
				"s3:PutObject"
			],
			"Resource": LOGS_LOCATION_BASE+"/*"
		}
	]
}

aws_cdp_idbroker_assume_role_policy_document ={
	"Version": "2012-10-17",
	"Statement": [{
		"Sid": "VisualEditor0",
		"Effect": "Allow",
		"Action": [
			"sts:AssumeRole"
		],
		"Resource": [
			"*"
		]
	}]
}

aws_cdp_ranger_audit_s3_policy_document = {
	"Version": "2012-10-17",
	"Statement": [{
			"Sid": "FullObjectAccessUnderAuditDir",
			"Effect": "Allow",
			"Action": [
				"s3:GetObject",
				"s3:PutObject"
			],
			"Resource": LOGS_LOCATION_BASE+"/ranger/audit/*" 
		},
		{
			"Sid": "LimitedAccessToDataLakeBucket",
			"Effect": "Allow",
			"Action": [
				"s3:AbortMultipartUpload",
				"s3:ListBucket",
				"s3:ListBucketMultipartUploads"
			],
			"Resource": LOGS_LOCATION_BASE 
		}
	]
}

aws_cdp_datalake_admin_s3_policy_document = {
	"Version": "2012-10-17",
	"Statement": [{
		"Sid": "VisualEditor3",
		"Effect": "Allow",
		"Action": [
			"s3:AbortMultipartUpload",
			"s3:DeleteObject",
			"s3:DeleteObjectVersion",
			"s3:GetAccelerateConfiguration",
			"s3:GetAnalyticsConfiguration",
			"s3:GetBucketAcl",
			"s3:GetBucketCORS",
			"s3:GetBucketLocation",
			"s3:GetBucketLogging",
			"s3:GetBucketNotification",
			"s3:GetBucketObjectLockConfiguration",
			"s3:GetBucketPolicy",
			"s3:GetBucketPolicyStatus",
			"s3:GetBucketPublicAccessBlock",
			"s3:GetBucketRequestPayment",
			"s3:GetBucketTagging",
			"s3:GetBucketVersioning",
			"s3:GetBucketWebsite",
			"s3:GetEncryptionConfiguration",
			"s3:GetInventoryConfiguration",
			"s3:GetLifecycleConfiguration",
			"s3:GetMetricsConfiguration",
			"s3:GetObject",
			"s3:GetObjectAcl",
			"s3:GetObjectLegalHold",
			"s3:GetObjectRetention",
			"s3:GetObjectTagging",
			"s3:GetObjectVersion",
			"s3:GetObjectVersionAcl",
			"s3:GetObjectVersionTagging",
			"s3:GetReplicationConfiguration",
			"s3:ListBucket",
			"s3:ListBucketMultipartUploads",
			"s3:ListBucketVersions",
			"s3:ListMultipartUploadParts",
			"s3:PutObject"
		],
		"Resource": [
			LOGS_LOCATION_BASE, 
			LOGS_LOCATION_BASE+"/*" 
		]
	}]
}

aws_cdp_bucket_access_policy_document = {
	"Version": "2012-10-17",
	"Statement": [{
			"Effect": "Allow",
			"Action": [
				"s3:CreateJob",
				"s3:GetAccountPublicAccessBlock",
				"s3:ListJobs"
			],
			"Resource": "*"
		},
		{
			"Sid": "AllowListingOfDataLakeFolder",
			"Effect": "Allow",
			"Action": [
				"s3:GetAccelerateConfiguration",
				"s3:GetAnalyticsConfiguration",
				"s3:GetBucketAcl",
				"s3:GetBucketCORS",
				"s3:GetBucketLocation",
				"s3:GetBucketLogging",
				"s3:GetBucketNotification",
				"s3:GetBucketPolicy",
				"s3:GetBucketPolicyStatus",
				"s3:GetBucketPublicAccessBlock",
				"s3:GetBucketRequestPayment",
				"s3:GetBucketTagging",
				"s3:GetBucketVersioning",
				"s3:GetBucketWebsite",
				"s3:GetEncryptionConfiguration",
				"s3:GetInventoryConfiguration",
				"s3:GetLifecycleConfiguration",
				"s3:GetMetricsConfiguration",
				"s3:GetObject",
				"s3:GetObjectAcl",
				"s3:GetObjectTagging",
				"s3:GetObjectVersion",
				"s3:GetObjectVersionAcl",
				"s3:GetObjectVersionTagging",
				"s3:GetReplicationConfiguration",
				"s3:ListBucket",
				"s3:ListBucketMultipartUploads",
				"s3:ListMultipartUploadParts"
			],
			"Resource": [
				LOGS_LOCATION_BASE, 
				LOGS_LOCATION_BASE+"/*"
			]
		}
	]
}

aws_cdp_backup_policy_document = {
	"Version": "2012-10-17",
	"Statement": [{
		"Effect": "Allow",
		"Action": [
			"s3:AbortMultipartUpload",
			"s3:ListMultipartUploadParts",
			"s3:PutObject"
		],
		"Resource": LOGS_LOCATION_BASE+"/*" 
	}]
}


# creating lists for policy names and policy documents

policy_names= [USERNAME+"aws_cdp_log_policy", USERNAME+"aws_cdp_idbroker_assume_role_policy",
 USERNAME+"aws_cdp_ranger_audit_s3_policy", USERNAME+"aws_cdp_datalake_admin_s3_policy", 
 USERNAME+"aws_cdp_bucket_access_policy", USERNAME+"aws_cdp_backup_policy"]

policy_documents = [aws_cdp_log_policy_document, aws_cdp_idbroker_assume_role_policy_document, 
 aws_cdp_ranger_audit_s3_policy_document, aws_cdp_datalake_admin_s3_policy_document, 
 aws_cdp_bucket_access_policy_document, aws_cdp_backup_policy_document]

#zip function pairs the first item of each list together

zipped_files = zip(policy_names, policy_documents) 


#####create_policy function creates IAM policies using policy names and policy documents#####

def create_policy(zip_list):
	for policy_names,policy_documents in zipped_files:
		cdp_policy_create = iam.create_policy(
			PolicyName=policy_names,
			PolicyDocument=json.dumps(policy_documents)
		)
	
create_policy(zipped_files)


#####Rough Code#####
