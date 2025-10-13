from django.contrib import admin
from .models import Article, ArticleImage

class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 1

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "published", "created_at")
    list_filter = ("published", "created_at")
    search_fields = ("title", "excerpt", "body", "seo_title", "seo_description", "seo_keywords")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        ("Content", {"fields": ("title", "slug", "excerpt", "body", "published")}),
        ("SEO", {"fields": ("seo_title", "seo_description", "seo_keywords", "og_image", "canonical_url")}),
        ("Timestamps", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
    readonly_fields = ("created_at", "updated_at")
    search_help_text = "Search by title, excerpt, body, or SEO fields."
    list_per_page = 50
    preserve_filters = True
    save_on_top = True

@admin.register(ArticleImage)
class ArticleImageAdmin(admin.ModelAdmin):
    list_display = ("article", "order", "caption")
    list_editable = ("order",)
