# Triggering an action with Raspberry Pi and Google Cloud Pub/Sub

This is a set of simple tools to demonstrate some ways to trigger a Raspberry Pi to do something based on a request made in the cloud. 

It is mainly a collection of sample code, so I disclaim any ownership I may have of these files and dedicate them to the public domain. 

For this example, we will trigger a request using a message service. A Raspberry Pi will respond to each request by activating attached hardware, taking a picture, and triggering the final response (delivery of an email). 

[rpi-gpio-setup.md](./rpi-gpio-setup.md) describes some of the work required to use the GPIO pins. 

[gcp-setup.md](./gcp-setup.md) describes some of the work required to configure services in Google Cloud Platform. 

[email-setup.md](./email-setup.md) explains how to embed images into an email and deliver the email successfully to end users. 

## Flow

These are the key steps in the flow:

1. Something triggers publication of a message to Google Pub/Sub. See [web](./src/web/readme.md).
2. A Pub/Sub client on the Raspberry Pi waits for messages. Whenever one is received, it writes a request to a local "trigger" queue. See [pubsub-client](./src/pubsub-client/).
3. An application waits for a request in the trigger queue. It will execute the process to trigger the action you want, capture an image, and then write out a new request to a new "notify" queue. See [local-trigger](./src/local-trigger/).
4. An application waits for a request in the notify queue. Then it emails the results. See [local-notify](./src/local-notify/).

## Queues

There are many ways to manage a queue of work. Pub/Sub is a convenient way to orchestrate things to happen in GCP, and it meets our needs for the project: our device needs to make a secure outbound connection to the cloud (as it's behind a NAT gateway). 

For work done on the device, we will simply use files in a directory as a queue (see [spooldir.py](./src/spooldir.py)). When a file appears, an application will process it and then delete the file. We could just as easily use Pub/Sub for this, but there's no need to incur extra costs for it. 

[iot-messaging.md](./iot-messaging.md) discusses some of the challenges in communicating between the cloud and an embedded device. 

## What's missing?

The python scripts in the repo demonstrate the basic functionality, but there are many things that are missing that are necessary to make this into a reliable system. 

The main thing that's missing is a lack of tooling to test, deploy, and update the software. For the services that run on the Pi, [systemd](https://www.thedigitalpictureframe.com/ultimate-guide-systemd-autostart-scripts-raspberry-pi/) is an option. Here's an example from another project: <https://github.com/jasonluther/rebar-heart/tree/master/src/orchestration>. 

There is a lot of work that should be done to monitor the components of the system. Consider using a unified logging framework, including a way to get logs from the Pi to GCP. Set up alerts in GCP to monitor the key health aspects of the system: <https://cloud.google.com/pubsub/docs/monitoring>. Also look out for log or spool files that can fill up storage on the Pi. 

The code and final setup also need a thorough security review. On the cloud side of things, make sure service accounts have only the access required, and use a different service account for each application. For the web front end, consider the [OWASP Top Ten](https://owasp.org/www-project-top-ten/). For the software on the Pi, be careful about how user input is handled, especially any place that commands are executed by a shell. 

Finally, consider the potential for abuse, whether intentional or accidental. Consider whether rate limits need to be applied to any of the services. Be especially careful with a service that generates email: you don't want someone to use this service to generate junk email for someone else, and you want to carefully control the content of the email so that it can't be used to launch phishing attacks. 