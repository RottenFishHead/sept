from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def hero(icon, css="w-6 h-6 text-gray-600"):
    """Render an inline Heroicon SVG."""
    # Path where your SVG icons live
    svg_path = f"static/icons/heroicons/{icon}.svg"
    try:
        with open(svg_path, "r", encoding="utf-8") as f:
            svg = f.read()
        return mark_safe(svg.replace("<svg", f"<svg class='{css}'"))
    except FileNotFoundError:
        return mark_safe(f"<!-- missing icon: {icon} -->")
