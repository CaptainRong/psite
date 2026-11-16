import sys
sys.path.insert(0, '.qa')
from font_source import fragment, contours, bounds, write_key
from key_b_preview import preview_circle


def encode(polygons):
    return ''.join('M'+' '.join(f'{x:.2f},{y:.2f}' for x,y in polygon)+'Z' for polygon in polygons)


def small_inward_dots():
    polygons = contours('丷')
    x0, y0, x1, y1 = bounds(polygons)
    scale = 38 / (x1-x0)
    cx, cy = (x0+x1)/2, (y0+y1)/2
    points = [[(32+(x-cx)*scale,32+(y-cy)*scale) for x,y in polygon] for polygon in polygons]
    return {'label':'丷的短内收形','paths':[encode(points)],'filled':True}


def vertical_two_dots():
    source = contours('丶')
    x0,y0,x1,y1 = bounds(source)
    scale = 17/(y1-y0)
    cx,cy = (x0+x1)/2,(y0+y1)/2
    polygons = []
    for target_x,target_y in [(30,16),(32,46)]:
        polygons.extend([[(target_x+(x-cx)*scale,target_y+(y-cy)*scale) for x,y in polygon] for polygon in source])
    return {'label':'上下纵排两点','paths':[encode(polygons)],'filled':True}


glyphs = {
    'u-short-dots':small_inward_dots(),
    'u-vertical-dots':vertical_two_dots(),
}
key = {
    'key':'U','zone':'dot','name':'立','short':'产',
    'roots':[
        ['立','@u-short-dots','六','䒑'],
        ['辛','冫','丷','疒'],
        ['丬','爿','门'],
    ],
    'stroke':'u-vertical-dots',
}
write_key('U',key,glyphs)
preview_circle('U',glyphs[key['stroke']])
