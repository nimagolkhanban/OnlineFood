from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from accounts.forms import UserForm
from accounts.models import User, UserProfile
from accounts.utils import detectuser
from vendor.forms import VendorForm
from vendor.models import Vendor
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

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
            user = User.objects.create_user(first_name=first_name, last_name=last_name,password=password,
                                            username=username, email=email, phone_number=phone_number)
            user.role = User.CUSTOMER
            messages.success(request, 'user created successfully!')
            user.save()
        else :
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
            vendor_name = ven_form.cleaned_data.get('vendor_name')
            vendor_license = ven_form.cleaned_data.get('vendor_license')
            vendor_profile = UserProfile.objects.get(user=user)
            vendor = Vendor.objects.create(user=user, user_profile=vendor_profile, vendor_license=vendor_license,
                                           vendor_name=vendor_name)
            vendor.save()
            messages.success(request, "your restaurant signed up successfully please waite till our admin register your account")
            return redirect("registervendor")
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
        return render(request, 'accounts/vendor_dashboard.html')


class CustomerDashboardView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'login'
    def get(self, request):
        return render(request, 'accounts/customer_dashboard.html')



