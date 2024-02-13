from django.contrib import admin
from django.contrib.auth.models import Group
from .models import CustomUser
# from django.contrib.auth.admin import UserAdmin
from .models import Profile

# Uregister Groups
admin.site.unregister(Group)


# Mix Profile info into Users info
class ProfileInline(admin.StackedInline):
    model = Profile


# Extend Users Model
class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    fields = ["email", "role", "password"]
    inlines = [ProfileInline]
    list_display = ("email", "role")


# Reregister CustomUser and CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
