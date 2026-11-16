"""Rebuild isolated key proposals and compare them with the shipped data."""
import argparse
import copy
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
SCRIPT_DIR = Path(__file__).resolve().parent
DATA = ROOT / 'features/root-chart/data/wubi86.js'
LETTERS = 'QWERTYUIOPASDFGHJKLZXCVBNM'


def read_data():
    text = DATA.read_text(encoding='utf-8')
    return json.loads(text.split('window.WUBI_DATA = ', 1)[1].rstrip(';\n'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('keys', nargs='*', help='Key letters, for example Q N. Default: all keys.')
    parser.add_argument('--output', type=Path, default=ROOT / '.qa/glyphs')
    parser.add_argument('--font', type=Path, help='Same Songti font used by the baseline')
    parser.add_argument('--apply', action='store_true', help='Write compared output to the runtime data file')
    args = parser.parse_args()
    letters = ''.join(args.keys).upper() or LETTERS.replace('Z', '')
    if any(letter not in LETTERS.replace('Z', '') for letter in letters):
        parser.error('Only the 25 Wubi root keys are supported')
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    environment = dict(os.environ, WUBI_OUTPUT=str(output))
    if args.font:
        environment['WUBI_FONT'] = str(args.font.resolve())
    original = read_data()
    rebuilt = copy.deepcopy(original)
    for letter in dict.fromkeys(letters):
        subprocess.run([sys.executable, str(SCRIPT_DIR / f'build-{letter}.py')],
                       check=True, cwd=ROOT, env=environment)
        proposal = json.loads((output / f'key-{letter}.json').read_text(encoding='utf-8'))
        index = next(i for i, key in enumerate(rebuilt['keys']) if key['key'] == letter)
        rebuilt['keys'][index] = proposal['key']
        for glyph in proposal['glyphs'].values():
            glyph.pop('filled', None)
        rebuilt['glyphs'].update(proposal['glyphs'])
    used = {value[1:] for key in rebuilt['keys'] for row in key['roots'] for value in row if value.startswith('@')}
    used.update(key['stroke'] for key in rebuilt['keys'] if key.get('stroke'))
    rebuilt['glyphs'] = {name: glyph for name, glyph in rebuilt['glyphs'].items() if name in used}
    differences = [letter for letter in letters if
                   next(key for key in original['keys'] if key['key'] == letter) !=
                   next(key for key in rebuilt['keys'] if key['key'] == letter)]
    glyph_changes = [name for name in rebuilt['glyphs'] if rebuilt['glyphs'][name] != original['glyphs'].get(name)]
    (output / 'rebuilt-data.json').write_text(json.dumps(rebuilt, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'keys': len(set(letters)), 'keyChanges': differences, 'glyphChanges': glyph_changes}, ensure_ascii=False))
    if args.apply:
        DATA.write_text('/* 五笔 86 宋体版。@ 引用 64 × 64 片形，片形按宋体部件提取或重绘。 */\n'
                        'window.WUBI_DATA = ' + json.dumps(rebuilt, ensure_ascii=False, indent=2) + ';\n', encoding='utf-8')
    elif differences or glyph_changes:
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
