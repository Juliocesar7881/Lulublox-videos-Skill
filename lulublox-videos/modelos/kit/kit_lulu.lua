-- ===================================================================== kit do lote lulu-20261102
-- Cenários prontos (o personagem fica em (-1.3, y, 0.4), câmera em z ~ -7.5) e bichos fofos com pivô no chão, de frente
-- para a câmera (-Z). Cada cenário devolve a altura do piso. Todo bicho nasce longe (y -200) e a cena o posiciona.
local MADEIRA, BRANCO = C(205, 150, 95), C(255, 255, 255)
local function fundoSala(corParede, corPiso, matPiso)
	gramado(200, C(110, 190, 90))
	K.piso(peca("Piso", V(40, 0.24, 24), CF(0, 0.12, 2), corPiso or C(210, 160, 110), matPiso or Enum.Material.WoodPlanks))
	peca("Parede", V(40, 16, 0.4), CF(0, 8, 6.2), corParede or C(255, 225, 200))
	peca("Rodape", V(40, 0.5, 0.1), CF(0, 0.5, 5.96), BRANCO, nil, nil, cen, false)
	-- faixa colorida e bandeirinhas no alto: a parte de cima do quadro não fica vazia
	local cores = { C(255, 90, 120), C(255, 200, 70), C(90, 190, 255), C(120, 220, 130), C(190, 130, 255) }
	peca("FaixaAlta", V(40, 3.6, 0.06), CF(0, 11.2, 5.97), (corParede or C(255, 225, 200)):Lerp(C(255, 255, 255), 0.45), nil, nil, cen, false)
	for i = -11, 11 do
		local x = i * 1.15
		local y = 10.1 - math.abs(math.sin((i % 5) / 5 * math.pi)) * 0.7
		peca("Bandeirinha", V(0.62, 0.62, 0.04), CF(x, y, 5.9) * ANG(0, 0, rad(45)), cores[i % 5 + 1], nil, nil, cen, false)
	end
	return 0.24
end
local function janela(x, y, z)
	peca("Ceu", V(3.2, 2.8, 0.05), CF(x, y, z), C(150, 215, 255), nil, nil, cen, false)
	bola("CopaFora", 2.0, V(x + 0.8, y - 0.9, z + 0.1), C(90, 190, 80), nil, cen, false)
	for _, f in ipairs({ { 0, 1.45, 3.5, 0.18 }, { 0, -1.45, 3.5, 0.18 }, { 1.7, 0, 0.18, 3 }, { -1.7, 0, 0.18, 3 }, { 0, 0, 0.1, 3 } }) do
		peca("Moldura", V(f[3], f[4], 0.2), CF(x + f[1], y + f[2], z - 0.06), BRANCO, nil, nil, cen, false)
	end
end
local function quadro(x, y, z, cor)
	peca("Quadro", V(1.8, 1.4, 0.08), CF(x, y, z), BRANCO, nil, nil, cen, false)
	peca("Tela", V(1.5, 1.1, 0.06), CF(x, y, z - 0.05), cor, nil, nil, cen, false)
end
local function mesa(x, z, larg, prof, alt, cor)
	cor = cor or MADEIRA
	local y0 = 0.24
	peca("Tampo", V(larg, 0.16, prof), CF(x, y0 + alt - 0.08, z), cor, Enum.Material.Wood)
	for _, s in ipairs({ { -1, -1 }, { 1, -1 }, { -1, 1 }, { 1, 1 } }) do
		peca("PeMesa", V(0.2, alt - 0.16, 0.2), CF(x + s[1] * (larg / 2 - 0.2), y0 + (alt - 0.16) / 2, z + s[2] * (prof / 2 - 0.2)), cor, Enum.Material.Wood)
	end
	return y0 + alt
end
local function setSala()
	local y = fundoSala(C(255, 225, 200))
	janela(3.0, 6.4, 5.95)
	quadro(-3.2, 6.4, 5.95, C(120, 190, 255))
	peca("Sofa", V(5, 1.3, 1.6), CF(-7, 0.9, 4.6), C(120, 170, 235))
	peca("EncostoSofa", V(5, 1.6, 0.6), CF(-7, 2.2, 5.3), C(100, 150, 220))
	K.piso(peca("Tapete", V(9, 0.03, 6), CF(0, 0.255, 0.8), C(255, 170, 190), nil, nil, cen, false))
	return y
end
local function setQuarto()
	local y = fundoSala(C(210, 200, 255))
	janela(-3.0, 6.4, 5.95)
	peca("Cama", V(5, 1.1, 3), CF(6.5, 0.8, 4.2), C(255, 150, 190))
	peca("Travesseiro", V(1.4, 0.4, 1), CF(5.4, 1.5, 4.8), BRANCO)
	peca("Estante", V(2.4, 4, 0.8), CF(-7, 2.2, 5.3), MADEIRA, Enum.Material.Wood)
	K.piso(peca("Tapete", V(8, 0.03, 6), CF(0, 0.255, 0.8), C(170, 230, 210), nil, nil, cen, false))
	return y
end
local function setCozinha(semJanela)
	local y = fundoSala(C(255, 245, 200), C(235, 205, 165))
	for i = -9, 9 do
		for j = 0, 8 do
			peca("Azulejo", V(0.95, 0.95, 0.1), CF(i, 0.9 + j, 5.95), (i + j) % 2 == 0 and C(255, 245, 190) or C(255, 255, 230), nil, nil, cen, false)
		end
	end
	if not semJanela then janela(3.2, 6.6, 5.85) end
	peca("Geladeira", V(2.2, 5.6, 1.6), CF(-5.2, 3.04, 4.9), C(240, 245, 255))
	peca("Puxador", V(0.12, 1.4, 0.12), CF(-4.3, 3.6, 4.05), C(180, 180, 190))
	peca("Prateleira", V(2.6, 0.12, 0.6), CF(-1.6, 6.4, 5.6), BRANCO)
	for i, cor in ipairs({ C(255, 120, 120), C(120, 200, 255), C(255, 210, 90) }) do
		cilindro("Pote", 0.6, 0.45, V(-2.5 + i * 0.6, 6.76, 5.6), cor, Enum.Material.Glass, cen, false)
	end
	return y
end
local function balcao(x, z, larg, prof, alt)
	peca("Balcao", V(larg, alt - 0.1, prof), CF(x, 0.24 + (alt - 0.1) / 2, z), BRANCO)
	peca("TampoBalcao", V(larg + 0.1, 0.1, prof + 0.1), CF(x, 0.24 + alt - 0.05, z), C(200, 150, 100), Enum.Material.Wood)
	return 0.24 + alt
end
local function setParque(semente)
	gramado(200, C(120, 205, 90))
	nuvensBrancas(10, semente or 77)
	for i = 0, 14 do
		bola("Arbusto", 1.6 + (i % 3) * 0.3, V(-10.5 + i * 1.5, 0.6, 8.6 + (i % 2) * 0.5), i % 2 == 0 and C(70, 170, 70) or C(90, 190, 80), nil, cen, false)
	end
	arvore(V(-8, 0, 12), 0.8)
	arvore(V(7.5, 0, 13), 0.9, C(90, 200, 110))
	arvore(V(-1.5, 0, 17), 0.75, C(80, 180, 90))
	flores(26, -9, 9, 6.4, 8, semente or 21)
	return 0.2
