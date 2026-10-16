"""Lulublox batch: original English Shorts starring Lulu, YouTube SEO and posting twice a day (09:00 and 18:00).

  python lote.py novo [--data YYYY-MM-DD]          creates entregas/lulu-YYYYMMDD with 2 empty projects
  python lote.py historico                        script log + premises found in entregas/ (originality check)
  python lote.py produzir LOTE [--so N ...]        runs fazer_short.py on each project and logs the script
  python lote.py registrar LOTE                   logs the produced scripts in the skill registry
  python lote.py metadados LOTE                   publicacao.json / publicacao.txt validated for YouTube
  python lote.py painel LOTE                      revisao.html: the videos with title, description, tags and time
  python lote.py agenda LOTE [--inicio YYYY-MM-DD] [--agora]
                                                  agenda.json: 09:00 and 18:00 of the same day (first day with both
                                                  slots still ahead); --agora = publish now (test runs the user asks for)
  python lote.py marcar LOTE N STATUS [--link URL] records the Studio result
  python lote.py status LOTE                      summary: produced, metadata, posted
Settings in config.json (overridden by config.local.json).
"""
import argparse, datetime as dt, html, json, re, shutil, subprocess, sys
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

AQUI = Path(__file__).resolve().parent
SKILL = AQUI.parent
SKILLS = SKILL.parent
ANIMADOR = SKILL  # the producer scripts live in this same skill
REGISTRO = ANIMADOR / 'historico' / 'roteiros.md'


def config():
    c = json.loads((SKILL / 'config.json').read_text(encoding='utf-8'))
    local = SKILL / 'config.local.json'
    if local.exists():
        extra = json.loads(local.read_text(encoding='utf-8'))
        for k, v in extra.items():
            if isinstance(v, dict) and isinstance(c.get(k), dict):
                c[k] = {**c[k], **v}
            else:
                c[k] = v
    return c


def caminho(p):
    return Path(p).expanduser()


def ler(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))


def gravar(p, dados):
    Path(p).write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding='utf-8')


def projetos(lote):
    return sorted(p for p in Path(lote).iterdir() if p.is_dir() and re.match(r'^\d\d-', p.name))


# ---------------------------------------------------------------- novo / historico / registrar

def cmd_novo(a):
    c = config()
    data = a.data or dt.date.today().isoformat()
    lote = caminho(c['pasta_entregas']) / f'lulu-{data.replace("-", "")}'
    if lote.exists():
        raise SystemExit(f'{lote} already exists')
    lote.mkdir(parents=True)
    for i in range(1, c['videos_por_lote'] + 1):
        p = lote / f'{i:02d}-to-define'
        (p / 'studio').mkdir(parents=True)
        (p / 'falas').mkdir()
        shutil.copy2(ANIMADOR / 'assets' / 'base.rbxlx', p / 'studio' / 'base.rbxlx')
    # Shared scene and edit base (timeline from the real lines, Luau helpers, set, captions and effects).
    for f in (SKILL / 'modelos' / 'base').glob('*.*'):
        shutil.copy2(f, lote / f.name)
    gravar(lote / 'lote.json', {'criado': data, 'videos': c['videos_por_lote'], 'status': {}})
    print(lote)
    print('Rename each NN-to-define folder to NN-<topic> when you write its script.')


def cmd_historico(a):
    c = config()
    if REGISTRO.exists():
        print(REGISTRO.read_text(encoding='utf-8'))
    registrados = REGISTRO.read_text(encoding='utf-8') if REGISTRO.exists() else ''
    extras = []
    for base in c['pastas_historico']:
        base = caminho(base)
        if not base.exists():
            continue
        for r in sorted(base.rglob('roteiro.json')):
            if f'<!-- {r.parent.name} -->' in registrados:
                continue
            try:
                rot = ler(r)
            except Exception:
                continue
            orig = r.parent / 'originalidade.json'
            premissa = ler(orig).get('premissa') if orig.exists() else None
            falas = ' / '.join(f.get('texto', '') for f in rot.get('falas', [])[:4])
            extras.append(f'- {r.parent.relative_to(base.parent)}: {rot.get("titulo", "?")}\n'
                          f'  premise: {premissa or "(no originalidade.json)"}\n  lines: {falas[:220]}')
    if extras:
        print(f'\n{len(extras)} scripts in entregas/ not in the log yet (in production or dropped):\n' + '\n'.join(extras))
    print('\nSkill models (infrastructure only, never the story):',
          ', '.join(p.name for p in (ANIMADOR / 'modelos').iterdir() if p.is_dir()))


