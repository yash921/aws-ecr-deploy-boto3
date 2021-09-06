import boto3

s3 = boto3.client('s3')
bucketName = 'concierge-fn-test-lambda'
get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))
objs = s3.list_objects_v2(Bucket=bucketName)['Contents']
last_added = [obj['Key'] for obj in sorted(objs, key=get_last_modified, reverse=True)][0]
# print(last_added)

s3.download_file(bucketName,last_added, '/home/yash/aws-ecr-deploy-boto3/hellp.zip')