end
local function setPraia()
	gramado(200, C(250, 225, 160))
	for _, p in ipairs(cen:GetChildren()) do if p.Name == "Gramado" then p.Material = Enum.Material.Sand end end
	local bp = workspace:FindFirstChild("Baseplate")
	if bp then bp.Material = Enum.Material.Sand end
	nuvensBrancas(8, 31)
	peca("Mar", V(300, 0.3, 200), CF(0, 0.1, 118), C(70, 180, 235), nil, nil, cen, false)
	peca("Espuma", V(300, 0.32, 1), CF(0, 0.1, 18.4), BRANCO, nil, nil, cen, false)
	for _, x in ipairs({ -8, 9 }) do
		cilindro("Palmeira", 9, 0.6, V(x, 4.5, 11), C(170, 120, 75), nil, cen, false)
		for a = 0, 5 do
			elipse("Folha", V(4.6, 0.3, 1.1), CF(x, 9.1, 11) * ANG(0, rad(a * 60), rad(-15)) * CF(2.1, 0, 0), C(70, 180, 80), nil, cen, false)
		end
	end
	return 0.2
end
local function setNeve(semente, comNeve)
	local L = game:GetService("Lighting")
	L.OutdoorAmbient = C(190, 205, 235)
	gramado(200, C(235, 242, 255))
	for _, p in ipairs(cen:GetChildren()) do if p.Name == "Gramado" then p.Material = Enum.Material.SmoothPlastic end end
	local bp = workspace:FindFirstChild("Baseplate")
	if bp then bp.Material = Enum.Material.SmoothPlastic end
	nuvensBrancas(6, semente or 1201)
	local rng = Random.new(semente or 1201)
	for i = 1, 10 do
		bola("MonteLonge", rng:NextNumber(3, 6), V(rng:NextNumber(-14, 14), -0.6, rng:NextNumber(10, 22)), C(245, 248, 255), nil, cen, false)
	end
	for _, q in ipairs({ { -6, 10, 1.3 }, { -10, 15, 1.6 }, { 8, 12, 1.4 }, { 11.5, 18, 1.7 } }) do
		local pos, s = V(q[1], 0, q[2]), q[3]
		cilindro("TroncoP", 1.2 * s, 0.5 * s, pos + V(0, 0.6 * s, 0), C(120, 80, 50), nil, cen, false)
		for k = 0, 3 do
			cilindro("Copa", 1.0 * s, (3.0 - k * 0.65) * s, pos + V(0, (1.4 + k * 0.95) * s, 0), C(40, 140, 80), nil, cen, false)
			cilindro("Neve", 0.18 * s, (2.7 - k * 0.65) * s, pos + V(0, (1.95 + k * 0.95) * s, 0), C(250, 252, 255), nil, cen, false)
		end
	end
	if comNeve ~= false then
		local placa = peca("PlacaNeve", V(40, 1, 24), CF(0, 18, 4), BRANCO, nil, nil, cen, false)
		placa.Transparency = 1
		local ne = Instance.new("ParticleEmitter")
		ne.Name = "Neve"
		ne.Texture = "rbxasset://textures/particles/sparkles_main.dds"
		ne.Color = ColorSequence.new(BRANCO)
		ne.Size = NumberSequence.new(0.25)
		ne.Lifetime = NumberRange.new(6, 8)
		ne.Speed = NumberRange.new(2, 3)
		ne.EmissionDirection = Enum.NormalId.Bottom
		ne.SpreadAngle = Vector2.new(15, 15)
		ne.Acceleration = V(0, -0.4, 0)
		ne.Rate = 40
		ne.LightEmission = 0.3
		ne.Parent = placa
	end
	return 0.2
end
local function setFazenda()
	gramado(200, C(135, 210, 95))
	nuvensBrancas(9, 88)
	peca("Celeiro", V(10, 7, 6), CF(-8, 3.5, 15), C(205, 60, 55), Enum.Material.WoodPlanks, nil, cen, false)
	peca("Telhado", V(11, 0.5, 7), CF(-8, 7.8, 15), C(240, 240, 240), nil, nil, cen, false)
	peca("Porta", V(3, 4, 0.1), CF(-8, 2, 11.95), BRANCO, nil, nil, cen, false)
	for i = -7, 7 do
		peca("Mourao", V(0.25, 1.8, 0.25), CF(i * 1.8, 0.9, 8), BRANCO, nil, nil, cen, false)
	end
	for _, y in ipairs({ 0.8, 1.5 }) do peca("Tabua", V(28, 0.2, 0.12), CF(0, y, 7.9), BRANCO, nil, nil, cen, false) end
	for _, q in ipairs({ { 6, 10 }, { 8.2, 11.5 } }) do cilindro("Feno", 2, 2.4, V(q[1], 1.2, q[2]), C(235, 200, 90), nil, cen, false) end
	return 0.2
end
local function setFeira()
	gramado(200, C(125, 200, 95))
	nuvensBrancas(8, 55)
	local cores = { C(255, 90, 110), BRANCO, C(90, 170, 255), C(255, 210, 80) }
	for i = 0, 3 do
		local x = -9 + i * 6
		peca("Barraca", V(4.6, 3.6, 3), CF(x, 1.8, 12), cores[i + 1], nil, nil, cen, false)
		for k = 0, 4 do
			peca("Toldo", V(0.92, 0.2, 3.6), CF(x - 1.84 + k * 0.92, 4.0, 11.8), k % 2 == 0 and C(255, 70, 90) or BRANCO, nil, nil, cen, false)
		end
	end
	for i = 0, 18 do
		bola("Luzinha", 0.3, V(-9 + i, 6.2 - math.sin(i / 18 * math.pi) * 0.8, 8.5), cores[i % 4 + 1], Enum.Material.Neon, cen, false)
	end
	return 0.2
end
local function setLab()
	local y = fundoSala(C(190, 225, 240), C(225, 230, 240), Enum.Material.SmoothPlastic)
	for i = 0, 2 do
		local x = -7 + i * 2.2
		peca("Armario", V(2, 5, 1.2), CF(x, 2.74, 5.3), C(120, 140, 170))
		for k = 0, 3 do
			bola("Led", 0.22, V(x - 0.5 + k % 2 * 0.9, 3.4 + k * 0.4, 4.66), k % 2 == 0 and C(255, 80, 90) or C(90, 240, 150), Enum.Material.Neon, cen, false)
		end
	end
	peca("Lousa", V(5, 3, 0.1), CF(3.6, 6, 5.94), C(40, 80, 70), nil, nil, cen, false)
	return y
end
local function setAcademia()
	local y = fundoSala(C(255, 200, 150), C(120, 130, 150), Enum.Material.Rubber)
	peca("Espelho", V(9, 4, 0.08), CF(5, 4, 5.94), C(190, 225, 245), Enum.Material.Glass, nil, cen, false)
	for i = 0, 3 do
		cilindro("Halter", 0.5, 0.5, V(-7.5 + i * 1.1, 0.5, 5.2), ({ C(255, 80, 90), C(255, 200, 70), C(80, 170, 255), C(90, 220, 130) })[i + 1], nil, cen, false)
	end
	return y
end
local function setRua()
	gramado(200, C(120, 205, 90))
	nuvensBrancas(9, 44)
	peca("Calcada", V(60, 0.24, 10), CF(0, 0.12, 2.5), C(215, 215, 220), Enum.Material.Concrete)
	K.piso(cen:FindFirstChild("Calcada"))
	predios(9, 22, 12)
	for i = -3, 3 do arvore(V(i * 7, 0, 12), 0.6) end
	return 0.24
end
local function setNoite(cor)
	local L = game:GetService("Lighting")
	L.ClockTime = 0.3
	L.Brightness = 1.5
	L.Ambient = cor or C(95, 105, 150)
	L.OutdoorAmbient = cor or C(95, 105, 150)
	local p = peca("LuzFrente", V(0.2, 0.2, 0.2), CF(0, 6, -5), BRANCO, nil, nil, cen, false)
	p.Transparency = 1
	local l = Instance.new("PointLight")
	l.Brightness, l.Range, l.Color = 0.8, 22, C(255, 235, 210)
	l.Parent = p
