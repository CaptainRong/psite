"""Local Song glyph inspection and fragment extraction for this revision."""
import json
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen
from PIL import Image, ImageDraw, ImageFont

FONT = TTFont(r"C:\Windows\Fonts\simsun.ttc", fontNumber=0)
GLYPHS = FONT.getGlyphSet()
CMAP = FONT.getBestCmap()
SCALE = 64 / FONT['head'].unitsPerEm
ROOT = Path(__file__).resolve().parent


class PolygonPen(BasePen):
    def __init__(self):
        super().__init__(GLYPHS)
        self.contours = []
        self.current = []

    def _moveTo(self, point):
        self.current = [point]

    def _lineTo(self, point):
        self.current.append(point)

    def _qCurveToOne(self, control, end):
        start = self.current[-1]
        for step in range(1, 13):
            t = step / 12
            self.current.append(tuple((1-t)**2*start[i] + 2*(1-t)*t*control[i] + t*t*end[i] for i in range(2)))

    def _curveToOne(self, c1, c2, end):
        start = self.current[-1]
        for step in range(1, 17):
            t = step / 16
            self.current.append(tuple((1-t)**3*start[i] + 3*(1-t)**2*t*c1[i] + 3*(1-t)*t*t*c2[i] + t**3*end[i] for i in range(2)))

    def _closePath(self):
        self.contours.append([(x*SCALE, 56-y*SCALE) for x, y in self.current])
        self.current = []

    def _endPath(self):
        self._closePath()


def contours(char):
    pen = PolygonPen()
    GLYPHS[CMAP[ord(char)]].draw(pen)
    return pen.contours


def bounds(polygons):
    points = [point for polygon in polygons for point in polygon]
    return [min(x for x, y in points), min(y for x, y in points), max(x for x, y in points), max(y for x, y in points)]


def clip_polygon(polygon, box):
    x0, y0, x1, y1 = box
    for axis, value, keep_greater in [(0,x0,True),(0,x1,False),(1,y0,True),(1,y1,False)]:
        clipped = []
        for index, current in enumerate(polygon):
            previous = polygon[index-1]
            current_in = current[axis] >= value if keep_greater else current[axis] <= value
            previous_in = previous[axis] >= value if keep_greater else previous[axis] <= value
            if current_in != previous_in:
                ratio = (value-previous[axis])/(current[axis]-previous[axis])
                clipped.append(tuple(previous[i]+ratio*(current[i]-previous[i]) for i in range(2)))
            if current_in:
                clipped.append(current)
        polygon = clipped
        if not polygon:
            break
    return polygon


def fragment(char, label, select=None, crop=None, erase=None):
    polygons = contours(char)
    if select is not None:
        polygons = [polygons[index] for index in select]
    if crop:
        polygons = [clip_polygon(polygon, crop) for polygon in polygons]
    if erase:
        for x0, y0, x1, y1 in erase:
            regions = [[-64,-64,x0,128],[x1,-64,128,128],[x0,-64,x1,y0],[x0,y1,x1,128]]
            polygons = [clip_polygon(polygon, region) for polygon in polygons for region in regions]
    polygons = [polygon for polygon in polygons if len(polygon)>2]
    x0,y0,x1,y1 = bounds(polygons)
    scale = 54/max(x1-x0,y1-y0)
    center_x,center_y = (x0+x1)/2,(y0+y1)/2
    parts = []
    for polygon in polygons:
        points = [(32+(x-center_x)*scale,32+(y-center_y)*scale) for x,y in polygon]
        parts.append('M'+' '.join(f'{x:.2f},{y:.2f}' for x,y in points)+'Z')
    return {'label':label,'paths':[''.join(parts)],'filled':True}


def inspect(chars, filename='font-inspect.png'):
    cell = 320
    image = Image.new('RGB',(cell*len(chars),cell+100),'#fff')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(r'C:\Windows\Fonts\simsun.ttc',24)
    for column,char in enumerate(chars):
        polygons=contours(char)
        for unit in range(0,65,8):
            draw.line((column*cell+unit*4+30,30,column*cell+unit*4+30,286),fill='#ddd')
            draw.line((column*cell+30,unit*4+30,column*cell+286,unit*4+30),fill='#ddd')
            draw.text((column*cell+unit*4+25,8),str(unit),fill='#555')
            draw.text((column*cell+5,unit*4+25),str(unit),fill='#555')
        for index,polygon in enumerate(polygons):
            points=[(column*cell+x*4+30,y*4+30) for x,y in polygon]
            draw.polygon(points,fill='#222' if index%2==0 else '#666',outline='#1465c0')
            x0,y0,x1,y1=bounds([polygon])
            draw.text((column*cell+(x0+x1)*2+24,(y0+y1)*2+24),str(index),fill='#ff3300',stroke_width=1,stroke_fill='#fff')
        draw.text((column*cell+40,330),char,fill='#000',font=font)
        draw.text((column*cell+40,366),str([(i,[round(v,1) for v in bounds([p])]) for i,p in enumerate(polygons)]),fill='#222')
    path=ROOT/filename
    image.save(path)
    return str(path)


def write_key(letter, key, glyphs):
    """Save an isolated proposal and a large, optically centred key preview."""
    from PIL import ImageChops
    import re
    output = {'key':key,'glyphs':glyphs}
    (ROOT/f'key-{letter}.json').write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf-8')
    size = 480
    image=Image.new('RGB',(size, max(520,len(key['roots'])*100+140)),'#080a09')
    draw=ImageDraw.Draw(image)
    for row,values in enumerate(key['roots']):
        for column,value in enumerate(values):
            em=90 if row==0 and column==0 else 66
            cx=65+column*112
            cy=70+row*100
            if value.startswith('@'):
                definition=glyphs[value[1:]]
                mask=Image.new('1',image.size)
                for path in definition['paths']:
                    path_mask=Image.new('1',image.size)
                    for part in re.findall(r'M([^M]+)',path):
                        numbers=[float(v) for v in re.findall(r'-?\d+(?:\.\d+)?',part)]
                        points=[(cx+(numbers[i]-32)*em/64,cy+(numbers[i+1]-32)*em/64) for i in range(0,len(numbers),2)]
                        area=sum(points[i-1][0]*point[1]-point[0]*points[i-1][1] for i,point in enumerate(points))
                        if abs(area)<.0001:
                            continue
                        polygon=Image.new('1',image.size)
                        ImageDraw.Draw(polygon).polygon(points,fill=1)
                        path_mask=ImageChops.logical_xor(path_mask,polygon)
                    mask=ImageChops.logical_or(mask,path_mask)
                image.paste('#f0f0e6',(0,0),mask)
            else:
                font=ImageFont.truetype(r'C:\Windows\Fonts\simsun.ttc',em)
                mask=Image.new('L',(em*3,em*3))
                ImageDraw.Draw(mask).text((em,em),value,font=font,fill=255)
                box=mask.getbbox()
                if box:
                    ink=mask.crop(box)
                    image.paste('#f0f0e6',(round(cx-ink.width/2),round(cy-ink.height/2)),ink)
    draw.text((30,image.height-90),letter,font=ImageFont.truetype(r'C:\Windows\Fonts\simsun.ttc',60),fill='#91bd77')
    image.save(ROOT/f'key-{letter}.png')


if __name__=='__main__':
    import sys
    print(inspect(sys.argv[1]))
