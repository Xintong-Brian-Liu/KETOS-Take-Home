import boto3
import json
import uuid
import urllib

ses = boto3.client('ses')
client = boto3.client('lambda')

email_from = 'brianliu9648@gmail.com'
email_to = 'jeeth.sellamuthu@ketos.co'

def lambda_handler(event, context):
    customer_name = event["queryStringParameters"]["name"]
    customer_email = event["queryStringParameters"]["email"]
    desc = event["queryStringParameters"]["desc"]

    # The subject line for the email.
    SUBJECT = "Receive Request"
    
    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = (
        "Click the URL below\r\n"
        "https://4tfwm9zuof.execute-api.us-west-2.amazonaws.com/default/replyEmailPython?name="+customer_name+"&email="+customer_email+"&desc="+urllib.parse.quote_plus(desc)
        )
                
    CHARSET = "UTF-8"

    #-----------Email-----------------
    response = ses.send_email(
        Source = email_from,
        Destination={
            'ToAddresses': [
                email_to,
            ],
        },
        Message={
            'Body': {

                'Text': {
                    'Charset': CHARSET,
                    'Data': BODY_TEXT,
                },
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': SUBJECT,
            }
        }
    )
