from django import forms


class SearchForm(forms.Form):
    restaurant_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Restaurant Name'}))


