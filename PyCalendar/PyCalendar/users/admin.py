from django.contrib import admin
from .models import NewUser
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ("email", "first_name")
    # Which filters to be available:
    list_filter = ("email", "first_name", "is_active",
                   "is_staff")
    ordering = ("first_name",)
    # What to display when listing all users:
    list_display = ("email", "first_name", "is_active",
                    "is_staff")
    # What to display on a user page:
    fieldsets = (
        (None, {'fields': ('email', 'first_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    # What to display when adding a new user:
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'password1', 'password2',
                       'is_active', 'is_staff')}
        ),
    )


admin.site.register(NewUser, UserAdminConfig)
