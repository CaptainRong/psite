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


inspect('羊春镸尤三厂丆左', 'inspect-D.png')
left=contours('左')[0]
cross_left=left[:33]+left[60:]
spring=contours('春')[0]
three_left=spring[:17]+spring[89:]
you=contours('尤')
you_without_bend=[you[0][:20]+you[0][108:],you[1]]
glyphs={
    'd-sheep':fragment('羊','羊去丷，竖从首横起',crop=[0,18.5,64,64]),
    'd-three-left':shape('三横交撇形，春去日和捺',[three_left]),
    'd-cross-left':shape('横与撇相交的𠂇片形',[cross_left]),
    'd-you':shape('尤去右下竖弯钩',you_without_bend),
    'd-three-horizontal':fragment('三','三横'),
}
key={
    'key':'D','zone':'horizontal','name':'大','short':'在',
    'roots':[
        ['大','犬','古','石'],
        ['@d-sheep','@d-three-left','镸','厂'],
        ['丆','@d-cross-left','@d-you'],
    ],
    'stroke':'d-three-horizontal',
}
write_key('D',key,glyphs)
