import sys
import boto3

ec2 = boto3.client('ec2')
# print(f'ec2.describe_instances(): {ec2.describe_instances()}')

INSTANCE_ID = sys.argv[1]

if len(sys.argv) > 2 and sys.argv[2] == 'ON':
    response = ec2.monitor_instances(InstanceIds=[INSTANCE_ID])
else:
    response = ec2.unmonitor_instances(InstanceIds=[INSTANCE_ID])
print(response)