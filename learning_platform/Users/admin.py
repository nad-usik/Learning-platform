from django.contrib import admin
from django.contrib.auth.models import Group
from .models import CustomUser
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin

# from .models import Profile

# Uregister Groups
admin.site.unregister(Group)


# Mix Profile info into Users info
# class ProfileInline(admin.StackedInline):
#     model = Profile


# Extend Users Model
# class CustomUserAdmin(admin.ModelAdmin):
#     model = CustomUser
#     fields = ["email", "role", "password", "last_name", "first_name", "second_name", "date_of_birth", "gender", "town", "phone_number", "profile_photo"]
#     # inlines = [ProfileInline]
#     list_display = ("email", "role")

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        "email",
        "first_name",
        "last_name",
        "role",
        "is_active",
    )
    list_filter = (
        "email",
        # "first_name",
        # "last_name",
        # "date_of_birth",
        # "is_staff",
        # "is_active",
    )
    fieldsets = (
        (None, {"fields": (
            "email",
            # "password",
            "role",
            "first_name",
            "last_name",
            "second_name",
            "date_of_birth",
            "gender",
            "town",
            "phone_number",
            "profile_photo")}
         ),
        ("Permissions", {"fields": (
            "is_staff",
            "is_active",
            # "groups",
            # "user_permissions"
            )}
         ),
    )
    add_fieldsets = (
        (None, {"fields": (
            "email",
            "password1",
            "password2",
            "role",
            "first_name",
            "last_name",
            "second_name",
            "date_of_birth",
            "gender",
            "town",
            "phone_number",
            "profile_photo",
            "is_staff",
            "is_active",
            # "user_permissions"
        )}
         ),
    )
    search_fields = ("email",)
    ordering = ("email",)


# Reregister CustomUser and CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
