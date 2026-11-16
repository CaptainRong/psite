import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from font_source import fragment, write_key

glyphs={
    'p-show-no-dot':fragment('礻','礻去末点，点、横撇、竖',select=[0,1]),
}
key={
    'key':'P','zone':'dot','name':'之','short':'这',
    'roots':[['之','辶','廴','冖'],['宀','@p-show-no-dot']],
}
write_key('P',key,glyphs)
