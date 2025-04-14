from django.db import models
from django.shortcuts import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django_summernote.fields import SummernoteTextField
from django.conf import settings


class ContactRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"
    

class CompanyContact(models.Model):
    """
    Model for the B2B contact form in the companies page
    """
    email = models.EmailField(blank=False, null=False)
    company_name = models.CharField(max_length=60, blank=True, null=True)
    name = models.CharField(max_length=60, blank=False, null=False)
    individual_packs = models.BooleanField(default=False)
    reduced_groups = models.BooleanField(default=False)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        """Returns users to the contact page on successful creation."""
        return reverse('companies')

    def save(self, *args, **kwargs):
        """Saves the email to the database and sends it to the admin."""
        email = self.email
        name = self.name
        subject = 'New Request from Company'
        message = self.message

        # Fills in the email templates and then send the email.
        contact_subject = render_to_string(
            'contact/emails/contact_subject.txt',
            {'subject': subject})
        contact_body = render_to_string(
            'contact/emails/contact_body.txt',
            {'name': name, 'email': email, 'message': message})
        send_mail(contact_subject,
                  contact_body,
                  email,
                  [settings.DEFAULT_FROM_EMAIL])
        super().save(*args, **kwargs)

    def __str__(self):
        """Display the name and email in the admin panel."""
        return f'{self.name} ({self.email})'


class Subscription(models.Model):
    """
    Model to store subscribers to the newsletter
    """
    name = name = models.CharField(max_length=60, blank=False, null=False)
    email = models.EmailField(unique=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class EmailTemplate(models.Model):
    """
    Model to create newsletters on an html template that can
    be sent in emailing campaigns
    """
    name = models.CharField(max_length=100, unique=True)
    subject = models.CharField(max_length=200)
    content = models.CharField(max_length=2000)

    def __str__(self):
        return self.name
    
class AboutSection(models.Model):
    content = models.TextField()  # Field for the <p> content

    def __str__(self):
        return "About Page Content"