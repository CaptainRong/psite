from font_source import ROOT
import json
import math
import sys
from pathlib import Path
import pymupdf

base=ROOT
for letter in 'QEANHDL':
    data=json.loads((base/f'key-{letter}.json').read_text(encoding='utf8'))
    glyphs=list(data['glyphs'].items())
    width,height=720,math.ceil(len(glyphs)/4)*200
    pieces=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',f'<rect width="{width}" height="{height}" fill="#080a09"/>']
    for index,(name,definition) in enumerate(glyphs):
        x,y=(index%4)*180,(index//4)*200
        pieces.append(f'<g transform="translate({x+10},{y+10}) scale(2.5)">')
        pieces.extend(f'<path fill="#f0f0e6" d="{path}"/>' for path in definition['paths'])
        pieces.append('</g>')
        pieces.append(f'<text x="{x+5}" y="{y+190}" fill="#91bd77" font-size="13">{name}</text>')
    pieces.append('</svg>')
    doc=pymupdf.open(stream=''.join(pieces).encode(),filetype='svg')
    doc[0].get_pixmap().save(base/f'actual-{letter}.png')
