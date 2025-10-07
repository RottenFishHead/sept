from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
from PIL import Image
from django.core.exceptions import ValidationError
from django_ckeditor_5.fields import CKEditor5Field


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    features = CKEditor5Field(blank=True, null=True)  # explanation field
    image = models.ImageField(upload_to="categories/", blank=True, null=True) 
    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=180)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    short_description = models.CharField(max_length=280, blank=True)
    description = CKEditor5Field(blank=True)
    section_1 = CKEditor5Field(blank=True)
    image_1 = models.ImageField(upload_to="products/", blank=True, null=True)
    caption_1 = models.CharField(max_length=255, blank=True)
    section_2 = CKEditor5Field(blank=True)
    image_2 = models.ImageField(upload_to="products/", blank=True, null=True)
    caption_2 = models.CharField(max_length=255, blank=True)
    section_3 = CKEditor5Field(blank=True)
    image_3 = models.ImageField(upload_to="products/", blank=True, null=True)
    caption_3 = models.CharField(max_length=255, blank=True)
    general_features = CKEditor5Field(blank=True, null=True)   # Tab 1
    specifications = CKEditor5Field(blank=True, null=True)     # Tab 2
    downloads = CKEditor5Field(blank=True, null=True)          # Tab 3
    accessories = CKEditor5Field(blank=True, null=True)  
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
      # --- SEO fields ---
    seo_title = models.CharField(max_length=70, blank=True, help_text="If blank, falls back to name.")
    seo_description = models.CharField(max_length=160, blank=True)
    seo_keywords = models.CharField(max_length=255, blank=True)
    og_image = models.ImageField(upload_to="seo/product_og/", blank=True, null=True)
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

        # Resize og_image to optimal size (600x330)
        if self.og_image:
            img = Image.open(self.og_image.path)
            max_size = (800, 630)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            img.save(self.og_image.path)

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