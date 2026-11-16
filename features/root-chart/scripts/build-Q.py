import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from font_source import fragment, inspect, write_key, contours, bounds


def shape(label, polygons):
    x0, y0, x1, y1 = bounds(polygons)
    scale = 54 / max(x1 - x0, y1 - y0)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    paths = []
    for polygon in polygons:
        paths.append('M' + ' '.join(
            f'{32 + (x-cx)*scale:.2f},{32 + (y-cy)*scale:.2f}' for x, y in polygon
        ) + 'Z')
    return {'label': label, 'paths': [''.join(paths)], 'filled': True}


def transformed(polygons, sx=1, sy=1, dx=0, dy=0):
    return [[(x*sx+dx, y*sy+dy) for x, y in polygon] for polygon in polygons]


inspect('犭氏夕儿鱼歹', 'inspect-Q.png')
children = contours('儿')
close_child = transformed([children[0]], dx=6) + transformed([children[1]], dx=-5)
double_child = transformed([children[0]], sx=.65, dx=2)
double_child += transformed([children[0]], sx=.65, dx=16)
double_child += transformed([children[1]], sx=.70, dx=15)

# 沿字体轮廓的节点删去分叉，避免矩形擦除切断相邻笔画。
dog_outline = contours('犭')[0]
dog_outline = dog_outline[:159] + dog_outline[184:]
evening_outline = contours('夕')[0]
evening_without_dot = evening_outline[:116] + evening_outline[188:]
short_dot_evening = evening_outline[:116] + [
    (21 + (x-21)*.67, 29 + (y-29)*.55)
    for x, y in evening_outline[116:188]
] + evening_outline[188:]
shi_outline = contours('氏')[0][88:167] + [(15, 14.8)]
shi = shape('氏去七，保留首撇与竖提', [shi_outline])
glyphs = {
    'q-child-close': shape('儿的并足变形', close_child),
    'q-child-double': shape('儿的双竖变形', double_child),
    'q-dog': shape('犬旁两笔片形，去末撇', [dog_outline]),
    'q-fish': fragment('鱼', '鱼去末横', select=[1,2,3,4,5,6]),
    'q-evening-nodot': shape('夕去内点', [evening_without_dot]),
    'q-evening-cross': shape('夕的交叉短撇变形', [short_dot_evening]),
    'q-evening-double': fragment('歹', '夕的双折变形，歹去顶横',
                                crop=[0, 13, 64, 64]),
    'q-shi': shi,
    'q-shi-wide': shape('氏去七的横卧变形', transformed([shi_outline], sx=1.3, sy=.62)),
}

key = {
    'key': 'Q', 'zone': 'left', 'name': '金', 'short': '我',
    'roots': [
        ['金', '钅', '儿', '@q-child-close'],
        ['勹', '@q-dog', '乂', '@q-child-double'],
        ['@q-fish', '夕', '@q-evening-nodot', '@q-evening-cross'],
        ['@q-evening-double', '@q-shi', '@q-shi-wide'],
    ],
}
write_key('Q', key, glyphs)
