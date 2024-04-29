from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy

from accounts.models import User, UserProfile


# Create your models here.

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='user_profile')
    vendor_name = models.CharField(max_length=100)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name

    def save(self, *args, **kwargs):
        # tip : we use pk because pk is same in the instance itself and the update version of instance and we cant change it
        if self.pk is not None:
            original = Vendor.objects.get(pk=self.pk)
            email = original.user.email
            # tip : inside the save we have the instance itself now we compare the instance with update form in admin
            if original.is_approved != self.is_approved:
                if self.is_approved:
                    html_message = render_to_string("accounts/emails/notification.html", {
                        'vendor': self.is_approved,

                    })
                    plain_message = strip_tags(html_message)
                    message = EmailMultiAlternatives(
                        subject=ugettext_lazy("Account Verification"),
                        body=plain_message,
                        from_email=settings.EMAIL_HOST_USER,
                        to=[email],
                    )
                    message.attach_alternative(html_message, "text/html")
                    message.send()
                else:
                    html_message = render_to_string("accounts/emails/notification.html", {
                        'vendor': original,

                    })
                    plain_message = strip_tags(html_message)
                    message = EmailMultiAlternatives(
                        subject=ugettext_lazy("Account Verification"),
                        body=plain_message,
                        from_email=settings.EMAIL_HOST_USER,
                        to=[email],
                    )
                    message.attach_alternative(html_message, "text/html")
                    message.send()

        return super(Vendor, self).save(*args, **kwargs)
