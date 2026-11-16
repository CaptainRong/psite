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


inspect('田甲四囗皿罒丷丨', 'inspect-L.png')
dot_polygons=contours('丷')
dx0,dy0,dx1,dy1=bounds(dot_polygons)
inside=[[(18+(x-dx0)*28/(dx1-dx0),21+(y-dy0)*19/(dy1-dy0))
         for x,y in p] for p in dot_polygons]
net_box=contours('囗')+inside
net_box=[[(x,y*.55) for x,y in p] for p in net_box]
flat_four=[[(x,y*.52) for x,y in p] for p in contours('四')]
vertical=contours('丨')
vx0,vy0,vx1,vy1=bounds(vertical)
vertical_center=(vx0+vx1)/2
four_verticals=[]
for center in [14,26,38,50]:
    four_verticals.extend([[(x-vertical_center+center,y) for x,y in p] for p in vertical])
glyphs={
    'l-net-dots':shape('罒的内八扁形',net_box),
    'l-flat-four':shape('四的扁形',flat_four),
    'l-four-verticals':shape('四竖片形',four_verticals),
}
key={
    'key':'L','zone':'vertical','name':'田','short':'国',
    'roots':[
        ['田','甲','四','囗'],
        ['皿','罒','@l-net-dots','@l-flat-four'],
        ['车','@l-four-verticals','力'],
    ],
}
write_key('L',key,glyphs)