def registrar(projs):
    projs = [p for p in projs if (p / 'roteiro.json').exists()]
    if projs:
        subprocess.run([sys.executable, ANIMADOR / 'scripts' / 'registrar_roteiro.py', *map(str, projs)], check=False)


def cmd_registrar(a):
    lote = Path(a.lote).resolve()
    registrar([p for p in projetos(lote) if _video_pronto(p)])


# ---------------------------------------------------------------- produzir

def cmd_produzir(a):
    lote = Path(a.lote).resolve()
    estado = ler(lote / 'lote.json')
    fs = ANIMADOR / 'scripts' / 'fazer_short.py'
    for p in projetos(lote):
        n = p.name[:2]
        if a.so and n not in a.so:
            continue
        faltam = [f for f in ('roteiro.json', 'originalidade.json', 'gerar_cena.py', 'montar_edicao.py', 'studio/cenario.lua')
                  if not (p / f).exists()]
        if faltam:
            print(f'[{n}] skipped: missing {", ".join(faltam)}')
            estado['status'][n] = {'producao': 'incompleto', 'faltam': faltam}
            continue
        if _video_pronto(p) and not a.refazer:
            print(f'[{n}] already done')
            estado['status'][n] = {'producao': 'pronto'}
            registrar([p])
            continue
        print(f'[{n}] producing {p.name} ...', flush=True)
        with open(p / 'producao.log', 'w', encoding='utf-8') as log:
            subprocess.run([sys.executable, fs, str(p)], stdout=log, stderr=subprocess.STDOUT)
        fim = (p / 'producao.log').read_text(encoding='utf-8', errors='replace').strip().splitlines()[-1:]
        # O fazer_short termina conferindo publicacao.txt, que o 'metadados' escreve depois: vale o MP4 final.
        estado['status'][n] = {'producao': 'pronto' if _video_pronto(p) else 'erro', 'ultima_linha': fim[0] if fim else ''}
        print(f'[{n}] {estado["status"][n]["producao"]}: {estado["status"][n]["ultima_linha"]}')
        if _video_pronto(p):
            registrar([p])  # roteiro anotado no registro da skill: nenhum vídeo futuro repete a ideia
        gravar(lote / 'lote.json', estado)
    gravar(lote / 'lote.json', estado)


def _video_pronto(p):
    rot = ler(p / 'roteiro.json')
    return bool(rot.get('arquivo')) and (p / 'final-en' / rot['arquivo']).exists()


# ---------------------------------------------------------------- metadados

def _creditos(p):
    arq = sorted((p / 'final-en').glob('*-creditos.txt'))
    if not arq:
        return ''
    texto = arq[0].read_text(encoding='utf-8').strip()
    # The renderer writes the credits in Portuguese: the channel is all in English.
    for pt, en in (('Fonte:', 'Source:'), ('Licenca:', 'License:'), ('Licença:', 'License:')):
        texto = texto.replace(pt, en)
    # Whatever wording the renderer used for the changes line, the English line is fixed.
    texto = re.sub(r'(?m)^Altera(?:c|ç)(?:oe|õe)s:.*$', 'Changes: excerpts, cuts, fades, volume and sync with the video.', texto)
    return texto


def _tags_validas(tags):
    """YouTube: soma dos caracteres das tags <= 500 (tag com espaço conta 2 a mais), sem < >."""
    saida, total = [], 0
    for t in dict.fromkeys(t.strip().lstrip('#') for t in tags if t.strip()):
        t = re.sub(r'[<>]', '', t)
        custo = len(t) + (2 if ' ' in t else 0) + 1
        if total + custo > 480:
            break
        saida.append(t)
        total += custo
    return saida


