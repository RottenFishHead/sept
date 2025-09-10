from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "is_active", "created_at")
    list_filter = ("is_active", "category", "created_at")
    search_fields = ("name", "short_description", "description", "seo_title", "seo_description", "seo_keywords")
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        ("Details", {"fields": ("name", "slug", "image", "short_description", "description", "category", "is_active")}),
        ("SEO", {"fields": ("seo_title", "seo_description", "seo_keywords", "og_image", "canonical_url")}),
        ("Timestamps", {"fields": ("created_at",), "classes": ("collapse",)}),
    )
    readonly_fields = ("created_at",)