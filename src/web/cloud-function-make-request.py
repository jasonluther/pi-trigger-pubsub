from google.cloud import pubsub_v1
import os
import uuid
import json


def publish_message(request):
    # Set the CORS headers for the preflight request
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }
        return ("", 204, headers)

    # Set the CORS headers for the main request
    headers = {"Access-Control-Allow-Origin": "*"}
    # Extract parameters from the request
    if request.method == "POST":
        guess = request.form.get("guess")
        email = request.form.get("email")
        form_response = request.form.get("form_response")
    elif request.method == "GET":
        guess = request.args.get("guess")
        email = request.args.get("email")
        form_response = request.args.get("form_response")

    project_id = os.getenv("GOOGLE_PROJECT_ID") or os.getenv("GOOGLE_CLOUD_PROJECT")
    topic_name = os.getenv("PUBSUB_TOPIC")

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    # Construct the message data
    message = {
        "guess": guess,
        "requestor_email": email,
        "request": "flip",
        "request_id": str(uuid.uuid4()),
    }
    message_data = bytes(json.dumps(message), "utf-8")

    # Publish the message
    publisher.publish(topic_path, data=message_data)

    # Redirect to the form_response URL if the operation is successful
    if form_response:
        return ("", 302, {"Location": form_response})

    return (
        f'Request {message["request_id"]} processed successfully.',
        200,
        headers,
    )


if __name__ == "__main__":
    """For local testing"""
    from flask import Flask, request

    app = Flask(__name__)

    @app.route("/coin", methods=["POST", "GET"])
    def handle_request():
        return publish_message(request)

    app.run()
