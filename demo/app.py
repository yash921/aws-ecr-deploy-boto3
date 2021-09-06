import json

import numpy
import requests
import pygame
import pandas

def handler(event, context):
    body = {
            "message": "Go Serverless v1.2.0! Your function executed successfully! :) :)",
        "input": event['key1']
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    
