import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from font_source import CMAP, write_key

roots = ['木', '丁', '西', '覀']
assert all(ord(char) in CMAP for char in roots)
key = {
    'key': 'S',
    'zone': 'horizontal',
    'name': '木',
    'short': '要',
    'roots': [roots],
}
write_key('S', key, {})
