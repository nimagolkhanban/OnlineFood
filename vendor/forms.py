from django import forms
from .validators import allow_image_only
from vendor.models import Vendor, OpeningHour


class VendorForm(forms.ModelForm):
    vendor_license = forms.FileField(
            widget=forms.FileInput(attrs={"class": 'upload-btn foodbakery-dev-featured-upload-btn'}), validators=[allow_image_only])
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']


class OpeningHourForm(forms.ModelForm):
    class Meta:
        model = OpeningHour
        fields = ['day', 'from_hour', 'to_hour', 'is_closed']
