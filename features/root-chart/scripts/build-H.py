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


inspect('虍具皮卜止足亅丨', 'inspect-H.png')
skin=contours('皮')[0]
skin_top=skin[:35]+[(32.8,31.8)]+skin[128:]
flat_divination=[(28,4),(34,7),(32,9),(32,27),(48,27),
                 (53,22),(59,29),(32,29),(32,58),(27,60),(28,56)]
glyphs={
    'h-tiger':fragment('虍','虎字头，虍去下七',select=[0]),
    'h-ju':fragment('具','具去八的头部，保留伸出的底横',select=[2,3,4,5,6]),
    'h-divination-flat':shape('卜的横点变形',[flat_divination]),
    'h-stop-foot':fragment('足','止的收紧变形，龰形',crop=[0,30,64,64]),
    'h-skin':shape('皮去又的头部',[skin_top]),
    'h-one-vertical':fragment('丨','一竖'),
}
key={
    'key':'H','zone':'vertical','name':'目','short':'上',
    'roots':[
        ['目','@h-tiger','@h-ju','亅'],
        ['卜','@h-divination-flat','上','止'],
        ['@h-stop-foot','@h-skin'],
    ],
    'stroke':'h-one-vertical',
}
write_key('H',key,glyphs)
