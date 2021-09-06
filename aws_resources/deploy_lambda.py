#!/usr/bin/python3

import base64
import json
import os

import docker
import boto3 


def build_and_deploy_lambda_container(lambda_fn_name,repo_name,zip_file_name,tag):
    """Build Docker image, push to AWS and update Lambda fn.
    
    :rtype: None
    """

    '''# get AWS credentials
    print("Get Credentials")

    aws_credentials = read_aws_credentials()
    access_key_id = aws_credentials['access_key_id']
    secret_access_key = aws_credentials['secret_access_key']
    aws_region = aws_credentials['region']'''
    
    print("Building Docker Image")
    # build Docker image
    docker_client = docker.from_env()
    image, build_log = docker_client.images.build(
        path='.', tag=repo_name, rm=True, buildargs={'zip_path':zip_file_name})
    
    print(image)
    
    print("ECR_LOGIN")
    # get AWS ECR login token
    '''ecr_client = boto3.client(
        'ecr' 
        aws_secret_access_key=secret_access_key, region_name=aws_region)
    '''
    ecr_client = boto3.client('ecr')
    
    ecr_credentials = (ecr_client.get_authorization_token()['authorizationData'][0])

    ecr_username = 'AWS'

    ecr_password = (
        base64.b64decode(ecr_credentials['authorizationToken'])
        .replace(b'AWS:', b'')
        .decode('utf-8'))

    ecr_url = ecr_credentials['proxyEndpoint']
    
    # get Docker to login/authenticate with ECR
    docker_client.login(
        username=ecr_username, password=ecr_password, registry=ecr_url)
    
    # tag image for AWS ECR
    ecr_repo_name = '{}/{}'.format(
        ecr_url.replace('https://', ''),repo_name)

    image.tag(ecr_repo_name, tag=tag)
    print("pushing to ecr repo")
    
    # push image to AWS ECR
    push_log = docker_client.images.push(ecr_repo_name, tag=tag)
    
    print("push sucessfull")

    image_uri =  ecr_url.split(":")[1][2:] + "/" + repo_name.split(":")[0] + ":" + tag

    # update the function with the new image 
    cmd = f"aws lambda update-function-code --function-name {lambda_fn_name} --image-uri {image_uri}"
    
    # execute the command 
    print(cmd) 
    os.system(cmd) 

    return None

'''
def read_aws_credentials(filename='.aws_credentials.json'):
    """Read AWS credentials from file.
    
    :param filename: Credentials filename, defaults to '.aws_credentials.json'
    :param filename: str, optional
    :return: Dictionary of AWS credentials.
    :rtype: Dict[str, str]
    """

    try:
        with open(filename) as json_data:
            credentials = json.load(json_data)

        for variable in ('access_key_id', 'secret_access_key', 'region'):
            if variable not in credentials.keys():
                msg = '"{}" cannot be found in {}'.format(variable, filename)
                raise KeyError(msg)
                                
    except FileNotFoundError:
        try:
            credentials = {
                'access_key_id': os.environ['AWS_ACCESS_KEY_ID'],
                'secret_access_key': os.environ['AWS_SECRET_ACCESS_KEY'],
                'region': os.environ['AWS_REGION']
            }
        except KeyError:
            msg = 'no AWS credentials found in file or environment variables'
            raise RuntimeError(msg)

    return credentials
'''
