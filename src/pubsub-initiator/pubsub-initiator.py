import os
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
import json
import uuid
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
credentials_path = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
project_id = os.environ["GOOGLE_PROJECT_ID"]
topic_name = os.environ["PUBSUB_TOPIC"]

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)

data = {"request": "flip", "guess": "heads", "requestor_email": "jason@ixid.net"}
data["request_id"] = str(uuid.uuid4())
message = json.dumps(data).encode("utf-8")
future = publisher.publish(topic_path, data=message)
print(f"Published message ID: {future.result()}")
