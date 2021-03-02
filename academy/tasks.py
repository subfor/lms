import os

from celery import shared_task

from django.template.loader import render_to_string

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


@shared_task
def send_mail(data):
    context = {
        'name': data['name'],
        'from_email': data['from_email'],
        'subject': data['subject'],
        'message': data['message']
    }
    content = render_to_string('emails/contact.html', context)
    message = Mail(
        from_email=os.environ.get('EMAIL_SENDER'),
        to_emails=os.environ.get('EMAIL_SENDER'),
        subject=data['subject'],
        html_content=content)
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    sg.send(message)