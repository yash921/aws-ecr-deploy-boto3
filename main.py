import os
from aws_resources.s3 import get_latest_object_from_s3,download_object_from_s3
from aws_resources.deploy_lambda import build_and_deploy_lambda_container


# env variable for s3
BUCKET_NAME = os.environ['BUCKET_NAME']
DOWNLOAD_BASE_LOCATION = os.environ.get('DOWNLOAD_BASE_LOCATION','.')

# env variable for docker and lambda
FUNCTION_NAME = os.environ.get('LAMBDA_FUNCTION_NAME','concierge-fn')
REPOSITORY = os.environ.get('ECR_REPOSITORY_NAME','concierge-project:latest')
tag = os.environ.get('TAG','latest')
#ZIP_FILE = os.environ.get('ZIP_FILE','hello.zip')


# get the latest object name 
latest_added_obj =  get_latest_object_from_s3(BUCKET_NAME)

# download the latest object
download_object_from_s3(BUCKET_NAME,latest_added_obj,DOWNLOAD_BASE_LOCATION + '/'+ latest_added_obj)

ZIP_FILE = DOWNLOAD_BASE_LOCATION + '/'+ latest_added_obj

# build anddeploy container lambda 
build_and_deploy_lambda_container(FUNCTION_NAME,REPOSITORY,ZIP_FILE,tag)