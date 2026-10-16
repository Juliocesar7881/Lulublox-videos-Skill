---
name: lulublox-videos
description: "Create animated Roblox Shorts for kids (9:16, ~25-35 s) starring Lulu, a charismatic and cute girl avatar, entirely in English: original kid-friendly script, Lulu's ElevenLabs voice (Jessica), scene built and animated in Roblox Studio through the official command line (no clicks), recording only the Studio window, and a punchy final edit with word-by-word captions, SFX and music."
---

# Lulublox Videos

Turn an idea from the user ("make one about which slide is the fastest") into a vertical Short that is **ready to post**, animated in Roblox Studio. The star is **Lulu**, a charismatic and cute R15 girl avatar:

- Peach skin and long chestnut hair with side-swept bangs, side locks framing the face, and a pink bow.
- Cartoon face: big oval eyes with violet irises, two highlights and lashes; thin brown eyebrows; blush; a mouth that moves with her voice.
- Outfit: pink top with puffy short sleeves, a purple pleated skirt that opens with her legs (they never cut through it), and white sneakers with pink soles.
- Animated with the **official Roblox packages** (Cartoony, Levitation and R15 emotes).

The audience is kids. Read [references/production-rules.md](references/production-rules.md), [references/format.md](references/format.md) and [references/animkit.md](references/animkit.md) before starting, and [references/youtube-studio.md](references/youtube-studio.md) before posting.

**Everything is in English, always:** script, voice, captions, on-screen signs, video title, description, tags and file names. Never produce Portuguese or Spanish lines for this skill. After the voice lines are ready, run `scripts/fazer_short.py PROJECT`. It runs the audits, records, edits, reviews the captions and renders, and only finishes with the final MP4. `--so-conferir` only checks the delivery.

This skill depends on the sibling skill `roblox-video-editor` (renderer, SFX/music library and stickers). The repository's `install.py` checks for it.

## Lulu's voice: Jessica (ElevenLabs, free default voice)

Lulu always speaks with **"Jessica - Playful, Bright, Warm"**, chosen by the user on 2026-10-15. It is a free default (premade) voice in **Voices → My Voices**, voice ID `cgSgspJ2msm6clMCkdW9`. Check the ID, not only the name. In each project's `roteiro.json`: `"vozes": {"lulu": "Jessica"}`. Do not switch to another voice unless the user asks.

- Model **Eleven v4**, language Automatic. Write each line in English with an emotion tag at the start, for example `[excited] Hi friends!`, `[giggles] Oops!`, `[gasps] No way!` or `[whispers] Shh...`. Do not add an accent tag.
- The Explore tab copies of these voices may ask for a paid plan. Always use the copy in **My Voices** and never suggest paying.
- How to generate and download the lines:
  - With an API key in `ELEVENLABS_API_KEY` (the user sets it): `python scripts/tts_elevenlabs.py roteiro.json --out falas`.
  - Without a key: in the user's logged-in browser, type each line, generate it with Ctrl+Enter and keep the `eleven_v4` take of the two the site creates. Move the files with `scripts/receptor_falas.py PASTA` (local server on 127.0.0.1) and `postMessage`. Then `python scripts/alinhar_falas.py roteiro.json falas` aligns them with Whisper (English).
  - Never type the user's password or keys.

## Originality in every video

Every new video needs an **original idea and script** in the kids' style of this skill. Before writing, read [historico/roteiros.md](historico/roteiros.md) and the `roteiro.json` files under `entregas/`, then compare premise, goal, mechanic, attempts and twist. Changing colors, names or the object of the same challenge does not make an idea new. Save `originalidade.json` in the project (`premissa`, `objetivo`, `mecanica`, `tentativas`, `reviravolta`, `projetos_comparados`, `diferenca_dos_anteriores`). After producing, log the script with `python scripts/registrar_roteiro.py PROJECT`.

## How Studio is driven (no MCP, no clicks)

Roblox Studio's command-line task runs a script on the place in edit mode and starts Play: `RobloxStudioBeta.exe -task RunScript -localPlaceFile place.rbxlx -runScriptFile script.lua -outputFile out.log -quitAfterExecution`.

