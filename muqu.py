import boto3
import json
from botocore.exceptions import ClientError


class MuQu:
    def __init__(self, access_key, secret_key, region_name="us-east-1"):
        self.session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region_name,
        )
        self.sqs = self.session.resource("sqs")

    def create_queue(self, queue_name):
        # Create a dead-letter queue first
        dl_queue_name = queue_name + "-dead-letter.fifo"
        dl_queue = self.sqs.create_queue(
            QueueName=dl_queue_name,
            Attributes={
                "FifoQueue": "true",
                "MessageRetentionPeriod": str(
                    14 * 24 * 60 * 60
                ),  # 14 days expressed in seconds
            },
        )
        print("Dead-letter Queue created:", dl_queue.url)

        # Get the DLQ's ARN (Amazon Resource Name)
        dl_queue_arn = dl_queue.attributes["QueueArn"]

        # Create a redrive policy
        redrive_policy = {"deadLetterTargetArn": dl_queue_arn, "maxReceiveCount": "2"}

        # Create the main queue with the redrive policy
        main_queue = self.sqs.create_queue(
            QueueName=queue_name + ".fifo",
            Attributes={
                "FifoQueue": "true",
                "ContentBasedDeduplication": "true",  # enable content-based deduplication
                "RedrivePolicy": json.dumps(
                    redrive_policy
                ),  # specify the redrive policy
                "ReceiveMessageWaitTimeSeconds": "20",  # enable long polling
            },
        )
        print("Main Queue created:", main_queue.url)

    def delete_queue(self, queue_name):
        dl_queue_name = queue_name + "-dead-letter.fifo"
        queue_name += ".fifo"
        queue = self.sqs.get_queue_by_name(QueueName=queue_name)
        queue.delete()

        dl_queue = self.sqs.get_queue_by_name(QueueName=dl_queue_name)
        dl_queue.delete()
        print("Queue deleted")

    def push(self, queue_name, data):
        queue_name += ".fifo"
        queue = self.sqs.get_queue_by_name(QueueName=queue_name)
        response = queue.send_message(
            MessageBody=json.dumps(data), MessageGroupId="MessageGroupId"
        )
        print("Message ID:", response["MessageId"])

    def fetch(self, queue_name):
        queue_name += ".fifo"
        queue = self.sqs.get_queue_by_name(QueueName=queue_name)
        messages = queue.receive_messages(MaxNumberOfMessages=1)
        if messages:
            message = messages[0]
            print("Received message:", message.body)
            data = json.loads(message.body)
            meta = {"receipt_handle": message.receipt_handle}
            m = {"data": data, "meta": meta}
            print("fetched message", m)
            return json.dumps(m)

    def remove(self, queue_name, message):
        message = json.loads(message)
        queue_name += ".fifo"
        queue = self.sqs.get_queue_by_name(QueueName=queue_name)
        message = queue.Message(message["meta"]["receipt_handle"])
        message.delete()
        print("Message deleted")

    def peek(self, queue_name):
        queue_name += ".fifo"
        queue = self.sqs.get_queue_by_name(QueueName=queue_name)
        messages = queue.receive_messages(MaxNumberOfMessages=1, VisibilityTimeout=0)
        if messages:
            message = messages[0]
            print("Peeked message:", message.body)
            return json.loads(message.body)
