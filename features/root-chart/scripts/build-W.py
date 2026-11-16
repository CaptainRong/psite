import sys
sys.path.insert(0, '.qa')
from font_source import contours, bounds, write_key

# 祭的前三条轮廓为上部左右两块，第三条为右块内白。
# 示的两横及下面三笔均不包含。左右各挪 1.5/64 字面，保持结构留空。
source = contours('祭')
polygons = []
for index in [0, 1, 2]:
    shift = -1.5 if index == 0 else 1.5
    polygons.append([(x + shift, y) for x, y in source[index]])
x0, y0, x1, y1 = bounds(polygons)
scale = 54 / max(x1 - x0, y1 - y0)
center_x, center_y = (x0 + x1) / 2, (y0 + y1) / 2
parts = []
for polygon in polygons:
    points = [(32 + (x - center_x) * scale, 32 + (y - center_y) * scale) for x, y in polygon]
    parts.append('M' + ' '.join(f'{x:.2f},{y:.2f}' for x, y in points) + 'Z')

glyphs = {
    'w-festival': {
        'label': '祭字头，去示，左右分开',
        'paths': [''.join(parts)],
        'filled': True,
    }
}
key = {
    'key': 'W',
    'zone': 'left',
    'name': '人',
    'short': '人',
    'roots': [['人', '亻', '八', '癶'], ['@w-festival']],
}
write_key('W', key, glyphs)
