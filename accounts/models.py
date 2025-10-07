from django.conf import settings
from django.contrib.auth.models import Group
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class Organization(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

class UserProfile(models.Model):
    ROLE_CHOICES = [
    ("STAFF", "Staff"),
    ("MANAGER", "Manager"),
    ("CLIENT", "Client"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, related_name="users")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    title = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=20, blank=True)


    def __str__(self):
        return f"{self.user} · {self.role}"
    
class Address(models.Model):
    LINE_TYPES = [
    ("WORK", "Work"), ("HOME", "Home"), ("BILLING", "Billing"), ("SHIPPING", "Shipping"),
    ]
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="addresses")
    line_type = models.CharField(max_length=10, choices=LINE_TYPES, default="WORK")
    line1 = models.CharField(max_length=200)
    line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100, help_text="State/Province")
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=2, default="US")


class Meta:
    ordering = ["country", "region", "city"]


def __str__(self):
    return f"{self.line1}, {self.city}"


phone_validator = RegexValidator(r"^[0-9+()\-\s]{7,}$", "Enter a valid phone number")

# A contact person at a client, vendor, or partner."
class BusinessContact(models.Model):

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="contacts")
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="created_contacts")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company = models.CharField(max_length=150, blank=True)
    job_title = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    phone_mobile = models.CharField(max_length=30, blank=True, validators=[phone_validator])
    phone_work = models.CharField(max_length=30, blank=True, validators=[phone_validator])
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    # Personal/PII (store only if truly needed)
    date_of_birth = models.DateField(null=True, blank=True)
    tax_id_last4 = models.CharField(max_length=4, blank=True, help_text="Last 4 only—never store full IDs.")
    # Classification & lifecycle
    is_active = models.BooleanField(default=True)
    tags = models.CharField(max_length=255, blank=True, help_text="Comma separated tags")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        unique_together = ("organization", "email")
        ordering = ["last_name", "first_name"]


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Client(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="clients")
    primary_contact = models.ForeignKey(BusinessContact, on_delete=models.PROTECT, related_name="client_primary_for")
    account_name = models.CharField(max_length=200)
    account_code = models.CharField(max_length=50, unique=True)
    billing_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name="client_billing")
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name="client_shipping")
    allow_portal_access = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.account_name

class Employee(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="employees")
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="employee_profile", null=True, blank=True)
    contact = models.OneToOneField(BusinessContact, on_delete=models.PROTECT, related_name="as_employee")
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    department = models.CharField(max_length=120, blank=True)
    manager = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    is_confidential = models.BooleanField(default=True, help_text="Hide from client views.")


    def __str__(self):
        return f"{self.contact}"
    

class Referral(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="referrals")
    from_contact = models.ForeignKey(BusinessContact, on_delete=models.PROTECT, related_name="referrals_made")
    to_client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="referrals_received")
    note = models.TextField(blank=True)
    source = models.CharField(max_length=120, blank=True, help_text="e.g., Event, LinkedIn, Partner")
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Referral to {self.to_client} from {self.from_contact}"

# """Internal staff-only notes. Never shown to clients."""
class SecureNote(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="secure_notes")
    contact = models.ForeignKey(BusinessContact, on_delete=models.CASCADE, related_name="secure_notes")
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ("view_secure_notes", "Can view secure staff notes"),
        ]
        

    def __str__(self):
        return f"Note for {self.contact}"