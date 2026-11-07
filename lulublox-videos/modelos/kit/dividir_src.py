"""Grava os arquivos de cada projeto a partir de _src/*.txt. Cada vídeo no arquivo:
    @@@ NN
    #### doc      (tabela de beats, vira o docstring do gerar_cena.py)
    #### corpo    (studio/cenario_corpo.lua)
    #### cena     (corpo do gerar_cena.py; c, ini, E, fimf, seq, abre, fecha já disponíveis)
    #### edicao   (corpo do montar_edicao.py; ed, T, ini, fimf, S disponíveis; fecha_ed é automático)
python dividir_src.py [arquivos]; imprime os projetos gravados. Sempre refaz o cenario_comum.lua (base + kit)."""
import re
import sys
from pathlib import Path

L = Path(__file__).resolve().parent
kit = (L / 'kit_lulu.lua').read_text(encoding='utf-8')
base = (Path.home() / '.claude' / 'skills' / 'lulublox-videos' / 'modelos' / 'base' / 'cenario_comum.lua').read_text(encoding='utf-8')
(L / 'cenario_comum.lua').write_text(base.rstrip() + '\n' + kit, encoding='utf-8')

CENA = '''"""{num} {doc}
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from comum import Cena
from kit_cena import seq, abre, fecha, close, plano, ins, soco, trav, orb, mao_, closev

c = Cena(__file__)
d, ini, E, fimf = c.d, c.ini, c.E, c.fim_fala
{cena}
'''
EDI = '''"""{num} (timeline-edicao.json)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from edicao import Edicao
from kit_cena import fecha_ed

ed = Edicao(__file__)
T, ini = ed.T, ed.ini
fimf = ed.fim_fala
S = ed.sfx_livre
{edicao}
fecha_ed(ed, {n})
'''
arqs = [Path(a) for a in sys.argv[1:]] or sorted((L / '_src').glob('*.txt'))
feitos = []
for a in arqs:
    txt = a.read_text(encoding='utf-8')
    for bloco in re.split(r'^@@@ ', txt, flags=re.M)[1:]:
        num, resto = bloco.split('\n', 1)
        num = num.strip()
        partes = dict(re.findall(r'^#### (\w+)\n(.*?)(?=^#### |\Z)', resto, flags=re.M | re.S))
        p = next(L.glob(f'{num}-*'))
        (p / 'studio' / 'cenario_corpo.lua').write_text(partes['corpo'].rstrip() + '\n', encoding='utf-8')
        (p / 'gerar_cena.py').write_text(CENA.format(num=num, doc=partes.get('doc', '').strip().replace('"""', "'''"), cena=partes['cena'].rstrip()), encoding='utf-8')
        (p / 'montar_edicao.py').write_text(EDI.format(num=num, edicao=partes['edicao'].rstrip(), n=int(num)), encoding='utf-8')
        feitos.append(p.name)
print(' '.join(feitos))
