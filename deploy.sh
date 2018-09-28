#!/bin/bash
# λ deployment script
# Modify as you see fit
echo 'STEP 1: >>> Zipping λ >>>'
zip -r ./lambda.zip .


# Push Zip to S3 bucket
echo 'STEP 2: >>> Upload lambda.zip  to S3 bucket>>>'
aws s3 cp ./lambda.zip s3://lambda/

# Delete Lambda function if it exists
echo 'STEP 3: >>> Delete lambda λ if it exists'
aws lambda delete-function --function-name lambda

# Create λ function if absentd
echo 'STEP 4: >>> Create and Deploy λ  function from S3 bucket >>>'
aws lambda create-function --function-name lambda --code S3Bucket=lambda,S3Key=lambda.zip --handler file_dir.file_name.lambda_handler --role 'ARN role here' --runtime python2.7 --timeout 15 --memory-size 512

# Push code to AWS
echo 'STEP 5: >>> Updating lambda λ code >>>'
aws lambda update-function-code --function-name lambda --s3-bucket lambda --s3-key lambda.zip --publish

# Remove Zip
echo 'STEP 6: >>> Removing ares.zip >>>'
rm lamba.zip
