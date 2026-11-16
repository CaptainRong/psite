import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from font_source import fragment, write_key
from preview_circle import add_circle


def scaled(definition, sx, sy):
    def point(match):
        x,y=float(match[1]),float(match[2])
        return f'{32+(x-32)*sx:.2f},{32+(y-32)*sy:.2f}'
    return {**definition,'paths':[re.sub(r'(-?\d+\.\d+),(-?\d+\.\d+)',point,p) for p in definition['paths']]}


four_bars=fragment('丰','短竖贯四横形，参考图Y右下')
four_bars['paths'].append('M5,56 50,56 54,52 59,57.5 12,57.5 7,58.2Z')
glyphs={
    'y-long-dot':scaled(fragment('丶','长点捺形'),.6,1),
    'y-high-head':fragment('高','高字头，点横与口',select=[0,1,3,4]),
    'y-four-bars':four_bars,
    'y-dot':scaled(fragment('丶','一点'),.45,.45),
}
key={'key':'Y','zone':'dot','name':'言','short':'主',
     'roots':[['言','讠','文','方'],['@y-long-dot','亠','@y-high-head','广'],['@y-four-bars']],
     'stroke':'y-dot'}
write_key('Y',key,glyphs)
add_circle('Y',key,glyphs)
