import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from font_source import fragment, write_key

glyphs={'c-jing-head':fragment('泾','泾右上部，横撇与捺',select=[0])}
key={'key':'C','zone':'fold','name':'又','short':'以',
     'roots':[['又','@c-jing-head','龴','厶'],['巴','马']]}
write_key('C',key,glyphs)
