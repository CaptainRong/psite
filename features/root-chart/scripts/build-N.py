import sys
sys.path.insert(0, '.qa')
from font_source import fragment, inspect, write_key, contours, bounds, clip_polygon


def shape(label, polygons):
    polygons = [p for p in polygons if len(p)>2]
    x0,y0,x1,y1=bounds(polygons)
    scale=54/max(x1-x0,y1-y0)
    cx,cy=(x0+x1)/2,(y0+y1)/2
    return {'label':label,'paths':[''.join(
        'M'+' '.join(f'{32+(x-cx)*scale:.2f},{32+(y-cy)*scale:.2f}' for x,y in p)+'Z'
        for p in polygons)],'filled':True}


inspect('已巳己彐羽心尸⺗乛乃儿忄乙', 'inspect-N.png')
frame=[clip_polygon(p,[0,0,64,34]) for p in contours('彐')]
short_frame=[[(x + (12 if y>27 and x<40 else 0),y) for x,y in p] for p in frame]
corpse_contours=contours('尸')
straight_stem=corpse_contours[1][32:71]+[
    (19.5,53),(28,53),(25,56),(15.7,56),(15.7,27.9)
]
straight_corpse=[corpse_contours[0],straight_stem]
corpse_with_stroke=contours('尸')+[
    [(32,10),(36,12),(35,14),(35,26.5),(32,26.5)]
]
folded=[(12,7),(17,9),(15,11),(15,24),(48,24),(51,26),
        (33,58),(29.5,56.5),(46.5,25.5),(12,25.5),(10.5,24)]
vertical_lift=[(16,7),(22,10),(20,12),(20,51),(46,40),
               (47,41.5),(19,59),(12,54),(16,51)]
long_fold_hook=[(7,12),(43,12),(47,8),(53,13),(49,16),
                (49,49),(48,53),(45,56),(41,58),(40,54),
                (30,51),(30,50),(42,51),(44,50),(44,14),(9,14)]
glyphs={
    'n-left-frame':shape('左框，横折横，开口向左',frame),
    'n-left-frame-short':shape('左框的短下横变形',short_frame),
    'n-corpse-straight':shape('尸的下笔直竖变形',straight_corpse),
    'n-corpse-inner':shape('尸内有短竖的片形',corpse_with_stroke),
    'n-folded':shape('竖折形，先竖后折横再折撇', [folded]),
    'n-long-fold-hook':shape('横折钩形，右端长下折钩',[long_fold_hook]),
    'n-fold-hook':fragment('乃','横折弯钩片形',crop=[31,0,64,64]),
    'n-vertical-lift':shape('竖提片形',[vertical_lift]),
    'n-vertical-bend':fragment('儿','竖弯钩片形',select=[1]),
    'n-fold-one':fragment('乙','乙，一折类笔画'),
}
key={
    'key':'N','zone':'fold','name':'已','short':'民',
    'roots':[
        ['已','巳','己','@n-left-frame'],
        ['@n-left-frame-short','羽','心','尸'],
        ['@n-corpse-straight','@n-corpse-inner','⺗','@n-long-fold-hook'],
        ['@n-folded','@n-fold-hook','@n-vertical-lift','@n-vertical-bend'],
        ['忄'],
    ],
    'stroke':'n-fold-one',
}
write_key('N',key,glyphs)
