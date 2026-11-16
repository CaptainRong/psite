import re
import sys
sys.path.insert(0,'.qa')
from font_source import fragment, write_key
from preview_circle import add_circle

base=fragment('彐','彐的下横左伸变形')
def shorten_upper(match):
    x,y=float(match[1]),float(match[2])
    if x<20 and y<40:
        x+=8
    return f'{x:.2f},{y:.2f}'
long_bottom={**base,'paths':[re.sub(r'(-?\d+\.\d+),(-?\d+\.\d+)',shorten_upper,p) for p in base['paths']]}
middle_cross=fragment('彐','彐的中横向右出头，右竖保留')
middle_cross['paths'].append('M52,29.66 59,29.66 61,27.66 64,31.24 52,31.24Z')
def fit_cross(match):
    x,y=float(match[1]),float(match[2])
    return f'{32+(x-34.5)*54/59:.2f},{32+(y-32)*54/59:.2f}'
middle_cross['paths']=[re.sub(r'(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)',fit_cross,p) for p in middle_cross['paths']]
glyphs={
    'v-long-bottom':long_bottom,
    'v-middle-cross':middle_cross,
    'v-three-folds':fragment('巛','三折'),
}
key={'key':'V','zone':'fold','name':'女','short':'发',
     'roots':[['女','刀','九','臼'],['彐','@v-long-bottom','@v-middle-cross']],
     'stroke':'v-three-folds'}
write_key('V',key,glyphs)
add_circle('V',key,glyphs)
