import sys
sys.path.insert(0, '.qa')
from font_source import fragment, contours, bounds, clip_polygon, write_key
from key_b_preview import preview_circle


def from_polygons(label, polygons):
    polygons = [polygon for polygon in polygons if len(polygon)>2]
    x0,y0,x1,y1 = bounds(polygons)
    scale=54/max(x1-x0,y1-y0)
    cx,cy=(x0+x1)/2,(y0+y1)/2
    paths=['M'+' '.join(f'{32+(x-cx)*scale:.2f},{32+(y-cy)*scale:.2f}' for x,y in polygon)+'Z' for polygon in polygons]
    return {'label':label,'paths':[''.join(paths)],'filled':True}


water=contours('水')
right=clip_polygon(water[0],[37,0,64,64])
no_middle = [right,[(64-x,y) for x,y in reversed(right)]]
left_short = [right,water[1]]
learn = contours('学')
small_inverted = contours('当')

glyphs={
    'i-water-sides':from_polygons('水去中竖，左右四笔相向变形',no_middle),
    'i-water-sides-short':from_polygons('水去中竖，左上为短横的变形',left_short),
    'i-water-bottom':{
        'label':'水底左点中竖右折相连的变形',
        'paths':[
            'M17 16L23 18L19 25L10 34L6 35L13 25Z',
            'M29 9L36 12L34 15L34 31L29 31Z',
            'M8 45L13 41L43 41L50 21L56 24L53 27L48 45L15 45L10 49Z',
        ],'filled':True,
    },
    'i-learn-top':from_polygons('学字头前三笔',[learn[0],learn[1],clip_polygon(learn[2],[36,0,56,19.5])]),
    'i-rise-top':fragment('兴','兴字头，三笔加底横',select=[0,1,2]),
    'i-small-inverted':from_polygons('倒小字形',[small_inverted[0],small_inverted[1],clip_polygon(small_inverted[2],[26,0,37,25])]),
    'i-small-inverted-line':fragment('光','倒小字形加底横',crop=[0,0,64,32]),
    'i-water-dots':fragment('氵','氵式纵排三点'),
}
key={
    'key':'I','zone':'dot','name':'水','short':'不',
    'roots':[
        ['水','氺','@i-water-sides','@i-water-sides-short'],
        ['小','@i-water-bottom','@i-learn-top','@i-rise-top'],
        ['@i-small-inverted','@i-small-inverted-line'],
    ],
    'stroke':'i-water-dots',
}
write_key('I',key,glyphs)
preview_circle('I',glyphs[key['stroke']])
