# Right the first time: plan every shot before writing Lua

The user asked (2026-10-16) for videos that come out right on the first recording: every re-record costs time and
tokens. In the 2026-10-23 batch, 13 of 16 videos were recorded twice. Every reason is listed below. Do this planning
**before** writing `cenario_corpo.lua`/`gerar_cena.py`, and run `scripts/lint_cena.py` (auditar.py runs it first) so
the known mistakes never reach Studio.

## 1. Beat table first (in the gerar_cena.py docstring)

For every beat write: time cue, where Lulu stands, where the key object is, where the camera is, and **what must be
visible** (her face + the thing the joke is about). Then check each row:

- **Line of sight.** Nothing stands between the camera and the joke. Lulu is never in front of the door, machine,
  skeleton or ghost that the beat reveals: put her 1.5–2.5 studs beside it, with the object on the side away from her
  prop arm (her right hand holds the bucket → the reveal is on her right only if the arm stays low).
- **Containers show their contents.** A box with things inside it is built hollow (back, sides, top, bottom, a front
  frame around the glass), never one solid block with props inside.
- **The prize/payoff is in the last shot.** If the punchline is an object (toasted marshmallow, candy pile, robot
  hug), that object is in frame during the punchline line, not only earlier.
- **Description and tags** only mention what the final video shows (no "water bed" when the video has two beds).

## 2. Camera

Lulu's real size, measured in renders (table of known width as the ruler): about **7 studs tall** (face around
y 6.5-7) and about **4.5 studs wide** in the idle pose (arms out, puffy sleeves). A 3-stud "giant" pumpkin looks
small next to her: a "giant" prop must be 4+ studs. Plan with these numbers:

- Width budget: at FOV 52 the frame is about 0.98 × distance wide, and the face rule (≥ 8%) caps the distance
  at about 9.5 studs, so the frame is at most about 9.3 studs wide. Her 4.5 studs plus the props must fit in about
  8. Keep her root within about 2.0 studs (x) of the camera target at 8–9 studs (the frame is about 8.3 studs wide
  there). Further out, her arm and body get cut at the frame edge even when the face passes the audit.
  `lint_cena.py` warns about this.
- The joke object goes at least about 3.5 studs (x) from her root: an easel, wheel or oven closer than that ends
  up behind her arm (09 easel at 1.7, 08 wheel at 2.1, 12 oven at 1.6). A small character next to her (a bird, a
  kitten) needs its own spot beside her head or in front of her, never at her side where her arm hangs.
- Small props are tiny next to her: scale a sock, cookie or robot vacuum 1.5–2.2×.
- Check the background right behind her head. A big round treetop or balloon there looks glued to her head.
- Don't stack brown cylinders into a cone (it looks like a poop emoji). Use many thin gray tiers for a volcano.
- PointLights inside props near the floor leave a yellow stain on the grass. Keep their Range at about 1.5, or
  use Neon only.
- Objects on the ground in front of her (a pet rock, a sock) land in the caption band (0.665–0.75) at a medium
  shot. Put a joke object on a table or stool (y ≥ 2), or keep the key moment in a pause between lines, when no
  caption is on screen.

- A medium shot is 6.5–8.5 studs from her with FOV 46–52. Closer than about 6 studs makes her hands and props
  huge. A close-up uses `cam.rosto`.
- Aim below her face: the target is about 1 stud under the eyes. The face sits in the upper half, never in the
  caption band (0.665–0.75).
- Selfie/POV shots: the camera is about her eye height and aims about 0.7 under the eyes.
- Follow shots use `cam.seguir(raiz, offset, 99, ...)` and end with the next cut, never with a fixed duration.
- Ride-along cameras use `BindToRenderStep(Camera.Value)`. They start from the current camera CFrame, blending
  over about 0.35–0.6 s so the switch is not a jump. Start the blend at the same instant as the motion, and make
  the motion start gently (smoothstep), or she leaves the frame before the camera catches up (trampoline launch).
