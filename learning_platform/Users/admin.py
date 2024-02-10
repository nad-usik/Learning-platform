from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import CastomUser
from .models import Profile


# Uregister Groups
admin.site.unregister(Group)

# Mix Profile info into User info
# class ProfileInline(admin.StackedInline):
# 	model = Profile

# Extend User Model
# class UserAdmin(admin.ModelAdmin):
# 	model = User
# 	# Just display username fields on admin page
# 	fields = ["first_name", "last_name", "email"]
# 	# inlines = [ProfileInline]
#
# # Unregister initial User
# admin.site.unregister(User)

# Reregister CastomUser
admin.site.register(CastomUser, UserAdmin)


