from django.contrib import admin
from .models import Service, ServiceBullet

class ServiceBulletInline(admin.TabularInline):
    model = ServiceBullet
    extra = 1
    fields = ("order", "text", "icon_class", "url")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "order")
    list_editable = ("is_active", "order")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "short_description")
    search_help_text = "Search by name or short description."
