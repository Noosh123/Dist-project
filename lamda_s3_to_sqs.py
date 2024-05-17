import json
import boto3

# Initialize the SQS client
sqs = boto3.client('sqs')

# Specify the URL of the SQS queue
queue_url = 'https://sqs.eu-north-1.amazonaws.com/533267349956/image-processing-q'

def lambda_handler(event, context):
    try:
        # Serialize the event object into JSON format
        message_body = json.dumps(event)
        
        # Send message to SQS queue
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body
        )
        
        print("Message sent successfully:", response)
    except Exception as e:
        print("Error sending message:", e)