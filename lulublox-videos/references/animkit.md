# AnimKit — quick reference

`ReplicatedStorage.AnimKit` (ModuleScript; source in `luau/AnimKit.lua`, installed by `studio_runscript.py montar --kit`). Function names are kept from the original kit (some are Portuguese); the English aliases below work everywhere.

## Constants

| Name | Default | Use |
|---|---|---|
| `K.VERTICAL` | `true` | Camera rolled 90°: the 9:16 frame uses the whole viewport; `captura_janela.processar` turns it back. |
| `K.FOV` | 50 | **Horizontal** field of view of the final vertical video. |
| `K.CABECA` | 1.0 | R15 `HeadScale` (standard proportions). |
| `K.CORES` | Lulu's palette | `pele`, `camisa` (top), `saia`, `calca` (legs), `tenis`, `cabelo`, `laco`, `iris`, `sobrancelha`, `labio`. Pass a table to `criarGarota` to change any of them. |
| `K.ALTURA_RAIZ` / `ALTURA_SENTADO` / `ALTURA_DEITADO` | 3.41 / 1.32 / 0.95 | Measured R15 heights of the HumanoidRootPart above the floor (idle), the seat (sitting) and the floor (lying). |
| `K.ATRASO` | 0.8 | Seconds between the magenta flash and timeline t=0. |
| `K.MARCAS` | 5 | Seconds between sync marks (magenta strip at the top of the viewport, cropped by the recording). |
| `K.ROSTO_TAM` / `ROSTO_LUZ` / `ROSTO_FAIXA` | 1.0 / 0.6 / {0.06, 0.97} | Face plate size, how much scene light affects the drawing, and the drawn vertical band (used by the camera audit). |
| `K.MARGEM_TOPO` | 0.075 | Top strip of the viewport cropped by the recording. |
| `K.FAIXA_LEGENDA` | {0.665, 0.75} | Video band used by the karaoke caption; her face must stay out of it. |

## Building (edit mode, in `cenario.lua`)

| Function | Use |
|---|---|
| `K.visual()` | Saturated colors, bloom, atmosphere, background blur; turns off `CharacterAutoLoads`. |
| `K.bloco{Size=, CFrame=, Color=, Material=, Name=, Parent=}` | Smooth anchored part. |
| `K.piso(part)` | Marks the part as floor (attribute `Piso`). **Mark every floor and platform anyone stands on.** |
| `K.chao(pos)` | Height of the marked floor at (x, z). |
| `K.emPe(pos, lookAt)` | CFrame standing exactly on the floor (y of `pos` is ignored). |
| `K.deitado(pos, headDir)` | Lying on her back on the floor, face up. |
| `K.criarGarota(name, CFrame, colors)` (= `K.criarNoob`) | Lulu: R15 standard proportions, cartoon face plate (big eyes with violet iris, two highlights and 3 lashes, thin brown brows, blush, sweat drop), hair with bangs/side locks/back strands, pink bow, puffy sleeves, pleated skirt that reacts to the legs, sneakers. Name the model `"Lulu"` (the base `comum.py` waits for it). |
| `K.escorregador(name, {topo=, dir=, comprimento=, queda=, cor=, corBorda=, largura=, segmentos=, curva=})` | Stairs, platform, straight or spiral slide and rails; stores the **seat points** in `Caminho`. |

## Acting (play mode, in `cena.lua`)

