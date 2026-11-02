"""Recorta as falas dos projetos dados encaixando cada corte no meio do silêncio mais próximo (até 0,45 s)."""
import json, re, subprocess, sys
from pathlib import Path
L = Path(__file__).resolve().parent
log = (L / 'dividir.log').read_text(encoding='utf-8', errors='replace')
blocos = {b.split('/')[0][:2]: b for b in re.split(r'^=== ', log, flags=re.M)[1:]}
for n in sys.argv[1:]:
    p = next(L.glob(f'{n}-*'))
    take = L / '_vozes' / f'E{n}-todas.mp3'
    ms = re.findall(r'fala-(\d+)\.mp3: ([\d.]+)-([\d.]+)s', blocos[n])
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(take), '-af', 'silencedetect=noise=-30dB:d=0.06', '-f', 'null', '-'], capture_output=True, text=True).stderr
    ini = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', r)]
    fim = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', r)]
    sil = [((a + b) / 2, b - a) for a, b in zip(ini, fim)]
    cortes = []
    for (a, b0, b1), (c, d0, d1) in zip(ms, ms[1:]):
        alvo = (float(b1) + float(d0)) / 2
        cand = [s for s in sil if abs(s[0] - alvo) <= 0.45]
        cortes.append(min(cand, key=lambda s: abs(s[0] - alvo) - s[1] * 0.5)[0] if cand else alvo)
    dur = float(ms[-1][2]) + 0.3
    pts = [0.0] + cortes + [dur]
    for k, (a, b) in enumerate(zip(pts, pts[1:]), 1):
        tmp = L / '_tmp.mp3'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a:.3f}', '-to', f'{b:.3f}', '-i', str(take), '-codec:a', 'libmp3lame', '-b:a', '192k', str(tmp)], check=True)
        subprocess.run([sys.executable, str(L / 'aparar_linha.py'), str(tmp), str(p / 'falas' / f'fala-{k:02d}.mp3')], check=True, capture_output=True)
    r = subprocess.run([sys.executable, str(Path.home() / '.claude/skills/lulublox-videos/scripts/alinhar_falas.py'), 'roteiro.json', 'falas'], cwd=p, capture_output=True, text=True, encoding='utf-8', errors='replace')
    print(n, [round(c, 2) for c in cortes], ' | '.join(l[:60] for l in r.stdout.splitlines() if l[:2].isdigit() or 'ATENCAO' in l)[:400])
