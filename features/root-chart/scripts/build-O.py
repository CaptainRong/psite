import sys
sys.path.insert(0, '.qa')
from font_source import fragment, contours, bounds, clip_polygon, write_key
from key_b_preview import preview_circle


def combine(label, polygons):
    polygons=[p for p in polygons if len(p)>2]
    x0,y0,x1,y1=bounds(polygons)
    scale=54/max(x1-x0,y1-y0)
    cx,cy=(x0+x1)/2,(y0+y1)/2
    parts=['M'+' '.join(f'{32+(x-cx)*scale:.2f},{32+(y-cy)*scale:.2f}' for x,y in p)+'Z' for p in polygons]
    return {'label':label,'paths':[''.join(parts)],'filled':True}


def positioned(polygon, center_x, center_y, scale):
    x0,y0,x1,y1=bounds([polygon])
    cx,cy=(x0+x1)/2,(y0+y1)/2
    return [(center_x+(x-cx)*scale,center_y+(y-cy)*scale) for x,y in polygon]


industry=contours('业')
small=contours('小')
industry_head=[industry[0],clip_polygon(industry[1],[20,0,30,52]),clip_polygon(industry[1],[34,0,43,52]),clip_polygon(industry[1],[43,0,64,52])]
short_industry=[clip_polygon(industry[1],[20,0,30,52]),clip_polygon(industry[1],[34,0,43,52])]
short_industry += [positioned(small[1],10,33,.5),positioned(small[2],53,34,.5)]
fire_variant=[small[0],small[2],positioned(small[1],14,29,.72),positioned(small[1],8,41,.72)]
glyphs={
    'o-industry':combine('业去底横',industry_head),
    'o-industry-short':combine('业字头，外侧短撇点变形',short_industry),
    'o-fire-bottom':combine('火字底变形，左双撇、中竖钩、右点',fire_variant),
    'o-four-dots':fragment('灬','四点底'),
}
key={
    'key':'O','zone':'dot','name':'火','short':'为',
    'roots':[['火','@o-industry','@o-industry-short','@o-fire-bottom'],['米']],
    'stroke':'o-four-dots',
}
write_key('O',key,glyphs)
preview_circle('O',glyphs[key['stroke']])
