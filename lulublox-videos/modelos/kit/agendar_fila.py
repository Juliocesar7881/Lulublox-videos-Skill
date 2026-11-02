"""Metadados + agenda.json do lote: projeto NN = NN-ésima vaga livre: 11/12 a 13/12 às 11:45/20:00, 14/12 a 01/01/2027 às 09:00/11:45/18:00/20:00. Preserva status/link.
Vaga que já passou (ou a menos de 40 min) sem vídeo agendado: é listada e o relatório precisa contar."""
import datetime as dt, json, subprocess, sys
from pathlib import Path
L = Path(__file__).resolve().parent
S = Path.home() / '.claude/skills/lulublox-videos/scripts/lote.py'
subprocess.run([sys.executable, str(S), 'metadados', str(L)], capture_output=True, text=True, encoding='utf-8', errors='replace')
fuso = dt.timezone(dt.timedelta(hours=-3))
ps = sorted(p for p in L.iterdir() if p.is_dir() and p.name[:2].isdigit())
old = {}
ag = L / 'agenda.json'
if ag.exists():
    old = {i['n']: i for i in json.loads(ag.read_text(encoding='utf-8'))['itens']}
slots, d0 = [], dt.date(2026, 12, 11)
for k in range(22):
    dia = d0 + dt.timedelta(days=k)
    horas = ((11, 45), (20, 0)) if k < 3 else ((9, 0), (11, 45), (18, 0), (20, 0))
    for hh, mm in horas:
        slots.append(dt.datetime(dia.year, dia.month, dia.day, hh, mm, tzinfo=fuso))
assert len(slots) == 82 == len(ps)
itens = []
for p, q in zip(ps, slots):
    m = json.loads((p / 'publicacao.json').read_text(encoding='utf-8'))
    n = p.name[:2]
    o = old.get(n, {})
    itens.append({'n': n, 'projeto': p.name, 'quando': q.strftime('%Y-%m-%d %H:%M'), 'data_studio': q.strftime('%d/%m/%Y'), 'hora_studio': q.strftime('%H:%M'),
                  'publish_at': q.isoformat(), 'video': m['video'], 'titulo': m['titulo'], 'descricao': m['descricao'], 'tags': m['tags'],
                  'feito_para_criancas': False, 'status': o.get('status', 'pendente'), 'link': o.get('link')})
agora = dt.datetime.now(fuso)
ag.write_text(json.dumps({'fuso': 'America/Sao_Paulo', 'gerado': agora.isoformat(timespec='minutes'), 'canal': 'LuluBlox YT (@lulu_bloxxof)',
                          'feito_para_criancas': False, 'categoria': 'Gaming', 'idioma': 'English', 'itens': itens}, ensure_ascii=False, indent=1), encoding='utf-8')
print(sum(1 for i in itens if i['status'] == 'agendado'), 'agendados')
