from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "image", "short_description", "description", "category", "is_active",
            "seo_title", "seo_description", "seo_keywords", "og_image", "canonical_url",]
        widgets = {
            "short_description": forms.TextInput(attrs={"placeholder": "Short teaser for cards…"}),
            "description": forms.Textarea(attrs={"rows": 6}),
            
        }
