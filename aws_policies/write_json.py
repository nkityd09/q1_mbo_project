import boto3
import json

iam = boto3.client('iam')

LOGS_BUCEKT="arn:aws:s3:::ankity-cdp"
LOGS_LOCATION_BASE="arn:aws:s3:::ankity-cdp"

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
			"AWS": "arn:aws:iam::${AWS_ACCOUNT_ID}:role/${IDBROKER_ROLE}" #TODO:
		},
		"Action": "sts:AssumeRole"
	}]
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
			"Resource": "arn:aws:s3:::${STORAGE_LOCATION_BASE}/ranger/audit/*" #TODO:
		},
		{
			"Sid": "LimitedAccessToDataLakeBucket",
			"Effect": "Allow",
			"Action": [
				"s3:AbortMultipartUpload",
				"s3:ListBucket",
				"s3:ListBucketMultipartUploads"
			],
			"Resource": "arn:aws:s3:::${DATALAKE_BUCKET}" #TODO:
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
			"arn:aws:s3:::${STORAGE_LOCATION_BASE}", #TODO:
			"arn:aws:s3:::${STORAGE_LOCATION_BASE}/*" #TODO:
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
				"arn:aws:s3:::${DATALAKE_BUCKET}", #TODO:
				"arn:aws:s3:::${DATALAKE_BUCKET}/*" #TODO:
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
		"Resource": "arn:aws:s3:::${BACKUP_LOCATION_BASE}/*" #TODO:
	}]
}

aws_cdp_dynamodb_policy_document = {
	"Version": "2012-10-17",
	"Statement": [{
			"Effect": "Allow",
			"Action": [
				"dynamodb:List*",
				"dynamodb:DescribeReservedCapacity*",
				"dynamodb:DescribeLimits",
				"dynamodb:DescribeTimeToLive"
			],
			"Resource": "*"
		},
		{
			"Effect": "Allow",
			"Action": [
				"dynamodb:BatchGetItem",
				"dynamodb:BatchWriteItem",
				"dynamodb:CreateTable",
				"dynamodb:DeleteItem",
				"dynamodb:DescribeTable",
				"dynamodb:GetItem",
				"dynamodb:PutItem",
				"dynamodb:Query",
				"dynamodb:UpdateItem",
				"dynamodb:Scan",
				"dynamodb:TagResource",
				"dynamodb:UntagResource"
			],
			"Resource": "arn:aws:dynamodb:*:*:table/${DYNAMODB_TABLE_NAME}" #TODO:
		}
	]
}

policy_names= ["aws_cdp_log_policy_ankity_boto3", "aws_cdp_ec2_role_trust_policy_ankity_boto3", "aws_cdp_idbroker_role_trust_policy_ankity_boto3", "aws_cdp_idbroker_assume_role_policy_ankity_boto3", "aws_cdp_ranger_audit_s3_policy_ankity_boto3", "aws_cdp_datalake_admin_s3_policy_ankity_boto3", "aws_cdp_bucket_access_policy_ankity_boto3", "aws_cdp_backup_policy_ankity_boto3", "aws_cdp_dynamodb_policy_ankity_boto3"]

policy_documents = [aws_cdp_log_policy_document, aws_cdp_ec2_role_trust_policy_document, aws_cdp_idbroker_role_trust_policy_document, aws_cdp_idbroker_assume_role_policy_document, aws_cdp_ranger_audit_s3_policy_document, aws_cdp_datalake_admin_s3_policy_document, aws_cdp_bucket_access_policy_document, aws_cdp_backup_policy_document, aws_cdp_dynamodb_policy_document]

zipped_files = zip(policy_names, policy_documents)

for i,j in zipped_files:
    cdp_policy_create = iam.create_policy(
    PolicyName=i,
    PolicyDocument=json.dumps(j)
    )



#####Rough Code#####

# def updateJsonFile():
#     jsonFile = open("aws-cdp-log-policy1.json", "r") # Open the JSON file for reading
#     data = json.load(jsonFile) # Read the JSON into the buffer    
#     print(data["Statement"][1]["Resource"])
#     data["Statement"][0]["Resource"] = LOGS_BUCEKT
#     data["Statement"][1]["Resource"] = LOGS_LOCATION_BASE+"/*"
#     ## Save our changes to JSON file
#     jsonFile = open("aws-cdp-log-policy1.json", "w+")
#     jsonFile.write(json.dumps(data))
#     jsonFile.close()

# updateJsonFile()