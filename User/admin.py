from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

# Register your models here.
ADDITIONAL_USER_FIELDS = (
    (None, {'fields': ('rut', 'gender', 'birthday')}),
)

class UsersAdmin(UserAdmin):
    model: Users
    add_fieldsets = UserAdmin.add_fieldsets + ADDITIONAL_USER_FIELDS
    fieldsets = UserAdmin.fieldsets + ADDITIONAL_USER_FIELDS

admin.site.register(Users, UsersAdmin)
admin.site.register(Administrators)
admin.site.register(Trainers)
admin.site.register(Members)
admin.site.register(UsersTypes)