end

-- ---------------------------------------------------------------- bichos
local nBicho = 0
local function novoBicho(nome)
	nBicho = nBicho + 1
	local m = modelo(nome)
	local O = V(nBicho * 30, -200, 0)
	local b = peca("Base", V(0.05, 0.05, 0.05), CF(O), C(0, 0, 0), nil, nil, m, false)
	b.Transparency = 1
	return m, O, b
end
local function olhosB(m, O, y, z, dx, d)
	for _, s in ipairs({ -1, 1 }) do
		bola("Olho", d, O + V(s * dx, y, z), C(30, 25, 25), nil, m, false)
		bola("BrilhoOlho", d * 0.38, O + V(s * dx - d * 0.18, y + d * 0.2, z - d * 0.42), BRANCO, Enum.Material.Neon, m, false)
	end
end
-- Quadrúpede fofo (1,75 de altura na escala 1). o = {cor, claro, escuro, orelha = "caida"|"ponta"|"longa"|"redonda"|"nenhuma", escala, rabo}
local function quadrupede(nome, o)
	local m, O, b = novoBicho(nome)
	local cor, claro, escuro = o.cor, o.claro or C(255, 235, 200), o.escuro or o.cor
	elipse("Corpo", V(0.8, 0.72, 1.35), CF(O + V(0, 0.78, 0.1)), cor, nil, m, false)
	elipse("Peito", V(0.55, 0.5, 0.25), CF(O + V(0, 0.8, -0.5)), claro, nil, m, false)
	bola("Cabeca", 0.78, O + V(0, 1.35, -0.62), cor, nil, m, false)
	elipse("Focinho", V(0.42, 0.3, 0.32), CF(O + V(0, 1.24, -0.98)), claro, nil, m, false)
	bola("Nariz", 0.14, O + V(0, 1.33, -1.14), o.nariz or C(40, 30, 30), nil, m, false)
	olhosB(m, O, 1.48, -0.95, 0.16, 0.16)
	for _, s in ipairs({ -1, 1 }) do
		if o.orelha == "caida" then
			elipse("Orelha", V(0.2, 0.5, 0.16), CF(O + V(s * 0.4, 1.35, -0.55)) * ANG(0, 0, rad(s * 15)), escuro, nil, m, false)
		elseif o.orelha == "ponta" then
			peca("Orelha", V(0.24, 0.3, 0.12), CF(O + V(s * 0.24, 1.76, -0.6)) * ANG(0, 0, rad(-s * 45)), escuro, nil, nil, m, false)
		elseif o.orelha == "longa" then
			elipse("Orelha", V(0.24, 0.85, 0.14), CF(O + V(s * 0.2, 2.05, -0.6)) * ANG(0, 0, rad(-s * 8)), escuro, nil, m, false)
			elipse("OrelhaDentro", V(0.13, 0.65, 0.05), CF(O + V(s * 0.2, 2.05, -0.68)) * ANG(0, 0, rad(-s * 8)), C(255, 170, 190), nil, m, false)
		elseif o.orelha == "redonda" then
			bola("Orelha", 0.32, O + V(s * 0.34, 1.72, -0.6), escuro, nil, m, false)
		end
		for _, z in ipairs({ -0.38, 0.52 }) do
			elipse("Perna", V(0.22, 0.6, 0.24), CF(O + V(s * 0.24, 0.3, z)), cor, nil, m, false)
		end
	end
	if o.rabo ~= false then
		elipse("Rabo", V(0.16, 0.16, 0.6), CF(O + V(0, 1.05, 0.9)) * ANG(rad(40), 0, 0), o.corRabo or escuro, nil, m, false)
	end
	if o.chifres then
		for _, s in ipairs({ -1, 1 }) do
			peca("Chifre", V(0.1, 0.5, 0.1), CF(O + V(s * 0.16, 1.9, -0.5)) * ANG(rad(-20), 0, rad(-s * 10)), C(120, 95, 70), nil, nil, m, false)
		end
		elipse("Barbicha", V(0.16, 0.34, 0.16), CF(O + V(0, 0.98, -1.05)), C(160, 140, 120), nil, m, false)
	end
	if o.vaca then
		for _, s in ipairs({ -1, 1 }) do
			peca("Chifre", V(0.1, 0.28, 0.1), CF(O + V(s * 0.2, 1.82, -0.62)) * ANG(0, 0, rad(-s * 18)), C(240, 230, 200), nil, nil, m, false)
		end
		for _, q in ipairs({ { 0.42, 0.95, 0.2 }, { -0.4, 0.8, 0.45 }, { -0.25, 1.05, -0.1 }, { 0.3, 0.72, 0.5 }, { 0.2, 1.62, -0.85 } }) do
			elipse("Mancha", V(0.34, 0.3, 0.42), CF(O + V(q[1], q[2], q[3])), escuro, nil, m, false)
		end
		elipse("Sino", V(0.2, 0.2, 0.2), CF(O + V(0, 0.98, -0.72)), C(255, 215, 70), nil, m, false)
	end
	fechar(m, b, false)
	if o.escala then m:ScaleTo(o.escala) end
	return m
end
local function criarCachorro(nome, cor, escala)
	return quadrupede(nome or "Cachorro", { cor = cor or C(230, 170, 100), escuro = C(170, 110, 60), orelha = "caida", escala = escala or 1.3 })
end
local function criarGato(nome, cor, escala)
	return quadrupede(nome or "Gato", { cor = cor or C(245, 165, 80), claro = C(255, 240, 220), escuro = C(215, 130, 60), orelha = "ponta", nariz = C(255, 130, 150), escala = escala or 1.2 })
end
local function criarCoelho(nome, cor, escala)
	return quadrupede(nome or "Coelho", { cor = cor or BRANCO, claro = BRANCO, escuro = cor or BRANCO, orelha = "longa", nariz = C(255, 130, 150), rabo = false, escala = escala or 1.1 })
end
local function criarUrso(nome, cor, escala)
	return quadrupede(nome or "Urso", { cor = cor or C(150, 100, 60), claro = C(225, 195, 150), orelha = "redonda", rabo = false, escala = escala or 2.2 })
end
local function criarHamster(nome, escala)
	return quadrupede(nome or "Hamster", { cor = C(240, 190, 120), claro = BRANCO, escuro = C(250, 170, 150), orelha = "redonda", nariz = C(255, 130, 150), rabo = false, escala = escala or 0.8 })
end
-- Vaca: cor do corpo e manchas.
local function criarVaca(nome, cor, mancha, escala)
	local m = quadrupede(nome or "Vaca", { cor = cor or BRANCO, claro = C(255, 195, 200), escuro = mancha or C(50, 45, 45), orelha = "ponta", nariz = C(230, 120, 140), vaca = true, escala = escala or 2.2 })
	return m
