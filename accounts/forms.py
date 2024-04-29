from django import forms

from accounts.models import User, UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'password', 'confirm_password']

    # tip : use clean for cleaning two or three field in the form that depend on each-other
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("passwords don't match")
        return cleaned_data

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(
        widget=forms.FileInput(attrs={"class": 'upload-btn foodbakery-dev-featured-upload-btn'}))
    cover_photo = forms.ImageField(
        widget=forms.FileInput(attrs={"class": 'upload-btn foodbakery-dev-featured-upload-btn'}))

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_photo', 'address_line_1', 'address_line_2', 'country', 'city', 'state',
                  'pincode', 'latitude', 'longitude']




















