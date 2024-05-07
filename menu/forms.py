from django import forms

from menu.models import Category, FoodItem


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']

    # tip: the below code is a veeeery interesting one because it's a generator that check in a dictionary called
    # changed_data this dictionary contain all the data that changed in the form, and we can use it in edit form
    # this is very handi tool so remember how to use it wisely
    def clean(self):
        if any(field_name in self.changed_data for field_name in ['description']):
            pass
        else:
            current_category_name = self.cleaned_data['category_name']
            flag = Category.objects.filter(category_name__iexact=current_category_name).exists()
            if flag:
                raise forms.ValidationError('there is a category with this name you pick')
            return current_category_name


class FoodForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['food_title', 'description', 'price', 'image', 'available']

    # tip: the below code is a veeeery interesting one because it's a generator that check in a dictionary called
    # changed_data this dictionary contain all the data that changed in the form, and we can use it in edit form
    # this is very handi tool so remember how to use it wisely

    def clean(self):
        if any(field_name in self.changed_data for field_name in ['description', 'price', 'image', 'available']):
            pass
        else:
            current_category_name = self.cleaned_data['category_name']
            flag = Category.objects.filter(category_name__iexact=current_category_name).exists()
            if flag:
                raise forms.ValidationError('there is a category with this name you pick')
            return current_category_name