def cmd_metadados(a):
    c = config()
    lote = Path(a.lote).resolve()
    problemas = []
    for p in projetos(lote):
        rot = ler(p / 'roteiro.json')
        arquivo = rot.get('arquivo')
        video = p / 'final-en' / arquivo if arquivo else None
        titulo = (rot.get('titulo_youtube') or rot.get('titulo') or '').strip()
        if '#shorts' not in titulo.lower():
            titulo = f'{titulo} #shorts #roblox'
        descricao = (rot.get('descricao') or '').strip()
        hashtags = rot.get('hashtags') or []
        creditos = _creditos(p)
        corpo = '\n\n'.join(x for x in [descricao, ' '.join(h if h.startswith('#') else '#' + h for h in hashtags),
                                        'Music:\n' + creditos if creditos else '', 'Voice: ElevenLabs ("Jessica" voice).'] if x)
        tags = _tags_validas(rot.get('tags') or [])
        meta = {'video': str(video) if video else None, 'titulo': titulo, 'descricao': corpo, 'tags': tags,
                'feito_para_criancas': c['feito_para_criancas'], 'categoria': c['categoria'],
                'idioma': c['canal']['idioma_video']}
        erros = []
        if not video or not video.exists():
            erros.append('final MP4 not found')
        if len(titulo) > 100:
            erros.append(f'title has {len(titulo)} characters (max 100)')
        if 'roblox' not in titulo.lower():
            erros.append('title without "ROBLOX" (main keyword)')
        if not descricao:
            erros.append('no description in the script')
        if len(corpo) > 5000:
            erros.append('description over 5000 characters')
        if re.search(r'[<>]', titulo + corpo):
            erros.append('title/description with < or > (YouTube rejects them)')
        if len(tags) < 12:
            erros.append(f'only {len(tags)} tags (use 15-20: broad Roblox/kids + topic)')
        if not creditos:
            erros.append('music credits not found (render in final-en/)')
        meta['erros'] = erros
        gravar(p / 'publicacao.json', meta)
        texto = f'TITLE:\n{titulo}\n\nDESCRIPTION:\n{corpo}\n\nTAGS:\n{", ".join(tags)}\n'
        (p / 'publicacao.txt').write_text(texto, encoding='utf-8')
        problemas += [f'{p.name}: {e}' for e in erros]
    print('\n'.join(problemas) if problemas else f'metadata OK ({len(projetos(lote))} publicacao.json files)')
    sys.exit(1 if problemas else 0)


# ---------------------------------------------------------------- painel de revisão

def cmd_painel(a):
    lote = Path(a.lote).resolve()
    agenda = ler(lote / 'agenda.json') if (lote / 'agenda.json').exists() else None
    quando = {it['n']: it['quando'] for it in agenda['itens']} if agenda else {}
    cards = []
    for p in projetos(lote):
        mp = p / 'publicacao.json'
        if not mp.exists():
            continue
        m = ler(mp)
        rel = Path(m['video']).relative_to(lote).as_posix() if m.get('video') else ''
        q = quando.get(p.name[:2], '')
        erros = ''.join(f'<li>{html.escape(e)}</li>' for e in m.get('erros', []))
        cards.append(f'''<article><video src="{html.escape(rel)}" controls preload="metadata"></video>
<div><p class="meta">{p.name}{' · ' + html.escape(q) if q else ''}</p>
<h2>{html.escape(m['titulo'])}</h2><pre>{html.escape(m['descricao'])}</pre>
<p class="tags">{html.escape(', '.join(m['tags']))}</p>{f'<ul class="erro">{erros}</ul>' if erros else ''}</div></article>''')
    pagina = f'''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Lulublox batch review</title><style>
:root{{--bg:#f7f5ff;--card:#fff;--tx:#1d1b2e;--mut:#6b6880;--err:#c62828}}
@media (prefers-color-scheme:dark){{:root{{--bg:#15131f;--card:#211e30;--tx:#eeeaff;--mut:#a29fbb;--err:#ff8a80}}}}
body{{background:var(--bg);color:var(--tx);font:15px system-ui,sans-serif;margin:0;padding:16px}}
h1{{font-size:20px}} article{{display:flex;gap:16px;background:var(--card);border-radius:12px;padding:12px;margin:0 0 14px}}
video{{width:200px;aspect-ratio:9/16;border-radius:8px;background:#000;flex:none}} h2{{font-size:16px;margin:4px 0}}
pre{{white-space:pre-wrap;font:13px system-ui;margin:6px 0}} .meta,.tags{{color:var(--mut);font-size:13px}} .erro{{color:var(--err)}}
@media (max-width:600px){{article{{flex-direction:column}} video{{width:100%}}}}</style>
<h1>Batch {html.escape(lote.name)}: {len(cards)} videos</h1>
<p>Two videos a day, at 09:00 and 18:00. The channel owner adds the thumbnails.</p>{''.join(cards)}'''
    (lote / 'revisao.html').write_text(pagina, encoding='utf-8')
    print(lote / 'revisao.html')


# ---------------------------------------------------------------- agenda

