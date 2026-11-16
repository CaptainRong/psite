import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from font_source import fragment, write_key
from key_b_preview import preview_circle

glyphs={
    'g-qing-top':fragment('青','青字头，三横一竖，竖止于下横',select=[1]),
    'g-rising':{'label':'提笔','paths':['M9 42L16 50L55 15L53 14L14 39Z'],'filled':True},
    'g-horizontal':fragment('一','一横'),
}
key={
    'key':'G','zone':'horizontal','name':'王','short':'一',
    'roots':[['王','@g-qing-top','@g-rising','五'],['戋']],
    'stroke':'g-horizontal',
}
write_key('G',key,glyphs)
preview_circle('G',glyphs[key['stroke']])
