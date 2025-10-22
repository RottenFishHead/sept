from django import template
from django.urls import resolve, reverse, NoReverseMatch

register = template.Library()

@register.inclusion_tag("partials/breadcrumbs.html", takes_context=True)
def breadcrumbs(context):
    request = context["request"]
    path = request.path.strip("/").split("/")
    crumbs = []
    url_accumulator = ""
    for segment in path:
        if not segment:
            continue
        url_accumulator += f"/{segment}"
        try:
            match = resolve(url_accumulator)
            name = match.url_name or segment.replace("-", " ").title()
        except Exception:
            name = segment.replace("-", " ").title()
        crumbs.append({
            "name": name,
            "url": url_accumulator,
        })
    return {"crumbs": crumbs}
