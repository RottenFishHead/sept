from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import ProfileForm


@login_required
def profile_view(request):
    """
    Simple profile view: displays and lets the logged-in user edit their Profile.
    """
    profile = getattr(request.user, "profile", None)
    if profile is None:
        # Defensive: if profile not present, create one
        from .models import Profile
        profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            # keep user on the same page after save
            return redirect("members:profile")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "members/profile.html", {"form": form, "profile": profile})