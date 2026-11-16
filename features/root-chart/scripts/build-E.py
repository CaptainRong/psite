import sys
sys.path.insert(0, '.qa')
from font_source import fragment, contours, bounds, write_key


def reshape(char, label, select=None, crop=None, x_scale=1, y_scale=1):
    from font_source import clip_polygon
    polygons = contours(char)
    if select is not None:
        polygons = [polygons[index] for index in select]
    if crop:
        polygons = [clip_polygon(polygon, crop) for polygon in polygons]
    polygons = [[(x * x_scale, y * y_scale) for x, y in polygon] for polygon in polygons if len(polygon) > 2]
    x0, y0, x1, y1 = bounds(polygons)
    scale = 54 / max(x1-x0, y1-y0)
    cx, cy = (x0+x1)/2, (y0+y1)/2
    paths = []
    for polygon in polygons:
        paths.append('M'+' '.join(f'{32+(x-cx)*scale:.2f},{32+(y-cy)*scale:.2f}' for x,y in polygon)+'Z')
    return {'label': label, 'paths': [''.join(paths)], 'filled': True}


glyphs = {
    'e-month-narrow': reshape('冃', '月的直竖窄形', x_scale=.72),
    'e-pig-no-top': fragment('豕', '豕去顶横', crop=[0, 14.5, 64, 64]),
    # 衣的亠在 y<21。下部从原字取形，左撇起点与右撇相距较小。
    'e-clothes': fragment('衣', '衣去亠的底部', crop=[0, 21, 64, 64]),
    # 表、裳中的同一衣底保留实际宋体部件笔势，纵向恢复独立片形比例。
    'e-clothes-spread': reshape('表', '衣底向右展开的变形，取表下部', crop=[0, 37.5, 64, 64], y_scale=1.55),
    'e-clothes-tight': reshape('裳', '衣底竖提与撇捺收紧的变形，取裳下部', select=[2], crop=[0, 44, 64, 64], x_scale=.88, y_scale=1.65),
    'e-pig-narrow': reshape('豕', '豕去顶横的右窄变形', crop=[0, 14.5, 64, 64], x_scale=.66),
    'e-three-left': fragment('彡', '三撇'),
}

key = {
    'key': 'E', 'zone': 'left', 'name': '月', 'short': '有',
    'roots': [
        ['月', '@e-month-narrow', '丹', '用'],
        ['爫', '乃', '豕', '@e-pig-no-top'],
        ['@e-clothes', '@e-clothes-spread', '@e-clothes-tight', '@e-pig-narrow'],
    ],
    'stroke': 'e-three-left',
}
write_key('E', key, glyphs)
