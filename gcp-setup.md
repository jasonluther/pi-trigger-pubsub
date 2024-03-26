For this example, we will use [Google Cloud Pub/Sub](https://cloud.google.com/pubsub/docs/overview), but the same thing can be done with any cloud hosting provider, and there are plenty of other ways to accomplish the same thing. 

Pub/Sub is convenient for this type of project for many reasons. The volume of messages will be low, so the cost will be low. Pub/Sub has decent latency, so our system will be pretty responsive to user input. Google's SDK makes it super easy to write applications. Finally, Pub/Sub works really well with Google Cloud Functions, which makes it easier to build a pipeline of applications in the cloud. 

Be aware that other solutions are a better choice if latency is critical or you're going to have a high volume of messages. 

## Setup

First, set up a dedicated GCP project. You'll need to set these things up:
 * Pub/Sub topic and subscription for each queue
 * Service accounts for each application that will be talking with GCP

I followed this [tutorial](https://www.youtube.com/watch?v=xOtrCmPjal8). 

Generally, you want your pubsub client to process messages as quickly as possible, so our client will pull each request from the cloud queue and add it to a local queue. Another set of programs will operate from that local queue. 

## Configuration

Configuration refers to the settings that are unique for a given device, user, or application, like credentials, hostnames, or logging levels. Keep configuration separate from your application code so that the code is reusable in different environments and situations (like development vs. production). You also don't want to check your precious secrets into a source control system!

In my examples, I'll use environment variables for this ([config.env](./src/config.env)). In development, you can store the environment setup in `.env` files and use something like [dotenv](https://pypi.org/project/python-dotenv/) to load them. Many GCP services, like Cloud Functions, also make use of environment variables for configuration. For sensitive secrets, you should look into using the cloud provider's [secret management](https://cloud.google.com/security/products/secret-manager) tools. 

You can also set environment variables on the Unix command line for each invocation of a program: 
```GCP_PROJECT=my-test-project ./program ...```

## Other Information

Here are some references for installing things onto a Raspberry Pi:

https://cloud-jake.medium.com/google-cloud-sdk-with-service-account-on-raspberry-pi-a06c86ebd3b0
```bash
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
sudo apt-get install apt-transport-https ca-certificates gnupg
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
sudo apt-get update && sudo apt-get install google-cloud-sdk
```

