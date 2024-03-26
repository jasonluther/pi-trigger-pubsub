import os
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
import json
from dotenv import load_dotenv, find_dotenv
from spooldir import write_spool_file

load_dotenv(find_dotenv())
credentials_path = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
project_id = os.environ['GOOGLE_PROJECT_ID']
subscription_name = os.environ['PUBSUB_SUBSCRIPTION']
trigger_spool_dir = os.environ['TRIGGER_SPOOL_DIRECTORY']

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_name)

def message_callback(message):
    try:
        request = json.loads(message.data.decode('utf-8'))
        message.ack()
    except json.JSONDecodeError as e:
        print(f'Error decoding message: {e}')
        message.nack()
        return
    print(f'Request: {request}')
    write_spool_file(trigger_spool_dir, f'{request["request_id"]}.json', json.dumps(request))

streaming_pull_future = subscriber.subscribe(subscription_path, callback=message_callback)
print(f'Listening for messages on {subscription_path}')

with subscriber:
        try:
            streaming_pull_future.result()
            
        except TimeoutError:
            streaming_pull_future.cancel()
            streaming_pull_future.result()