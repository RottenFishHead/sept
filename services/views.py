from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Service

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
    return render(request, "services/service_detail.html", {"service": service, "related": related})
