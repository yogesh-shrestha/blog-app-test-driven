from time import sleep
from celery import shared_task
from django.core.mail import mail_admins

@shared_task
def send_mail_task(name, email, message):
    sleep(10)
    mail_admins(subject=f'Message from {name}, {email}',
                message=message)
    print('Email successfully sent!')


