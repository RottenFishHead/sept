from http import client
from urllib import request
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import BusinessContact, Client, Referral, SecureNote, Organization, UserProfile
from .forms import BusinessContactForm, ClientForm, ReferralForm, RegisterForm, UserProfileForm \
    , UserForm, UserProfileSelfForm
from .utils import require_role, org_queryset

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # attach to default org
            org, _ = Organization.objects.get_or_create(slug="default", defaults={"name": "Default"})
            UserProfile.objects.create(user=user, organization=org, role="CLIENT")
            login(request, user)
            return redirect("accounts:contacts_list")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})

@login_required
@require_role("STAFF")
def profile_edit(request, pk):
    profile = get_object_or_404(UserProfile, pk=pk, organization=request.user.profile.organization)
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("accounts:contacts_list")
    else:
        form = UserProfileForm(instance=profile)
    return render(request, "accounts/form.html", {"form": form, "title": f"Edit Profile for {profile.user.username}"})

@login_required
@require_role("STAFF", "CLIENT")
def contacts_list(request):
    qs = org_queryset(BusinessContact.objects.select_related("address"), request)

    # Clients can only see active contacts
    if request.user.profile.role == "CLIENT":
        qs = qs.filter(is_active=True)

    return render(request, "accounts/contacts_list.html", {"contacts": qs})

@login_required
@require_role("STAFF")
def contact_create(request):
    if request.method == "POST":
        form = BusinessContactForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.organization = request.user.profile.organization
            obj.created_by = request.user
            obj.save()
            return redirect("accounts:contacts_list")
    else:
        form = BusinessContactForm()
    return render(request, "accounts/form.html", {"form": form, "title": "New Contact"})

@login_required
@require_role("STAFF", "CLIENT")
def clients_list(request):
    qs = org_queryset(Client.objects.select_related("primary_contact"), request)
    if request.user.profile.role == "CLIENT":
        # Optionally restrict to the client tied to the logged‑in user; adjust as needed.
        qs = qs.filter(allow_portal_access=True)
    return render(request, "accounts/clients_list.html", {"clients": qs})

@login_required
@require_role("STAFF")
def client_create(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.organization = request.user.profile.organization
            obj.save()
            return redirect("accounts:clients_list")
    else:
        form = ClientForm()
    return render(request, "accounts/form.html", {"form": form, "title": "New Client"})

@login_required
@require_role("STAFF", "CLIENT")
def referrals_list(request):
    qs = org_queryset(Referral.objects.select_related("from_contact", "to_client"), request)
    if request.user.profile.role == "CLIENT":
        # Clients see referrals that target clients marked portal‑visible
        qs = qs.filter(to_client__allow_portal_access=True)
    return render(request, "accounts/referrals_list.html", {"referrals": qs})

@login_required
@require_role("STAFF")
def referral_create(request):
    if request.method == "POST":
        form = ReferralForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.organization = request.user.profile.organization
            obj.save()
            return redirect("accounts:referrals_list")
    else:
        form = ReferralForm()
    return render(request, "accounts/form.html", {"form": form, "title": "New Referral"})

@login_required
@permission_required("accounts.view_securenote", raise_exception=True)
@require_role("STAFF")
def secure_notes_for_contact(request, pk):
    contact = get_object_or_404(org_queryset(BusinessContact.objects, request), pk=pk)
    notes = org_queryset(SecureNote.objects.filter(contact=contact).select_related("author"), request)
    return render(request, "accounts/secure_notes.html", {"contact": contact, "notes": notes})


# --- CONTACT DETAIL & EDIT ---
@login_required
@require_role("STAFF", "CLIENT")
def contact_detail(request, pk):
    contact = get_object_or_404(org_queryset(BusinessContact.objects, request), pk=pk)
# Clients may only see active contacts
    if request.user.profile.role == "CLIENT" and not contact.is_active:
        return HttpResponseForbidden("Not allowed")
    return render(request, "accounts/contact_detail.html", {"contact": contact})


@login_required
@require_role("STAFF")
def contact_edit(request, pk):
    contact = get_object_or_404(org_queryset(BusinessContact.objects, request), pk=pk)
    if request.method == "POST":
        form = BusinessContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
        return redirect("accounts:contacts_list")
    else:
        form = BusinessContactForm(instance=contact)
    return render(request, "accounts/form.html", {"form": form, "title": f"Edit {contact}"})


# --- CLIENT DETAIL & EDIT ---
@login_required
@require_role("STAFF", "CLIENT")
def client_detail(request, pk):
    client = get_object_or_404(org_queryset(Client.objects, request), pk=pk)
    if request.user.profile.role == "CLIENT" and not client.allow_portal_access:
        return HttpResponseForbidden("Not allowed")
    return render(request, "accounts/client_detail.html", {"client": client})


@login_required
@require_role("STAFF")
def client_edit(request, pk):
    client = get_object_or_404(org_queryset(Client.objects, request), pk=pk)
    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
        return redirect("accounts:clients_list")
    else:
        form = ClientForm(instance=client)
    return render(request, "accounts/form.html", {"form": form, "title": f"Edit {client}"})


# --- REFERRAL DETAIL & EDIT ---
@login_required
@require_role("STAFF", "CLIENT")
def referral_detail(request, pk):
    referral = get_object_or_404(org_queryset(Referral.objects, request), pk=pk)
    if request.user.profile.role == "CLIENT" and not referral.to_client.allow_portal_access:
        return HttpResponseForbidden("Not allowed")
    return render(request, "accounts/referral_detail.html", {"referral": referral})


@login_required
@require_role("STAFF")
def referral_edit(request, pk):
    referral = get_object_or_404(org_queryset(Referral.objects, request), pk=pk)
    if request.method == "POST":
        form = ReferralForm(request.POST, instance=referral)
        if form.is_valid():
            form.save()
        return redirect("accounts:referrals_list")
    else:
        form = ReferralForm(instance=referral)
    return render(request, "accounts/form.html", {"form": form, "title": f"Edit Referral #{referral.pk}"})


@login_required
def profile_view(request):
    return render(request, "accounts/profile.html", {
        "user_obj": request.user,
        "profile": request.user.profile,
    })

@login_required
def profile_edit_self(request):
    user = request.user
    profile = user.profile

    if request.method == "POST":
        u_form = UserForm(request.POST, instance=user)
        p_form = UserProfileSelfForm(request.POST, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profile updated successfully")
            return redirect("accounts:profile")
    else:
        u_form = UserForm(instance=user)
        p_form = UserProfileSelfForm(instance=profile)

    return render(request, "accounts/profile_edit.html", {
        "u_form": u_form,
        "p_form": p_form,
    })

@login_required
@require_role("STAFF")
def user_list(request):
    qs = User.objects.select_related("profile").all()
    # Optional: scope to same organization only
    qs = qs.filter(profile__organization=request.user.profile.organization)
    return render(request, "accounts/user_list.html", {"users": qs})