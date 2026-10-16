# Production rules

They apply to every Lulublox Short. Most of them come from the user's earlier client feedback on the Roblox Shorts; follow them without waiting to be asked.

## Character and acting
- Lulu is an R15 girl avatar built by `K.criarGarota`. Her parts:
  - peach skin;
  - long chestnut hair with side-swept bangs, side locks and a pink bow;
  - pink top with puffy sleeves, a purple pleated skirt and white sneakers with pink soles;
  - a cartoon face with big eyes, violet irises, lashes, thin brown eyebrows and blush.
- Hair, bow, sleeves, sneakers and skirt are soft `Visual` parts welded to her body. The skirt opens with her legs every frame (walking, running, jumping and sitting), so her legs never cut through it.
- Movement uses the official Roblox packages: Cartoony for locomotion, Levitation for floating and the R15 emotes (`wave`, `point`, `laugh`, `cheer`, `dance`, `sit`). Do not invent locomotion poses.
- **The mouth moves with the real voice** (`K.falar` with the MP3 envelope). A line never plays with a still mouth.
- No shaking during the countdown: reactions come from expression, gaze and animation.
- Every animation change must be clean. Check the frames before, during and after each change.

## Camera rule no. 1: the face is the star
- The head fills at least 10% of the frame height (close-up 22–26%, medium 14%, wide 10%), with the eyes in the upper third.
- The camera stays within 45° of where she looks and never shows her back without a story reason. Compute the camera from the real head direction.
- Every important event ends in a reaction close-up of at least 1 s.
- Objects, effects and captions never cover her eyes and mouth for more than 0.3 s. The karaoke caption sits at ~0.665–0.72 of the height, so her whole face stays above it.
- A following camera aims **below** the head (`cam.seguir(noob.Head, offset, t, V(0, -1.5, 0))`).
- Shots without Lulu (showing the options) are short inserts marked with `K.inserto(true)`.
- `K.auditarCamera` and `K.auditar` must both end with zero problems.

## Face
- Expressions by moment:
  - tension or countdown: `scared`/`nervous`;
  - shock or fall: `scream`;
  - relief or victory: `happy`;
  - question: `surprised`;
  - tumble: `dizzy`/`knockout`;
  - charm and endings: **`wink`**;
  - calm: `normal` (small smile).
- No floating sweat-drop stickers; the sweat drop belongs to the face.

## Cuts
- Dry cuts, with no white flash or effect on the cut. When she changes place, the first frame of the new shot already has the right pose (`K.cortarPara`).
- Chained moves (slide → flight → landing) end on timeline times, and the landing cut happens on the real landing.
- Frame sync: mouth, cuts and sound effects on the same frame (sync marks in the recording).

## Collisions in 5 beats
1. Threat (≥ 0.6 s): the obstacle shows first, with a close-up on her face.
2. Speed-up (0.4–0.8 s): Lulu and the obstacle in the same shot.
3. Real contact (2–4 frames): it really touches, with squash, a short freeze and a light shake. The sound effect starts only there.
4. Stuck or slipping (0.5–1 s).
5. Consequence: she falls with real gravity and never floats still after an impact.

## Lines, voice and continuity
- English only, with Lulu's voice: ElevenLabs "Jessica - Playful, Bright, Warm" (My Voices, ID cgSgspJ2msm6clMCkdW9), model Eleven v4, an emotion tag at the start of each line and no accent tag.
- The intention line comes before the action; the reaction starts on the event.
- No stutter or wrong words: fix the source audio. A correct caption does not fix a wrong line.
- Measure the lines first, then fit the action timing.

## Captions
- A caption never announces what has not appeared yet. The cut to an option lands on its word ("yellow"), and the phrase that starts before it only shows at the cut (`legendas_karaoke(..., cortes=)`).
- Show one idea at a time and keep the screen clean in pauses.
- A chunk never ends on "a/the/of/to/and/my…".
- Style: Lilita One in white, outline `#10283E` and a downward shadow. The spoken word is `#FFE54F`, numbers are cyan, and "no/not/never" are coral. Each group pops in elastically, inside the lower safe area.

## Edit and sound
- A full 5 s countdown after "Pick fast!", with a clock tick and puzzle music during the decision, then lively music on the celebration.
- A sound effect on every action (step, jump, whoosh, impact, fall), chosen by the event and with a recorded source.
- No effect over a line: whooshes and drum rolls end before the word or land in the pause.
- **No sound effect is ever cut in the middle.** Every effect plays to its end. Continuous sounds (a ringing alarm, wind, water) go in as one continuous track with volume automation, never as restarted chunks. The music ends with a 1.2 s fade.
- No camera move or zoom is cut before it ends (`c.ate_corte`).

## Image
- 1080×1920, bitrate ≥ 12 Mbps (CRF ≤ 18), no Studio/Roblox interface, no cursor, no borders.
- A living, textured set (clouds, trees, flowers, props), with Future lighting, Atmosphere, Bloom and ColorCorrection.
- Indoors, avoid lots of white, strong PointLights, Neon and semi-transparent beams between the camera and Lulu: they wash out the image. Use mid-tone colors and weak lights.

