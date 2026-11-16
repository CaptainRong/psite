import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from font_source import fragment, write_key
from preview_circle import add_circle

glyphs={'k-chuan':fragment('川','川，左笔为撇，中竖较短')}
key={'key':'K','zone':'vertical','name':'口','short':'中',
     'roots':[['口']], 'stroke':'k-chuan'}
write_key('K',key,glyphs)
add_circle('K',key,glyphs)
