"""Static checks of a Lulu project BEFORE opening Studio: the mistakes that made the 2026-10-23 batch re-record
13 of 16 videos, caught in a second instead of after a full record + review.

    python lint_cena.py PROJECT [PROJECT ...]

Reads studio/cenario_corpo.lua, gerar_cena.py, montar_edicao.py and (when present) tempos.json + falas/falas.json.
ERRO = will break or look wrong for sure (fix before the audit); aviso = look at it on purpose (keep it only if the
shot was planned that way, see references/first-time-right.md). Exit code 1 when there is any ERRO."""
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HELPERS = ('peca', 'bola', 'cilindro', 'elipse', 'texto', 'modelo', 'fechar', 'mover', 'animar', 'soldar', 'soltar')


def numeros(txt):
    return [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', txt)]


def tamanho_da_linha(linha):
    """First V(a, b, c) of a peca/elipse line (its Size)."""
    m = re.search(r'V\(([^()]*)\)', linha)
    if not m:
        return None
    n = numeros(m.group(1))
    return n if len(n) == 3 else None


def checar(proj):
    erros, avisos = [], []
    cen = (proj / 'studio' / 'cenario_corpo.lua')
    gen = proj / 'gerar_cena.py'
    edi = proj / 'montar_edicao.py'
    textos = {p.name: p.read_text(encoding='utf-8') for p in (cen, gen, edi) if p.exists()}
    tudo = '\n'.join(textos.values())

    # every model gets a PrimaryPart (soldar/soltar/PivotTo crash without it and the scene stops before its first camera)
    for nome, txt in textos.items():
        for m in re.finditer(r'local\s+(\w+)\s*=\s*modelo\(', txt):
            var = m.group(1)
            if not re.search(r'fechar\(\s*' + re.escape(var) + r'\s*,', txt):
                erros.append(f'{nome}: model "{var}" is never closed with fechar({var}, primary) (no PrimaryPart)')
        for h in HELPERS:
            if re.search(r'local\s+' + h + r'\s*=\s*' + h + r'\(', txt):
                erros.append(f'{nome}: "local {h} = {h}(...)" hides the helper {h}() for the rest of the file')

    # follow cameras end with the next cut, never with a duration (the scene clock can run behind os.clock)
    for m in re.finditer(r'cam\.seguir\(([^()]*(?:\([^()]*\)[^()]*)*)\)', tudo):
        partes = [p.strip() for p in re.split(r',(?![^()]*\))', m.group(1))]
        if len(partes) >= 3 and partes[2] not in ('99', 'math.huge'):
            erros.append(f'cam.seguir with duration "{partes[2]}": use 99 and end it with the next cut')

    # a weld must happen in the same frame as the prop's last move
    linhas = tudo.splitlines()
    for i, l in enumerate(linhas):
        if re.search(r'\bmover\(\s*(\w+)', l):
            obj = re.search(r'\bmover\(\s*(\w+)', l).group(1)
            for l2 in linhas[i + 1:i + 3]:
                if 'task.delay' in l2 and re.search(r'soldar\(\s*' + re.escape(obj) + r'\b', l2):
                    erros.append(f'"{obj}": mover() then soldar() in a task.delay — weld inside the animar callback '
                                 '(if k >= 1 then soldar(...) end), or the last move drags her body')

    # materials and light that already ruined shots
    for nome, txt in textos.items():
        for n, l in enumerate(txt.splitlines(), 1):
            cor = re.search(r'C\((\d+),\s*(\d+),\s*(\d+)\)', l)
            claro = cor and min(int(x) for x in cor.groups()) >= 200
            if 'Enum.Material.Fabric' in l and claro and l.lstrip().startswith(('peca(', 'local', 'elipse(')):
                t = tamanho_da_linha(l)
                if t and max(t) >= 1.5:
                    avisos.append(f'{nome}:{n}: light Fabric on a {max(t):.1f}-stud part renders as gray knit (use SmoothPlastic for white cloth)')
            if 'Enum.Material.Neon' in l:
                t = tamanho_da_linha(l)
                if t:
                    a, b = sorted(t)[-2:]
                    if a * b >= 9:
                        avisos.append(f'{nome}:{n}: Neon on a {a:.1f}x{b:.1f} surface washes the image out (keep Neon to small accents)')
            if re.search(r'\.Material\s*=\s*Enum\.Material\.Neon', l) and 'Luz' not in l:
                avisos.append(f'{nome}:{n}: switching a part to Neon at runtime: check it is not big or close to the camera')
            for m in re.finditer(r'Brightness\s*=\s*([\d.]+)', l):
                if float(m.group(1)) > 1.5:
                    avisos.append(f'{nome}:{n}: light Brightness {m.group(1)} (> 1.5 overexposes faces; 0.8-1.3 indoors)')
            m = re.search(r'l\.Color,\s*l\.Range,\s*l\.Brightness[^=]*=\s*[^,]+\([^)]*\)\s*,\s*[\d.]+\s*,\s*([\d.]+)', l)
            if m and float(m.group(1)) > 1.5:
                avisos.append(f'{nome}:{n}: light Brightness {m.group(1)} (> 1.5 overexposes faces; 0.8-1.3 indoors)')
            if re.search(r'K\.anim\(noob,\s*"rir"', l):
                avisos.append(f'{nome}:{n}: "rir" throws her head back (de costas in close-ups); use pulo() + happy face')
            if re.search(r'"segurarFrente(Junto)?"', l):
                avisos.append(f'{nome}:{n}: segurarFrente brings her hands up to chin level in medium shots; '
                              'hold props low: { LeftShoulder = { 35, -15 }, RightShoulder = { 35, -15 }, LeftElbow = { 75, 0 }, RightElbow = { 75, 0 } }')

    # timeline: lines never overlap, and not too many cuts
    tj, fj = proj / 'tempos.json', proj / 'falas' / 'falas.json'
    if tj.exists() and fj.exists():
        T = json.loads(tj.read_text(encoding='utf-8'))
        F = {f['id']: f for f in json.loads(fj.read_text(encoding='utf-8'))}
        ini = T['falas']
        ids = sorted(ini, key=lambda i: ini[i])
        for a, b in zip(ids, ids[1:]):
            fim_a = ini[a] + F[a]['palavras'][-1]['end']
            if ini[b] < fim_a + 0.15:
                erros.append(f'line {b} starts at {ini[b]:.2f}s but line {a} only ends at {fim_a:.2f}s (overlap)')
        ultimo = ids[-1]
        if T['fim'] < ini[ultimo] + F[ultimo]['palavras'][-1]['end'] + 0.9:
            erros.append(f'the video ends {T["fim"]:.2f}s, too close to the last word (no room for the ending)')
        if len(T.get('cortes', [])) > 3:
            avisos.append(f'{len(T["cortes"])} cuts: the user asked for few, soft cuts (travel or follow the camera instead)')

    # first shot: Lulu is about 4.5 studs wide in idle (arms out); more than ~2.0 studs off the camera target she is cut at
    # the frame edge even when her face passes the audit (02 gift boxes, 2026-10-17)
    corpo = proj / 'studio' / 'cenario_corpo.lua'
    gc = proj / 'gerar_cena.py'
    if corpo.exists() and gc.exists():
        mg = re.search(r'criarGarota\([^,]+,\s*K\.emPe\(V\(\s*([-\d.]+)\s*,\s*[-\d.]+\s*,\s*([-\d.]+)', corpo.read_text(encoding='utf-8'))
        mc = re.search(r'cam\.corte\(V\(([-\d.]+),\s*([-\d.]+),\s*([-\d.]+)\),\s*V\(([-\d.]+),', gc.read_text(encoding='utf-8'))
        if mg and mc:
            lx, lz = float(mg.group(1)), float(mg.group(2))
            dist = ((float(mc.group(1)) - lx) ** 2 + (float(mc.group(3)) - lz) ** 2) ** 0.5
            limite = 0.49 * dist - 2.25          # half the frame width at her depth (FOV 52) minus half her width
            dx = abs(lx - float(mc.group(4)))
            if dx > limite:
                avisos.append(f'first shot: Lulu stands {dx:.1f} studs from the camera target x (limit {limite:.1f} at '
                              f'{dist:.1f} studs) - her arm/body gets cut at the frame edge; move the camera or the props')
    return erros, avisos


def main():
    total = 0
    for nome in sys.argv[1:]:
        proj = Path(nome).resolve()
        erros, avisos = checar(proj)
        for e in erros:
            print(f'[lint] {proj.name}: ERRO {e}')
        for a in avisos:
            print(f'[lint] {proj.name}: aviso {a}')
        print(f'[lint] {proj.name}: {len(erros)} erro(s), {len(avisos)} aviso(s)')
        total += len(erros)
    sys.exit(1 if total else 0)


if __name__ == '__main__':
    main()
