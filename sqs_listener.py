import boto3
import json
import img_proc

# Initialize the SQS client
sqs = boto3.client('sqs', region_name='eu-north-1')
# Initialize the S3 client
s3 = boto3.client('s3')

# Specify the name of the bucket and the key (path) of the image
bucket_name = 'dist-s3bucket'

# Specify the URL of the SQS queue
queue_url = 'https://sqs.eu-north-1.amazonaws.com/533267349956/image-processing-q'

def download_image_from_s3(bucket_name, image_key):
    try:
        # Download the image from S3 bucket to local file system
        s3.download_file(bucket_name, image_key, 'local_image.jpg')  # Specify the local file path to save the image
        print("Image downloaded successfully")
    except Exception as e:
        print("Error downloading image:", e)

def upload_image_to_s3(bucket_name, image_key):
    try:
        # Upload the image to S3 bucket
        s3.upload_file('result.jpg', bucket_name, 'processed/' + image_key)  # Specify the local file path to upload the image
        print("Image uploaded successfully")
    except Exception as e:
        print("Error uploading image:", e)

# takes the object as input
def process_message(object):

    # Print the key of the object
    print("object key: ", object['key'])

    # Download the image from S3
    download_image_from_s3(bucket_name, object['key'])


    process_name = object['key'].split('/')[1].split('_')[0].strip()
    result_name = object['key'].split('/')[1].split('_')[1].strip()
    print("process_name:", process_name)

    # Process the image
    return_value = img_proc.process_main('local_image.jpg', process_name)

    if return_value == 1:
        print("Image processed successfully")
        upload_image_to_s3(bucket_name, result_name)
    else:
        print("Image processing failed")

    




def listen_for_messages():
    while True:
        try:
            # Long-poll for messages from SQS queue
            response = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=1,  # Receive at most 1 message
                WaitTimeSeconds=20  # Long-polling: Wait for up to 20 seconds
            )

            # Check if there are any messages
            if 'Messages' in response:
                for message in response['Messages']:
                    data = json.loads(message['Body'])
                    object= data['Records'][0]['s3']['object']
                    process_message(object)

                    # Delete the message from the queue once processed
                    sqs.delete_message(
                        QueueUrl=queue_url,
                        ReceiptHandle=message['ReceiptHandle']
                    )
            else:
                print("No messages received")

        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    listen_for_messages()