import json
from pathlib import Path
from fontTools.pens.boundsPen import BoundsPen
from fontTools.svgLib.path import parse_path
from font_source import CMAP

root = Path(__file__).resolve().parent.parent
script = (root / 'wubi-data.js').read_text(encoding='utf-8')
data = json.loads(script.split('window.WUBI_DATA = ', 1)[1].rstrip(';\n'))
expected = dict(zip('QWERTYUIOPASDFGHJKLZXCVBNM',
                    [15,5,12,9,8,9,11,10,5,6,13,4,11,9,5,10,4,1,11,0,8,6,7,12,17,8]))
assert len(data['keys']) == 26
assert len({key['key'] for key in data['keys']}) == 26
assert ''.join(data['rows']) == ''.join(expected)
used = set()
missing_text = set()
for key in data['keys']:
    roots = [value for row in key['roots'] for value in row]
    assert len(roots) == expected[key['key']], key['key']
    assert all(len(row) <= 4 for row in key['roots'])
    used.update(value[1:] for value in roots if value.startswith('@'))
    for value in roots:
        if not value.startswith('@'):
            missing_text.update(char for char in value if ord(char) not in CMAP)
    if key.get('stroke'):
        used.add(key['stroke'])
assert used == set(data['glyphs']), 'missing or unused glyphs'
assert not missing_text, missing_text
for glyph_id, glyph in data['glyphs'].items():
    assert glyph['label'] and glyph['paths'], glyph_id
    pen = BoundsPen(None)
    for outline in glyph['paths']:
        parse_path(outline, pen)
    assert pen.bounds is not None, glyph_id
    assert all(-.01 <= coordinate <= 64.01 for coordinate in pen.bounds), glyph_id
print(json.dumps({'keys':26,'rootItems':sum(expected.values()),
                  'circleItems':sum(bool(key.get('stroke')) for key in data['keys']),
                  'svgDefinitions':len(used),'missingSongtiCharacters':len(missing_text)},ensure_ascii=False))
