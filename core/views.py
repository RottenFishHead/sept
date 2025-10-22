from multiprocessing import context
from django.shortcuts import render
from products.models import Product, Category
from services.models import Service
from articles.models import Article  

def index(request):
    categories = Category.objects.all()    
    context = {
        "categories": categories,
    }
    return render(request, "account/index.html", context)


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

    return render(request, "account/search_results.html", {"q": q, "results": results})

def about(request):
    return render(request, "account/about.html")

def contact(request):
    return render(request, "account/contact.html")