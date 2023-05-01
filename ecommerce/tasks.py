from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from buylando.celery import app


@app.task
def queue_email(subject, temp_html, temp_str, context, recipients):
    message_html = render_to_string(temp_html, context)
    message_str = render_to_string(temp_str, context)

    send_mail(
        subject=subject,
        message=message_str,
        html_message=message_html,
        from_email=settings.EMAIL_SENDER,
        recipient_list=recipients,
    )

    return "Email sent."
