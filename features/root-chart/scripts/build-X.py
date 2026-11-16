import sys
sys.path.insert(0, '.qa')
from font_source import fragment, inspect, write_key, contours, bounds


def shape(label, polygons):
    x0,y0,x1,y1=bounds(polygons)
    scale=54/max(x1-x0,y1-y0)
    cx,cy=(x0+x1)/2,(y0+y1)/2
    return {'label':label,'paths':[''.join(
        'M'+' '.join(f'{32+(x-cx)*scale:.2f},{32+(y-cy)*scale:.2f}' for x,y in p)+'Z'
        for p in polygons)],'filled':True}


inspect('母毋幺比互彑', 'inspect-X.png')
silk=contours('幺')[0]
silk_without_dot=silk[:115]+silk[199:]
mother=contours('母')[0]
mother_outline=mother[:2]+mother[6:101]+mother[105:]
mother_inner=[(47.5,9.5),(19,9.5),(15,46.75),(44.8,46.75)]
glyphs={
    'x-silk-no-dot':shape('幺去末点，丝的左上部',[silk_without_dot]),
    'x-mother-frame':shape('毋母的外框，去内横与两点',[mother_outline,mother_inner]),
    'x-mutual-middle':fragment('互','互去上下两横的中间框形',crop=[0,16,47.5,51]),
    'x-compare-left':fragment('比','比的左旁',select=[0]),
}
key={
    'key':'X','zone':'fold','name':'纟','short':'经',
    'roots':[
        ['纟','@x-silk-no-dot','幺','@x-mother-frame'],
        ['@x-mutual-middle','弓','匕','@x-compare-left'],
    ],
}
write_key('X',key,glyphs)
