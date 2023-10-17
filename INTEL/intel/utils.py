from django.core.mail import send_mail
from django.conf import settings

def send_verification_email_request_demo(submission):
    subject = 'Intellisense Demo Request'
    message = 'Thank you for your request. We will review it shortly.'
    from_email = settings.EMAIL_HOST_USER  # Use the sender's email address
    recipient_list = [submission.Business_email]

    send_mail(subject, message, from_email, recipient_list)

def send_verification_email_contact(submission):
    subject = 'User Request to Contact Verification'
    message = 'Thank you for your  Contact request. We will review it shortly.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [submission.Business_email]

    send_mail(subject, message, from_email, recipient_list)


def send_verification_email_help_and_support(submission):
    subject = 'User Request to HelpandSupport Verification'
    message = 'Thank you for your  HelpandSupport request. We will review it shortly.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [submission.Business_email]

    send_mail(subject, message, from_email, recipient_list)