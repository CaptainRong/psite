from font_source import ROOT
from pathlib import Path
import re
from PIL import Image, ImageDraw, ImageChops


def preview_circle(letter, glyph):
    path = ROOT / f'key-{letter}.png'
    image = Image.open(path).convert('RGB')
    cx,cy = image.width//2,image.height-60
    size = 66
    ImageDraw.Draw(image).ellipse((cx-42,cy-42,cx+42,cy+42),outline='#bb6e65',width=2)
    mask = Image.new('1',image.size)
    for data in glyph['paths']:
        for part in re.findall(r'M([^M]+)',data):
            values = [float(v) for v in re.findall(r'-?\d+(?:\.\d+)?',part)]
            points = [(cx+(values[i]-32)*size/64,cy+(values[i+1]-32)*size/64) for i in range(0,len(values),2)]
            contour = Image.new('1',image.size)
            ImageDraw.Draw(contour).polygon(points,fill=1)
            mask=ImageChops.logical_xor(mask,contour)
    image.paste('#f0f0e6',(0,0),mask)
    image.save(path)
