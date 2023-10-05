import base64
import json
from io import BytesIO

from celery import shared_task
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage, send_mail
from django.core.management import call_command
from PIL import Image, ImageDraw


@shared_task
def send_html_email(subject, html_content, recipient_list):
    message = EmailMessage(
        subject, html_content, settings.DEFAULT_FROM_EMAIL, recipient_list
    )
    message.mixed_subtype = "related"
    message.content_subtype = "html"
    message.send()


@shared_task
def send_email(*, subject, message, from_email=None, recipient_list):
    send_mail(subject, message, from_email, recipient_list)