end
local function criarPonei(nome, cor, escala)
	local m, O, b = novoBicho(nome or "Ponei")
	cor = cor or C(190, 130, 80)
	local crina = C(90, 60, 45)
	elipse("Corpo", V(1.0, 1.0, 2.2), CF(O + V(0, 1.85, 0.2)), cor, nil, m, false)
	elipse("Pescoco", V(0.6, 1.3, 0.7), CF(O + V(0, 2.75, -0.8)) * ANG(rad(25), 0, 0), cor, nil, m, false)
	elipse("Cabeca", V(0.62, 0.7, 1.05), CF(O + V(0, 3.3, -1.25)), cor, nil, m, false)
	elipse("Focinho", V(0.5, 0.42, 0.44), CF(O + V(0, 3.12, -1.72)), C(235, 205, 170), nil, m, false)
	olhosB(m, O, 3.48, -1.55, 0.26, 0.18)
	for _, s in ipairs({ -1, 1 }) do
		peca("Orelha", V(0.16, 0.34, 0.1), CF(O + V(s * 0.2, 3.76, -1.0)), cor, nil, nil, m, false)
		for _, z in ipairs({ -0.55, 0.95 }) do
			cilindro("Perna", 1.5, 0.3, O + V(s * 0.32, 0.75, z), cor, nil, m, false)
			cilindro("Casco", 0.18, 0.34, O + V(s * 0.32, 0.09, z), C(70, 50, 40), nil, m, false)
		end
	end
	for k = 0, 4 do bola("Crina", 0.34, O + V(0, 3.75 - k * 0.3, -1.0 + k * 0.2), crina, nil, m, false) end
	elipse("Rabo", V(0.3, 0.3, 1.1), CF(O + V(0, 1.7, 1.55)) * ANG(rad(50), 0, 0), crina, nil, m, false)
	fechar(m, b, false)
	if escala then m:ScaleTo(escala) end
	return m
end
local function criarGirafa(nome)
	local m, O, b = novoBicho(nome or "Girafa")
	local cor, mancha = C(250, 205, 100), C(190, 120, 60)
	elipse("Corpo", V(1.6, 1.6, 2.6), CF(O + V(0, 4.0, 0.6)), cor, nil, m, false)
	for k = 0, 8 do
		bola("Pescoco", 1.25 - k * 0.05, O + V(0, 4.8 + k * 0.72, -0.2 - k * 0.1), cor, nil, m, false)
		if k % 2 == 0 then bola("Mancha", 0.42, O + V(0.28, 4.9 + k * 0.72, -0.72 - k * 0.09), mancha, nil, m, false) end
	end
	elipse("Cabeca", V(1.3, 1.3, 2.0), CF(O + V(0, 11.0, -1.5)), cor, nil, m, false)
	elipse("Focinho", V(1.0, 0.75, 0.75), CF(O + V(0, 10.65, -2.4)), C(255, 235, 190), nil, m, false)
	olhosB(m, O, 11.35, -2.3, 0.44, 0.3)
	for _, s in ipairs({ -1, 1 }) do
		cilindro("Chifre", 0.5, 0.12, O + V(s * 0.2, 11.7, -1.2), mancha, nil, m, false)
		bola("PontaChifre", 0.2, O + V(s * 0.2, 12, -1.2), mancha, nil, m, false)
		peca("Orelha", V(0.4, 0.14, 0.2), CF(O + V(s * 0.58, 11.3, -1.0)), cor, nil, nil, m, false)
		for _, z in ipairs({ -0.3, 1.5 }) do cilindro("Perna", 3.6, 0.42, O + V(s * 0.5, 1.8, z), cor, nil, m, false) end
	end
	fechar(m, b, false)
	return m
end
local function criarCanguru(nome, escala)
	local m, O, b = novoBicho(nome or "Canguru")
	local cor, claro = C(195, 140, 90), C(240, 215, 180)
	elipse("Corpo", V(1.2, 1.8, 1.1), CF(O + V(0, 1.7, 0)), cor, nil, m, false)
	elipse("Barriga", V(0.8, 1.2, 0.3), CF(O + V(0, 1.6, -0.48)), claro, nil, m, false)
	bola("Cabeca", 0.86, O + V(0, 3.0, -0.1), cor, nil, m, false)
	elipse("Focinho", V(0.46, 0.34, 0.4), CF(O + V(0, 2.88, -0.52)), claro, nil, m, false)
	bola("Nariz", 0.14, O + V(0, 2.96, -0.7), C(40, 30, 30), nil, m, false)
	olhosB(m, O, 3.15, -0.48, 0.2, 0.17)
	for _, s in ipairs({ -1, 1 }) do
		elipse("Orelha", V(0.24, 0.7, 0.14), CF(O + V(s * 0.3, 3.65, 0)) * ANG(0, 0, rad(-s * 12)), cor, nil, m, false)
		elipse("Pe", V(0.4, 0.3, 1.2), CF(O + V(s * 0.4, 0.16, -0.3)), cor, nil, m, false)
		elipse("Braco", V(0.22, 0.7, 0.22), CF(O + V(s * 0.5, 2.0, -0.45)) * ANG(rad(30), 0, 0), cor, nil, m, false)
	end
	elipse("Rabo", V(0.4, 0.4, 1.9), CF(O + V(0, 0.6, 1.2)) * ANG(rad(20), 0, 0), cor, nil, m, false)
	fechar(m, b, false)
	if escala then m:ScaleTo(escala) end
	return m
end
local function criarPinguim(nome, escala)
	local m, O, b = novoBicho(nome or "Pinguim")
	local p = C(45, 50, 70)
	elipse("Corpo", V(1.1, 1.5, 1.0), CF(O + V(0, 0.9, 0)), p, nil, m, false)
	elipse("Barriga", V(0.8, 1.15, 0.3), CF(O + V(0, 0.82, -0.42)), BRANCO, nil, m, false)
	bola("Cabeca", 0.86, O + V(0, 1.85, 0), p, nil, m, false)
	elipse("Rosto", V(0.6, 0.5, 0.2), CF(O + V(0, 1.82, -0.36)), BRANCO, nil, m, false)
	olhosB(m, O, 1.95, -0.42, 0.16, 0.14)
	elipse("Bico", V(0.26, 0.14, 0.3), CF(O + V(0, 1.78, -0.52)), C(255, 170, 50), nil, m, false)
	for _, s in ipairs({ -1, 1 }) do
		elipse("Asa", V(0.18, 0.9, 0.34), CF(O + V(s * 0.6, 1.0, 0)) * ANG(0, 0, rad(s * 14)), p, nil, m, false)
		elipse("Pe", V(0.34, 0.12, 0.5), CF(O + V(s * 0.26, 0.06, -0.2)), C(255, 170, 50), nil, m, false)
	end
	fechar(m, b, false)
	if escala then m:ScaleTo(escala) end
	return m
end
local function criarPassaro(nome, cor, escala)
	local m, O, b = novoBicho(nome or "Passaro")
	cor = cor or C(90, 170, 255)
	bola("Corpo", 0.8, O + V(0, 0.7, 0), cor, nil, m, false)
	elipse("Barriga", V(0.5, 0.5, 0.2), CF(O + V(0, 0.62, -0.32)), BRANCO, nil, m, false)
	bola("Cabeca", 0.54, O + V(0, 1.2, -0.08), cor, nil, m, false)
	olhosB(m, O, 1.27, -0.3, 0.13, 0.11)
	elipse("Bico", V(0.16, 0.1, 0.22), CF(O + V(0, 1.17, -0.4)), C(255, 180, 50), nil, m, false)
	for _, s in ipairs({ -1, 1 }) do
		elipse("Asa", V(0.14, 0.5, 0.42), CF(O + V(s * 0.42, 0.75, 0.05)), cor, nil, m, false)
		cilindro("Perninha", 0.34, 0.05, O + V(s * 0.14, 0.17, 0), C(255, 170, 50), nil, m, false)
	end
	fechar(m, b, false)
	if escala then m:ScaleTo(escala) end
	return m
end
local function criarPintinho(nome, escala)
	return criarPassaro(nome or "Pintinho", C(255, 225, 80), escala or 1.2)
