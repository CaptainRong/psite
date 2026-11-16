import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from font_source import fragment, write_key


def narrow(definition, factor):
    paths = []
    for path in definition['paths']:
        def point(match):
            x, y = float(match[1]), float(match[2])
            return f'{32+(x-32)*factor:.2f},{y:.2f}'
        paths.append(re.sub(r'(-?\d+\.\d+),(-?\d+\.\d+)', point, path))
    return {**definition, 'paths': paths}


glyphs = {
    'r-hand-narrow': narrow(fragment('手', '手的窄形，三横与竖钩'), .72),
    'r-wu-head': fragment('午', '午字去中竖，保留上撇与两横',
                          crop=[0, 0, 64, 35.75], erase=[[30.1,16.5,34.15,34.25]]),
    'r-jin-head': fragment('斤', '𠂆，斤去右下横和竖，撇起笔',
                          erase=[[19.25,12.5,64,64]]),
    'r-jin-narrow': narrow(fragment('斤', '斤的窄形，右竖从横下起'), .76),
    'r-left-two': fragment('彡', '两撇', select=[1, 2]),
}
key = {
    'key': 'R', 'zone': 'left', 'name': '白', 'short': '的',
    'roots': [
        ['白', '手', '@r-hand-narrow', '扌'],
        ['龵', '@r-wu-head', '斤', '@r-jin-head'],
        ['@r-jin-narrow'],
    ],
    'stroke': 'r-left-two',
}
write_key('R', key, glyphs)
