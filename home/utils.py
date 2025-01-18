from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Subscription, EmailTemplate


def send_email_campaign(template_id):
    try:
        template = EmailTemplate.objects.get(id=template_id)
        subject = template.subject
        email_content = template.content  # Use the raw HTML content

        subscriber_emails = Subscription.objects.values_list('email',
                                                             flat=True)
        for email in subscriber_emails:
            # Render the email with the template and send
            send_mail(
                subject=subject,
                message="",  # noqa Leave this empty because we are using HTML content
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                html_message=email_content
            )
        return True
    except EmailTemplate.DoesNotExist:
        return False