end
local function criarGalinha(nome, escala)
	local m, O, b = novoBicho(nome or "Galinha")
	bola("Corpo", 1.1, O + V(0, 0.85, 0), BRANCO, nil, m, false)
	bola("Cabeca", 0.6, O + V(0, 1.55, -0.3), BRANCO, nil, m, false)
	olhosB(m, O, 1.62, -0.56, 0.14, 0.11)
	elipse("Bico", V(0.18, 0.1, 0.2), CF(O + V(0, 1.53, -0.66)), C(255, 180, 50), nil, m, false)
	elipse("Crista", V(0.1, 0.3, 0.4), CF(O + V(0, 1.92, -0.3)), C(235, 50, 60), nil, m, false)
	for _, s in ipairs({ -1, 1 }) do
		elipse("Asa", V(0.16, 0.56, 0.6), CF(O + V(s * 0.56, 0.9, 0.05)), C(245, 240, 230), nil, m, false)
		cilindro("Perninha", 0.34, 0.07, O + V(s * 0.2, 0.17, 0), C(255, 170, 50), nil, m, false)
	end
	fechar(m, b, false)
	if escala then m:ScaleTo(escala) end
	return m
end
local function criarAvestruz(nome)
	local m, O, b = novoBicho(nome or "Avestruz")
	local preto = C(60, 55, 65)
	elipse("Corpo", V(1.8, 1.5, 2.2), CF(O + V(0, 3.0, 0.3)), preto, nil, m, false)
	elipse("Cauda", V(1.0, 0.8, 0.8), CF(O + V(0, 3.4, 1.4)), BRANCO, nil, m, false)
	for k = 0, 6 do bola("Pescoco", 0.4, O + V(0, 3.6 + k * 0.45, -0.7 - k * 0.04), C(240, 190, 170), nil, m, false) end
	bola("Cabeca", 0.66, O + V(0, 6.5, -1.0), C(240, 190, 170), nil, m, false)
	olhosB(m, O, 6.62, -1.28, 0.16, 0.16)
	elipse("Bico", V(0.34, 0.14, 0.44), CF(O + V(0, 6.4, -1.42)), C(250, 170, 90), nil, m, false)
	for _, s in ipairs({ -1, 1 }) do cilindro("Perna", 2.4, 0.24, O + V(s * 0.4, 1.2, 0.2), C(240, 190, 170), nil, m, false) end
	fechar(m, b, false)
	return m
end
local function criarFormiga(nome, escala)
	local m, O, b = novoBicho(nome or "Formiga")
	local cor = C(170, 60, 45)
	bola("Traseiro", 0.5, O + V(0, 0.3, 0.42), cor, nil, m, false)
	bola("Meio", 0.34, O + V(0, 0.28, 0), cor, nil, m, false)
	bola("Cabeca", 0.44, O + V(0, 0.34, -0.36), cor, nil, m, false)
	olhosB(m, O, 0.42, -0.54, 0.1, 0.12)
	for _, s in ipairs({ -1, 1 }) do
		for _, z in ipairs({ -0.15, 0, 0.15 }) do
			peca("Pata", V(0.34, 0.04, 0.04), CF(O + V(s * 0.28, 0.14, z)) * ANG(0, 0, rad(s * 35)), cor, nil, nil, m, false)
		end
		peca("Antena", V(0.04, 0.3, 0.04), CF(O + V(s * 0.1, 0.68, -0.44)) * ANG(0, 0, rad(-s * 20)), cor, nil, nil, m, false)
	end
	fechar(m, b, false)
	if escala then m:ScaleTo(escala) end
	return m
end
local function criarPeixe(nome, cor, escala)
	local m, O, b = novoBicho(nome or "Peixe")
	cor = cor or C(255, 140, 50)
	elipse("Corpo", V(1.4, 1.0, 0.5), CF(O + V(0, 0.6, 0)), cor, nil, m, false)
	peca("Cauda", V(0.5, 0.6, 0.06), CF(O + V(0.85, 0.6, 0)) * ANG(0, 0, rad(45)), cor, nil, nil, m, false)
	peca("Barbatana", V(0.3, 0.3, 0.06), CF(O + V(0, 1.08, 0)) * ANG(0, 0, rad(45)), BRANCO, nil, nil, m, false)
	bola("Olho", 0.22, O + V(-0.4, 0.72, -0.2), C(30, 25, 25), nil, m, false)
	bola("BrilhoOlho", 0.09, O + V(-0.44, 0.76, -0.3), BRANCO, Enum.Material.Neon, m, false)
	elipse("Boca", V(0.1, 0.16, 0.1), CF(O + V(-0.68, 0.5, -0.1)), C(200, 70, 60), nil, m, false)
	fechar(m, b, false)
	if escala then m:ScaleTo(escala) end
	return m
end
local function criarRena(nome, escala)
	local m = quadrupede(nome or "Rena", { cor = C(150, 100, 60), claro = C(225, 195, 150), orelha = "ponta", nariz = C(230, 50, 50), escala = 1 })
	local base = m.PrimaryPart
	local O = base.Position
	for _, s in ipairs({ -1, 1 }) do
		for _, q in ipairs({ { 0.24, 2.05, 0.1, 0.5, 0 }, { 0.38, 2.35, 0.08, 0.36, -30 }, { 0.16, 2.35, 0.08, 0.36, 30 } }) do
			local p = peca("Chifre", V(q[3], q[4], q[3]), CF(O + V(s * q[1], q[2], -0.62)) * ANG(0, 0, rad(-s * q[5])), C(205, 165, 110), nil, nil, m, false)
			p.Anchored = false
			local w = Instance.new("WeldConstraint")
			w.Part0, w.Part1 = base, p
			w.Parent = p
		end
	end
	if escala then m:ScaleTo(escala) end
	return m
end
local function criarDino(nome, escala)
	local m, O, b = novoBicho(nome or "Dino")
	local cor, claro = C(110, 205, 110), C(210, 245, 170)
	elipse("Corpo", V(1.2, 1.4, 1.2), CF(O + V(0, 1.1, 0)), cor, nil, m, false)
	elipse("Barriga", V(0.8, 1.0, 0.3), CF(O + V(0, 1.0, -0.5)), claro, nil, m, false)
	bola("Cabeca", 1.1, O + V(0, 2.2, -0.15), cor, nil, m, false)
	elipse("Focinho", V(0.8, 0.5, 0.5), CF(O + V(0, 2.05, -0.65)), claro, nil, m, false)
	olhosB(m, O, 2.42, -0.62, 0.26, 0.2)
	for k = 0, 3 do bola("Placa", 0.3, O + V(0, 2.75 - k * 0.5, 0.3 + k * 0.2), C(255, 150, 80), nil, m, false) end
	for _, s in ipairs({ -1, 1 }) do
		elipse("Pe", V(0.5, 0.4, 0.8), CF(O + V(s * 0.42, 0.2, -0.15)), cor, nil, m, false)
		elipse("Braco", V(0.2, 0.5, 0.2), CF(O + V(s * 0.56, 1.4, -0.3)) * ANG(rad(30), 0, 0), cor, nil, m, false)
	end
	elipse("Rabo", V(0.5, 0.5, 1.5), CF(O + V(0, 0.6, 1.0)) * ANG(rad(20), 0, 0), cor, nil, m, false)
	fechar(m, b, false)
	if escala then m:ScaleTo(escala) end
	return m
