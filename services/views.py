from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Service
from django.utils.html import strip_tags
from django.template.defaultfilters import truncatechars
from django.templatetags.static import static

def service_list(request):
    qs = Service.objects.filter(is_active=True).order_by("order", "name")
    q = request.GET.get("q")
    if q:
        qs = qs.filter(name__icontains=q) | qs.filter(short_description__icontains=q)

    paginator = Paginator(qs, 9)
    page = request.GET.get("page")
    services = paginator.get_page(page)

    return render(request, "services/service_list.html", {"services": services, "q": q or ""})


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    related = Service.objects.filter(is_active=True).exclude(pk=service.pk)[:4]

    # Build a concise description (prefer short_description; fallback to stripped CKEditor content)
    raw_desc = service.short_description or strip_tags(service.description or "")
    meta_description = truncatechars(raw_desc.strip(), 160)

    # Absolute OG image URL: prefer service.image; fallback to a sitewide default
    if service.image:
        og_image_url = request.build_absolute_uri(service.image.url)
        og_image_alt = f"{service.name} image"
    else:
        default_og = request.build_absolute_uri(static("img/og-default.jpg"))
        og_image_url = default_og
        og_image_alt = "Raveon Technologies"

    context = {
        "service": service,
        "related": related,

        # OG / SEO
        "page_title": service.name,
        "meta_description": meta_description,
        "og_type": "product",         # or "website" if you prefer
        "og_image_url": og_image_url,
        "og_image_alt": og_image_alt,
        # og:url will use request.build_absolute_uri in your base template
    }

    return render(request, "services/service_detail.html", context)