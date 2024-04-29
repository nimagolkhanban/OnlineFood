from django import forms

from vendor.models import Vendor


class VendorForm(forms.ModelForm):
    vendor_license = forms.ImageField(
        widget=forms.FileInput(attrs={"class": 'upload-btn foodbakery-dev-featured-upload-btn'}))
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']

