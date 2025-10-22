from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile
User = get_user_model()

# Create or update Profile on User save
@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        # create a profile with defaults
        Profile.objects.create(user=instance)
    else:
        # ensure profile exists and update timestamp
        if hasattr(instance, "profile"):
            instance.profile.save()
        else:
            Profile.objects.get_or_create(user=instance)


# If django-allauth is installed, ensure profiles are created on social signups too.
try:
    from allauth.account.signals import user_signed_up as allauth_user_signed_up
    from allauth.socialaccount.signals import social_account_added  # not required but available
    from django.dispatch import receiver as allauth_receiver

    @allauth_receiver(allauth_user_signed_up)
    def allauth_create_profile(request, user, **kwargs):
        Profile.objects.get_or_create(user=user)

except Exception:
    # allauth not installed yet — signals will still work via post_save
    pass