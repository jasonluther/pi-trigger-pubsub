from dotenv import load_dotenv, find_dotenv
import json
import os
import base64
import sendgrid
from sendgrid.helpers.mail import *
from spooldir import spool_loop_forever

load_dotenv(find_dotenv())
notify_spool_dir = os.environ["NOTIFY_SPOOL_DIRECTORY"]
email_from = os.environ["EMAIL_FROM"]
sendgrid_api_key = os.environ["SENDGRID_API_KEY"]


def process_request(raw_request):
    request = json.loads(raw_request)

    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get("SENDGRID_API_KEY"))
    from_email = Email(email_from)
    to_email = To(request["requestor_email"])
    subject = f"Was it {request['guess']}?"

    prog_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(prog_dir, "template.html")
    with open(template_path, "r") as file:
        html_content = file.read()
    content = Content("text/html", html_content)

    mail = Mail(from_email, to_email, subject, content)

    image_path = request["image_filename"]
    with open(image_path, "rb") as f:
        image_data = f.read()
        image_data_base64 = base64.b64encode(image_data).decode()
        image_cid = ContentId("image_coin")
    attachment = Attachment(
        FileContent(image_data_base64),
        FileName("image.jpg"),
        FileType("image/jpg"),
        Disposition("inline"),
        content_id=image_cid,
    )
    mail.attachment = attachment

    response = sg.send(mail)
    if response.status_code != 202:
        raise Exception(f"Failed to send email: {response.body}")
    else:
        os.remove(request["image_filename"])
    return True


spool_loop_forever(notify_spool_dir, process_request, ".json")
