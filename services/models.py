from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field

class Service(models.Model):
    name = models.CharField(max_length=180, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    short_description = models.CharField(max_length=50, blank=True)
    h1 = models.CharField(max_length=200, blank=True)
    h2 = models.CharField(max_length=200, blank=True)
    cta = models.CharField(max_length=100, blank=True)
    description = CKEditor5Field(blank=True)
    icon = models.ImageField(upload_to="services/icons/", blank=True, null=True)
    image = models.ImageField(upload_to="services/images/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
      # --- SEO fields ---
    seo_title = models.CharField(max_length=70, blank=True, help_text="If blank, falls back to name.")
    seo_description = models.CharField(max_length=160, blank=True)
    seo_keywords = models.CharField(max_length=255, blank=True)
    og_image = models.ImageField(upload_to="seo/product_og/", blank=True, null=True)
    canonical_url = models.URLField(blank=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("services:service_detail", args=[self.slug])
    

class ServiceBullet(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="bullets")
    text = models.CharField(max_length=300)
    icon_class = models.CharField(max_length=80, blank=True, default="fa-solid fa-check")
    url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.text[:60]