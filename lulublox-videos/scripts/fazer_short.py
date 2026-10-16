"""Produces the English Short and only finishes with the final MP4.

  1. generates the scene (gerar_cena.py) and runs the audits in Roblox Studio (collisions + camera, both total 0);
  2. records only the Studio window (no audit), re-recording if the capture drops frames, and processes it to cena.mp4;
  3. builds the edit (montar_edicao.py), reviews the captions (total 0) and renders to final-en/;
  4. copies the final MP4 to the project root.
At the end it checks the final MP4 and publicacao.txt; anything missing -> exits with an error saying what.
The project needs gerar_cena.py and montar_edicao.py (see modelos/base) and falas/fala-XX.mp3 (ElevenLabs,
Lulu's voice). --so-conferir: only the final check (records nothing). Every Short is in English.
"""
import argparse, json, re, shutil, subprocess, sys, time
from pathlib import Path

AQUI = Path(__file__).resolve().parent
EDITOR = AQUI.parent.parent / 'roblox-video-editor' / 'scripts'
QUADROS_MIN_POR_S = 40  # captura abaixo disso (GPU ocupada) e regravada


def rodar(cmd, cwd, **kw):
    print('>', ' '.join(str(c) for c in cmd), flush=True)
    return subprocess.run([str(c) for c in cmd], cwd=cwd, text=True, encoding='utf-8', errors='replace', **kw)


def auditar(proj, suf):
    rodar([sys.executable, AQUI / 'studio_runscript.py', 'montar', '--kit', '--cenario', 'studio/cenario.lua',
           '--cena', f'studio/cena{suf}.lua', '--play', '--saida', f'studio/pipeline{suf}.lua'], proj, check=True,
          capture_output=True)
    r = rodar([sys.executable, AQUI / 'studio_runscript.py', 'rodar', f'studio/pipeline{suf}.lua', '--place', 'studio/base.rbxlx'],
              proj, capture_output=True, timeout=600)
    linhas = [l for l in r.stdout.splitlines() if l.startswith(('[auditoria]', '[camera]'))]
    print('\n'.join(linhas[-12:]))
    totais = [int(m.group(1)) for l in linhas for m in [re.search(r'total (\d+)', l)] if m]
    if len(totais) < 2:
        return None  # o Studio nao devolveu a saida: auditoria nao confirmada
    return sum(totais) == 0


def gravar(proj, idioma, suf):
    tempos = json.loads((proj / f'tempos{suf}.json').read_text(encoding='utf-8'))
    rodar([sys.executable, 'gerar_cena.py', '--idioma', idioma, '--sem-auditoria'], proj, check=True, capture_output=True)
    rodar([sys.executable, AQUI / 'studio_runscript.py', 'montar', '--kit', '--cenario', 'studio/cenario.lua',
           '--cena', f'studio/cena{suf}.lua', '--play', '--saida', f'studio/pipeline{suf}.lua'], proj, check=True,
          capture_output=True)
    minimo = QUADROS_MIN_POR_S * tempos['fim']
    video, meta = proj / 'studio' / f'viewport{suf}.mp4', proj / 'studio' / f'viewport{suf}.json'
    for tentativa in range(1, 5):
        inicio = time.time()
        rodar([sys.executable, AQUI / 'studio_runscript.py', 'rodar', f'studio/pipeline{suf}.lua', '--place', 'studio/base.rbxlx',
               '--gravar', f'studio/viewport{suf}.mp4', '--frente'], proj, capture_output=True, timeout=600)
        info = json.loads(meta.read_text(encoding='utf-8')) if meta.exists() and meta.stat().st_mtime >= inicio else {}
        # Sem o flash de sincronia (Play que nao comecou) o gravador nao escreve nada e o viewport da gravacao
        # anterior continua no disco: isso e falha, nunca uma captura valida.
        if not info.get('escritos') or not info.get('regiao') or not video.exists() or video.stat().st_mtime < inicio:
            print(f'{idioma}: tentativa {tentativa} falhou (o Play nao comecou ou nao apareceu o flash de sincronia)')
            continue
        n = info['recebidos']
        print(f'{idioma}: tentativa {tentativa}, {n} quadros (minimo {minimo:.0f})')
        if n >= minimo:
            break
    else:
        raise SystemExit(f'{idioma}: nenhuma captura valida em 4 tentativas (Play sem flash ou abaixo de {minimo:.0f} quadros)')
    sys.path.insert(0, str(AQUI))
    import captura_janela
    captura_janela.processar(str(proj / 'studio' / f'viewport{suf}.mp4'), str(proj / f'cena{suf}.mp4'), 0.8, tempos['fim'])
    # Valida a duracao do video processado antes de editar (gravacao truncada).
    from media_utils import probe
    try:
        dur_real = float(probe(proj / f'cena{suf}.mp4')['duration'])
    except Exception:
        dur_real = 0
    if dur_real < tempos['fim'] * 0.7:
        raise SystemExit(f'{idioma}: cena{suf}.mp4 tem {dur_real:.1f}s mas deveria ter ~{tempos["fim"]:.1f}s (gravação truncada?)')
    print(f'{idioma}: cena{suf}.mp4 validado ({dur_real:.1f}s)')
    rodar([sys.executable, 'gerar_cena.py', '--idioma', idioma], proj, check=True, capture_output=True)  # volta a cena com auditoria


