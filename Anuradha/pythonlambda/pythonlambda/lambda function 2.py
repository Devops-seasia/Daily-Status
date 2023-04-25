import boto3
import smtplib
import datetime

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    instance_id = event['instance_id']
    
    # Stop the instance
    ec2.stop_instances(InstanceIds=[instance_id])
    
    # Send an email
    from_email = '***********'
    to_email = '*************'
    subject = 'EC2 instance shutdown'
    body = 'The EC2 instance has been shut down.'
    message = f"Subject: {subject}\n\n{body}"
    
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(from_email, 'YOUR_EMAIL_PASSWORD')
        smtp.sendmail(from_email, to_email, message)
    
    print("Email sent successfully")
    
    return {
        'statusCode': 200,
        'body': f"Instance {instance_id} terminated successfully"
    }
