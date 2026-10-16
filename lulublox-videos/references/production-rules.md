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
