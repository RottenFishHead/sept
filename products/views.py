from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_safe

from .forms import ProductForm
from .models import Product

def seo_context(obj):
    return {
        "meta_title": getattr(obj, "meta_title", None),
        "meta_description": getattr(obj, "meta_description", None),
        "meta_canonical": getattr(obj, "meta_canonical", None),
        "meta_og_image": getattr(obj, "og_image", None),
    }


@require_safe
def product_list(request):
    qs = Product.objects.filter(is_active=True)
    q = request.GET.get("q")
    category = request.GET.get("category")
    if q:
        qs = qs.filter(name__icontains=q) | qs.filter(short_description__icontains=q)
    if category:
        qs = qs.filter(category__iexact=category)

    paginator = Paginator(qs, 12)
    page = request.GET.get("page")
    products = paginator.get_page(page)
    categories = (
        Product.objects.filter(is_active=True)
        .exclude(category="")
        .values_list("category", flat=True)
        .distinct()
        .order_by("category")
    )
    return render(request, "products/product_list.html", {"products": products, "q": q or "", "category": category or "", "categories": categories})

@require_safe
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related = Product.objects.filter(is_active=True, category=product.category).exclude(pk=product.pk)[:4]
    ctx = {"product": product, "related": related, **seo_context(product)}
    return render(request, "products/product_detail.html", ctx)

@require_http_methods(["GET", "POST"])
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, "Product created.")
            return redirect("products:detail", slug=product.slug)
    else:
        form = ProductForm()
    return render(request, "products/product_form.html", {"form": form, "mode": "create"})

@require_http_methods(["GET", "POST"])
def product_update(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated.")
            return redirect("products:detail", slug=product.slug)
    else:
        form = ProductForm(instance=product)
    return render(request, "products/product_form.html", {"form": form, "mode": "edit", "product": product})

@require_http_methods(["POST"])
def product_delete(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product.delete()
    messages.success(request, "Product deleted.")
    return redirect("products:list")
