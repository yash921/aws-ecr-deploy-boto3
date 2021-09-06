import sys
def handler(event, context):
    return 'Hello from AWS Lambda Updated using Python' + sys.version + '!'   
