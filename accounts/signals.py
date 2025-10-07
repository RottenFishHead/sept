from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import UserProfile, Organization


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
# Ensure default org exists or attach per your onboarding flow
        org, _ = Organization.objects.get_or_create(slug="default", defaults={"name": "Default"})
        UserProfile.objects.create(user=instance, organization=org, role="CLIENT")
        # Create groups if missing
        Group.objects.get_or_create(name="STAFF")
        Group.objects.get_or_create(name="MANAGER")
        Group.objects.get_or_create(name="CLIENT")