from django import forms
from .models import Profile, ROLE_CHOICES


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "role",
            "phone",
            "company",
            "website",
            "address_line1",
            "address_line2",
            "city",
            "state",
            "postal_code",
            "country",
            "notes",
        ]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 4}),
        }