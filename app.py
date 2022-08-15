import json
import requests
import os
import inspect
import urllib.request
import logging
import datetime
import pytz
import boto3
import botocore
import ast

# logger
logger = logging.getLogger()
logger_level = logging.getLevelName(os.environ['LOGGER_LEVEL'])
logger.setLevel(logger_level)

# vars
aws_region = os.environ['AWS_REGION']
tmp_dir = os.environ['TEMP_DIR']
bucket_name = os.environ['BUCKET_NAME']
files_to_download = ast.literal_eval(os.environ['FILES_TO_DOWNLOAD'])

use_timezone = pytz.timezone('America/Sao_Paulo')
my_ct = datetime.datetime.now(tz=pytz.UTC)
new_ct = my_ct.astimezone(use_timezone)
my_timestamp = new_ct.strftime('%Y%m%d%H%M%S')

logger.info("aws_region: [%s]", aws_region)
logger.info("my_timestamp: [%s]", my_timestamp)
logger.info("tmp_dir: [%s]", tmp_dir)
logger.info("files_to_download: [%s]", files_to_download)

# delete folder and files recursively
def deltree(target):
    logger.debug("Inside function: [%s]", inspect.currentframe().f_code.co_name)
    for d in os.listdir(target):
        try:
            deltree(target + '/' + d)
        except OSError:
            os.remove(target + '/' + d)
    os.rmdir(target)

# create response
def create_response(status_code, message):
    logger.debug("Inside function: [%s]", inspect.currentframe().f_code.co_name)
    return {
        'statusCode': str(status_code),
        'body': json.dumps({ "message": message }),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
            },
        }

# upload file to S3
def upload_to_s3(local_file, bucket_name, s3_file):
    logger.debug("Inside function: [%s]", inspect.currentframe().f_code.co_name)
    
    s3 = boto3.client('s3')
    try:
        response = s3.upload_file(local_file, bucket_name, s3_file)
    except botocore.exceptions.ClientError as e:
        logger.error("Something went wrong")
        logger.error(e)
        return False
    logger.info("Upload Successful")
    return True

# main
def execute_handler(event, context):
    logger.debug("Inside function: [%s]", inspect.currentframe().f_code.co_name)

    # clean tmp dir
    if os.path.isdir(tmp_dir):
        logger.info("deltree: [%s]", tmp_dir)
        deltree(tmp_dir)

    # create tmp dir
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    for file_name_url in files_to_download:
        logger.info("file_name_url: [%s]", file_name_url)
        tmp_only_file_name = os.path.basename(file_name_url)
        tmp_file_name = my_timestamp + "_" + tmp_only_file_name
        tmp_complete_file_name = tmp_dir + "/" + tmp_file_name
        logger.info("tmp_complete_file_name: [%s]", tmp_complete_file_name)

        # download file
        r1 = requests.get(file_name_url)
        with open(tmp_complete_file_name, 'wb') as f:
            f.write(r1.content)
        logger.info("File [%s] size is: [%s]", tmp_complete_file_name, os.path.getsize(tmp_complete_file_name))
        logger.debug("After writing the file")
        logger.info(os.listdir(tmp_dir))

        # upload file
        logger.debug("upload_to_s3(%s, %s, %s)", tmp_complete_file_name, bucket_name, tmp_file_name)
        upload_to_s3(tmp_complete_file_name, bucket_name, tmp_file_name)
        logger.debug("=================================================================================================")

    return create_response(200, "Success")

# End;