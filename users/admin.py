from django.contrib import admin
from .models import Address
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()

# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email','username','first_name','last_name','is_verified','is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_verified', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering =  ('-date_joined',)


    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields':('phone_number','date_of_birth','is_verified')
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('email', 'first_name', 'last_name', 'phone_number', 'date_of_birth')
        }),
    )

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_type', 'city', 'country', 'is_default', 'created_at')
    list_filter = ('address_type', 'is_default', 'country', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'city', 'country')
    ordering = ('-created_at',)



