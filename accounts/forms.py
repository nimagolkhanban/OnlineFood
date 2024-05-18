from django import forms
from .validators import allow_image_only

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
    ZONE_CHOICES = (
        ('Z1', 'Zone 1'),
        ('Z2', 'Zone 2'),
        ('Z3', 'Zone 3'),
        ('Z4', 'Zone 4'),
        ('Z5', 'Zone 5'),
        ('Z6', 'Zone 6'),
        ('Z7', 'Zone 7'),
        ('Z8', 'Zone 8'),
        ('Z9', 'Zone 9'),
        ('Z10', 'Zone 10'))
    address = forms.CharField(widget=forms.TextInput(attrs={'required': 'required'}))
    profile_picture = forms.FileField(
        widget=forms.FileInput(attrs={"class": 'upload-btn foodbakery-dev-featured-upload-btn'}), validators=[allow_image_only])
    cover_photo = forms.FileField(
        widget=forms.FileInput(attrs={"class": 'upload-btn foodbakery-dev-featured-upload-btn'}), required=False, validators=[allow_image_only])
    zone = forms.ChoiceField(choices=ZONE_CHOICES, label="zone", initial='', widget=forms.Select(attrs={"class":"multiple chosen-select"}), required=True)

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_photo', 'address', 'country', 'city', 'state',
                  'pincode', 'zone']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number']
















