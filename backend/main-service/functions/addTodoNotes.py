import boto3
import json
import os
import logging
import uuid
from datetime import datetime

client = boto3.client('dynamodb', region_name='ca-central-1')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def addTodoNotes(todoID, notes):
    response = client.update_item(
        TableName=os.environ['TODO_TABLE'],
        Key={
            'todoID': {
                'S': todoID
            }
        },
        UpdateExpression="SET notes = :b",
        ExpressionAttributeValues={':b': {'S': notes}}
    )
    response = {}
    response["Update"] = "Success"

    return json.dumps(response)
def lambda_handler(event, context):
    logger.info(event)
    eventBody = json.loads(event["body"])

    todoID = event['pathParameters']['todoID']
    notes = eventBody["notes"]
    
    logger.info(f'adding notes for : {todoID}')
    response = addTodoNotes(todoID, notes)
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': 'https://todoaug.houessou.com',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Content-Type': 'application/json'
        },
        'body': response
    }