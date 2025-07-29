from collections import defaultdict
import json 
import boto3

from botocore.exceptions import ClientError

def call_llm(prompt, modelName):
    # Initialize a session using Amazon Bedrock
    client = boto3.client('bedrock-runtime', 'us-west-2')
    modelId = modelName
    native_request = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 51200,
    "temperature": 0.5,
    "messages": [
        {
            "role": "user",
            "content": [{"type": "text", "text": prompt}],
        }
    ],
    }
    
    request = json.dumps(native_request)

    try:
        # Invoke the model with the request.
        response = client.invoke_model(modelId=modelId, body=request)

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{modelId}'. Reason: {e}")
        exit(1)

    # Decode the response body.
    model_response = json.loads(response["body"].read())

    # Extract and print the response text.
    response_text = model_response["content"][0]["text"]
    return response_text

def investigate_issue(error_timestamp, tableName, tableRegion, modelName):
    
    #Fetch all the logs from the DDB timeBlocks where startTime is newer than error_timestamp - 1 Day
    all_logs = fetch_logs_from_timestamp(error_timestamp, tableName, tableRegion)

    print(f'Fetched {len(all_logs)} for all services!')

    # Group All the logs based on service that emitted it
    service_to_log_mapping = group_logs_by_service(all_logs)

    print('Completed Grouping of logs by service type!')

    # summarize the logs for each service individually 
    service_to_summary_mapping = {}

    for service in service_to_log_mapping:
        service_to_summary_mapping[service] = generate_log_summary_by_service(service, service_to_log_mapping[service], modelName)
        print(f'Generated Log Summary for {service}')

    # Generate Event Summary for the error incident
    print(f'Generating overall Event Summary for error on {error_timestamp}')
    return generate_event_summary(service_to_summary_mapping, modelName)
    



def fetch_logs_from_timestamp(timestamp, tableName, tableRegion):
    import boto3
    import datetime

    # Initialize a session using Amazon DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name=tableRegion)
    table = dynamodb.Table(tableName)

    # Calculate the target timestamp (timestamp - 1 day)
    target_timestamp = (datetime.datetime.fromisoformat(timestamp) - datetime.timedelta(days=1)).isoformat()

    # Scan the table for logs with startTime newer than target_timestamp
    response = table.scan(
        FilterExpression="startTime > :val",
        ExpressionAttributeValues={":val": target_timestamp}
    )

    # Extract logs from the response
    logs = response.get('Items', [])
    return logs

def group_logs_by_service(logs):
    all_logs = []

    for block in logs: 
        all_logs.extend(block["logs"])

    
    logs_by_service = defaultdict(list)

    for log in all_logs: 
        logs_by_service[log["service"]].append(log)
        

    
    for service in logs_by_service.keys():
        logs_by_service[service] = sorted(logs_by_service[service], key= lambda x : x['timestamp'])
    
    return logs_by_service

def batch_logs_by_quantity(logs, limit=50):
    batched_logs = []
    current_batch = []

    for log in logs:
        current_batch.append(log)
        if len(current_batch) == limit:
            batched_logs.append(current_batch)
            current_batch = []

    if current_batch:
        batched_logs.append(current_batch)

    return batched_logs

def generate_log_summary_by_service(serviceName, service_logs, modelName):
    
    # batch the serviceLogs
    batched_logs = batch_logs_by_quantity(service_logs)

    sub_log_summary = []
    i = 1 
    for logList in batched_logs:
        sub_log_summary.append(prepare_sub_log_prompt(logList, serviceName, modelName))
        print(f'  * Generating Summary for Log Group {i} for {serviceName}')
        i += 1
        break # TODO: REMOVE
    print(f'  * Generated Individual TimeBlock Summaries for {serviceName}')

    service_summary = prepare_overall_service_summary(sub_log_summary, modelName)

    return service_summary

        
def prepare_overall_service_summary(sub_log_summary, modelName):
    prompt = f"""
You are a cloud infrastructure assistant analyzing service logs.

Below are summaries of log batches from a specific service:

{chr(10).join(f"- {s}" for s in sub_log_summary)}

Your task is to carefully review these summaries and identify:
1. Any anomalies, recurring errors, or failure patterns
2. Warnings or performance degradation signs
3. Possible root causes (if evident)
4. Any parts of the system that may require attention

Be concise, structured, and technical in your analysis. If there are no issues, state clearly that the service appears healthy.
"""

    return call_llm(prompt, modelName)

def generate_event_summary(service_to_summary_mapping, modelName):
    """
    Generates a high-level summary of a system-wide event based on per-service log summaries.

    Args:
        service_to_summary_mapping (dict): Mapping from service name to its log summary.
        modelName (str): The name of the LLM model to use.

    Returns:
        str: An overall event summary generated by the LLM.
    """
    service_summaries_str = "\n".join(
        f"- {service}: {summary}" for service, summary in service_to_summary_mapping.items()
    )

    prompt = f"""
You are a cloud incident analysis agent. Your task is to analyze logs from multiple services and generate a high-level summary of the event that occurred.

Here are the log summaries from each service:

{service_summaries_str}

Your goal is to:
1. Determine what went wrong, if anything.
2. Identify how different services were impacted.
3. Detect any root causes or cascading failures.
4. Highlight which service likely experienced the initial fault.
5. Summarize the system-wide impact and potential recovery steps.

Be concise, technical, and structured in your response. If the system appears healthy, state that explicitly.
"""

    return call_llm(prompt, modelName)


def prepare_sub_log_prompt(logs, serviceName, modelName):

    generate_sub_log_summary_prompt = f'''
    Service Name: {serviceName}

    Logs:
    {logs}

    Instructions:
    - Analyze the logs provided above.
    - Infer the type of service based on the Service Name.
    - Prepare a summary of what the logs indicate.
    - Highlight any errors or anomalies found in the logs.
    '''

    return (call_llm(generate_sub_log_summary_prompt, modelName))

    pass
