import sys
import boto3
from botocore.exceptions import ClientError

instance_id = sys.argv[1]
action = sys.argv[2].upper()

ec2 = boto3.client('ec2')


if action == 'ON':
    # Do a dryrun first to verify permissions
    try:
        ec2.start_instances(InstanceIds=[instance_id], DryRun=True)
        # print(f'success: {instance_id} dry run successfully started')
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, run start_instances without dryrun
    try:
        response = ec2.start_instances(InstanceIds=[instance_id], DryRun=False)
        print(response)
        # print(f'success: {instance_id} successfully started')
    except ClientError as e:
        print(e)
else:
    # Do a dryrun first to verify permissions
    try:
        ec2.stop_instances(InstanceIds=[instance_id], DryRun=True)
        # print(f'success: {instance_id} dry run successfully stopped')
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, call stop_instances witout dryrun
    try:
        response = ec2.stop_instances(InstanceIds=[instance_id], DryRun=False)
        # print(f'success: {instance_id} successfully stopped')
        print(response)
    except ClientError as e:
        print(e)