from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *


class CustomUserAdmin(UserAdmin):
    ...
    ordering = ('email',)
    list_display = ('id', 'email', 'companyName',
                    'companyAddress', 'contactPerson', 'contactPhone')


class RadioactiveDisplay(admin.ModelAdmin):
    list_display = ('user', 'acknowleged',
                    'payment', 'siteVisit', 'installation',
                    'sourceCategory', 'sourceName', 'sourceState',
                    'sourceAddress'
                    )


class MessagesAdmin(admin.ModelAdmin):
    list_display = ('user', 'message',
                    'date',
                    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(RadioActiveSourcesModel, RadioactiveDisplay)
admin.site.register(Message, MessagesAdmin)
