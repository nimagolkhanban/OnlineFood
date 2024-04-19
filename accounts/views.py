from django.shortcuts import render
from django.views import View

from accounts.forms import UserForm
from accounts.models import User


# Create your views here.

class RegisterUserView(View):
    form_class = UserForm
    template_name = 'accounts/user_registration.html'

    def get(self, request):
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
            user.save()

        context = {
            "form": form
        }
        return render(request, self.template_name, context)


