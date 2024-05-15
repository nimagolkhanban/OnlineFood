from django.contrib import admin

from vendor.models import Vendor, OpeningHour


class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'vendor_name', 'is_approved', 'created_at')
    list_display_links = ('user', 'vendor_name')


class OpeningHourAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'from_hour', 'day')


admin.site.register(Vendor, VendorAdmin)
admin.site.register(OpeningHour, OpeningHourAdmin)