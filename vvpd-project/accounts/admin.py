from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm
from main.models import User


@admin.register(User)
class MyUserAdmin(UserAdmin):
    add_form = UserCreationForm

    list_display = ('username', 'get_full_name', 'user_status', 'is_superuser')
    list_filter = ('user_status',)
    fieldsets = (
        ('Login info', {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name',
         'last_name', 'middle_name', 'email')}),
        ('Permissions', {'fields': ('user_status',
         'is_staff', 'is_active', 'is_superuser')}),
        ('About', {'fields': ('date_joined', 'last_login')}),
    )

    add_fieldsets = (
        ('Login info', {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name',
         'last_name', 'middle_name', 'email')}),
        ('Permissions', {'fields': ('user_status',
         'is_staff', 'is_active', 'is_superuser')}),
        ('About', {'fields': ('date_joined', 'last_login')}),
    )
    readonly_fields = ('date_joined', 'last_login')


admin.site.unregister(Group)