end
local function criarEsquilo(nome, escala)
	local m = quadrupede(nome or "Esquilo", { cor = C(190, 110, 60), claro = C(250, 225, 190), escuro = C(150, 85, 45), orelha = "redonda", rabo = false, escala = 1 })
	local base = m.PrimaryPart
	local O = base.Position
	local p = elipse("RaboGrande", V(0.8, 1.6, 0.8), CF(O + V(0, 1.4, 1.1)), C(190, 110, 60), nil, m, false)
	p.Anchored = false
	local w = Instance.new("WeldConstraint")
	w.Part0, w.Part1 = base, p
	w.Parent = p
	if escala then m:ScaleTo(escala) end
	return m
end
local function criarBoneco(nome, escala)
	local m, O, b = novoBicho(nome or "Boneco")
	bola("Base", 1.8, O + V(0, 0.8, 0), BRANCO, nil, m, false)
	bola("Meio", 1.3, O + V(0, 2.0, 0), BRANCO, nil, m, false)
	bola("Cabeca", 1.0, O + V(0, 2.95, 0), BRANCO, nil, m, false)
	olhosB(m, O, 3.08, -0.42, 0.18, 0.14)
	elipse("Cenoura", V(0.14, 0.14, 0.5), CF(O + V(0, 2.92, -0.6)), C(255, 130, 40), nil, m, false)
	for k = 0, 2 do bola("Botao", 0.13, O + V(0, 2.3 - k * 0.3, -0.62 + k * 0.03), C(40, 40, 50), nil, m, false) end
	fechar(m, b, false)
	if escala then m:ScaleTo(escala) end
	return m
end
local function criarUrsoPelucia(nome, cor, escala)
	local m, O, b = novoBicho(nome or "Teddy")
	cor = cor or C(190, 135, 85)
	elipse("Corpo", V(1.3, 1.5, 1.1), CF(O + V(0, 0.95, 0)), cor, nil, m, false)
	bola("Cabeca", 1.1, O + V(0, 2.05, 0), cor, nil, m, false)
	elipse("Focinho", V(0.5, 0.36, 0.3), CF(O + V(0, 1.92, -0.48)), C(240, 215, 180), nil, m, false)
	bola("Nariz", 0.16, O + V(0, 1.98, -0.62), C(40, 30, 30), nil, m, false)
	olhosB(m, O, 2.2, -0.46, 0.22, 0.15)
	for _, s in ipairs({ -1, 1 }) do
		bola("Orelha", 0.42, O + V(s * 0.46, 2.55, 0), cor, nil, m, false)
		elipse("Braco", V(0.36, 0.9, 0.36), CF(O + V(s * 0.74, 1.2, -0.1)) * ANG(0, 0, rad(s * 20)), cor, nil, m, false)
		elipse("PernaT", V(0.44, 0.4, 0.8), CF(O + V(s * 0.4, 0.22, -0.3)), cor, nil, m, false)
	end
	fechar(m, b, false)
	if escala then m:ScaleTo(escala) end
	return m
end

local function arvoreNatal(pos, s)
	s = s or 1
	cilindro("TroncoN", 0.8 * s, 0.6 * s, pos + V(0, 0.4 * s, 0), C(120, 80, 50), nil, cen, false)
	local cores = { C(255, 70, 80), C(255, 215, 70), C(90, 190, 255), C(255, 130, 200) }
	for k = 0, 3 do
		local d = (3.6 - k * 0.8) * s
		cilindro("CopaN", 1.1 * s, d, pos + V(0, (1.2 + k * 0.95) * s, 0), C(40, 150, 80), nil, cen, false)
		for a = 0, 5 do
			local q = rad(a * 60 + k * 20)
			bola("BolaN", 0.3 * s, pos + V(math.cos(q) * d * 0.5, (1.0 + k * 0.95) * s, math.sin(q) * d * 0.5), cores[(a + k) % 4 + 1], Enum.Material.Neon, cen, false)
		end
	end
	for _, r in ipairs({ 0, 45 }) do
		peca("EstrelaN", V(0.7 * s, 0.7 * s, 0.1), CF(pos + V(0, 5.0 * s, 0)) * ANG(0, 0, rad(r)), C(255, 215, 50), Enum.Material.Neon, nil, cen, false)
	end
end
local function presente(x, y, z, s, cor)
	peca("Presente", V(s, s, s), CF(x, y + s / 2, z), cor, nil, nil, cen, false)
	peca("Fita", V(s + 0.04, s + 0.04, s * 0.2), CF(x, y + s / 2, z), C(255, 240, 150), nil, nil, cen, false)
	peca("Fita", V(s * 0.2, s + 0.04, s + 0.04), CF(x, y + s / 2, z), C(255, 240, 150), nil, nil, cen, false)
end
local function criarNoel(nome, escala)
	local m, O, b = novoBicho(nome or "Noel")
	local V1 = C(215, 40, 50)
	elipse("Corpo", V(2.3, 2.6, 2.0), CF(O + V(0, 1.9, 0)), V1, nil, m, false)
	peca("Cinto", V(2.2, 0.3, 2.0), CF(O + V(0, 1.7, -0.1)), C(40, 35, 40), nil, nil, m, false)
	peca("Fivela", V(0.5, 0.4, 0.1), CF(O + V(0, 1.7, -1.08)), C(255, 215, 70), nil, nil, m, false)
	bola("Cabeca", 1.3, O + V(0, 3.6, 0), C(255, 215, 180), nil, m, false)
	olhosB(m, O, 3.8, -0.58, 0.24, 0.18)
	bola("Nariz", 0.24, O + V(0, 3.62, -0.66), C(250, 160, 140), nil, m, false)
	elipse("Barba", V(1.5, 1.3, 0.8), CF(O + V(0, 3.1, -0.4)), BRANCO, nil, m, false)
	cilindro("Aba", 0.28, 1.45, O + V(0, 4.2, 0), BRANCO, nil, m, false)
	elipse("Gorro", V(1.15, 1.5, 1.15), CF(O + V(0, 4.8, 0)), V1, nil, m, false)
	bola("Pompom", 0.4, O + V(0, 5.5, 0), BRANCO, nil, m, false)
	for _, s in ipairs({ -1, 1 }) do
		elipse("Braco", V(0.6, 1.7, 0.6), CF(O + V(s * 1.35, 2.2, 0)) * ANG(0, 0, rad(s * 20)), V1, nil, m, false)
		peca("Bota", V(0.7, 0.6, 1.0), CF(O + V(s * 0.5, 0.3, -0.2)), C(40, 35, 40), nil, nil, m, false)
	end
	fechar(m, b, false)
	if escala then m:ScaleTo(escala) end
	return m
end
local function criarTreno(nome)
	local m, O, b = novoBicho(nome or "Treno")
	local V1 = C(235, 60, 70)
	peca("Assento", V(2.6, 0.6, 3.6), CF(O + V(0, 1.0, 0.2)), V1, nil, nil, m, false)
	peca("Encosto", V(2.6, 1.3, 0.3), CF(O + V(0, 1.7, 1.9)), V1, nil, nil, m, false)
	peca("Bico", V(2.6, 0.9, 0.3), CF(O + V(0, 1.1, -1.7)) * ANG(rad(-25), 0, 0), V1, nil, nil, m, false)
	for _, s in ipairs({ -1, 1 }) do
		peca("Esqui", V(0.2, 0.14, 5.0), CF(O + V(s * 1.1, 0.1, 0)), C(255, 215, 70), Enum.Material.Metal, nil, m, false)
		for _, z in ipairs({ -0.9, 1.1 }) do peca("Apoio", V(0.14, 0.7, 0.14), CF(O + V(s * 1.1, 0.45, z)), C(255, 215, 70), Enum.Material.Metal, nil, m, false) end
	end
	fechar(m, b, false)
	return m
end

