# aws-services-list

## Table of Contents
- [What does it do ?](https://github.com/groorj/registrobr-listaliberacao#what-does-it-do)
- [This project uses](https://github.com/groorj/registrobr-listaliberacao#this-project-uses)
- [Notes](https://github.com/groorj/registrobr-listaliberacao#notes)

## What does it do

The code in this repo will download files that you specify and store them in an S3 bucket. This can be useful if you need to track different versions of a file and want to keep a history version of it.

## This project uses / Dependencies

- SAM (AWS Serverless Application Model)
- AWS Lambda
- AWS CloudWatch Logs
- AWS S3
- AWS CloudFormation
- Amazon EventBridge Rules
- Python3
  - boto3
  - pytz
  - logging
  - requests
  - textract-trp

This project uses the AWS Serverless Application Model CLI in order to deploy it to a Lambda serverless function. It will also create an EventBridge Rule to schedule the execution of the function (cronjob).

## Install

Please refer to the AWS SAM CLI installation instructions [here](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html).

Install the required Python modules.

``pip3 -r requirements.txt``

## Configuration

The `template.yaml` template contains the required configuration.
1. Change `<your application name here>` with your app name, without any spaces.
2. Create an S3 bucket and change `BUCKET_NAME` with it. This bucket is where your files will be uploaded to.
3. Update `FILES_TO_DOWNLOAD` with the full URL(s) of the file(s) you want to download and store in S3.
4. (optional) You can also change the frequency that your file(s) will be downloaded by changing the cron-like expression under `Schedule`.

You can also use the file `template.yaml-example` as an example to start with.


## How to build it

Replace <your-aws-profile-name> with your AWS named profile. Check [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html) how to configure your AWS profile.

``sam build``

``sam deploy --profile <your-aws-profile-name> --guided``

The first time you run it, it will prompt you to input information related to your deployment. Here is an example:

```
Configuring SAM deploy
======================

	Looking for config file [samconfig.toml] :  Not found

	Setting default arguments for 'sam deploy'
	=========================================
	Stack Name [sam-app]: aws-serverless-file-downloader-mytest-app
	AWS Region [us-east-1]: us-west-2
	#Shows you resources changes to be deployed and require a 'Y' to initiate deploy
	Confirm changes before deploy [y/N]: y
	#SAM needs permission to be able to create roles to connect to the resources in your template
	Allow SAM CLI IAM role creation [Y/n]:
	#Preserves the state of previously provisioned resources when an operation fails
	Disable rollback [y/N]:
	Save arguments to configuration file [Y/n]:
	SAM configuration file [samconfig.toml]:
	SAM configuration environment [default]:

	Looking for resources needed for deployment:
	Creating the required resources...
```

## Notes

- Running this code will create AWS resources in your account that might not be included in the free tier.
- Use this code at your own risk, I am not responsible for anything related to its use.