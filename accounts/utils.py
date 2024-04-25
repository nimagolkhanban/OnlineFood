from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def detectuser(user):
    if user.role == 1:
        redirecturl = 'vendordashboard'
        return redirecturl
    elif user.role == 2:
        redirecturl = 'customerdashboard'
        return redirecturl
    elif user.role == None and user.is_admin:
        redirecturl = '/admin'
        return redirecturl


# def send_verification_email(request, user):
#     corrent_site = get_current_site(request)
#     mail_subject = 'Verification Email please activate your account'
#     message = render_to_string('accounts/emails/account_verifiation.html',
#                                {
#                                    'user': user,
#                                    'domain': corrent_site.domain,
#                                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                                    'token': default_token_generator.make_token(user),
#                                })
#     to_email = user.email
#     mail = EmailMessage(mail_subject, message, to=[to_email])
#     mail.send()























