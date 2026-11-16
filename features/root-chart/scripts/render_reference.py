from pathlib import Path
import pymupdf

source = Path(__file__).resolve().parents[1] / 'docs/references/reference-book.pdf'
output = Path(__file__).resolve().parents[3] / '.qa/references'
output.mkdir(parents=True, exist_ok=True)
pdf = pymupdf.open(source)
for index in (28, 29):
    pdf[index].get_pixmap(matrix=pymupdf.Matrix(2, 2)).save(output / f'reference-page-{index+1}.png')
pdf[28].get_pixmap(matrix=pymupdf.Matrix(7, 7), clip=pymupdf.Rect(57, 360, 328, 449)).save(output / 'book-keyboard.png')
