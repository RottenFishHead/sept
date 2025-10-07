from django import forms
from .models import Product, Category
from django_ckeditor_5.widgets import CKEditor5Widget


class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select a category",
        required=False,
        widget=forms.Select(attrs={
            "class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        })
    )
    
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ["slug"] 
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            }),
            "short_description": forms.Textarea(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 h-24"
            }),
            "description": CKEditor5Widget(attrs={"class": "django_ckeditor_5"}, config_name="default"),
            "section_1": CKEditor5Widget(),
            "section_2": CKEditor5Widget(), 
            "section_3": CKEditor5Widget(),

            "seo_title": forms.TextInput(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            }),
            "seo_description": forms.Textarea(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 h-24"
            }),
            "seo_keywords": forms.TextInput(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            }),
            "canonical_url": forms.URLInput(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            }),

            # Bonus: hide actual file inputs, styled via label/button
            "image": forms.ClearableFileInput(attrs={"class": "hidden"}),
            "image_1": forms.ClearableFileInput(attrs={"class": "hidden"}),
            "image_2": forms.ClearableFileInput(attrs={"class": "hidden"}),
            "image_3": forms.ClearableFileInput(attrs={"class": "hidden"}),
            "og_image": forms.ClearableFileInput(attrs={"class": "hidden"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].label_from_instance = lambda obj: obj.name