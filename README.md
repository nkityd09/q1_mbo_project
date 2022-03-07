Script will create/use below AWS resources

1. Create S3 buckets
   
2. Create Policy Files
  - aws-cdp-idbroker-assume-role-policy.json
  - TODO: Add AWS_ACCOUNT_ID and IDBROKER_ROLE -> aws-cdp-idbroker-role-trust-policy.json
  - aws-cdp-ec2-role-trust-policy.json
  - TODO: Add LOGS_BUCKET and LOGS_LOCATION_BASE -> aws-cdp-log-policy.json
  - TODO: Add BACKUP_LOCATION_BASE -> aws-cdp-backup-policy.json
  - TODO: Add STORAGE_LOCATION_BASE and DATALAKE_BUCKET -> aws-cdp-ranger-audit-s3-policy.json
  - TODO: Add STORAGE_LOCATION_BASE and STORAGE_LOCATION_BASE -> aws-cdp-datalake-admin-s3-policy.json
  - TODO: Add DATALAKE_BUCKET -> aws-cdp-bucket-access-policy.json
  - TODO: Add DYNAMODB_TABLE_NAME -> aws-cdp-dynamodb-policy.json

3. Set variables for 
- ${AWS_ACCOUNT_ID} - Your AWS account ID
- ${DATALAKE_BUCKET} - Your S3 bucket. For example my-bucket
- ${STORAGE_LOCATION_BASE} - Path to your Data Lake directory in the S3 bucket specified as ${DATALAKE_BUCKET}/SOME_PATH. For example my-bucket/my-dl
- ${LOGS_LOCATION_BASE} - Path to your S3 location for logs. For example my-bucket/my-dl/logs
- ${DYNAMODB_TABLE_NAME} - The name of your DynamoDB table used for S3Guard. This should correspond to your DynamoDB Table Name provided under Enable S3Guard during environment creation.

4. Create IAM Role

5. Create IAM Policies

Use function outputs as input for other functions ?