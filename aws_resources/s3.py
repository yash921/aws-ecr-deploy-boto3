import boto3


# s3 client
s3 = boto3.client('s3')

def get_latest_object_from_s3(bucket_name):

    get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))

    # all the objects
    objs = s3.list_objects_v2(Bucket=bucket_name)['Contents']

    # get the last added object
    last_added_obj = [obj['Key'] for obj in sorted(objs, key=get_last_modified, reverse=True)][0]

    
    return last_added_obj 

def download_object_from_s3(bucket_name,object_name,download_location):
    # download the latest object
    s3.download_file(bucket_name,object_name, download_location)


