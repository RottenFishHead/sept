from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=230, unique=True, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    excerpt = models.TextField(blank=True)
    body = models.TextField()
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    seo_title = models.CharField(max_length=70, blank=True, help_text="If blank, falls back to title.")
    seo_description = models.CharField(max_length=160, blank=True, help_text="Short summary for search engines.")
    seo_keywords = models.CharField(max_length=255, blank=True, help_text="Comma-separated keywords (optional).")
    og_image = models.ImageField(upload_to="seo/article_og/%Y/%m/%d/", blank=True, null=True)
    canonical_url = models.URLField(blank=True, help_text="Optional override; defaults to this page’s URL.")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:200]
            candidate = base
            i = 1
            while Article.objects.filter(slug=candidate).exists():
                i += 1
                candidate = f"{base}-{i}"
            self.slug = candidate
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("articles:detail", kwargs={"slug": self.slug})

    @property
    def meta_title(self):
        return self.seo_title or self.title

    @property
    def meta_description(self):
        if self.seo_description:
            return self.seo_description
        if self.excerpt:
            return self.excerpt[:157] + "…" if len(self.excerpt) > 160 else self.excerpt
        return (self.body or "")[:157] + "…"

    @property
    def meta_canonical(self):
        return self.canonical_url or None

class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="articles/%Y/%m/%d/")
    caption = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"Image for {self.article.title} ({self.id})"