- Show where she is. On an obby, rope, roof or ramp, raise the camera (offset y about 3.5) and look down at her,
  so the platforms below are in frame.
- Wide shots of a big object (a ramp, the snowman) must still keep her face at 8% of the frame height or more.
  In numbers: at FOV 52 the camera can be at most about 8.4 studs from her (the frame is then about 14.6 studs
  tall). At 9.2 studs with FOV 55 the face drops under 8%. If everything doesn't fit, make the props smaller
  or closer together, not the shot wider. In a ride loop, check the farthest point of the path too.
- A default `CFrame.new(pos)` already faces -Z (the camera). Never add `ANG(0, math.pi, 0)` to "face the camera":
  that turns her back to it.
- Cuts: 0–1 per video, only when the place or time changes. Hide a cut in a poof or a flash.

- The face-size check is tight at 8.8+ studs: a lean back, a pull-back or a step away from the camera drops it below
  8%. Start at 8.3–8.6 studs, or dolly in while she leans.
- A slide that comes down TOWARD the camera (`K.escorregador` with `dir = V(0, 0, -1)`) lets her slide facing us;
  sideways slides are profile shots. Use `largura = 5` or more and keep her arms up until she leaves the borders.

## 3. Hands and props

- Hold things low against her belly, with arms `{ LeftShoulder = { 35, -15 }, RightShoulder = { 35, -15 },
  LeftElbow = { 75, 0 }, RightElbow = { 75, 0 } }`. Weld the prop about 0.3 up and 0.8–1.0 forward of the root.
  `segurarFrente`/`segurarFrenteJunto` put her hands at chin level.
- Things moving around her (juggling balls, snowballs being lifted) stay below the chin. They rise at her side,
  never across her face.
- Arms coming down from above go out to the sides first: `{ x 10, z 95 }`, then `nil`. Coming straight down
  through the front, the hands sweep through counters and tables.

## 4. Materials and light

- Use SmoothPlastic for white cloth (ghost sheets, bed sheets). Light-colored Fabric renders as gray knit.
- Neon only on small accents (eyes, buttons, lamps). A big Neon floor or panel, or Neon close to the camera,
  washes the frame to white. The same goes for a part stuck to the lens: use SmoothPlastic plus a weak PointLight
  of about 0.9.
- Light brightness: 0.8–1.3 indoors, spotlights at most 1.3. A dark room still needs a soft front light (about
  0.5) for her face.

## 5. Physics and welds

- Every `modelo()` gets `fechar(m, primary)`. Otherwise `soldar`/`soltar` crash, and the scene stops before its
  first camera ("rosto fora do quadro" from 0 s).
