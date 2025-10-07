from django.contrib import admin
from .models import Organization, UserProfile, Address, BusinessContact, Client, Employee, Referral, SecureNote

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created")
    search_fields = ("name", "slug")

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "organization", "role", "title")
    list_filter = ("organization", "role")
    search_fields = ("user__username", "user__email")

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("line1", "city", "region", "country", "line_type")
    list_filter = ("country", "line_type")

@admin.register(BusinessContact)
class BusinessContactAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "company", "email", "organization", "is_active")
    list_filter = ("organization", "is_active")
    search_fields = ("first_name", "last_name", "company", "email")

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("account_name", "account_code", "primary_contact", "organization", "allow_portal_access")
    list_filter = ("organization", "allow_portal_access")
    search_fields = ("account_name", "account_code")

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("contact", "department", "start_date", "end_date", "organization")
    list_filter = ("organization", "department")

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ("to_client", "from_contact", "source", "created")
    list_filter = ("organization",)

@admin.register(SecureNote)
class SecureNoteAdmin(admin.ModelAdmin):
    list_display = ("contact", "author", "created")
    list_filter = ("organization",)