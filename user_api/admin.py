from django.contrib import admin

from .models import User


@admin.register(User)
class TitleAdmin(admin.ModelAdmin):
    list_display = ['bio', 'email', 'role', 'confirmation_code', 'username']
    empty_value_display = '-empty-'
