from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models

User = settings.AUTH_USER_MODEL

ROLE_MANAGEMENT = "management"
ROLE_STAFF = "staff"
ROLE_CLIENT = "client"
ROLE_OTHER = "other"

ROLE_CHOICES = [
    (ROLE_MANAGEMENT, "Management"),
    (ROLE_STAFF, "Staff"),
    (ROLE_CLIENT, "Client"),
    (ROLE_OTHER, "Other"),
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default=ROLE_OTHER)

    # Contact fields
    phone = models.CharField(max_length=50, blank=True)
    company = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True)

    # Address
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=120, blank=True)
    postal_code = models.CharField(max_length=40, blank=True)
    country = models.CharField(max_length=120, blank=True)

    # Misc
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        username = getattr(self.user, "get_full_name", None)
        display = self.user.get_full_name() if callable(self.user.get_full_name) and self.user.get_full_name() else getattr(self.user, "username", str(self.user))
        return f"{display} ({self.get_role_display()})"

    def group_roles(self):
        """
        Returns a queryset of GroupRole entries that apply to any group this user belongs to.
        """
        from .models import GroupRole  # local import to avoid circular issues
        groups = self.user.groups.all()
        return GroupRole.objects.filter(group__in=groups)


class GroupRole(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group_roles")
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ("group", "role")
        verbose_name = "Group Role"
        verbose_name_plural = "Group Roles"

    def __str__(self):
        return f"{self.group.name} → {self.get_role_display()}"