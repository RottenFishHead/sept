from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods, require_safe
from articles.forms import ArticleForm, ArticleImageFormSet
from .models import Article

def seo_context(obj):
    return {
        "meta_title": getattr(obj, "meta_title", None),
        "meta_description": getattr(obj, "meta_description", None),
        "meta_canonical": getattr(obj, "meta_canonical", None),
        "meta_og_image": getattr(obj, "og_image", None),
    }

@require_safe
def article_list(request):
    qs = Article.objects.filter(published=True)
    return render(request, "articles/article_list.html", {"articles": qs})

@require_safe
def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, published=True)
    ctx = {"article": article, **seo_context(article)}
    return render(request, "articles/article_detail.html", ctx)

@require_http_methods(["GET", "POST"])
def article_create(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        formset = ArticleImageFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            article = form.save(commit=False)
            article.author = request.user if request.user.is_authenticated else None
            article.save()
            formset.instance = article
            formset.save()
            messages.success(request, "Article created.")
            return redirect("articles:detail", slug=article.slug)
    else:
        form = ArticleForm()
        formset = ArticleImageFormSet()
    return render(request, "articles/article_form.html", {"form": form, "formset": formset, "mode": "create"})

@require_http_methods(["GET", "POST"])
def article_update(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        formset = ArticleImageFormSet(request.POST, request.FILES, instance=article)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Article updated.")
            return redirect("articles:detail", slug=article.slug)
    else:
        form = ArticleForm(instance=article)
        formset = ArticleImageFormSet(instance=article)
    return render(request, "articles/article_form.html", {"form": form, "formset": formset, "mode": "edit", "article": article})

@require_http_methods(["POST"])
def article_delete(request, slug):
    article = get_object_or_404(Article, slug=slug)
    article.delete()
    messages.success(request, "Article deleted.")
    return redirect("articles:list")
