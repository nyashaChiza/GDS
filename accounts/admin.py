from django.contrib import admin
from .models import User, Site, Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact', 'created', 'updated')
    search_fields = ('name', 'address', 'contact')
    list_filter = ('created', 'updated')
    ordering = ('-created',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'company','email', 'gender', 'role', 'status', 'is_logged_in')
    list_filter = ('role', 'status', 'is_logged_in')
    search_fields = ('username', 'email', 'phone_number')

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'company','capacity', 'operator','manager')
    list_filter = ('status', 'manager', 'company','operator') 
    search_fields = ('name', 'status')
