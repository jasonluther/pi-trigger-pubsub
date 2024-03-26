# Trigger the Action

[trigger-action.py](./trigger-action.py) uses the utility methods in [spooldir.py](../spooldir.py) to wait for files to show up in a spool directory. 

The file contains the request for work to be done, formatted as a JSON message:
```json
{
    "guess": "heads",
    "requestor_email": "requestor@example.com",
    "request": "flip",
    "request_id": "0e6c6afb-24c0-4faa-9453-33795f8c4bc4",
}
```

There are two tasks to execute. First, a relay is activated by changing the state of the Raspberry Pi's GPIO pin. Second, a still image is captured from a camera. 

The camera image file name needs to be added to the work request, so the next application will get this JSON message, which adds the `image_filename` field:
```json
{
    "guess": "heads",
    "requestor_email": "requestor@example.com",
    "request": "flip",
    "request_id": "0e6c6afb-24c0-4faa-9453-33795f8c4bc4",
    "image_filename": ".../spool/image/0e6c6afb-24c0-4faa-9453-33795f8c4bc4.jpg"
}
```

If those operations are successful, the next application ([local-notify](../local-notify/)) is passed the work request, and the spool file for this application is deleted (similar to acknowledging the pubsub message in the previous step).