## Camera tricks that pass the face audit
- Spins, loops and flips show her back: shoot them as inserts (`K.inserto(true)`), because "de costas" always counts.
- On rides (swings, rockets) keep her on the ride by moving her root in the same function that moves the ride
  (never in a separate Heartbeat: she lags one frame behind and jitters). A **ride-along camera** bound with
  `RunService:BindToRenderStep(name, Enum.RenderPriority.Camera.Value, fn)` (before the kit camera and the audit)
  keeps her face in frame even upside down.
- A camera that `cam.rosto` computes in the same frame as a big move can still see the old place: when an
  animation (`animar`) also calls `cam.corte` every frame, end it **before** the cut that changes the scene.
- Tall props (a tower of scoops, a giant cake): the face still needs ≥ 8% of the frame height and must stay above
  the caption band (0.665–0.75). Crop the top of the prop instead of shrinking her face; show the whole prop in an
  insert.
- Things she holds in front of her (a magnet, a bowl) and things that stick to them stay below her chin from the
  front camera; check the `[camera-detalhe]` lines for the face position.
- Water: the pond is a non-solid part, and nothing solid (grass, baseplate) may stay under the area where she sinks.

## Variety inside a batch
- Do not repeat the same punchline in a row (things landing on her head, a 1-10-100 escalation): change the
  mechanic or the twist and spread similar ideas apart in the schedule.

## Found in the 2026-10-16 review (check these in every contact sheet)
- **Sitting**: the `sentadoReto` pose (legs straight out) points her sneaker soles at a front camera: two big
  pink squares in front of her body. On swings, tires, floats and boats use the plain `sentar` animation (knees
  bent, legs hanging). Keep `sentadoReto` only when she sits on the floor, and shoot it from a high
  three-quarter angle.
- **Things she holds** (a beach ball, a bowl, a giant magnet, a basket) go below her chin: hold them low, or
  raise the camera. The camera audit does not see props covering her face.
- **Option inserts**: the number cards go on the table's front edge, below the objects (never standing in
  front of them), and the shot uses a fixed focus (`K.foco(nil)`, back to `K.foco(noob.Head)` when she is on
  screen again). Otherwise close objects come out blurred.
- **No jump cuts**: a cut needs a clearly different camera (angle or size). Two nearly identical shots look
  like a glitch: keep one shot and move the camera instead.
- **Wide inserts of small fast things** (a ball, a paper plane) need a trail or a bigger prop to read on a
  phone.
- **Studio panel over the viewport**: Studio's Creator Store panel sometimes opens over the left side of the
  3D viewport. `captura_janela.processar` detects it from the recorded region and centres the 9:16 crop on the
  real viewport (`[captura] viewport partly covered`). Without that, everything sat 10% too low and faces went
  behind the captions.

## Found in the 2026-10-16 feedback (user) and the 2026-10-23 batch audits
- **The skirt must never jump.** The kit opens and closes each pleat smoothly (soft weights, time-constant
  smoothing and a speed limit in `atualizarSaia`); never set a pleat angle directly in a scene.
- **Effects are never cut and never cover a word.** Use `ed.sfx_livre(cat, t)` in every edit: it places the
  WHOLE sound in the nearest pause (±0.3 s), and when it does not fit it swaps to a shorter whole sound
  (`RESERVA`: impacto → impacto_curto, explosao → explosao_curta, brilho → brilho_curto, apito_sobe →
  apito_sobe_curto, ...). The short ones are synthesized by `scripts/criar_sfx_inteiros.py` and end on their own.
  A skipped effect (no pause at all) is better than a cut one. `conferir_sfx.py` must report 0 for every video.
- **Fewer, softer cuts.** Prefer one continuous shot with camera travels, follow cameras and ride-along cameras;
  cut only when the story changes place or time (a big poof or a flash can hide it). Most videos of the batch
  have 0 or 1 cut.
- **Follow camera**: `cam.seguir(raiz, offset, 99, ...)` and end it with the next cut. The scene clock can run
  behind `os.clock()` (Studio in the background), so a follow with an exact duration ended ~1 s early and she
  fell out of the frame.
- **Welded props**: `soldar` makes the prop massless (a big welded sheet or hat dragged her 0.4 into the floor).
  Weld only in the same frame as the prop's last move (`animar(..., function(k) ...; if k >= 1 then soldar(...) end)`),
  never in a `task.delay` next to a `mover` (the move's last frame then drags her whole body). Unweld (`soltar`)
  before re-positioning a welded prop: `PivotTo` on a welded model moves the character too.
- **Every model needs `fechar(m, primaria)`** (PrimaryPart): `soldar`/`soltar` crash without it and the scene
  stops before the first camera move ("rosto fora do quadro" from 0 s).
- **Laughing in a close-up**: the `rir` animation throws her head back ("de costas"); use little hops (`pulo`)
  and the happy face instead.
- **Selfie / point-of-view shots**: aim the camera below her face (target ~0.7 under the eyes); with the camera
  at eye level and the target higher, the face slides into the caption band.
- **Lines never overlap**: check that every line starts ≥ 0.15 s after the previous one ends (long tags like
  "Ah! Too high!" make a line longer than the event it covers).
