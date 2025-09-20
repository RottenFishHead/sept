from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field


class Product(models.Model):
    name = models.CharField(max_length=180)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    image = models.ImageField(upload_to="products/%Y/%m/%d/", blank=True, null=True)
    short_description = models.CharField(max_length=280, blank=True)
    description = CKEditor5Field(blank=True)
    category = models.CharField(max_length=120, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
      # --- SEO fields ---
    seo_title = models.CharField(max_length=70, blank=True, help_text="If blank, falls back to name.")
    seo_description = models.CharField(max_length=160, blank=True)
    seo_keywords = models.CharField(max_length=255, blank=True)
    og_image = models.ImageField(upload_to="seo/product_og/%Y/%m/%d/", blank=True, null=True)
    canonical_url = models.URLField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)[:200]
            candidate = base
            i = 1
            while Product.objects.filter(slug=candidate).exists():
                i += 1
                candidate = f"{base}-{i}"
            self.slug = candidate
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"slug": self.slug})

    @property
    def meta_title(self):
        return self.seo_title or self.name

    @property
    def meta_description(self):
        if self.seo_description:
            return self.seo_description
        src = self.short_description or self.description or ""
        return src[:157] + "…" if len(src) > 160 else src

    @property
    def meta_canonical(self):
        return self.canonical_url or None