from boto3.dynamodb.types import TypeDeserializer

from notificationService import investigate_issue

deserializer = TypeDeserializer()

def deserialize(dynamo_json):
    return {k: deserializer.deserialize(v) for k, v in dynamo_json.items()}

def lambda_handler(event, context):

    # Initiate TableName, Region, ModelName from env 
    tableName = "Apollog-TimeBlock-Logs"
    tableRegion = "us-west-2"
    modelName = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"

    summaryTableName = "Apollog-event-summary"
    summaryTableRegion = "us-west-2"

    investigate_events_timestamps = []

    for record in event['Records']:
        if 'NewImage' in record['dynamodb']:
            raw = record['dynamodb']['NewImage']
            item = deserialize(raw)

            if item.get('investigate'):
                investigate_events_timestamps.append(item.get('startTime'))            
    
    print(f'Found {len(investigate_events_timestamps)} issues!')
    overall_issue_summary = []

    if(investigate_events_timestamps):
        
        for error_timestamps in investigate_events_timestamps:
            issue_summary = investigate_issue(error_timestamps, tableName, tableRegion, modelName)
            overall_issue_summary.append([error_timestamps, issue_summary])
        
        print("Completed Generating Event Summaries, Writing to Table now!")
        write_summary_table(overall_issue_summary, summaryTableName, summaryTableRegion)
        print("Flow completed Successfully, Write to Summary table complete!")

    else: 
        print("No Issues detected")

def write_summary_table(eventSummaries, tableName, tableregion):
    import boto3
    from botocore.exceptions import ClientError
    import uuid

    # Initialize a session using Amazon DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name=tableregion)
    table = dynamodb.Table(tableName)

    for summary in eventSummaries:
        try:
            # Autogenerate eventID as UUID
            item = {
                'eventID': str(uuid.uuid4()),
                'eventTimestamp': summary[0],
                'summary': summary[1]
            }
            # Insert each summary into the table
            table.put_item(Item=item)
        except ClientError as e:
            print(f"ERROR: Unable to write to table {tableName}. Reason: {e}")
            continue


