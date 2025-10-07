from django.contrib import admin
from .models import Product, Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "is_active", "created_at")
    list_filter = ("is_active", "category", "created_at")
    search_fields = ("name", "short_description", "description", "seo_title", "seo_description", "seo_keywords")
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        ("Details", {"fields": ("category","name", "slug", "image", "short_description", "description", "section_1", "image_1", "caption_1", "section_2", "image_2", "caption_2", "section_3", "image_3", "caption_3", "is_active")}),
        ("Specs", {"fields": ("general_features", "specifications", "downloads", "accessories")}),
        ("SEO", {"fields": ("seo_title", "seo_description", "seo_keywords", "og_image", "canonical_url")}),
        ("Timestamps", {"fields": ("created_at",), "classes": ("collapse",)}),
    )
    readonly_fields = ("created_at",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "id")
    search_fields = ("name", "id")


