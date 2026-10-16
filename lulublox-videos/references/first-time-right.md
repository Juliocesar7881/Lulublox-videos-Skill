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
