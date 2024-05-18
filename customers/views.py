
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from accounts.forms import UserProfileForm, UserInfoForm
from accounts.models import UserProfile


# Create your views here.

class CustomerProfileView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'login'

    def get(self, request):
        user_form = UserInfoForm(instance=request.user)
        current_profile = UserProfile.objects.get(user=request.user)
        profile_form = UserProfileForm(instance=current_profile)

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'current_profile': current_profile,
        }
        return render(request, 'customers/customer_profile.html', context)

    def post(self, request):
        user_form = UserInfoForm(request.POST, instance=request.user)
        current_profile = UserProfile.objects.get(user=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=current_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('customer-profile')
        else:
            print(user_form.errors)
            print(profile_form.errors)
            return redirect('customer-profile')

