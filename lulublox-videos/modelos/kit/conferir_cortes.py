"""Confere se cada corte das falas caiu num silêncio do take. Sem argumento: lista os suspeitos."""
import re, subprocess
from pathlib import Path
L = Path(__file__).resolve().parent
log = (L / 'dividir.log').read_text(encoding='utf-8', errors='replace')
ruins = {}
for bloco in re.split(r'^=== ', log, flags=re.M)[1:]:
    nome = bloco.split('/')[0]
    n = nome[:2]
    ms = re.findall(r'fala-(\d+)\.mp3: ([\d.]+)-([\d.]+)s', bloco)
    if not ms:
        ruins[nome] = 'sem cortes'
        continue
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(L / '_vozes' / f'E{n}-todas.mp3'), '-af', 'silencedetect=noise=-30dB:d=0.06', '-f', 'null', '-'], capture_output=True, text=True).stderr
    ini = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', r)]
    fim = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', r)]
    sil = list(zip(ini, fim))
    maus = []
    for (a, b0, b1), (c, d0, d1) in zip(ms, ms[1:]):
        b1, d0 = float(b1), float(d0)
        ok = any(s - 0.04 <= b1 and d0 <= e + 0.04 for s, e in sil)
        if not ok:
            maus.append((a, round(b1, 2)))
    if maus:
        ruins[nome] = (maus, [(round(s, 2), round(e, 2)) for s, e in sil])
for k, v in ruins.items():
    print(k, v)
print(len(ruins), 'suspeitos')