-- ---------------------------------------------------------------- bichos e objetos do lote lulu-20261211
local function criarElefante(nome, escala)
	local m, O, b = novoBicho(nome or "Elefante")
	local cor, claro = C(165, 175, 200), C(255, 190, 200)
	elipse("Corpo", V(2.6, 2.4, 3.0), CF(O + V(0, 2.0, 0.4)), cor, nil, m, false)
	bola("Cabeca", 1.9, O + V(0, 2.9, -1.2), cor, nil, m, false)
	olhosB(m, O, 3.25, -2.0, 0.42, 0.24)
	for k = 0, 6 do bola("Tromba", 0.6 - k * 0.04, O + V(0, 2.6 - k * 0.36, -2.1 - math.sin(k / 6 * 1.2) * 0.5), cor, nil, m, false) end
	for k = 0, 6 do
		local t = bola("Tromba2", 0.6 - k * 0.04, O + V(-k * 0.42, 2.7 + k * 0.28, -2.15 - k * 0.04), cor, nil, m, false)
		t.Transparency = 1
	end
	for _, s in ipairs({ -1, 1 }) do
		elipse("Orelha", V(1.6, 1.8, 0.2), CF(O + V(s * 1.5, 3.1, -1.0)) * ANG(0, rad(-s * 20), 0), cor, nil, m, false)
		elipse("OrelhaDentro", V(1.1, 1.3, 0.06), CF(O + V(s * 1.5, 3.1, -1.12)) * ANG(0, rad(-s * 20), 0), claro, nil, m, false)
		for _, z in ipairs({ -0.5, 1.3 }) do cilindro("Perna", 1.3, 0.8, O + V(s * 0.8, 0.65, z), cor, nil, m, false) end
	end
	fechar(m, b, false)
	if escala then m:ScaleTo(escala) end
	return m
end
local function criarMacaco(nome, escala)
	local m, O, b = novoBicho(nome or "Macaco")
	local cor, claro = C(140, 95, 60), C(240, 205, 165)
	elipse("Corpo", V(1.1, 1.4, 1.0), CF(O + V(0, 1.0, 0)), cor, nil, m, false)
	elipse("Barriga", V(0.7, 0.9, 0.2), CF(O + V(0, 0.95, -0.42)), claro, nil, m, false)
	bola("Cabeca", 1.05, O + V(0, 2.05, 0), cor, nil, m, false)
	elipse("Rosto", V(0.8, 0.66, 0.24), CF(O + V(0, 1.98, -0.42)), claro, nil, m, false)
	olhosB(m, O, 2.14, -0.5, 0.18, 0.15)
	elipse("Sorriso", V(0.34, 0.06, 0.05), CF(O + V(0, 1.82, -0.56)), C(120, 60, 50), nil, m, false)
	for _, s in ipairs({ -1, 1 }) do
		bola("Orelha", 0.36, O + V(s * 0.58, 2.1, 0), claro, nil, m, false)
		elipse("Braco", V(0.26, 1.1, 0.26), CF(O + V(s * 0.66, 1.0, -0.1)) * ANG(0, 0, rad(s * 16)), cor, nil, m, false)
		elipse("Pe", V(0.3, 0.2, 0.5), CF(O + V(s * 0.3, 0.1, -0.1)), cor, nil, m, false)
	end
	elipse("Rabo", V(0.16, 0.16, 1.2), CF(O + V(0.1, 0.8, 0.8)) * ANG(rad(-30), 0, 0), cor, nil, m, false)
	fechar(m, b, false)
	if escala then m:ScaleTo(escala) end
	return m
end
local function criarPorco(nome, escala)
	return quadrupede(nome or "Porco", { cor = C(255, 175, 190), claro = C(255, 205, 215), escuro = C(240, 145, 170), orelha = "ponta", nariz = C(225, 105, 135), rabo = false, escala = escala or 1.4 })
end
local function criarRato(nome, escala)
	return quadrupede(nome or "Rato", { cor = C(190, 190, 205), claro = BRANCO, escuro = C(255, 170, 190), orelha = "redonda", nariz = C(255, 130, 150), escala = escala or 0.6 })
end
-- Só a cabeça, com o pivô na linha da água.
local function criarHipo(nome, escala)
	local m, O, b = novoBicho(nome or "Hipo")
	local cor = C(165, 135, 175)
	elipse("Cabeca", V(3.0, 1.5, 3.2), CF(O + V(0, 0.3, 0)), cor, nil, m, false)
	elipse("Focinho", V(2.2, 1.1, 1.2), CF(O + V(0, 0.2, -1.4)), C(190, 160, 195), nil, m, false)
	for _, s in ipairs({ -1, 1 }) do
		bola("Saliencia", 0.8, O + V(s * 0.8, 1.0, -0.2), cor, nil, m, false)
		bola("Olho", 0.34, O + V(s * 0.8, 1.14, -0.5), C(30, 25, 25), nil, m, false)
		bola("BrilhoOlho", 0.12, O + V(s * 0.74, 1.2, -0.65), BRANCO, Enum.Material.Neon, m, false)
		bola("Orelha", 0.4, O + V(s * 1.1, 1.14, 0.8), C(255, 170, 190), nil, m, false)
		bola("Narina", 0.2, O + V(s * 0.45, 0.68, -1.72), C(90, 70, 100), nil, m, false)
	end
	fechar(m, b, false)
	if escala then m:ScaleTo(escala) end
	return m
end
-- Baleia com uma ilhota nas costas: topo da areia em y = 3.9 do pivô, olhos em y = 1.5.
local function criarBaleia(nome)
	local m, O, b = novoBicho(nome or "Baleia")
	local cor = C(70, 125, 205)
	elipse("Corpo", V(13, 5, 7), CF(O + V(1.5, 1.2, 1)), cor, nil, m, false)
	elipse("Barriga", V(10, 2.6, 6.8), CF(O + V(0.5, 0.1, 0.8)), C(220, 235, 250), nil, m, false)
	for _, x in ipairs({ -1.6, 2.8 }) do
		bola("Olho", 0.7, O + V(x, 1.5, -2.45), C(30, 25, 30), nil, m, false)
		bola("BrilhoOlho", 0.26, O + V(x - 0.12, 1.64, -2.76), BRANCO, Enum.Material.Neon, m, false)
	end
	elipse("Sorriso", V(3.4, 0.2, 0.2), CF(O + V(0.6, 0.55, -3.34)), C(40, 70, 130), nil, m, false)
	elipse("Ilha", V(7, 0.9, 5), CF(O + V(-1.3, 3.5, 0.6)), C(250, 225, 160), Enum.Material.Sand, m, false)
	cilindro("Palmeira", 5, 0.4, O + V(1.3, 6.2, 1.6), C(170, 120, 75), nil, m, false)
	for a = 0, 5 do elipse("Folha", V(3.2, 0.24, 0.9), CF(O + V(1.3, 8.8, 1.6)) * ANG(0, rad(a * 60), rad(-15)) * CF(1.4, 0, 0), C(70, 180, 80), nil, m, false) end
	fechar(m, b, false)
	return m
