Refer to your favorite tutorial on how to set up the hardware you are going to control with your Raspberry Pi. Here's one from [Adafruit](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup?view=all). 

If you are using a GPIO pin to control a relay, for example, here is one way to set it up. There are two key tasks: setting up the GPIO pins at boot time so that they are in the correct state and controlling the inputs and outputs from your application software. 

Install any needed software, like [wiring-pi](https://github.com/WiringPi/WiringPi). This used to be simple:
```bash
sudo apt-get install wiringpi
```
However, I had to install it from source following [these instructions](https://github.com/WiringPi/WiringPi?tab=readme-ov-file#from-source).  

## Boot initialization

You want to set up your digital outputs so that they are in a known good state when your device boots. You don't want to trigger the attached hardware accidentally any time you reboot your Pi. 

Create an executable file called `/home/pi/pirelay-init.sh` that will be run when the system boots to set up your GPIO pins:
```bash
#!/bin/sh
# Enable digital output on GPIO 22, 
# which is physical pin 15
gpio -g write 22 1
sleep 1
gpio -g mode 22 tri
sleep 1
gpio -g mode 22 out
sleep 1
gpio -g write 22 1
```

Create a file called `pirelay-init.service`:
```conf
[Unit]
Description=Configure GPIO pin to control a relay

[Service]
ExecStart=/home/pi/pirelay-init.sh

[Install]
WantedBy=multi-user.target
```

Install the service config file:
```bash
SERVICE=pirelay-init
sudo cp -f $SERVICE.service /etc/systemd/system/$SERVICE.service
sudo chmod 644 /etc/systemd/system/$SERVICE.service
sudo systemctl enable $SERVICE
sudo systemctl start $SERVICE
```

After rebooting the Pi, your GPIO pin should be ready to use. 

See [hardware-setup](./src/hardware-setup/) for a concrete example. 

## Application

Pick a library that works for your environment. I'm using <https://pypi.org/project/RPi.GPIO/>, which is perfectly adequate for what I need, which is just turning a GPIO pin high and low. 

If you have trouble finding something suitable for your language of choice, don't forget that you can invoke a program/command from another program, so you could relocate the GPIO operations to a smaller application and orchestrate its operations with a language you're more comfortable with. 

## Camera

Refer to the documentation to set up the [camera](https://www.raspberrypi.com/documentation/accessories/camera.html). 

If it's been a while, be sure to update all of the pi's packages and install any dependencies you'll need:
```bash
sudo apt-get update --allow-releaseinfo-change
sudo apt install python3-pip
pip3 install  google-cloud-pubsub
```

## Things to be aware of

These are some miscellaneous things to be aware of when working with the Pi's GPIO pins.

The Pi expect 3.3V signaling, not 5V. 

Some pins are shared with other built-in peripherals, and some functionality has to be enabled (or disabled) in `raspi-config`. If something isn't working, check that the Pi is configured properly. 

There's a lot of old Pi documentation (especially forum discussions) on the Internet, so be prepared to experiment to find solutions. 
