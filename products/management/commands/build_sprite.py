from django.core.management.base import BaseCommand
from pathlib import Path
import re

class Command(BaseCommand):
    help = "Builds a combined SVG sprite from static/icons/source/"

    def handle(self, *args, **options):
        project_root = Path(__file__).resolve().parents[3]
        icon_dir = project_root / "static" / "icons" / "source"
        output_file = project_root / "static" / "icons" / "sprite.svg"

        icon_dir.mkdir(parents=True, exist_ok=True)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Begin SVG sprite cleanly
        sprite_content = ['<svg xmlns="http://www.w3.org/2000/svg" style="display:none">']

        for svg_file in icon_dir.glob("*.svg"):
            name = svg_file.stem
            svg = svg_file.read_text(encoding="utf-8")

            # Strip XML declarations and outer <svg> tags
            svg = re.sub(r'<\?xml.*?\?>', '', svg)
            svg = re.sub(r'<!DOCTYPE.*?>', '', svg)
            svg = re.sub(r'<(/)?svg[^>]*>', '', svg)

            sprite_content.append(f'<symbol id="icon-{name}" viewBox="0 0 24 24">{svg.strip()}</symbol>')

        sprite_content.append("</svg>")

        # Write without any BOM or leading newlines
        output_file.write_text("\n".join(sprite_content).strip(), encoding="utf-8")

        self.stdout.write(self.style.SUCCESS(
            f"✅ Built sprite with {len(list(icon_dir.glob('*.svg')))} icons → {output_file}"
        ))