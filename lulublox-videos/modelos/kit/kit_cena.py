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
-- ---- camera em movimento (dono, 2026-11-07: "parece 2D com varias cameras"): todo corte novo para a anterior
camAnim = nil
function pararCam()
	if camAnim then camAnim:Disconnect() camAnim = nil end
end
local function suave(k) return 0.5 - math.cos(k * math.pi) / 2 end
-- arco em volta de 'centro' (Vector3 ou funcao que devolve Vector3): angulo a0 -> a1 (graus; 0 = de frente, do lado -Z;
-- positivo vai para +X), raio r0 -> r1, altura h0 -> h1 acima do centro, olhando para centro + V(0, alvoY, 0)
local function quadroOrbita(centro, r0, r1, h0, h1, a0, a1, fov, alvoY, e)
	local c0 = type(centro) == "function" and centro() or centro
	local a = math.rad(a0 + (a1 - a0) * e)
	local r = r0 + (r1 - r0) * e
	cam.corte(c0 + V(math.sin(a) * r, h0 + (h1 - h0) * e, -math.cos(a) * r), c0 + V(0, alvoY or 0, 0), fov)
end
function orbita(centro, r0, r1, h0, h1, a0, a1, t, fov, alvoY)
	pararCam()
	quadroOrbita(centro, r0, r1, h0, h1, a0, a1, fov, alvoY, 0)
	local t0 = os.clock()
	camAnim = game:GetService("RunService").RenderStepped:Connect(function()
		local k = math.clamp((os.clock() - t0) / t, 0, 1)
		quadroOrbita(centro, r0, r1, h0, h1, a0, a1, fov, alvoY, suave(k))
		if k >= 1 then pararCam() end
	end)
end
-- travelling reto de (p0, a0) para (p1, a1) com fov f0 -> f1 (posicoes Vector3)
function travel(p0, a0, p1, a1, t, f0, f1)
	pararCam()
	cam.corte(p0, a0, f0)
	local t0 = os.clock()
	camAnim = game:GetService("RunService").RenderStepped:Connect(function()
		local k = math.clamp((os.clock() - t0) / t, 0, 1)
		local e = suave(k)
		cam.corte(p0:Lerp(p1, e), a0:Lerp(a1, e), f0 + ((f1 or f0) - f0) * e)
		if k >= 1 then pararCam() end
	end)
end
-- camera na mao: balanco leve continuo ate o proximo corte
function mao(p, a, fov, amp)
	pararCam()
	cam.corte(p, a, fov)
	local t0 = os.clock()
	camAnim = game:GetService("RunService").RenderStepped:Connect(function()
		local k = os.clock() - t0
		local d = V(math.noise(k * 1.3, 1.7), math.noise(k * 1.1, 2.3), 0) * (amp or 0.12)
		cam.corte(p + d, a + d * 0.4, fov)
	end)
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


# ---- camera variety (user, 2026-11-06): change the shot about every 2 s, like "Lulu vs the storm" (1.47M views):
# wide shot with the joke object -> face close-up on the reaction -> another angle on the action -> punch zoom on the
# payoff. Every helper registers the cut, so the edit knows where it is.
def close(c, t, lado=0.0, dist=4.4, fov=36, altura=0.32, extra=''):
    """Cut to a face close-up (cam.rosto puts the face in the upper third)."""
    c.corte(t)
    c.E(t, f'pararCam()\nK.inserto(false)\nK.foco(noob.Head)\ncam.rosto(noob, {dist}, {fov}, {{altura = {altura}, lado = {lado}}}){extra}')


def plano(c, t, cam, alvo, fov=50, extra=''):
    """Cut to another fixed angle cam -> alvo (both (x, y, z))."""
    c.corte(t)
    c.E(t, f'pararCam()\nK.inserto(false)\nK.foco(noob.Head)\ncam.corte(V({cam[0]}, {cam[1]}, {cam[2]}), V({alvo[0]}, {alvo[1]}, {alvo[2]}), {fov}){extra}')


def ins(c, t, cam, alvo, fov=46, extra=''):
    """Insert shot on an object (her face may be out of frame: the camera audit is off until the next close/plano)."""
    c.corte(t)
    c.E(t, f'pararCam()\nK.inserto(true)\nK.foco(nil)\ncam.corte(V({cam[0]}, {cam[1]}, {cam[2]}), V({alvo[0]}, {alvo[1]}, {alvo[2]}), {fov}){extra}')


def soco(c, t, k=0.14):
    """Punch zoom in the camera itself (fast FOV squeeze and back)."""
    c.E(t, f'cam.soco({k}, 0.3)')


