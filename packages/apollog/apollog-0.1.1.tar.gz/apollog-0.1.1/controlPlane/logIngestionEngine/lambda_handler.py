import boto3
import os
import logging
from logIngestionService import fetchLogs, convertLogsIntoTimeBlocks, exportLogsToDB, getLatestEndTime

def lambda_handler(event, context):
    # Retrieve configuration from environment variables
    table_name = os.environ.get('TABLE_NAME', 'Apollog-TimeBlock-Logs')
    table_region = os.environ.get('TABLE_REGION', 'us-west-2')
    services = os.environ.get('SERVICES', '[]')  # Expecting a JSON string of services

    # Convert services from JSON string to Python list
    import json
    services = json.loads(services)

    checkpoint_timestamp = getLatestEndTime(table_name, table_region)

    logging.info("Starting log ingestion process.")
    logs = []
    for service in services:
        service_logs = fetchLogs(service['namespace'], service["region"], checkpoint_timestamp)
        for log in service_logs:
            logs.append({
                "service": service['serviceName'],
                "timestamp": log[0],
                "message": log[1]
            })
    
    logging.info(f"Fetched {len(logs)} logs from services.")
    time_blocks = convertLogsIntoTimeBlocks(logs)

    exportLogsToDB(time_blocks, table_name, table_region)
    logging.info(f"Created {len(time_blocks)} time blocks.")
    logging.info("Log ingestion process completed.")
    return {
        'statusCode': 200,
        'body': f"Successfully ingested logs and created {len(time_blocks)} time blocks."
    }
