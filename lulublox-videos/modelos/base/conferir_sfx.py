"""Lists sound effects that play over a spoken word (the voice must stay clear).
    python conferir_sfx.py NN-projeto [NN-projeto ...]
Reads timeline-edicao.json and falas/falas.json; quiet beds (gain <= -20 dB, e.g. rain) are ignored."""
import json, sys
from pathlib import Path

LOTE = Path(__file__).resolve().parent
LIB = Path.home() / '.claude' / 'skills' / 'roblox-video-editor' / 'assets' / 'biblioteca-audio'
dur = {a['path']: float(a['duration_seconds']) for a in json.loads((LIB / 'catalogo.json').read_text(encoding='utf-8'))['assets']}

for nome in sys.argv[1:]:
    proj = LOTE / nome
    spec = json.loads((proj / 'timeline-edicao.json').read_text(encoding='utf-8'))['outputs'][0]
    falas = {f['arquivo']: f for f in json.loads((proj / 'falas' / 'falas.json').read_text(encoding='utf-8'))}
    palavras = []
    for v in spec['voice']:
        f = falas[Path(v['file']).name]
        palavras += [(v['at'] + p['start'], v['at'] + p['end'], p['w']) for p in f['palavras']]
    n = 0
    for s in spec['sfx']:
        if s['gain_db'] <= -20:
            continue
        d = s.get('duration') or dur.get(s['file'], 0) / s.get('pitch', 1)
        a, b = s['at'], s['at'] + d
        em = [w for (i, f, w) in palavras if i < b - 0.05 and f > a + 0.05]
        if em:
            n += 1
            print(f'[sfx] {nome}: {Path(s["file"]).name} {a:.2f}-{b:.2f}s ({s["gain_db"]} dB) over: {" ".join(em)}')
    print(f'[sfx] {nome}: {n} effect(s) over the voice')
