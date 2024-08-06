from django.contrib import admin
from .models import User, Site

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'gender', 'role', 'status', 'is_logged_in')
    list_filter = ('role', 'status', 'is_logged_in')
    search_fields = ('username', 'email', 'phone_number')

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'capacity', 'manager')
    list_filter = ('status', 'manager') 
    search_fields = ('name', 'status')
