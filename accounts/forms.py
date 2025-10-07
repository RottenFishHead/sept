from django import forms
from .models import BusinessContact, Client, Referral, Address
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["role", "title", "phone"]


TW_INPUT = "block w-full rounded-lg border border-gray-300 bg-white dark:bg-gray-900 px-3 py-2 text-sm text-gray-900 dark:text-gray-100 shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500"


class BaseTWForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            css = f.widget.attrs.get('class', '')
        f.widget.attrs['class'] = f"{css} {TW_INPUT}".strip()


class AddressForm(BaseTWForm):
    class Meta:
        model = Address
        fields = ["line_type","line1","line2","city","region","postal_code","country"]


class BusinessContactForm(BaseTWForm):
    class Meta:
        model = BusinessContact
        exclude = ["organization","created_by","created","updated"]


class ClientForm(BaseTWForm):
    class Meta:
        model = Client
        exclude = ["organization","created","updated"]


class ReferralForm(BaseTWForm):
    class Meta:
        model = Referral
        exclude = ["organization","created"]

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]

class UserProfileSelfForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["title", "phone"]  # no role here!