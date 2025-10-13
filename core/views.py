from django.shortcuts import render
from products.models import Product
from services.models import Service
from articles.models import Article  

def index(request):
    return render(request, "core/index.html")


def site_search(request):
    q = request.GET.get("q", "").strip()
    results = []

    if q:
        # Gather results from multiple apps
        service_results = Service.objects.filter(
            name__icontains=q
        ).values("name", "slug", "short_description")

        product_results = Product.objects.filter(
            name__icontains=q
        ).values("name", "slug", "short_description")

        article_results = Article.objects.filter(
            title__icontains=q
        ).values("title", "slug", "excerpt")

        results = {
            "services": service_results,
            "products": product_results,
            "articles": article_results,
        }

    return render(request, "core/search_results.html", {"q": q, "results": results})

def about(request):
    return render(request, "core/about.html")

def contact(request):
    return render(request, "core/contact.html")