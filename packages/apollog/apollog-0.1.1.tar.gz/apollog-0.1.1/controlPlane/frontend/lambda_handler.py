# lambda_handler.py
import json
import boto3
import os

dynamodb = boto3.client('dynamodb', os.environ.get('TABLE_REGION', 'us-west-2'))
SUMMARY_TABLE_NAME = os.environ.get('TABLE_NAME', '')

def handler(event, context):
    # Handle OPTIONS method for CORS preflight
    response = dynamodb.scan(TableName=SUMMARY_TABLE_NAME)
    items = response.get('Items', [])
    
    # Convert DynamoDB JSON to regular JSON
    from boto3.dynamodb.types import TypeDeserializer
    deserializer = TypeDeserializer()
    
    output = [
        {k: deserializer.deserialize(v) for k, v in item.items()}
        for item in items
    ]
    
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",  # CORS
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Methods": "GET,OPTIONS",
            "Content-Type": "application/json"
        },
        "body": json.dumps(output)
    }
