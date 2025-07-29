import boto3
import yaml
import logging

def convertYAMLtoDict(config):
    with open(config, 'r') as file:
        return yaml.safe_load(file)
    
def convertLogsIntoTimeBlocks(logs):
    timeDividedLogs = []
    timeDividedLogs.append({"timeBlock": 1, "startTime":None, "endTime":None, "logSummary": 
                            {
                                "services":['API', 'Lambda'],
                                "errors":"None",
                                "logs":[]
                             }})
    return timeDividedLogs

def fetchLogs(nameSpace, region, last_timestamp):
    client = boto3.client('logs', region_name=region)
    import datetime

    # Convert last_timestamp from ISO format to Unix timestamp in milliseconds
    if last_timestamp:
        last_timestamp = int(datetime.datetime.fromisoformat(last_timestamp).timestamp() * 1000)

    response = client.filter_log_events(
        logGroupName=nameSpace,
        startTime=last_timestamp + 1  # Fetch logs newer than the given timestamp
    )

    events = response.get('events', [])

    logs = [(event['timestamp'], event['message']) for event in events]
    return logs

def exportLogsToDB(time_blocks, table_name='Apollog-TimeBlock-Logs', region_name='us-west-2'):
    dynamodb = boto3.resource('dynamodb', region_name=region_name)
    table = dynamodb.Table(table_name)
    
    for block in time_blocks:
        # Convert datetime objects to strings
        block['startTime'] = block['startTime'].isoformat()
        block['endTime'] = block['endTime'].isoformat()
        
        table.put_item(Item=block)

def getLatestEndTime(table_name='Apollog-TimeBlock-Logs', region_name='us-west-2'):
    dynamodb = boto3.resource('dynamodb', region_name=region_name)
    table = dynamodb.Table(table_name)
    
    response = table.scan()
    items = response.get('Items', [])
    
    if not items:
        return 0
    
    latest_end_time = max(item['endTime'] for item in items)
    return latest_end_time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ingestLogs(config):
    config = convertYAMLtoDict(config)
    
    # get the table name and region for log export
    table_name = config['architecture']['tableName']
    table_region = config['architecture']['tableRegion']

    checkpoint_timestamp = getLatestEndTime(table_name, table_region)

    logging.info("Starting log ingestion process.")
    logs = []
    for service in config["services"]:
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
    return time_blocks

def create_time_block(block_start_time, block_duration, current_block, block_rank):
    import uuid
    return {
        "Id": str(uuid.uuid4()),  # Added Id key
        "rowID": str(uuid.uuid4()),
        "startTime": block_start_time,
        "endTime": block_start_time + block_duration,
        "logs": current_block,
        "blockRank": block_rank,
        "investigate": any("error" in log['message'].lower() or "warning" in log['message'].lower() or 'failed' in log['message'].lower() for log in current_block)
    }

def convertLogsIntoTimeBlocks(logs):
    import datetime

    # Sort logs by timestamp
    logs.sort(key=lambda x: x['timestamp'])
    
    # Create time blocks
    time_blocks = []
    current_block = []
    block_start_time = None
    block_duration = datetime.timedelta(seconds=10)
    block_rank = 1
    
    for log in logs:
        log_time = datetime.datetime.fromtimestamp(log['timestamp'] / 1000.0)
        
        if block_start_time is None:
            block_start_time = log_time
        
        if log_time - block_start_time < block_duration:
            if len(current_block) < 10:
                current_block.append(log)
            else:
                time_blocks.append(create_time_block(block_start_time, block_duration, current_block, block_rank))
                current_block = [log]
                block_rank += 1
        else:
            if current_block:
                time_blocks.append(create_time_block(block_start_time, block_duration, current_block, block_rank))
            current_block = [log]
            block_start_time = log_time
            block_rank = 1
    
    # Add the last block if it has logs
    if current_block:
        time_blocks.append(create_time_block(block_start_time, block_duration, current_block, block_rank))
    
    return time_blocks




if __name__ == "__main__":

    ingestLogs("examples/config.yaml")
