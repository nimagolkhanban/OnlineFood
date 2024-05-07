from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.views import View
from django.views.generic import UpdateView

from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from menu.forms import CategoryForm, FoodForm
from menu.models import Category, FoodItem
from vendor.forms import VendorForm
from vendor.models import Vendor


def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


class RestaurantProfileView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'login'
    profile_form = UserProfileForm
    vendor_form = VendorForm

    def get(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)
        vendor = get_object_or_404(Vendor, user=request.user)
        # tip : instance part will complete the existing data that user fill in registration form
        profile_form = self.profile_form(instance=profile)
        vendor_form = self.vendor_form(instance=vendor)
        zone = UserProfile.objects.filter()
        context = {
            "profile_form": profile_form,
            "vendor_form": vendor_form,
            'current_profile': profile,
            'current_vendor': vendor,
        }
        return render(request, "vendor/vendor_profile.html", context)

    def post(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)
        vendor = get_object_or_404(Vendor, user=request.user)
        profile_form = self.profile_form(request.POST, request.FILES, instance=profile)
        vendor_form = self.vendor_form(request.POST, request.FILES, instance=vendor)
        context = {
            "profile_form": profile_form,
            "vendor_form": vendor_form,
            'current_profile': profile,
            'current_vendor': vendor,

        }

        zone = request.POST.get('zone')
        profile.zone = zone
        profile.save()

        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Your profile has been updated')

            return redirect("restaurant_profile")
        else:
            messages.error(request, "there is something wrong in your information")

            return render(request, "vendor/vendor_profile.html", context)


class MenuBuilderView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'login'
    def get(self, request):
        vendor = get_vendor(request)
        categories = Category.objects.filter(vendor=vendor).order_by('created_at')
        context = {
            'categories': categories,
        }
        return render(request, 'vendor/restaurant-menu-builder.html', context)


class FoodItemsByCategoryView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'login'
    def get(self, request, pk=None):
        vendor = get_vendor(request)
        category = get_object_or_404(Category, pk=pk)
        food_items = FoodItem.objects.filter(vendor=vendor, category=category).order_by('created_at')
        context = {
            "fooditems": food_items,
            'category': category,
        }
        return render(request, 'vendor/food_iteme_category.html', context)


class AddCategoryView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'login'

    def get(self, request):
        form = CategoryForm()
        context = {
            'form': form
        }
        return render(request, 'vendor/add_category.html', context)

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            # tip : look in the next line we don't use the category variable because we need to take the data out of
            # the form that user sends
            category_name = form.cleaned_data["category_name"]
            # tip : when we use the commit=false we create an instance of the model, but we don't save it inside the db,
            # so we can access the model field even if it's not in the form field of that model
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('menu-builder')
        else:

            messages.error(request, 'there is something wrong with your information')
            context = {
                 'form': form
            }
            return render(request, 'vendor/add_category.html', context)


class EditCategoryView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'login'

    def get(self, request, pk):
        current_category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(instance=current_category)
        context = {
            'form': form,
            'category': current_category,
        }
        return render(request, 'vendor/edit_category.html', context)

    def post(self, request, pk):
        current_category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(request.POST, instance=current_category)
        if form.is_valid():
            # tip : look in the next line we don't use the category variable because we need to take the data out of
            # the form that user sends
            category_name = form.cleaned_data["category_name"]
            # tip : when we use the commit=false we create an instance of the model, but we don't save it inside the db,
            # so we can access the model field even if it's not in the form field of that model
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('menu-builder')
        else:

            messages.error(request, 'there is something wrong with your information')
            context = {
                'form': form,
                'category': current_category,
            }
            return render(request, 'vendor/edit_category.html', context)


class DeleteCategoryView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'login'

    def get(self, request, pk):
        current_category = get_object_or_404(Category, pk=pk)
        current_category.delete()
        messages.success(request, 'category deleted successfully!')
        return redirect('menu-builder')

class AddFoodView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'login'

    def get(self, request, pk):
        form = FoodForm()
        category = get_object_or_404(Category, pk=pk)
        context = {
            'form': form,
            'category': category,

        }
        return render(request, 'vendor/add_food.html', context)

    def post(self, request, pk):
        form = FoodForm(request.POST, request.FILES)
        category = get_object_or_404(Category, pk=pk)
        if form.is_valid():
            food_name = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.category = category
            food.slug = slugify(food_name)
            food.save()
            context = {
                'form': form,
                'category': category
            }
            return redirect('food-items-by-category', category.pk)
        else:
            messages.error(request, 'there is something wrong with your information')
            context = {
                'form': form,
                'category': category
            }
            return render(request, 'vendor/add_food.html', context)


class EditFoodView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'login'

    def get(self, request, pk):
        current_food = get_object_or_404(FoodItem, pk=pk)
        form = FoodForm(instance=current_food)
        context = {
            'form': form,
            'food': current_food

        }
        return render(request, 'vendor/edit_food.html', context)

    def post(self, request, pk):
        current_food = get_object_or_404(FoodItem, pk=pk)
        category = Category.objects.get(pk=current_food.category.pk)
        form = FoodForm(request.POST, request.FILES, instance=current_food)
        if form.is_valid():
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.category = category
            food.slug = slugify(form.cleaned_data['food_title'])
            food.save()
            messages.success(request, 'food edited')
            return redirect('food-items-by-category', pk=category.pk)
        else:
            messages.error(request, 'invalid information')
            context= {
                'form': form,
                'food': current_food,
            }
            return render(request, "vendor/edit_food.html", context)


class DeleteFoodView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'login'

    def get(self, request, pk):
        current_food = get_object_or_404(FoodItem, pk=pk)
        current_food.delete()
        category = Category.objects.get(pk=current_food.category.pk)
        messages.success(request, 'food deleted successfully')
        return redirect('food-items-by-category', pk=category.pk)













