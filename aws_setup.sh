#!/bin/bash

#Check current IAM User/Role

aws sts get-caller-identity;

#Setup S3 bucket
aws s3api create-bucket --bucket q1_mbo_project --region us-east-2



