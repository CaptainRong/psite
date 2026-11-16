import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from font_source import fragment, inspect, write_key, contours, bounds


def shape(label, polygons):
    x0, y0, x1, y1 = bounds(polygons)
    scale = 54 / max(x1-x0, y1-y0)
    cx, cy = (x0+x1)/2, (y0+y1)/2
    parts = []
    for polygon in polygons:
        parts.append('M'+' '.join(
            f'{32+(x-cx)*scale:.2f},{32+(y-cy)*scale:.2f}'
            for x, y in polygon
        )+'Z')
    return {'label': label, 'paths': [''.join(parts)], 'filled': True}


inspect('廾艹廿龷匸比七弋', 'inspect-A.png')
# 保持宋体七的笔画轮廓，将其竖弯一段改成斜折，形成参考图的横折变体。
folded_seven = [[(x-.43*max(0, y-20), y) for x, y in polygon]
                for polygon in contours('七')]
glyphs = {
    'a-box-separated': fragment('匸', '上横分离的右框变形',
                                 erase=[[0, 17, 25, 37]]),
    'a-seven-short': fragment('比', '七的短竖提变形', select=[0]),
    'a-seven-folded': shape('七的横折形变形', folded_seven),
    'a-seven-curved': fragment('弋', '七的弯钩变形，弋去点', select=[0]),
}
key = {
    'key': 'A', 'zone': 'horizontal', 'name': '工', 'short': '工',
    'roots': [
        ['工', '戈', '弋', '匚'],
        ['廾', '艹', '廿', '龷'],
        ['@a-box-separated', '七', '@a-seven-short', '@a-seven-folded'],
        ['@a-seven-curved'],
    ],
}
write_key('A', key, glyphs)
