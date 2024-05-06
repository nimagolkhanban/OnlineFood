from django import forms

from menu.models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']

    def clean_category_name(self):
        current_category_name = self.cleaned_data['category_name']
        flag = Category.objects.filter(category_name__iexact=current_category_name).exists()
        if flag:
            raise forms.ValidationError('there is a category with this name you pick')
        return current_category_name