def editar(proj, idioma, suf):
    rodar([sys.executable, 'montar_edicao.py', '--idioma', idioma], proj, check=True)
    tl = f'timeline-edicao{suf}.json'
    r = rodar([sys.executable, EDITOR / 'revisar_legendas.py', tl], proj, capture_output=True)
    print(r.stdout.strip())
    if r.returncode:
        raise SystemExit(f'{idioma}: legendas com problema (acima); corrija e rode de novo')
    saida = proj / f'final-{idioma}'
    if saida.exists():
        shutil.rmtree(saida)
    rodar([sys.executable, EDITOR / 'renderizar.py', tl, '--out', saida.name], proj, check=True)
    nome = json.loads((proj / tl).read_text(encoding='utf-8'))['outputs'][0]['name']
    shutil.copy2(saida / nome, proj / nome.upper().replace('.MP4', '.mp4'))


def conferir(proj, roteiro, idiomas):
    faltando = []
    for idioma in idiomas:
        suf = '' if idioma == 'en' else f'-{idioma}'
        nome = roteiro.get('arquivo' if idioma == 'en' else f'arquivo_{idioma}')
        if not nome or not (proj / f'final-{idioma}' / nome).exists():
            faltando.append(f'{idioma}: MP4 final ({nome or "arquivo" + suf + " no roteiro"})')
        if not (proj / f'publicacao{suf}.txt').exists():
            faltando.append(f'{idioma}: publicacao{suf}.txt')
    return faltando


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('projeto', type=Path)
    ap.add_argument('--idiomas', nargs='+')
    ap.add_argument('--so-conferir', action='store_true')
    ap.add_argument('--sem-confirmar-auditoria', action='store_true',
                    help='grava mesmo se o Studio nao devolver a saida da auditoria (revise os quadros a mao)')
    a = ap.parse_args()
    proj = a.projeto.resolve()
    roteiro = json.loads((proj / 'roteiro.json').read_text(encoding='utf-8'))
    idiomas = a.idiomas or ['en']
    if not a.so_conferir:
        for idioma in idiomas:
            suf = '' if idioma == 'en' else f'-{idioma}'
            pasta = proj / f'falas{suf}'
            if not list(pasta.glob('fala-*.mp3')):
                raise SystemExit(f'{idioma}: missing voice lines in {pasta.name}/ (ElevenLabs, Lulu voice, language {idioma})')
            if not (pasta / 'falas.json').exists():
                rodar([sys.executable, AQUI / 'alinhar_falas.py', '--idioma', idioma, 'roteiro.json', pasta.name], proj, check=True)
            rodar([sys.executable, 'gerar_cena.py', '--idioma', idioma], proj, check=True)
            lint = subprocess.run([sys.executable, str(Path(__file__).with_name('lint_cena.py')), str(proj)], capture_output=True,
                                  text=True, encoding='utf-8', errors='replace')
            print(lint.stdout.strip())
            if lint.returncode:
                raise SystemExit(f'{idioma}: lint_cena.py found errors (above); see references/first-time-right.md')
            # Auditoria zerada antes de gravar (regra da skill). Problema encontrado sempre bloqueia;
            # saida do Studio nao capturada bloqueia, a menos que --sem-confirmar-auditoria (o usuario pediu).
            audit_ok = auditar(proj, suf)
            if audit_ok is False:
                raise SystemExit(f'{idioma}: auditoria da cena nao zerou (acima); corrija gerar_cena.py/cenario e rode de novo')
            if audit_ok is None:
                if not a.sem_confirmar_auditoria:
                    raise SystemExit(f'{idioma}: o Studio nao devolveu a saida da auditoria; rode de novo '
                                     '(ou --sem-confirmar-auditoria, revisando os quadros a mao)')
                print(f'[aviso] {idioma}: auditoria nao confirmada; revise os quadros da gravacao a mao')
            gravar(proj, idioma, suf)
            editar(proj, idioma, suf)
    faltando = conferir(proj, roteiro, idiomas)
    if faltando:
        print('ENTREGA INCOMPLETA:\n  ' + '\n  '.join(faltando))
        sys.exit(1)
    print('Entrega completa:', ', '.join(idiomas))


if __name__ == '__main__':
    main()