- `scripts/studio_runscript.py montar --kit --cenario studio/cenario.lua --cena studio/cena.lua --play --saida studio/pipeline.lua` installs this skill's AnimKit, builds the set, installs the scene and runs Play.
- `scripts/studio_runscript.py rodar studio/pipeline.lua --place studio/base.rbxlx --gravar viewport.mp4` opens a new Studio window behind the user's windows and records **only that window**. Never record the whole desktop.
- The user's own Studio windows are never touched.
- **The display must be on to record.** With the monitor off or asleep, Studio does not draw the 3D viewport (the
  window capture gets a black viewport at ~2-4 fps and never sees the start flash). Audits still work with the
  display off: write and audit every scene, then record when the monitor is back.

## Workflow

1. **Project and original idea**: create `entregas/<topic>-<date>`. Copy `modelos/base/` (`comum.py`, `edicao.py`, `cenario_comum.lua`) next to the project folders as in a batch: each project has `gerar_cena.py`, `montar_edicao.py`, `studio/cenario_corpo.lua` and `roteiro.json`.
2. **Script** (`roteiro.json`): English `texto` for each line, `titulo`, `arquivo` (MP4 name), `"idiomas": ["en"]`, `vozes`, `destaques` (words in yellow) and a plan per line. Short lines, one idea each, with an emotion tag for ElevenLabs. Format in [references/format.md](references/format.md).
3. **Voice**: as described above.
4. **Set** (`studio/cenario_corpo.lua`):
   - Colorful and alive, with props around.
   - Mark every floor with `K.piso(...)`.
   - Create Lulu with `K.criarGarota("Lulu", K.emPe(pos, lookAt))`.
5. **Scene** (`gerar_cena.py` → `studio/cena.lua`):
   - The timeline comes from the real voice timings, and every line has `K.falar` from the MP3 envelope.
   - Expressions follow the emotion: `happy`, `smile`, `surprised`, `scared`, `scream`, `nervous`, `confident`, `angry`, `doubt`, `dizzy`, `squint`, `knockout` and **`wink`**, her signature.
   - Use dry cuts and `K.cortarPara` when she changes place.
   - Camera moves end before the next cut (`c.ate_corte`).
6. **Automatic audit and fixes (mandatory)**: `K.auditar(noob)` (collisions) and `K.auditarCamera(noob)` (face rule) must end with `total 0`. Her hair, bow and skirt are soft parts (`Visual`) and are not audited. In a batch, `python auditar.py NN-project ...` (copied from `modelos/base/`) runs `gerar_cena.py`, builds and plays each scene in Studio without recording and prints only the audit lines. Then review the frames around every cut, including every 60 fps frame from 0.05 s before to 0.1 s after each cut.
7. **Edit** (`montar_edicao.py` → `roblox-video-editor` renderer, `"entrega": "shorts"`):
   - Karaoke captions in English, one idea at a time.
   - A chunk never ends on an article or preposition; "no", "not" and "never" are shown in coral.
   - SFX on every action.
   - Never cut an effect in the middle, and never cut before a zoom ends.
   - Short licensed music at −24 dB under the voice.
   - **No effect over a spoken word**: `python conferir_sfx.py NN-project` (from `modelos/base/`) lists every effect
     that plays over the voice; fix them all (move the action to a pause, pick a shorter sound or a pitch up).
   - Stickers only in English: `wow-en`, `oops-en`, `haha-en` (plus `confete`, `interrogacao`, `estrelas-tontas`,
     `check`). Never `wow`, `oops`, `kkkk` or `tum` (they read in Portuguese).
8. **Final review**: `revisar_legendas.py` total 0, about −14 LUFS with peaks under −1.5 dBTP, Whisper transcript of the final audio in English, and frame checks.
9. **Delivery** (`fazer_short.py PROJECT --so-conferir`): the final MP4 plus `publicacao.txt` with an English title, description, hashtags, music credits and voice credit.

## Posting (LuluBlox YT)

- Channel: **LuluBlox YT** only. Two videos per day, **09:00 and 18:00** of the same day (`lote.py agenda`).
- Made for kids: yes. Category Gaming with the game title Roblox. Video language English.
- `lote.py metadados` writes the SEO title/description/tags and the credits; the user makes the thumbnails.
- The upload and scheduling steps in YouTube Studio are in [references/youtube-studio.md](references/youtube-studio.md).

## Content rules (kids)

- Original scripts. The user's references are only a format guide.
- No real Robux promises, links, requests for personal data, scary content, humiliation or bad words. Twists are silly and light.
- No third-party characters, logos or music.
- Lulu is kind, curious and funny. She can fail and laugh about it, but she is never mean.
- Vary sets, jokes and camera angles between videos: AI voices and serial scripts can be flagged as repetitive content.
