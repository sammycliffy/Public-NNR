from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *






class CustomUserAdmin(UserAdmin):
    ...
    ordering = ('email',)
    list_display = ('id','email', 'companyName', 'companyAddress', 'contactPerson')


admin.site.register(User, CustomUserAdmin)
