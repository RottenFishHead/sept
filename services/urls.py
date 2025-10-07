from django.urls import path
from . import views

app_name = "services"

urlpatterns = [
    # List all services
    path("", views.service_list, name="service_list"),

    # Single service detail (by slug)
    path("<slug:slug>/", views.service_detail, name="service_detail"),
]