def cmd_agenda(a):
    c = config()
    lote = Path(a.lote).resolve()
    try:
        fuso = ZoneInfo(c['fuso'])
    except ZoneInfoNotFoundError:  # Windows sem o pacote tzdata: Brasília não tem horário de verão desde 2019
        if c['fuso'] != 'America/Sao_Paulo':
            raise SystemExit('install the time zone data: pip install tzdata')
        fuso = dt.timezone(dt.timedelta(hours=-3), 'BRT')
    agora = dt.datetime.now(fuso)
    ps = projetos(lote)
    if a.agora:
        # Test run the user asked to see right away: every video goes public now.
        slots = [agora] * len(ps)
    else:
        # Every day has all the slots of config['horarios'] (09:00 and 18:00): the pair goes out on the same day,
        # so the first day used is the first one whose earliest slot is still at least 30 min ahead.
        primeiro = min(c['horarios'])
        hh, mm = map(int, primeiro.split(':'))
        inicio = dt.date.fromisoformat(a.inicio) if a.inicio else agora.date()
        while dt.datetime(inicio.year, inicio.month, inicio.day, hh, mm, tzinfo=fuso) < agora + dt.timedelta(minutes=30):
            inicio += dt.timedelta(days=1)
        slots, d = [], 0
        while len(slots) < len(ps):
            dia = inicio + dt.timedelta(days=d)
            for h in sorted(c['horarios']):
                hh, mm = map(int, h.split(':'))
                if len(slots) < len(ps):
                    slots.append(dt.datetime(dia.year, dia.month, dia.day, hh, mm, tzinfo=fuso))
            d += 1
    itens = []
    for p, quando in zip(ps, slots):
        m = ler(p / 'publicacao.json')
        if m.get('erros'):
            raise SystemExit(f'{p.name}: metadata errors ({"; ".join(m["erros"])}); run metadados again')
        itens.append({'n': p.name[:2], 'projeto': p.name, 'quando': quando.strftime('%Y-%m-%d %H:%M'),
                      'data_studio': quando.strftime('%d/%m/%Y'), 'hora_studio': quando.strftime('%H:%M'),
                      'publish_at': 'now' if a.agora else quando.isoformat(), 'video': m['video'], 'titulo': m['titulo'],
                      'descricao': m['descricao'], 'tags': m['tags'], 'status': 'pendente', 'link': None})
    canal = c['canal']
    agenda = {'fuso': c['fuso'], 'gerado': agora.isoformat(timespec='minutes'),
              'canal': f'{canal["nome"]} ({canal["handle"]})', 'feito_para_criancas': c['feito_para_criancas'],
              'categoria': c['categoria'], 'idioma': canal['idioma_video'], 'itens': itens}
    gravar(lote / 'agenda.json', agenda)
    print(f'Channel {agenda["canal"]}: {"made for kids" if c["feito_para_criancas"] else "not made for kids"}, '
          f'{c["categoria"]}, {canal["idioma_video"]}')
    for it in itens:
        print(f'  {it["quando"]}  {it["projeto"]}  {it["titulo"]}')


def cmd_marcar(a):
    lote = Path(a.lote).resolve()
    agenda = ler(lote / 'agenda.json')
    for it in agenda['itens']:
        if it['n'] == a.n.zfill(2):
            it['status'] = a.status
            if a.link:
                it['link'] = a.link
            gravar(lote / 'agenda.json', agenda)
            print(f'{it["n"]}: {a.status} {a.link or ""}')
            return
    raise SystemExit('video not found in the agenda')


def cmd_status(a):
    lote = Path(a.lote).resolve()
    agenda = ler(lote / 'agenda.json') if (lote / 'agenda.json').exists() else {'itens': []}
    st = {it['n']: it for it in agenda['itens']}
    for p in projetos(lote):
        rot = ler(p / 'roteiro.json') if (p / 'roteiro.json').exists() else {}
        pronto = bool(rot.get('arquivo')) and (p / 'final-en' / rot['arquivo']).exists()
        meta = (p / 'publicacao.json').exists()
        ag = st.get(p.name[:2])
        print(f'{p.name.ljust(32)} {"video" if pronto else "-----"} {"meta" if meta else "----"} '
              f'{(ag["status"] + " " + ag["quando"] + (" " + ag["link"] if ag.get("link") else "")) if ag else ""}')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    s = sub.add_parser('novo'); s.add_argument('--data')
    sub.add_parser('historico')
    s = sub.add_parser('produzir'); s.add_argument('lote'); s.add_argument('--so', nargs='+'); s.add_argument('--refazer', action='store_true')
    s = sub.add_parser('registrar'); s.add_argument('lote')
    s = sub.add_parser('metadados'); s.add_argument('lote')
    s = sub.add_parser('painel'); s.add_argument('lote')
    s = sub.add_parser('agenda'); s.add_argument('lote'); s.add_argument('--inicio'); s.add_argument('--agora', action='store_true')
    s = sub.add_parser('marcar'); s.add_argument('lote'); s.add_argument('n')
    s.add_argument('status', choices=['agendado', 'publicado', 'erro', 'pendente']); s.add_argument('--link')
    s = sub.add_parser('status'); s.add_argument('lote')
    a = ap.parse_args()
    globals()['cmd_' + a.cmd](a)


if __name__ == '__main__':
    main()
