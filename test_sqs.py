import boto3;

# Get the service resource
sqs = boto3.resource('sqs')

# Create the queue. This returns an SQS.Queue instance
queue = sqs.create_queue(QueueName='test', Attributes={'DelaySeconds': '5'})

# You can now access identifiers and attributes
print(queue.url)
print(queue.attributes.get('DelaySeconds'))

# Print out each queue name, which is part of its ARN
for queue in sqs.queues.all():
    print(f'queue url: {queue.url}')
    print(f'queue name: {queue.attributes["QueueArn"].split(":")[-1]}')

# Create a new message
# response = queue.send_message(MessageBody='world')

# The response is NOT a resource, but gives you a message ID and MD5
# print(response.get('MessageId'))
# print(response.get('MD5OfMessageBody'))

# queue.send_message(MessageBody='boto3', MessageAttributes={
#     'Author': {
#         'StringValue': 'Daniel',
#         'DataType': 'String'
#     }
# })

response = queue.send_messages(Entries=[
    {
        'Id': '1',
        'MessageBody': 'world'
    },
    {
        'Id': '2',
        'MessageBody': 'boto3',
        'MessageAttributes': {
            'Author': {
                'StringValue': 'Daniel',
                'DataType': 'String'
            }
        }
    }
])

# Print out any failures
# print(f'Failed: {response.get("Failed")}')
#
# Print out any successes
# print(f'Successful: {response.get("Successful")}')

# Process messages by printing out body and optional author name
print('Batch processing...')
print(f'{queue.receive_messages(MessageAttributeNames=["Author"])}')
for message in queue.receive_messages(MessageAttributeNames=['Author']):
    # Get the custom author message attribute if it was set
    author_text = ''
    if message.message_attributes is not None:
        author_name = message.message_attributes.get('Author').get('StringValue')
        if author_name:
            author_text = ' ({0})'.format(author_name)

    # Print out the body and author (if set)
    print('Hello, {0}!{1}'.format(message.body, author_text))

    # Let the queue know that the message is processed
    message.delete()

