from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
# Contacts
path("contacts/", views.contacts_list, name="contacts_list"),
path("contacts/new/", views.contact_create, name="contact_create"),
path("contacts/<int:pk>/", views.contact_detail, name="contact_detail"),
path("contacts/<int:pk>/edit/", views.contact_edit, name="contact_edit"),

# Clients
path("clients/", views.clients_list, name="clients_list"),
path("clients/new/", views.client_create, name="client_create"),
path("clients/<int:pk>/", views.client_detail, name="client_detail"),
path("clients/<int:pk>/edit/", views.client_edit, name="client_edit"),

# Referrals
path("referrals/", views.referrals_list, name="referrals_list"),
path("referrals/new/", views.referral_create, name="referral_create"),
path("referrals/<int:pk>/", views.referral_detail, name="referral_detail"),
path("referrals/<int:pk>/edit/", views.referral_edit, name="referral_edit"),

# Secure Notes
path("contacts/<int:pk>/secure-notes/", views.secure_notes_for_contact, name="secure_notes_for_contact"),
# Password management
path("register/", views.register, name="register"),
path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
path("logout/", auth_views.LogoutView.as_view(next_page="accounts:login"), name="logout"),
path("password_change/", auth_views.PasswordChangeView.as_view(
        template_name="accounts/password_change.html"), name="password_change"),
path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(
        template_name="accounts/password_change_done.html"), name="password_change_done"),
path("password_reset/", auth_views.PasswordResetView.as_view(
        template_name="accounts/password_reset.html",
        email_template_name="accounts/password_reset_email.html",
        subject_template_name="accounts/password_reset_subject.txt",
        success_url="/accounts/password_reset/done/"), name="password_reset"),
path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_done.html"), name="password_reset_done"),
path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_confirm.html",
        success_url="/accounts/reset/done/"), name="password_reset_confirm"),
path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_complete.html"), name="password_reset_complete"),
        path("profile/", views.profile_view, name="profile"),
path("profile/edit/", views.profile_edit_self, name="profile_edit"),
path("users/", views.user_list, name="user_list"),  # staff-only
]