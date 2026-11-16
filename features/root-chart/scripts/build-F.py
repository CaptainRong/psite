import sys
sys.path.insert(0, '.qa')
from font_source import fragment, write_key
from key_b_preview import preview_circle

glyphs={
    'f-leather-bottom':fragment('革','革去廿后的下部，口框、下横与穿竖',crop=[0,26,64,64]),
    'f-rain-top':fragment('雪','雨字头，去下框的扁形',select=[1,2,3,4,5]),
    'f-inch-no-dot':fragment('寸','寸去内点',select=[0]),
    'f-two-horizontal':fragment('二','二横'),
}
key={
    'key':'F','zone':'horizontal','name':'土','short':'地',
    'roots':[['土','士','干','@f-leather-bottom'],['十','雨','@f-rain-top','寸'],['@f-inch-no-dot']],
    'stroke':'f-two-horizontal',
}
write_key('F',key,glyphs)
preview_circle('F',glyphs[key['stroke']])
