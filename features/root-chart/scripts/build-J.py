import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from font_source import fragment, write_key
from preview_circle import add_circle

vertical = fragment('丨', '一竖')['paths'][0]
def placed(offset, factor):
    def point(match):
        x,y=float(match[1]),float(match[2])
        return f'{x+offset:.2f},{59+(y-59)*factor:.2f}'
    return re.sub(r'(-?\d+\.\d+),(-?\d+\.\d+)',point,vertical)

glyphs = {'j-two-vertical': {
    'label':'两竖，左竖略短、右竖略长',
    'paths':[placed(-9,.88),placed(9,1)], 'filled':True,
}}
key = {'key':'J','zone':'vertical','name':'日','short':'是',
       'roots':[['日','早','刂','虫']], 'stroke':'j-two-vertical'}
write_key('J',key,glyphs)
add_circle('J',key,glyphs)
