from dotenv import load_dotenv, find_dotenv
from time import sleep
import json
import os
import platform

if platform.system() != "Darwin":
    import RPi.GPIO as GPIO
import subprocess
from spooldir import spool_loop_forever, write_spool_file

load_dotenv(find_dotenv())
trigger_spool_dir = os.environ["TRIGGER_SPOOL_DIRECTORY"]
notify_spool_dir = os.environ["NOTIFY_SPOOL_DIRECTORY"]
image_spool_dir = os.environ["IMAGE_SPOOL_DIRECTORY"]
PIN = int(os.environ["GPIO_PIN"])


def process_request(raw_request):
    request = json.loads(raw_request)

    # Trigger the relay on GPIO PIN
    if platform.system() == "Darwin":
        subprocess.run(
            [
                "ssh",
                "pi@coin.local",
                "/home/pi/git/pi-trigger-pubsub/src/hardware-setup/pirelay-trip.sh",
            ],
            check=True,
        )
    else:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN, GPIO.OUT)
        GPIO.output(PIN, GPIO.LOW)
        sleep(0.2)
        GPIO.output(PIN, GPIO.HIGH)
        sleep(1)
        GPIO.cleanup()

    # take a still image from the camera
    request_id = request["request_id"]
    # Verify that the request_id is a properly-formatted UUID that is
    # safe to use as a filename and pass to a shell.
    # You should do a better job of this.
    request_id = request_id.replace(";", "").replace("&", "").replace(" ", "")
    image_filename = f"{image_spool_dir}/{request_id}.jpg"
    if platform.system() == "Darwin":
        subprocess.run(["imagesnap", image_filename], check=True)
    else:
        subprocess.run(["raspistill", "-o", image_filename], check=True)
    if not os.path.exists(image_filename):
        print("Failed to generate image")
        return False

    # write the request into json into a file in the notify spool directory
    request["image_filename"] = image_filename

    write_spool_file(notify_spool_dir, f"{request_id}.json", json.dumps(request))
    print(f"Processed request: {request}")
    return True


spool_loop_forever(trigger_spool_dir, process_request, ".json")
