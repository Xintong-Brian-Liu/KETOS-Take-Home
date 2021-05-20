import boto3
import json
import uuid
import urllib.parse

ses = boto3.client('ses')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('customerFeedback')


email_from = 'brianliu9648@gmail.com'

def lambda_handler(event, context):
    
    ticket_number = str(uuid.uuid4())
    customer_name = event["queryStringParameters"]["name"]
    customer_email = event["queryStringParameters"]["email"]
    desc = event["queryStringParameters"]["desc"]
    
    # The subject line for the email.
    SUBJECT = "Responded"
    
    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Thank you for your feedback\r\n"
                 "Here is your service number " + ticket_number
                )
                
    CHARSET = "UTF-8"

    response = ses.send_email(
        Source = email_from,
        Destination={
            'ToAddresses': [
                customer_email
            ]
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
    table.put_item(
       Item={
            'serviceId': ticket_number,
            'customer_email': customer_email,
            'support request': urllib.parse.unquote_plus(desc),
            'customer_name': customer_name
        }
    )