if __name__ == "__main__":
    event = event = {
    "Records": [
        {
            "eventID": "1",
            "eventName": "INSERT",
            "eventVersion": "1.1",
            "eventSource": "aws:dynamodb",
            "awsRegion": "us-west-2",
            "dynamodb": {
                "Keys": {
                    "UserId": { "S": "user_123" }
                },
                "NewImage": {
  "Id": {
    "S": "c665d71c-1b5a-4b7b-b2c0-8b256b699a0c"
  },
  "blockRank": {
    "N": "1"
  },
  "endTime": {
    "S": "2025-07-06T09:11:57.444000"
  },
  "investigate": {
    "BOOL": "True"
  },
  "logs": {
    "L": [
      {
        "M": {
          "message": {
            "S": "{\"requestId\": \"request-1084\", \"ip\": \"192.168.155.188\", \"requestTime\": \"06/Jul/2025:16:11:46 -0800\", \"httpMethod\": \"PUT\", \"resourcePath\": \"/api/resource/9\", \"status\": 404, \"responseLength\": 505}"
          },
          "service": {
            "S": "DummyAPIGateway"
          },
          "timestamp": {
            "N": "1751818307444"
          }
        }
      },
      {
        "M": {
          "message": {
            "S": "{\"requestId\": \"request-8429\", \"ip\": \"192.168.214.182\", \"requestTime\": \"06/Jul/2025:16:11:46 -0800\", \"httpMethod\": \"PUT\", \"resourcePath\": \"/api/resource/8\", \"status\": 404, \"responseLength\": 4589}"
          },
          "service": {
            "S": "DummyAPIGateway"
          },
          "timestamp": {
            "N": "1751818307444"
          }
        }
      },
      {
        "M": {
          "message": {
            "S": "{\"requestId\": \"request-6846\", \"ip\": \"192.168.56.83\", \"requestTime\": \"06/Jul/2025:16:11:46 -0800\", \"httpMethod\": \"DELETE\", \"resourcePath\": \"/api/resource/1\", \"status\": 400, \"responseLength\": 4552}"
          },
          "service": {
            "S": "DummyAPIGateway"
          },
          "timestamp": {
            "N": "1751818307444"
          }
        }
      },
      {
        "M": {
          "message": {
            "S": "{\"requestId\": \"request-9440\", \"ip\": \"192.168.194.100\", \"requestTime\": \"06/Jul/2025:16:11:46 -0800\", \"httpMethod\": \"GET\", \"resourcePath\": \"/api/resource/4\", \"status\": 400, \"responseLength\": 4284}"
          },
          "service": {
            "S": "DummyAPIGateway"
          },
          "timestamp": {
            "N": "1751818307444"
          }
        }
      },
      {
        "M": {
          "message": {
            "S": "{\"requestId\": \"request-8587\", \"ip\": \"192.168.226.100\", \"requestTime\": \"06/Jul/2025:16:11:46 -0800\", \"httpMethod\": \"DELETE\", \"resourcePath\": \"/api/resource/4\", \"status\": 500, \"responseLength\": 563}"
          },
          "service": {
            "S": "DummyAPIGateway"
          },
          "timestamp": {
            "N": "1751818307444"
          }
        }
      },
      {
        "M": {
          "message": {
            "S": "{\"executionArn\": \"arn:aws:states:us-east-1:123456789012:execution:stateMachine-8076\", \"stateMachineArn\": \"arn:aws:states:us-east-1:123456789012:stateMachine:stateMachine-6468\", \"name\": \"execution-8781\", \"status\": \"SUCCEEDED\", \"startDate\": \"2025-07-06T16:11:46.934Z\", \"stopDate\": \"2025-07-06T16:11:46.934Z\"}"
          },
          "service": {
            "S": "DummyStepFunctions"
          },
          "timestamp": {
            "N": "1751818307819"
          }
        }
      },
      {
        "M": {
          "message": {
            "S": "{\"executionArn\": \"arn:aws:states:us-east-1:123456789012:execution:stateMachine-1701\", \"stateMachineArn\": \"arn:aws:states:us-east-1:123456789012:stateMachine:stateMachine-4972\", \"name\": \"execution-2838\", \"status\": \"RUNNING\", \"startDate\": \"2025-07-06T16:11:46.934Z\", \"stopDate\": \"2025-07-06T16:11:46.934Z\"}"
          },
          "service": {
            "S": "DummyStepFunctions"
          },
          "timestamp": {
            "N": "1751818307819"
          }
        }
      },
      {
        "M": {
          "message": {
            "S": "{\"executionArn\": \"arn:aws:states:us-east-1:123456789012:execution:stateMachine-9264\", \"stateMachineArn\": \"arn:aws:states:us-east-1:123456789012:stateMachine:stateMachine-2102\", \"name\": \"execution-8202\", \"status\": \"SUCCEEDED\", \"startDate\": \"2025-07-06T16:11:46.934Z\", \"stopDate\": \"2025-07-06T16:11:46.934Z\"}"
          },
          "service": {
            "S": "DummyStepFunctions"
          },
          "timestamp": {
            "N": "1751818307819"
          }
        }
      },
      {
        "M": {
          "message": {
            "S": "{\"executionArn\": \"arn:aws:states:us-east-1:123456789012:execution:stateMachine-5458\", \"stateMachineArn\": \"arn:aws:states:us-east-1:123456789012:stateMachine:stateMachine-1744\", \"name\": \"execution-6317\", \"status\": \"RUNNING\", \"startDate\": \"2025-07-06T16:11:46.934Z\", \"stopDate\": \"2025-07-06T16:11:46.934Z\"}"
          },
          "service": {
            "S": "DummyStepFunctions"
          },
          "timestamp": {
            "N": "1751818307819"
          }
        }
      },
      {
        "M": {
          "message": {
            "S": "{\"executionArn\": \"arn:aws:states:us-east-1:123456789012:execution:stateMachine-6444\", \"stateMachineArn\": \"arn:aws:states:us-east-1:123456789012:stateMachine:stateMachine-3601\", \"name\": \"execution-2643\", \"status\": \"FAILED\", \"startDate\": \"2025-07-06T16:11:46.934Z\", \"stopDate\": \"2025-07-06T16:11:46.934Z\"}"
          },
          "service": {
            "S": "DummyStepFunctions"
          },
          "timestamp": {
            "N": "1751818307819"
          }
        }
      }
    ]
  },
  "rowID": {
    "S": "76ee72c4-3360-454f-98c2-632b8d38f2e9"
  },
  "startTime": {
    "S": "2025-07-06T09:11:47.444000"
  }
},
                "SequenceNumber": "111",
                "SizeBytes": 59,
                "StreamViewType": "NEW_IMAGE"
            },
            "eventSourceARN": "arn:aws:dynamodb:us-west-2:123456789012:table/Users/stream/2024-01-01T00:00:00.000"
        }
    ]
}
    lambda_handler(event, None)
