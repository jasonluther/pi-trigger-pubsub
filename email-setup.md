There are many ways to programmatically send email, but it has gotten more difficult to ensure that an email will be delivered as the world works harder on preventing spam. 

## Delivering Email

There are many options:
  * Configure a local mail transfer agent (MTA) like Postfix to deliver mail to a service provider. If you are already relying on a local MTA for other purposes, this is convenient. Otherwise, it's a pain to manage. The main benefit is that your application doesn't have to retry deliveries if there are connectivity issues, as that's the job of the MTA. 
  * Similarly, use an SMTP library in the application to deliver mail to a service provider. This is straightforward, but you are on the hook to retry in case of connectivity issues. 
  * Use a transactional email delivery service, like Mailgun, Sendgrid, or Amazon SES. This is the approach I suggest. They all offer an SDK or simple API to post messages to their service. 

Aside from technical concerns, each of those options has a different cost structure that depends on the service provider and the volume of email. 

Sendgrid is available through the Google Cloud Platform marketplace, and it's pretty easy to configure. After signing up for an account, you must verify ownership of an individual email address or of a domain. Then you can create an API key and start sending mail. 

## Emailing Images

Without getting into the specifics, there are many ways to generate an email that includes images. All have limitations. This article goes into more detail: <https://sendgrid.com/en-us/blog/embedding-images-emails-facts>. 

 * Host images in cloud storage and link to them from the HTML content. This obviously requires that you retain the images for some time. 
 * Include the image in the message:
   * Add it as an attachment. This is reliable, but is the least attractive option.
   * Embed it as an inline attachment by using HTML's Content ID (CID) feature. 
   * Embed it by encoding the image as a base64 string. 

Embedding images as a base64 string or using CID will work for some mail clients and not others. Sometimes mail will be rejected as spam. Other times the images just won't show up, or they will show up as a standard attachment instead of inline.

[src/local-notify/notify-action.py](./src/local-notify/notify-action.py) uses Sendgrid and CID embedding to send an email. 