- Weld in the same frame as the prop's last move: `animar(..., function(k, e) ... if k >= 1 then soldar(...) end
  end)`. Never `mover` and then `task.delay(soldar)`.
- `soltar` a welded prop before moving it again with `PivotTo`/`CFrame`. Moving a welded prop drags her whole
  body.
- Sitting with the `sentar` animation needs the seat at least 1.6 above the floor, or legs hidden inside
  non-colliding stuff (water, cloud, leaf pile).
- Parts you tween one by one (Size/CFrame, like a sandcastle melting) must be anchored and unwelded first.
  `fechar()` welds a model's parts to its primary part.
- Hiding her inside an object (popping out of a cake) still needs her feet on the floor: the audit flags legs
  under the floor even when no one can see them. Make the object taller than her (head top is about root + 2.8)
  instead of sinking her.
- Models whose primary part is a `cilindro()` carry a 90° Z rotation in their pivot. To place one (a crown, a
  lampshade) use `target * ANG(0, 0, rad(90))`, or rotate around a saved `rel = CF(center):Inverse() * pivot0`.
- A model that grows out of something (a cake out of the oven) gets an invisible primary part at its base, so
  `ScaleTo` grows it upward.
- Lay out moving characters on paper first: list every path (puppy, vacuum) with its start and end points and
  times, and check the closest distance to her body (more than her half width 0.7 plus theirs).

- Never weld an object (`soldar`) while an `arco()`/`mover()`/`animar()` still moves it: the next `PivotTo` of the
  welded object drags her whole body (in the 2026-10-31 basketball she stayed in profile for the rest of the video).
  Weld inside the animation's final callback, or let the flight end 0.15 s before the catch.
- Two Lulus (clones, twins) side by side touch hands unless they are 4.6+ apart at the same depth; put the second
  one ~2 studs further back instead. The `dancar` emote swings the arms ~2.7 studs: keep dancers 3.5+ apart.
- In `cenario_corpo.lua` `CF` is `CFrame.new` (a function): write `CFrame.lookAt`, never `CF.lookAt`.
- Leaning her (limbo, sneeze build-up): rotate around the FEET point, `CF(feet) * ANG(lean, 0, 0) * CF(0, ALT, 0) *
  ROT`, and lift her 0.25 while leaning when she walks (the toes of the walk swing lower).

## 6. Timing and sound

- Leave a pause after each impact before the next line (0.5–0.8 s), so the whole sound fits: `sfx_livre` swaps in
  a short sound or skips it otherwise.
- Lines never overlap. Long emotion tags (laughs, screams) make a line longer than the event it covers: the next
  beat waits for `fim_fala`.
- No `rir` animation in close-ups: it throws her head back. Use `pulo()` with the happy face.

## 7. One verification pass

Run lint and the audit (0/0), then record once. Review the contact sheet against the beat table: is every "must
be visible" item visible? Also grep the audit log for Lua runtime errors (`attempt to`, `nil value`,
`is not a valid member`, `Infinite yield`). The audit totals do not count them.

Result of the 2026-10-17 batch (14 videos written with this checklist): 10 of 14 scenes passed the Studio audit on
the first run. Four needed one fix each: a too-wide shot, a ride camera starting late, legs under the floor in the
cake, and a cloud puff over her chest that was caught before running.

Result of the 2026-10-31 batch (20 videos): lint caught a held prop at the chin and a too-bright flash before any
run; 12 of 20 passed the Studio audit at once. The fixes: clones touching her hands (moved back), a hug ring and a
lean-walk touching the table/floor, two face-size dips (camera closer), a CF.lookAt typo, the weld-while-flying bug
above, and arms hitting the slide borders. `auditar.py` prints only 60 lines: read `NN/auditoria.log` for all of it.

## 8. What the audit cannot see (contact-sheet lessons of 2026-10-31)

The audit checks collisions and the face size, not what covers the face or whether the joke reads. Plan for these:

- Anything in front of her face hides it: a pile she lands in (compute the surface height at HER spot, face at
  ~6.5), a bubble from her mouth (grow it sideways and a bit back), held props, foam, a beard (put it on the chin,
  under the mouth). `segurarAcimaJunto` / `segurarAcima` put the hands at FACE height (root + 2.2): holding
  something over her head needs `esticarCima`.
- Never tint the skin or the head (wet, chocolate, cold): it reads as a gray or sick face. Tint clothes and hair only
  and put blobs on the skin where they contrast (cheeks, forearms, shins); brown on brown hair does not show.
- The payoff object must be whole in the frame at its moment: a sign, a tent, a hoop or a gnome at x 4.4+ with the
  camera at x 0.4-0.6 is cut. Keep key props within ~3.5 studs of the camera x at 9-11 studs depth.
- A ceiling, a floor pattern or a spiral only reads if the camera sees it: give a ceiling its own color and beams,
  tilt the camera toward it, and look down ~30 degrees at floor layouts.
- Big props lying toward the camera (fallen giant dominoes) cover what is behind them.
- Sitting (`sentadoReto`) with the legs toward the camera shows two blocks in front of her body: let her stand
  in the pot/tub instead (legs hidden by its walls).
- Lasers, ropes and beams that run toward the camera pass IN FRONT of her: end them before her depth.
