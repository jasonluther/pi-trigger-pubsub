Communication between and embedded IoT device and a cloud service can be challenging, especially when you have constrained compute, power, or bandwidth. We are interested in a small number of devices, which means we don't have to worry about a lot of the scaling and management challenges with a large fleet of devices. 

## Security

The one critical constraint is security. You must have a secure channel for communication between the device and its cloud service. That implies that the device has adequate resources to deal with the cryptography overhead, and it also implies that you have a management framework in place to rotate and renew keys. If you can do all of this over HTTPS using TLS certificates, you will benefit from a rich ecosystem of tools. However, do not underestimate the challenge of managing certificates and trust. 

If your device can't handle that on its own, you'll need a gateway device that makes a secure connection to the cloud and then a separate connection to the device. That separate connection can provide security in other ways, like a physical network/serial connection or a less robust encryption method that is adequate for the device's environment and risks. 

## Message Queues

For a distributed system, it's important to consider how each component in the system can tolerate a loss of connectivity to other components. Sometimes it doesn't matter: if someone wants to do something *right now* and the device has lost its network connection, then retrying that activity later doesn't help the user.  But for most things, we want have some way to keep track of a list of work and hand it out to different components. 

Fundamentally, you just need to be able to submit work to a queue, store the queue, and pull work from it. For a one-off project, you have the luxury of ignoring a lot of the performance, scaling, and operational constraints that different messaging systems optimize for. 

For example, for communication between programs running on the same host, a simple "spool" directory with files that represent work can be very effective, but you have to make sure that the directory doesn't consume all of the available disk space. One producer program writes files to the spool directory. A consumer program looks for new files, does the work, and deletes the file (or moves it elsewhere). 

For communication across a network, there are plenty of ways to use off-the-shelf services to implement a queue:
 * A cloud storage bucket used as a spool directory, with HTTP operations are used to interact with the files
 * A relational database or key-value store 
 * Full-featured message queue services like Google Cloud Pub/Sub and Amazon SQS

MQTT is also a popular choice, especially for communication between a gateway and an embedded device, but it usually requires you to run your own MQTT broker. It can also be a good option for communication between processes on the same machine. 

## Tradeoffs

Working on embedded devices involves a lot of tradeoffs, including human time, hardware cost, power consumption, bandwidth, and reliability. If you can afford to spend more money on hardware capabilities, you can spend less human time building and operating the system. 

Raspberry Pi gives you a very inexpensive way to get a full computing environment, complete with support for peripherals like cameras. But then you are stuck managing a computer, which is a lot of work: you have to constantly upgrade software to avoid security vulnerabilities, the attack surface is big, and it's easy to misconfigure things and accidentally create a vulnerability. You can also run a wider variety of off-the-shelf software and use higher-level (more productive) programming languages, which should save you a lot of time vs. working in a more embedded environment. 

If you have more modest software requirements, there are plenty of great IoT-style devices that are relatively easy to work with, including commercial products from Particle and open-source-friendly development boards based on Espressif Wi-Fi SoCs. 

## The Unix Philosophy and Decoupling with Messaging

We are going to apply the spirit of the [Unix Philosophy](https://en.wikipedia.org/wiki/Unix_philosophy) to this project. As much as possible, we'll separate our software into  small applications that each do one task, and we'll use a standard format to communicate between them (JSON messages). 

This approach is really convenient for project like this because it makes it much easier to replace and update parts of the system when the need arises. For example, if you have a program that interacts with a camera, you can easily update it to work with a different camera without affecting your other components. You can also shift work from your device to the cloud and back, depending on your specific needs. 

Using a message bus like Pub/Sub also makes it easy to expand the functionality of the system without impacting what's already there. For example, if you trigger something to happen from a web form by publishing an event to a topic, you can trigger the same event from some other source, like a scheduled task or the results of an API call. Or you can add more consumers to a topic to have other systems react to the same input. 