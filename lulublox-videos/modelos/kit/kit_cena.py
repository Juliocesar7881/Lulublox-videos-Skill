"""Atalhos das cenas e edições (usados pelos gerar_cena.py e montar_edicao.py gerados de _src/)."""

MUSICAS = ['quirky-dog', 'carefree', 'sneaky-snitch', 'merry-go', 'life-of-riley', 'hyperfun', 'the-show-must-be-go',
           'move-forward', 'itty-bitty-8-bit', 'happy-happy-game-show', 'funkorama', 'bit-quest', 'wallpaper',
           'sneaky-adventure', 'marty-gots-a-plan', 'happy-boy-theme', 'fluffing-a-duck', 'batty-mcfaddin', 'sunshine',
           'pixelland', 'on-my-way', 'jaunty-gumption', 'investigations', 'happy-alley', 'the-cannery', 'the-builder',
           'motivator', 'monkeys-spinning-monkeys', 'maccary-bay', 'fretless', 'comic-hero', 'amazing-plan',
           'getting-it-done']

KIT = r'''
-- poses e ajudantes do lote
cen = W("Cenario")
function P(n) return cen:WaitForChild(n) end
function some(o) porPivo(o, CF(0, -150, 0)) end
function brilha(pos, cor, n) estouro(pos, cor or C(255, 240, 150), n or 14, 0.35, 5) end
function naCabeca(o, d)
	d = d or V(0, 0.8, 0.1)
	return game:GetService("RunService").Heartbeat:Connect(function() porPivo(o, CF(noob.Head.Position + d)) end)
end
APONTA = { RightShoulder = { 85, 60 }, RightElbow = { 5, 0 } }
ALCANCA = { RightShoulder = { 95, 70 }, RightElbow = { 5, 0 } }
ALTO = { RightShoulder = { 140, 45 }, RightElbow = { 5, 0 } }
LADO = { RightShoulder = { 10, 95 }, RightElbow = { 0, 0 } }
SEGURA = { LeftShoulder = { 35, -15 }, RightShoulder = { 35, -15 }, LeftElbow = { 75, 0 }, RightElbow = { 75, 0 } }
DOIS_LADOS = { LeftShoulder = { 10, 95 }, RightShoulder = { 10, 95 } }
DOIS_ALTO = { LeftShoulder = { 150, 30 }, RightShoulder = { 150, 30 }, LeftElbow = { 5, 0 }, RightElbow = { 5, 0 } }
function acenarBraco(t)
	for i = 0, math.floor(t / 0.3) do
		task.delay(i * 0.3, function() K.bracos(noob, { RightShoulder = { 160, i % 2 == 0 and 20 or 50 } }, 0.25) end)
	end
	task.delay(t + 0.3, function() K.bracos(noob, nil, 0.3) end)
end
-- pulinhos de um modelo no lugar (n saltos em t segundos)
function quicar(m, n, t, h)
	local base = m:GetPivot()
	return animar(t, function(k)
		m:PivotTo(base * CF(0, math.abs(math.sin(k * math.pi * n)) * (h or 0.3), 0))
		if k >= 1 then m:PivotTo(base) end
	end, Enum.EasingStyle.Linear)
end
-- caminha até 'para' (CFrame) com balanço
function trotar(m, para, t, h)
	local de = m:GetPivot()
	return animar(t, function(k, e)
		m:PivotTo(de:Lerp(para, e) * CF(0, math.abs(math.sin(k * math.pi * math.max(2, t * 5))) * (h or 0.15), 0))
		if k >= 1 then m:PivotTo(para) end
	end, Enum.EasingStyle.Sine, Enum.EasingDirection.InOut)
end
-- aparece crescendo do nada num ponto
function brotar(m, cf, esc, t)
	m:ScaleTo(0.02)
	m:PivotTo(cf)
	return escalar(m, esc or 1, t or 0.35)
end
-- treme um modelo ou peça
function sacudir(obj, t, amp)
	local base = pivo(obj)
	return animar(t, function(k)
		porPivo(obj, base * CF(math.sin(k * 70) * (amp or 0.08), 0, math.cos(k * 55) * (amp or 0.08) * 0.5))
		if k >= 1 then porPivo(obj, base) end
	end, Enum.EasingStyle.Linear)
end
'''


def seq(c, gaps, inicio=0.35):
    """Marca o início das falas em ordem: gaps[i] = pausa entre o fim da fala i e o início da seguinte."""
    ids = [f['id'] for f in c.falas]
    c.ini[ids[0]] = inicio
    for a, b, g in zip(ids, ids[1:], list(gaps) + [0.45] * len(ids)):
        c.ini[b] = c.fim_fala(a) + g
    return ids


def abre(c, cam, alvo, fov=52, rosto='happy', extra=''):
    """Primeiro quadro: Lulu na pose inicial e câmera cortada em cam -> alvo."""
    c.E(0, f'\t\traiz.CFrame = inicio\n\t\tif preparar then preparar() end\n\t\tK.anim(noob, "idle", {{fade = 0}})\n'
           f'\t\tK.rosto(noob, "{rosto}", 0)\n\t\tK.olhar(noob, 0, 0, 0)\n'
           f'\t\tcam.corte(V({cam[0]}, {cam[1]}, {cam[2]}), V({alvo[0]}, {alvo[1]}, {alvo[2]}), {fov}){extra}')


def fecha(c, fim, lua='', tempos=None):
    c.E(fim - 0.8, '\t\tK.rosto(noob, "wink")')
    c.escrever(fim, KIT + lua, tempos)


def fecha_ed(ed, n, confete=True, sucesso=True):
    fimf, ini = ed.fim_fala, ed.ini
    ult = sorted(ini, key=lambda i: ini[i])[-1]
    S = ed.sfx_livre
    S('ding', fimf(ult) + 0.04, gain=-15, pitch=1.2)
    if sucesso:
        S('sucesso', fimf(ult) + 0.5, gain=-11)
    if confete:
        for x in (0.0, 0.62):
            ed.sticker('confete', fimf(ult) + 0.05, ed.fim - fimf(ult) - 0.15, x, 0.1, 0.38)
    ed.musica(MUSICAS[n % len(MUSICAS)] + '-short.mp3', -24)
    ed.legendas()
    ed.escrever()
