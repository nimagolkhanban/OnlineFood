from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify
from django.views import View
from accounts.forms import UserForm
from accounts.models import User, UserProfile
from accounts.utils import detectuser
from vendor.forms import VendorForm
from vendor.models import Vendor
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import ugettext_lazy


def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        try:
            vendor = Vendor.objects.get(user=user)
            if vendor:
                vendor.is_approved = True
                vendor.save()
                user.is_active = True
                user.save()
                messages.success(request, 'Your account activated')
                return redirect("myaccount")
        except:
            user.is_active = True
            user.save()
            messages.success(request, 'Your account activated')
            return redirect("myaccount")



class RegisterUserView(View):
    form_class = UserForm
    template_name = 'accounts/user_registration.html'

    def get(self, request):
        if request.user.is_authenticated:
            messages.warning(request, "you are already logged in")
            return redirect("login")
        form = self.form_class()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # tip : old way
            # password = form.cleaned_data["password"]
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # form.save()
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, password=password,
                                            username=username, email=email, phone_number=phone_number)
            user.role = User.CUSTOMER
            user.save()

            # send verification link by email
            corrent_site = get_current_site(request)
            html_message = render_to_string("accounts/emails/account_verifiation.html", {
                                   'user': user,
                                   'domain': corrent_site.domain,
                                   'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                   'token': default_token_generator.make_token(user),
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

            messages.success(request, 'user created successfully!')
            return redirect('customerdashboard')
        else:
            messages.error(request, "invalid form please check again")
        context = {
            "form": form
        }
        return render(request, self.template_name, context)


class RegisterVendorView(View):
    user_form = UserForm
    vendor_form = VendorForm

    def get(self, request):
        if request.user.is_authenticated:
            messages.warning(request, "you are already logged in")
            return redirect("login")
        context = {
            'form': self.user_form,
            'v_form': self.vendor_form,
        }
        return render(request, "accounts/vendor_registration.html", context)

    def post(self, request):
        us_form = self.user_form(request.POST)
        # tip : remember request.file is for accepting the image file that send by user in request
        ven_form = self.vendor_form(request.POST, request.FILES)
        if us_form.is_valid() and ven_form.is_valid():
            first_name = us_form.cleaned_data['first_name']
            last_name = us_form.cleaned_data['last_name']
            username = us_form.cleaned_data['username']
            email = us_form.cleaned_data['email']
            phone_number = us_form.cleaned_data['phone_number']
            password = us_form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, password=password,
                                            username=username, email=email, phone_number=phone_number)
            user.role = User.RESTAURANT
            user.save()
            # tip : send activate email
            # send verification link by email
            corrent_site = get_current_site(request)
            html_message = render_to_string("accounts/emails/account_verifiation.html", {
                'user': user,
                'domain': corrent_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
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

            vendor_name = ven_form.cleaned_data.get('vendor_name')
            vendor_license = ven_form.cleaned_data.get('vendor_license')
            vendor_profile = UserProfile.objects.get(user=user)
            vendor_slug = slugify(vendor_name+'-'+str(user.id))
            vendor = Vendor.objects.create(user=user, user_profile=vendor_profile, vendor_license=vendor_license,
                                           vendor_name=vendor_name, vendor_slug=vendor_slug)
            vendor.save()
            messages.success(request,
                             "your restaurant signed up successfully please waite till our admin register your account")
            return redirect('vendordashboard')
        else:
            messages.error(request, "there is something wrong with your registration data")
            return redirect("registervendor")


class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated:
            messages.warning(request, "you are already logged in")
            return redirect("home")
        return render(request, 'accounts/login.html')

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "you logged in successfully")
            return redirect("myaccount")
        messages.error(request, "email or password is wrong, please try again")
        return redirect("login")


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return redirect("home")


# tip : this view is really tricky because its actually does not do anything
# it's just for detecting the user type and redirect to the proper url
@login_required(login_url='login')
def myaccount(request):
    user = request.user
    redirect_url = detectuser(user)
    return redirect(redirect_url)


class VendorDashboardView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'login'

    def get(self, request):
        user = request.user
        role = user.role
        if role == 1:
            return render(request, 'accounts/vendor_dashboard.html')
        elif role == 2:
            return redirect("customerdashboard")
        elif role == None or user.is_admin:
            return redirect("/admin")
        else:
            return redirect("home")



class CustomerDashboardView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'login'

    def get(self, request):
        user = request.user
        role = user.role
        if role == 1:
            return redirect("vendordashboard")
        elif role == 2:
            return render(request, 'accounts/customer_dashboard.html')
        elif role == None or user.is_admin:
            return redirect("/admin")
        else:
            return redirect("home")


# forgot password and reset password section
class ForgotPasswordView(View):
    def get(self, request):
        return render(request, 'accounts/forgot_password.html')

    def post(self, request):
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            # password reset email

            corrent_site = get_current_site(request)
            html_message = render_to_string("accounts/emails/forgot_password_email.html", {
                'user': user,
                'domain': corrent_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
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
            return redirect("login")
        else:
            messages.error(request, "account does not exist")
            return redirect("forgotpassword")

class ResetPasswordValidateView(View):
    def get(self, request, *args, **kwargs):
        try :
            uid = kwargs.get('uidb64')
            uid = urlsafe_base64_decode(uid).decode()
            token = kwargs.get('token')
            user = User.objects.get(pk=uid)

        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            messages.error(request, "your information is wrong")
            return redirect("forgotpassword")
        if user is not None and default_token_generator.check_token(user, token):
            request.session['uid'] = uid
            messages.info(request, "please reset your password")
            return redirect("resetpassword")
        else :
            messages.error(request, "your information is wrong")
            return redirect("forgotpassword")





class ResetPasswordView(View):
    def get(self, request):
        uid = request.session.get('uid')
        if uid:
            return render(request, "accounts/reset_password.html")
        else:
            messages.error(request, "you cant access this page ")
            return  redirect("forgotpassword")
    def post(self, request):
        uid = request.session.get('uid')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, "your password has been updated")
            del request.session['uid']
            return redirect("login")
        else:
            messages.error(request, "password and confirmation are not same")
            return redirect("resetpassword")

