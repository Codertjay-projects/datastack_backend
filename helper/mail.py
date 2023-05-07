from django.conf import settings
from . import message
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import threading
from threading import Thread


class sendMail(threading.Thread):
    def __init__(self, subject, code, recipient_list, template):
        self.subject = subject
        self.code = code
        self.recipient_list = recipient_list
        self.template = template
        threading.Thread.__init__(self)

    def run(self):
        html_content = render_to_string(
            self.template, {'code': self.code})
        email = EmailMessage(
            self.subject,
            html_content,
            settings.EMAIL_HOST_USER,
            self.recipient_list
        )
        email.content_subtype = "html"
        email.send()
        print("email sent")


def sendOTP(to, otp):
    sendMail(message.OTP_SUBJECT, otp, [to], "otp.html").start()
    return True


def sendVerification(to, code):
    sendMail(message.OTP_SUBJECT, code, [
             to], "confirm_subscription.html").start()
    return True
