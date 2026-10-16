"""Audit run (no recording): gerar_cena.py, montar, rodar in a fresh Studio window; prints the audit lines.
    python auditar.py NN-projeto [NN-projeto ...]"""
import re, subprocess, sys
from pathlib import Path

LOTE = Path(__file__).resolve().parent
RS = Path.home() / '.claude' / 'skills' / 'lulublox-videos' / 'scripts' / 'studio_runscript.py'
PY = sys.executable

for nome in sys.argv[1:]:
    proj = LOTE / nome
    st = proj / 'studio'
    r = subprocess.run([PY, 'gerar_cena.py'], cwd=proj, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode:
        print(f'== {nome}: gerar_cena failed\n{r.stdout[-1500:]}{r.stderr[-1500:]}', flush=True)
        continue
    subprocess.run([PY, str(RS), 'montar', '--kit', '--cenario', str(st / 'cenario.lua'), '--cena', str(st / 'cena.lua'),
                    '--play', '--saida', str(st / 'pipeline.lua')], check=True, capture_output=True)
    r = subprocess.run([PY, str(RS), 'rodar', str(st / 'pipeline.lua'), '--place', str(st / 'base.rbxlx')],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    saida = r.stdout + r.stderr
    (proj / 'auditoria.log').write_text(saida, encoding='utf-8')
    linhas = [l for l in saida.splitlines()
              if re.search(r'\[auditoria\]|\[camera\]|error|Error|ERRO|stack|Script |infinite yield|cenario ok', l)]
    print(f'== {nome}', flush=True)
    for l in linhas[:60]:
        print('  ', l[:300], flush=True)
