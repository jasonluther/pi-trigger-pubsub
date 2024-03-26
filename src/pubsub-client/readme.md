# Pub/Sub Client

The Pub/Sub client's ([pubsub-client.py](./pubsub-client.py)) job is to wait for requests on the topic, do some basic validation, and then put the request into the next application's queue, adding any additional information that might be needed by the next step (in this case, nothing is added). 

The next application ([local-trigger](../local-trigger/)) is waiting for a file with the JSON message to appear in a spool directory. It could just as easily use the same Pub/Sub system with a different topic, a local MQTT broker, or one of many other ways to model a work queue. 