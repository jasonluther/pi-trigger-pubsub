import os
import uuid
from flask import Flask, request, redirect
from google.cloud import pubsub_v1
from dotenv import load_dotenv, find_dotenv
import json

app = Flask(__name__)

load_dotenv(find_dotenv())
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
project_id = os.getenv("GOOGLE_PROJECT_ID") or os.getenv("GOOGLE_CLOUD_PROJECT")
topic_name = os.getenv("PUBSUB_TOPIC")
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)


@app.route("/coin", methods=["POST", "GET"])
def make_request():
    if request.method == "GET":
        form=request.args
    elif request.method == "POST":
        form=request.form
         
    email = form.get("email")
    guess = form.get("guess")
    form_response = form.get("form_response")
    
    if form_response is None:
        form_response = "/default-url"  
    
    message = {
        "guess": guess,
        "requestor_email": email,
        "request": "flip",
        "request_id": str(uuid.uuid4()),
    }
    message_json = json.dumps(message)
    publisher.publish(topic_path, data=message_json.encode("utf-8"))
    return redirect(form_response)


if __name__ == "__main__":
    app.run()
