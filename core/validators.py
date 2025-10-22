from django.core.exceptions import ValidationError

def validate_svg_or_image(file):
    """
    Lightweight validator to allow both raster images and SVGs safely.
    """
    allowed_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg')
    ext = file.name.lower().split('.')[-1]

    if f".{ext}" not in allowed_extensions:
        raise ValidationError("Unsupported file type. Upload PNG, JPG, WEBP, GIF, or SVG.")

    # SVG safety check
    if ext == 'svg':
        header = file.read(500).decode(errors='ignore').lower()
        file.seek(0)  # Reset file pointer
        if "<script" in header or "<iframe" in header or "onload=" in header:
            raise ValidationError("Insecure SVG file — contains forbidden scripts.")
