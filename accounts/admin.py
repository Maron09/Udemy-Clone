from django.contrib import admin
from .models import *
# Register your models here.


class StudentAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = []
    fieldsets = ()


admin.site.register(User, StudentAdmin)
admin.site.register(UserPofile)