"""English comic stickers for Lulublox (same style as the roblox-video-editor overlays, which are in Portuguese).

Writes wow-en.png, oops-en.png and haha-en.png (512x512, transparent) to the roblox-video-editor overlays folder and a
copy to this skill's assets/stickers/. Use them with ed.sticker('wow-en', ...), never 'wow'/'oops'/'kkkk' (UAU, OPS, KKKK).

    python criar_stickers_en.py
"""
import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SKILLS = Path.home() / '.claude' / 'skills'
OV = SKILLS / 'roblox-video-editor' / 'assets' / 'overlays'
FONTE = SKILLS / 'roblox-video-editor' / 'assets' / 'fontes' / 'LilitaOne-Regular.ttf'
COPIA = Path(__file__).resolve().parent.parent / 'assets' / 'stickers'
ESCURO = (32, 30, 34, 255)


def estrela(draw, cx, cy, r_ext, r_int, pontas, cor, giro=0.0, contorno=10):
    pts = []
    for i in range(pontas * 2):
        r = r_ext if i % 2 == 0 else r_int
        r *= 1 + 0.08 * math.sin(i * 2.3)  # uneven spikes, like hand drawn
        a = giro + i * math.pi / pontas
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=ESCURO)
    # inner polygon a bit smaller = the dark outline
    inner = [(cx + (x - cx) * (1 - contorno / r_ext), cy + (y - cy) * (1 - contorno / r_ext)) for x, y in pts]
    draw.polygon(inner, fill=cor)


def texto(img, msg, tam, cor, contorno, angulo):
    camada = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)
    fonte = ImageFont.truetype(str(FONTE), tam)
    caixa = d.textbbox((0, 0), msg, font=fonte, stroke_width=contorno)
    w, h = caixa[2] - caixa[0], caixa[3] - caixa[1]
    x, y = (img.size[0] - w) / 2 - caixa[0], (img.size[1] - h) / 2 - caixa[1]
    d.text((x + 6, y + 8), msg, font=fonte, fill=ESCURO, stroke_width=contorno, stroke_fill=ESCURO)  # drop shadow
    d.text((x, y), msg, font=fonte, fill=cor, stroke_width=contorno, stroke_fill=ESCURO)
    camada = camada.rotate(angulo, resample=Image.BICUBIC, center=(img.size[0] / 2, img.size[1] / 2))
    img.alpha_composite(camada)


def main():
    COPIA.mkdir(parents=True, exist_ok=True)
    feitos = []
    for nome, msg, cor_estrela, tam, ang in (('wow-en', 'WOW!', (30, 185, 90, 255), 150, 6),
                                              ('oops-en', 'OOPS!', (255, 80, 165, 255), 132, 5)):
        img = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
        estrela(ImageDraw.Draw(img), 256, 256, 250, 150, 13, cor_estrela, giro=0.2)
        texto(img, msg, tam, (255, 255, 255, 255), 9, ang)
        feitos.append((nome, img))
    img = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
    texto(img, 'HAHA!', 150, (255, 228, 60, 255), 11, 8)
    feitos.append(('haha-en', img))
    for nome, img in feitos:
        img.save(OV / f'{nome}.png')
        shutil.copy2(OV / f'{nome}.png', COPIA / f'{nome}.png')
        print(OV / f'{nome}.png')


if __name__ == '__main__':
    main()
