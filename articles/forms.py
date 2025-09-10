from django import forms
from django.forms import inlineformset_factory
from .models import Article, ArticleImage

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            "title", "excerpt", "body", "published",
            "seo_title", "seo_description", "seo_keywords", "og_image", "canonical_url",
        ]

class ArticleImageForm(forms.ModelForm):
    class Meta:
        model = ArticleImage
        fields = ["image", "caption", "order"]
        widgets = {
            "caption": forms.TextInput(attrs={"placeholder": "Caption (optional)"}),
            "order": forms.NumberInput(attrs={"min": 0}),
        }

ArticleImageFormSet = inlineformset_factory(
    parent_model=Article,
    model=ArticleImage,
    form=ArticleImageForm,
    fields=["image", "caption", "order"],
    extra=3,            # number of blank forms shown by default
    can_delete=True,
)
