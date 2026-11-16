import re
import sys
sys.path.insert(0,'.qa')
from font_source import fragment, write_key


def mapped(definition, mapping):
    def point(match):
        x,y=mapping(float(match[1]),float(match[2]))
        return f'{x:.2f},{y:.2f}'
    return {**definition,'paths':[re.sub(r'(-?\d+\.\d+),(-?\d+\.\d+)',point,p) for p in definition['paths']]}


def left_falling(x,y):
    if x<25 and y>25:
        x-=8*((y-25)/34)**2
    return x,y


glyphs={
    'm-frame-left-fall':mapped(fragment('冂','冂的左笔撇形'),left_falling),
    'm-frame-wide':mapped(fragment('冂','冂的直角宽形'),lambda x,y:(32+(x-32)*1.3,32+(y-32)*.85)),
    'm-bone-head':fragment('骨','骨字头，去月，保留内短横与内竖',select=[1,2,3]),
}
key={'key':'M','zone':'vertical','name':'山','short':'同',
     'roots':[['山','由','贝','几'],['冂','@m-frame-left-fall','@m-frame-wide','@m-bone-head']]}
write_key('M',key,glyphs)
