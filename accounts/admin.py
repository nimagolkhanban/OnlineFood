from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User, UserProfile
# Register your models here.


# tip: UserAdmin is a class that built for user model with a lot of variable
# tip: this also make the password only readable not editable
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'role')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)