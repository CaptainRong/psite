import sys
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).parent / 'pdf-lib'))
import pymupdf


def add_circle(letter, key, glyphs):
    if not key.get('stroke'):
        return
    definition = glyphs[key['stroke']]
    paths = ''.join(f'<path fill="#f0f0e6" d="{path}"/>' for path in definition['paths'])
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 80 80"><rect width="80" height="80" fill="#080a09"/><circle cx="40" cy="40" r="38" fill="none" stroke="#bb6e65" stroke-width="2"/><g transform="translate(12,12) scale(.875)">{paths}</g></svg>'
    document = pymupdf.open(stream=svg.encode(), filetype='svg')
    pixmap = document[0].get_pixmap()
    circle = Image.frombytes('RGB', [pixmap.width,pixmap.height], pixmap.samples)
    target = Path(__file__).parent/f'key-{letter}.png'
    image=Image.open(target)
    image.paste(circle, (200,image.height-100))
    image.save(target)
