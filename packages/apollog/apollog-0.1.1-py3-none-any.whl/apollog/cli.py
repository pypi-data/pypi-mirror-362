import argparse
import boto3
import yaml
import zipfile
import os
import json 
import shutil
import subprocess
import tempfile
import pkg_resources

def build_lambda_package(source_dir, output_zip):
    with tempfile.TemporaryDirectory() as temp_dir:
        # Install dependencies if requirements.txt exists
        requirements_path = os.path.join(source_dir, 'requirements.txt')
        if os.path.exists(requirements_path):
            subprocess.check_call([
                'pip', 'install', '-r', requirements_path, '-t', temp_dir
            ])

        # Copy all .py and other files to temp_dir
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, source_dir)
                dest_path = os.path.join(temp_dir, rel_path)

                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(src_path, dest_path)

        # Zip the contents
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, temp_dir)
                    zipf.write(full_path, arcname=rel_path)

def get_package_path(relative_path):
    """Get the absolute path to a file within the package."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

def create_lambda_zip(project_dir=None):
    """
    Create Lambda deployment packages.
    
    Args:
        project_dir: Optional directory where the project is located. If None, uses the current directory.
    """
    if project_dir is None:
        project_dir = os.getcwd()
    
    os.makedirs('build', exist_ok=True)

    # Build zip for log ingestion Lambda
    log_ingestion_dir = os.path.join(project_dir, 'controlPlane/logIngestionEngine')
    build_lambda_package(
        source_dir=log_ingestion_dir,
        output_zip='build/lambda_function.zip'
    )
    print("ZIP creation for Log Ingestion Lambda Complete!")

    # Build zip for summary Lambda
    notification_dir = os.path.join(project_dir, 'controlPlane/notificationEngine')
    build_lambda_package(
        source_dir=notification_dir,
        output_zip='build/summary_lambda_function.zip'
    )
    print("ZIP Creation for Summary Lambda Complete!")

    # Build zip for frontend Lambda
    frontend_dir = os.path.join(project_dir, 'controlPlane/frontend')
    build_lambda_package(
        source_dir=frontend_dir, 
        output_zip='build/frontend_lambda_function.zip'
    )
    print("ZIP Creation for Frontend Lambda Complete!")

def deploy_stack(config_path, project_dir=None):
    """
    Deploy the CloudFormation stack.
    
    Args:
        config_path: Path to the configuration YAML file
        project_dir: Optional directory where the project is located. If None, uses the current directory.
    """
    if project_dir is None:
        project_dir = os.getcwd()
    
    create_lambda_zip(project_dir)
    
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    region = config.get("architecture", {}).get("tableRegion", "us-west-2")
    logs_table_name = config.get("architecture", {}).get("logTableName", "MyDDBTable")
    summary_table_name = config.get("architecture", {}).get("summaryTableName", "Apollog-event-summary")
    stack_name = config.get('stack_name', 'default-stack-name')

    cloudformation = boto3.client('cloudformation', region)
    s3 = boto3.client('s3', region)

    bucket_name = 'apollog-dev-artifacts'

    try:
        response = s3.delete_public_access_block(Bucket=bucket_name)
        print("Public access block removed.")
    except s3.exceptions.ClientError as e:
        print(f"Note: Could not remove public access block: {e}")
    
    # Upload zip to S3
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} already exists. Utilizing existing bucket.")
    except s3.exceptions.ClientError:
        s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': region})
        print(f"Bucket {bucket_name} created.")
    
    s3.upload_file('build/lambda_function.zip', bucket_name, 'lambda_function.zip')
    s3.upload_file('build/summary_lambda_function.zip', bucket_name, 'summary_lambda_function.zip')
    s3.upload_file('build/frontend_lambda_function.zip', bucket_name, 'frontend_lambda_function.zip')
    
    # Reference S3 object in CloudFormation template
    s3_key_lambda = 'lambda_function.zip'
    s3_key_summary = 'summary_lambda_function.zip'
    s3_key_frontend = 'frontend_lambda_function.zip'
    
    # Get CloudFormation template path
    template_path = os.path.join(project_dir, 'cloudformation_template.yaml')
    if not os.path.exists(template_path):
        # Try to find it in the package resources
        template_path = pkg_resources.resource_filename('apollog', 'cloudformation_template.yaml')
    
    with open(template_path, 'r') as template_file:
        template_body = template_file.read()

    parameters = [
        {'ParameterKey': 'BucketName', 'ParameterValue': bucket_name},
        {'ParameterKey': 'S3KeyLambda', 'ParameterValue': s3_key_lambda},
        {'ParameterKey': 'S3KeySummary', 'ParameterValue': s3_key_summary},
        {'ParameterKey': 'S3KeyFrontend', 'ParameterValue': s3_key_frontend},
        {'ParameterKey': 'LogsTableName', 'ParameterValue': logs_table_name},
        {'ParameterKey': 'SummaryTableName', 'ParameterValue': summary_table_name},
        {'ParameterKey': 'FrontendTableName', 'ParameterValue': summary_table_name},
        {'ParameterKey': 'Region', 'ParameterValue': region},
        {'ParameterKey': 'Services', 'ParameterValue': json.dumps(config.get("services", []))}
    ]

    try:
        # Check if stack exists
        cloudformation.describe_stacks(StackName=stack_name)
        # If it exists, prompt user for action
        user_input = input(f"Stack {stack_name} already exists. Do you want to update it? (Y/N): ").strip().upper()
        if user_input == 'Y':
            response = cloudformation.update_stack(
                StackName=stack_name,
                TemplateBody=template_body,
                Parameters=parameters,
                Capabilities=['CAPABILITY_NAMED_IAM']
            )
            print(f'Stack {stack_name} update initiated. Response: {response}')
        else:
            print("Update cancelled by user.")
            return
    except cloudformation.exceptions.ClientError as e:
        if 'does not exist' in str(e):
            # If it doesn't exist, create the stack
            response = cloudformation.create_stack(
                StackName=stack_name,
                TemplateBody=template_body,
                Parameters=parameters,
                Capabilities=['CAPABILITY_NAMED_IAM']
            )
            print(f'Stack {stack_name} creation initiated. Response: {response}')
        else:
            raise

    # Track stack creation progress
    import time

    def print_stack_events(stack_name):
        events = cloudformation.describe_stack_events(StackName=stack_name)['StackEvents']
        for event in events:
            print(f"Resource: {event['LogicalResourceId']}, Status: {event['ResourceStatus']}, Reason: {event.get('ResourceStatusReason', 'N/A')}")

    print(f'Tracking progress for stack {stack_name}...')
    while True:
        print_stack_events(stack_name)
        time.sleep(10)  # Wait for 10 seconds before checking again
        stack_status = cloudformation.describe_stacks(StackName=stack_name)['Stacks'][0]['StackStatus']
        if stack_status.endswith('_COMPLETE') or stack_status.endswith('_FAILED'):
            break

    print(f'Stack {stack_name} has reached status: {stack_status}')

    # Get frontend files
    frontend_dir = os.path.join(project_dir, 'controlPlane/frontend')
    index_path = os.path.join(frontend_dir, 'index.html')
    config_json_path = os.path.join(frontend_dir, 'config.json')

    # Upload index.html and config.json to S3
    s3.upload_file(index_path, bucket_name, 'index.html', ExtraArgs={'ContentType': 'text/html'})
    s3.upload_file(config_json_path, bucket_name, 'config.json', ExtraArgs={'ContentType': 'application/json'})
    print('Uploaded index.html and config.json to S3.')

    # Set S3 bucket policy to allow public read access
    bucket_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/*"
            }
        ]
    }

    s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(bucket_policy))
    print('Set S3 bucket policy to allow public read access.')

    # Retrieve the API ID from the stack outputs
    stack_description = cloudformation.describe_stacks(StackName=stack_name)
    outputs = stack_description['Stacks'][0].get('Outputs', [])
    api_id = next((output['OutputValue'] for output in outputs if output['OutputKey'] == 'ApiGatewayRestApiId'), None)

    if api_id:
        # Update the config.json file with the API ID and region
        with open(config_json_path, 'w') as config_file:
            json.dump({"apiId": api_id, "region": region}, config_file, indent=2)
        print(f'Updated {config_json_path} with API ID and region.')
    else:
        print('API ID not found in stack outputs.')

def init_project(destination):
    """
    Initialize a new Apollog project in the specified directory.
    
    Args:
        destination: Directory where the project will be created
    """
    if not os.path.exists(destination):
        os.makedirs(destination)
    
    # Copy template files from package
    for resource in ['cloudformation_template.yaml', 'examples/config.yaml']:
        try:
            source = pkg_resources.resource_filename('apollog', resource)
            dest = os.path.join(destination, resource)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(source, dest)
        except Exception as e:
            print(f"Warning: Could not copy {resource}: {e}")
    
    # Create controlPlane directory structure
    for dir_path in ['controlPlane/frontend', 'controlPlane/logIngestionEngine', 'controlPlane/notificationEngine']:
        os.makedirs(os.path.join(destination, dir_path), exist_ok=True)
    
    print(f"Apollog project initialized in {destination}")
    print("Next steps:")
    print("1. Configure your AWS credentials")
    print("2. Edit examples/config.yaml to specify your services")
    print("3. Run 'apollog deploy --config examples/config.yaml' to deploy the stack")

def main():
    parser = argparse.ArgumentParser(description='Apollog CLI')
    subparsers = parser.add_subparsers(dest='command')

    # Deploy command
    deploy_parser = subparsers.add_parser('deploy', help='Deploy a CloudFormation stack')
    deploy_parser.add_argument('--config', required=True, help='Path to the configuration file')
    deploy_parser.add_argument('--project-dir', help='Path to the project directory (default: current directory)')

    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize a new Apollog project')
    init_parser.add_argument('--destination', default='.', help='Directory where the project will be created (default: current directory)')

    args = parser.parse_args()

    if args.command == 'deploy':
        deploy_stack(args.config, args.project_dir)
    elif args.command == 'init':
        init_project(args.destination)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
