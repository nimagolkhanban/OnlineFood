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
            user = form.save(commit=False)
            user.role = User.CUSTOMER
            form.save()
        context = {
            "form": form
        }
        return render(request, self.template_name, context)


