import sys
sys.path.insert(0, '.qa')
from font_source import fragment, write_key
from key_b_preview import preview_circle


glyphs={
    't-grain-narrow':fragment('和','禾去末捺的窄形，末笔为短点',select=[0]),
    't-person-top':fragment('乞','𠂉，撇与短横',select=[0]),
    't-bamboo-top':fragment('笑','竹字头',select=[0,2]),
    't-left-stroke':fragment('丿','一撇'),
}
key={
    'key':'T','zone':'left','name':'禾','short':'和',
    'roots':[['禾','@t-grain-narrow','@t-person-top','竹'],['@t-bamboo-top','攵','夂','彳']],
    'stroke':'t-left-stroke',
}
write_key('T',key,glyphs)
preview_circle('T',glyphs[key['stroke']])
