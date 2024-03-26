This example is meant to illustrate how a web form can be used to create a request. 

I haven't yet actually provisioned this code as a Google Cloud Function, but that's what it's intended for. 

[cloud-function-make-request.py](./cloud-function-make-request.py) shows how to handle the request without many external dependencies. [cloud-function-make-request-flask.py](./cloud-function-make-request-flask.py) does the same thing, but the code is shorter because it uses Flask. 

[serve-html.sh](./serve-html.sh) simply runs `python -m http.server`, which starts serving files from the directory you start it in. [form.html](./form.html) and [response.html](./response.html) are simple web pages to display the form and acknowledge the request. This represents what the production web server will be doing.

Ultimately, the result of this process is that a JSON message is published to our Google Pub/Sub topic:
```json
{
    "guess": "heads",
    "requestor_email": "requestor@example.com",
    "request": "flip",
    "request_id": "0e6c6afb-24c0-4faa-9453-33795f8c4bc4",
}
```

From there, the pubsub client processes the request. See [pubsub-client](../pubsub-client/). 