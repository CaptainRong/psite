import re
import sys
sys.path.insert(0,'.qa')
from font_source import fragment, write_key
from preview_circle import add_circle


def shorter(definition, factor):
    def point(match):
        x,y=float(match[1]),float(match[2])
        return f'{x:.2f},{32+(y-32)*factor:.2f}'
    return {**definition,'paths':[re.sub(r'(-?\d+\.\d+),(-?\d+\.\d+)',point,p) for p in definition['paths']]}


glyphs={
    'b-hook-upper':fragment('卩','参考图底排首项，卩形上部，左竖下截的钩形',crop=[0,0,64,43]),
    'b-child-lower':fragment('子','子去上方横折，保留竖钩与短横',crop=[0,19,64,64]),
    'b-fold-hook':shorter(fragment('司','参考图底排第三项，横折钩形',select=[0]),.72),
    'b-two-folds':fragment('巜','两折'),
}
key={'key':'B','zone':'fold','name':'子','short':'了',
     'roots':[
         ['子','孑','了','也'],
         ['阝','卩','㔾','耳'],
         ['@b-hook-upper','@b-child-lower','@b-fold-hook','凵'],
     ],'stroke':'b-two-folds'}
write_key('B',key,glyphs)
add_circle('B',key,glyphs)