end
local function criarPreguica(nome, escala)
	local m, O, b = novoBicho(nome or "Preguica")
	local cor, claro = C(165, 130, 95), C(235, 215, 185)
	elipse("Corpo", V(1.6, 2.0, 1.3), CF(O + V(0, 1.1, 0)), cor, nil, m, false)
	bola("Cabeca", 1.25, O + V(0, 2.5, 0), cor, nil, m, false)
	elipse("Rosto", V(0.95, 0.8, 0.2), CF(O + V(0, 2.45, -0.54)), claro, nil, m, false)
	for _, s in ipairs({ -1, 1 }) do
		elipse("Mancha", V(0.36, 0.24, 0.08), CF(O + V(s * 0.24, 2.56, -0.66)) * ANG(0, 0, rad(-s * 18)), C(85, 60, 45), nil, m, false)
		bola("Olho", 0.14, O + V(s * 0.24, 2.56, -0.72), C(25, 20, 20), nil, m, false)
		elipse("Perna", V(0.4, 0.9, 0.4), CF(O + V(s * 0.45, 0.4, -0.2)), cor, nil, m, false)
	end
	elipse("Sorriso", V(0.42, 0.06, 0.05), CF(O + V(0, 2.26, -0.66)), C(110, 70, 55), nil, m, false)
	fechar(m, b, false)
	if escala then m:ScaleTo(escala) end
	return m
end
local function criarTartaruga(nome, escala)
	local m, O, b = novoBicho(nome or "Tartaruga")
	local cor = C(120, 200, 110)
	elipse("Casco", V(2.2, 1.3, 2.6), CF(O + V(0, 0.8, 0.2)), C(90, 165, 95), nil, m, false)
	bola("Cabeca", 0.8, O + V(0, 0.95, -1.4), cor, nil, m, false)
	olhosB(m, O, 1.08, -1.72, 0.2, 0.16)
	elipse("Sorriso", V(0.3, 0.05, 0.05), CF(O + V(0, 0.82, -1.8)), C(50, 110, 60), nil, m, false)
	for _, s in ipairs({ -1, 1 }) do
		for _, z in ipairs({ -0.7, 1.0 }) do elipse("Pata", V(0.5, 0.36, 0.6), CF(O + V(s * 0.95, 0.2, z)), cor, nil, m, false) end
	end
	fechar(m, b, false)
	if escala then m:ScaleTo(escala) end
	return m
end
-- Ieti: 7 de altura na escala 1.
local function criarIeti(nome, escala)
	local m, O, b = novoBicho(nome or "Ieti")
	local cor = C(245, 248, 255)
	elipse("Corpo", V(4, 4.6, 3), CF(O + V(0, 3.0, 0)), cor, nil, m, false)
	bola("Cabeca", 2.6, O + V(0, 5.6, 0), cor, nil, m, false)
	elipse("Rosto", V(1.9, 1.5, 0.3), CF(O + V(0, 5.5, -1.14)), C(150, 195, 240), nil, m, false)
	olhosB(m, O, 5.75, -1.28, 0.42, 0.3)
	elipse("Sorriso", V(0.9, 0.12, 0.08), CF(O + V(0, 5.1, -1.3)), C(70, 110, 170), nil, m, false)
	for _, s in ipairs({ -1, 1 }) do
		elipse("Braco", V(1.1, 3.4, 1.1), CF(O + V(s * 2.3, 3.1, -0.2)) * ANG(0, 0, rad(s * 14)), cor, nil, m, false)
		elipse("PePeludo", V(1.5, 0.9, 2.1), CF(O + V(s * 0.9, 0.45, -0.3)), cor, nil, m, false)
	end
	for i = 1, 14 do bola("Pelo", 0.9, O + V(math.sin(i * 2.1) * 1.7, 1.4 + (i % 7) * 0.65, -0.9 - (i % 3) * 0.12), C(235, 240, 250), nil, m, false) end
	fechar(m, b, false)
	if escala then m:ScaleTo(escala) end
	return m
end
local function criarRoboP(nome, escala)
	local m, O, b = novoBicho(nome or "Robo")
	local cor = C(175, 195, 220)
	peca("Corpo", V(1.8, 2.0, 1.2), CF(O + V(0, 1.6, 0)), cor, Enum.Material.Metal, nil, m, false)
	peca("Cabeca", V(1.5, 1.2, 1.1), CF(O + V(0, 3.2, 0)), C(205, 220, 240), Enum.Material.Metal, nil, m, false)
	peca("Painel", V(1.0, 0.7, 0.06), CF(O + V(0, 1.7, -0.63)), C(60, 70, 95), nil, nil, m, false)
	for i = 0, 2 do bola("Led", 0.18, O + V(-0.3 + i * 0.3, 1.7, -0.68), ({ C(255, 80, 90), C(255, 210, 70), C(90, 240, 150) })[i + 1], Enum.Material.Neon, m, false) end
	for _, s in ipairs({ -1, 1 }) do
		bola("Olho", 0.36, O + V(s * 0.36, 3.3, -0.56), C(90, 220, 255), Enum.Material.Neon, m, false)
		peca("Braco", V(0.3, 1.5, 0.3), CF(O + V(s * 1.1, 1.7, 0)), C(150, 170, 195), Enum.Material.Metal, nil, m, false)
		cilindro("Roda", 0.6, 0.7, O + V(s * 0.6, 0.35, 0), C(60, 65, 80), nil, m, false)
	end
	cilindro("Antena", 0.6, 0.08, O + V(0, 4.1, 0), C(120, 130, 150), nil, m, false)
	bola("PontaAntena", 0.2, O + V(0, 4.45, 0), C(255, 80, 90), Enum.Material.Neon, m, false)
	fechar(m, b, false)
	if escala then m:ScaleTo(escala) end
	return m
end
local function criarPolvo(nome, escala)
	local m, O, b = novoBicho(nome or "Polvo")
	local cor = C(235, 110, 170)
	elipse("Cabeca", V(2.0, 2.3, 2.0), CF(O + V(0, 2.2, 0)), cor, nil, m, false)
	olhosB(m, O, 2.25, -0.92, 0.4, 0.3)
	elipse("Sorriso", V(0.5, 0.08, 0.06), CF(O + V(0, 1.8, -1.0)), C(160, 50, 110), nil, m, false)
	for a = 0, 7 do
		local q = rad(a * 45 + 22)
		elipse("Tentaculo", V(0.4, 1.8, 0.4), CF(O + V(math.cos(q) * 1.0, 0.7, math.sin(q) * 1.0)) * ANG(math.sin(q) * rad(30), 0, -math.cos(q) * rad(30)), cor, nil, m, false)
	end
	fechar(m, b, false)
	if escala then m:ScaleTo(escala) end
	return m
end
local function criarAlien(nome, escala)
	local m, O, b = novoBicho(nome or "Alien")
	local cor = C(130, 225, 120)
	elipse("Corpo", V(0.9, 1.3, 0.8), CF(O + V(0, 0.7, 0)), cor, nil, m, false)
	elipse("Cabeca", V(1.6, 1.3, 1.3), CF(O + V(0, 1.9, 0)), cor, nil, m, false)
	for _, s in ipairs({ -1, 1 }) do
		elipse("Olho", V(0.46, 0.56, 0.1), CF(O + V(s * 0.36, 2.0, -0.6)) * ANG(0, 0, rad(s * 15)), C(25, 25, 40), nil, m, false)
		bola("BrilhoOlho", 0.12, O + V(s * 0.3, 2.14, -0.68), BRANCO, Enum.Material.Neon, m, false)
		cilindro("Antena", 0.5, 0.06, O + V(s * 0.3, 2.8, 0), cor, nil, m, false)
		bola("PontaAntena", 0.16, O + V(s * 0.3, 3.05, 0), C(255, 220, 90), Enum.Material.Neon, m, false)
	end
	fechar(m, b, false)
	if escala then m:ScaleTo(escala) end
	return m
end
local function placa(nome, x, y, z, larg, alt, txt, corFundo, corTexto)
	local p = peca(nome, V(larg, alt, 0.12), CF(x, y, z), corFundo or BRANCO, nil, nil, cen, false)
	texto(p, txt, corTexto or C(40, 40, 60), BRANCO)
	return p
end