def _v(x):
    """(x, y, z) -> 'V(x, y, z)'; a string passes as Lua (e.g. 'P("Caixa").Position')."""
    return x if isinstance(x, str) else f'V({x[0]}, {x[1]}, {x[2]})'


def _modo(inserto):
    return f'K.inserto({str(inserto).lower()})\nK.foco({"nil" if inserto else "noob.Head"})\n'


# ---- camera em 3D (dono, 2026-11-07): fewer cuts, and each shot MOVES. Shots of 2-4 s; a cut lands on an action or a
# new beat, not on every line. Mix: trav (dolly in/out, crane, truck), orb (arc around her or the object), mao_
# (handheld drift on a held shot), closev (close-up that pushes in). inserto=True turns the face audit off (object
# shots, over-the-shoulder shots with her back to the camera).
def trav(c, t, p0, a0, p1, a1, dur, f0=50, f1=None, inserto=False, extra=''):
    """Cut, then a straight camera move p0/a0 -> p1/a1 in dur seconds."""
    c.corte(t)
    c.E(t, _modo(inserto) + f'travel({_v(p0)}, {_v(a0)}, {_v(p1)}, {_v(a1)}, {dur}, {f0}, {f1 or f0}){extra}')


def orb(c, t, centro, r0, r1, h0, h1, a0, a1, dur, fov=50, alvo_y=0, inserto=False, extra=''):
    """Cut, then an arc around centro ((x, y, z) or a Lua expression/function): angle a0 -> a1 degrees (0 = from the
    front, -Z side; positive goes toward +X = screen-left), radius r0 -> r1, height h0 -> h1 above centro."""
    c.corte(t)
    c.E(t, _modo(inserto) + f'orbita({_v(centro)}, {r0}, {r1}, {h0}, {h1}, {a0}, {a1}, {dur}, {fov}, {alvo_y}){extra}')


def mao_(c, t, cam, alvo, fov=50, amp=0.12, inserto=False, extra=''):
    """Cut to a held shot with a light handheld drift until the next cut."""
    c.corte(t)
    c.E(t, _modo(inserto) + f'mao({_v(cam)}, {_v(alvo)}, {fov}, {amp}){extra}')


def closev(c, t, dist0=5.6, dist1=4.0, dur=1.6, fov=36, lado=0.0, altura=0.32, extra=''):
    """Face close-up that pushes in (cam.rosto at dist0, then a move to dist1)."""
    c.corte(t)
    c.E(t, f'pararCam()\nK.inserto(false)\nK.foco(noob.Head)\ncam.rosto(noob, {dist0}, {fov}, {{altura = {altura}, lado = {lado}}})\n'
           f'cam.rosto(noob, {dist1}, {fov}, {{altura = {altura}, lado = {lado}, t = {dur}}}){extra}')


def zooms_auto(ed, intensidade=0.07, soco=0.1):
    """Edit-side motion on every line: a slow push-in on even lines and a punch on odd ones, always clipped to the
    shot (never across a camera cut, which edicao.conferir refuses)."""
    cortes = sorted(ed.T.get('cortes', []))
    ids = sorted(ed.ini, key=lambda i: ed.ini[i])
    for k, i in enumerate(ids):
        a = ed.ini[i] + 0.02
        b = min(ed.fim_fala(i) + 0.3, ed.fim - 0.05)
        prox = next((x for x in cortes if x > a + 0.01), ed.fim)
        if any(a < x < a + 0.35 for x in cortes):
            continue
        b = min(b, prox - 0.06)
        if k % 2 == 0 and b - a >= 0.8:
            ed.zoom(a, round(b - a, 2), intensidade)
        elif b - a >= 0.35:
            ed.punch(a, soco, 0.3)


def fecha_ed(ed, n, confete=True, sucesso=True, zooms=False):
    fimf, ini = ed.fim_fala, ed.ini
    ult = sorted(ini, key=lambda i: ini[i])[-1]
    S = ed.sfx_livre
    S('ding', fimf(ult) + 0.04, gain=-15, pitch=1.2)
    if sucesso:
        S('sucesso', fimf(ult) + 0.5, gain=-11)
    if confete:
        for x in (0.0, 0.62):
            ed.sticker('confete', fimf(ult) + 0.05, ed.fim - fimf(ult) - 0.15, x, 0.1, 0.38)
    if zooms:
        zooms_auto(ed)
    ed.musica(MUSICAS[n % len(MUSICAS)] + '-short.mp3', -24)
    ed.legendas()
    ed.escrever()