| Function | Use |
|---|---|
| `K.rosto(lulu, expr, t)` | Expressions: `normal` (small smile), `happy`, `smile`, `surprised`, `scared` (+ sweat), `scream` (+ sweat), `nervous`, `confident`, `angry`, `doubt`, `dizzy`, `squint` (>_<), `knockout` (X eyes) and **`wink`** (one eye closed "^" with an open smile). Portuguese names (`feliz`, `sorrindo`, `surpreso`, `medo`, `grito`, `piscadinha`…) also work. One controller per frame merges expression, blink, gaze and speech. |
| `K.olhar(lulu, dx, dy, t)` | Iris direction, −1 to 1. |
| `K.piscar(lulu)` | Automatic blinks (the eye squashes and returns in 0.16 s; the lashes follow). |
| `K.anim(lulu, name, {loop=, velocidade=, fade=, manter=})` | Cartoony (`idle`, `idle2`, `walk`, `run`, `jump`, `fall`, `climb`, `swim`), Levitation (`float`, `flyPose`, `superJump`) and R15 emotes (`sit`, `wave`, `point`, `laugh`, `cheer`, `dance`). Portuguese names also work. Call `K.preCarregar(lulu)` before the scene. |
| `K.falar(lulu, envelope, fps)` | Lip sync from the real voice volume (`scripts/envelope_boca.py`): closed mouth + 3 open ovals with tongue, each held ≥ 60 ms; brows lift on emphasis. |
| `K.bracos(lulu, pose, t)` | Arm poses (`segurarFrente` hold in front, `segurarAcima` hold above, `arremesso` throw, `esticarCima` reach up, or your own table). |
| `K.pose(lulu, name)` | Fixed pose on top of the animation (`sentadoReto` sit straight, `bracosPraCima` arms up, or your own table); `nil` clears it. |
| `K.mover(lulu, Vector3, t, anim)` | Walk/run to the target with feet on the floor. |
| `K.deslizar(lulu, K.caminho(model), t, anim, onEnd)` | Slide down sitting, tilted with the ramp, clock-driven (ends exactly at `t`). |
| `K.voar(lulu, target, height, t, turns, anim, onLand)` | Arc with side rolls (the face keeps facing the front camera); with a `CFrame` target (`K.deitado`) it ends in the landing pose. On landing switch to `idle` and cut with `K.cortarPara`. |
| `K.tremer(lulu, t, amp)` / `K.poeira(pos, n)` | Shake and a dust puff. |
| `K.camera.rosto(lulu, dist, fovH, {lado=, altura=, queixo=, t=})` | Close-up from the real head: head in the upper third. `t` makes it a dolly. For objects held in front of her, use a telephoto (larger `dist`, smaller `fovH`). |
| `K.camera.corte(pos, target, fovH, up)` / `K.camera.mover(pos, target, t, fovH, style, up)` | Cut and dolly; `up` sets the frame's up vector (e.g. `V(0,0,1)` to film her lying from above). |
| `K.camera.seguir(part, offset, t, aim)` | Follow keeping the offset; following `lulu.Head` use `aim = V(0, -1.5, 0)`. |
| `K.camera.tremor(i, t)` / `K.camera.soco(i, t)` | Camera shake and punch-zoom. |
| `K.cortarPara(lulu, cf, anim, camera, {pose=})` | Cut with teleport and no frame of her "old pose in the new place". Use it on every cut that moves her. |
| `K.foco(part)` | Background-blur focus follows the part every frame. |
| `K.rodar(events, duration)` | Hides the UI, prepares the first frame (events with t ≤ 0), magenta flash, fires the events, final flash and `K.encerrar()`. |

Events with t ≤ 0 only prepare the first frame; movement starts at t ≥ 0.05.

## Skirt

The skirt is 18 pleat panels welded to `LowerTorso` with adjustable welds. In play mode `AnimKit` updates them every frame:
- each pleat opens just enough to keep every leg corner inside it, plus 0.1 stud;
- it opens instantly and falls back with a 0.12 s ease;
- neighbouring pleats differ by at most ~13°.

The parameters live in model attributes (`SaiaRx`, `SaiaRz`, `SaiaTopo`, `SaiaAlt`, `SaiaAbre`, `SaiaLarg`).

## Audits (mandatory before recording)

| Function | Use |
|---|---|
| `K.auditar(lulu)` | Collisions: body parts inside the floor/objects, with time and part (`[auditoria]`). Soft parts (`Visual`: hair, bow, sleeves, sneakers, skirt) are skipped. |
| `K.auditarCamera(lulu, min)` | Camera rule no. 1 measured on the final 9:16 frame (`[camera]`): face too small, back to camera, profile (> 0.5 s), off frame, cut at the edge (> 0.2 s) or in the caption band (> 0.3 s). |
| `K.inserto(true/false)` | Marks shots without Lulu (showing the options). |
