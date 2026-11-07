# Short format

Vertical 9:16, **30–40 s** (owner, 2026-11-07: "era pra ser vídeos de 30 a 40 segundos"; the 7-line 12–15 s batches of November were too short), 60 fps, Lulu as the star, word-by-word captions with the key word in yellow. Everything in English. The reasons for the length, the hook and the topics are in [what-performs.md](what-performs.md).

## Main structure (~20–30 s): a problem, then "Pick fast!"

| Time | Block | What happens |
|---|---|---|
| 0–2 s | Hook | A concrete situation already happening: "Oh no! The slide is on fire!". First frame: medium shot with Lulu, the joke object and a short readable sign when it helps, her face already reacting. The close-up comes after. |
| 2–6 s | Options | Now the question: "Which one gets me down?", then "The red one, the blue one… or the giant yellow one?". One quick cut per option, on the word that names it. Ends with "**Pick fast!**". |
| 6–11 s | Countdown | Badge 5→4→3→2→1 (1 s each) on a wide shot of the options; Lulu looking from one to the other (`scared`/`nervous`, no shaking). Tick on every number. |
| 11–22 s | Attempts | She picks one ("The red one! It's the shortest!"), something unexpected happens, big reaction. She may try a second one. |
| 22–30 s | Twist | An ending that breaks the expectation, light and silly. The last frame is a strong reaction or her `wink`. |

The video does not end with a goodbye: it ends at the peak of the joke (it helps replays). Lines of 2–6 words, one idea per line. Never open the voice with "Which X is the Y?": the question comes second, once there is a reason to care.

Other formats that fit Lulu (always original): "When…" moments, a sibling, mom or pet conflict, a tiny "how not to…" story, "Lulu vs X", a world with a strange rule, "1 vs 10 vs 100" escalation, "guess what's inside", a helping-a-friend story or a pet adventure.

## Visual language

- Cuts every 1–2.5 s, alternating wide (set + options), medium (body) and close-up (face). Low camera (below the eyes) makes Lulu and the objects look grand.
- The face always reacts and the pupils look at what she names.
- Colorful, saturated sets with big simple objects and a clear sky. No Roblox interface on screen.
- On-screen signs and numbers in English (1, 2, 3 or strong colors) so kids can choose along.

## Audio

- Lulu's voice (ElevenLabs Jessica) clear and in front; lively background music, low.
- SFX on almost every event: whoosh on cuts, pop on reaction captions, tick/ding on every countdown number, impact/boing on falls, applause or an "error" sound on the twist. Every effect plays to its end.

## Script (`roteiro.json`)

```json
{
  "titulo": "I GOT STUCK ON THE SLIDE IN ROBLOX... WHICH ONE GETS ME DOWN?",
  "idiomas": ["en"],
  "arquivo": "stuck-on-the-slide.mp4",
  "vozes": {"lulu": "Jessica"},
  "destaques": ["STUCK", "RED", "BLUE", "YELLOW", "PICK FAST"],
  "falas": [
    {"id": "01", "personagem": "lulu", "tag": "gasps", "texto": "Oh no! I'm stuck up here!"},
    {"id": "02", "personagem": "lulu", "tag": "curious", "texto": "Which slide gets me down?"},
    {"id": "03", "personagem": "lulu", "tag": "excited", "texto": "The red one, the blue one... or the giant yellow one?"},
    {"id": "04", "personagem": "lulu", "tag": "excited", "texto": "Pick fast!"}
  ],
  "planos": [
    {"fala": "01", "camera": "low medium shot with Lulu and the three slides in frame", "rosto": "surprised", "acao": "looks down at the ground"}
  ]
}
```

`titulo_youtube`, `descricao`, `hashtags` and `tags` also go in English (kid-friendly SEO: "roblox", "roblox shorts", "roblox for kids", "lulu roblox", the topic words). Tags did not separate strong videos from weak ones, so use the template and spend the effort on the hook and the first frame.


## 2026-11-07: length, camera and zoom (owner's review of the "music box" test)

The owner rejected a 12 s test: too short, "parece só 2D com várias câmeras", zooms that look buggy and cuts that feel off.
What changed (reference: `entregas/lulublox/lulu-20261107/_src/a.txt`, 31 s):

- **Length 30–40 s**: 11–15 lines (2–6 words each, 1.5–3 s of voice), plus silent action beats (music plays, suspense
  pause, the final dance ~3 s). Story: hook with the object on screen → 3 escalating tries → a quiet suspense beat ("Wait...
  it stopped.") → twist → a happy shared ending.
- **The camera moves inside each shot** (kit_cena: `trav` dolly/crane, `orb` arc around her or the object, `mao_` handheld
  drift, `closev` close-up that pushes in). Shots of 2–4 s, about 12–14 cuts in 30 s. A static `plano`/`close` is the
  exception, not the rule. Use over-the-shoulder shots from behind her (`mao_(..., inserto=True)`) and arcs around the
  object to show depth.
- **360 sets**: rooms get `paredes360()` after `setSala/setQuarto/setCozinha`, so arcs and reverse angles see walls, a
  door, shelves and bunting instead of the void. Outdoor sets already surround her.
- **Zoom**: `fecha_ed(..., zooms=False)` is the default now (no automatic push/punch on every line, which the next cut
  chopped in half). Keep at most one in-camera `soco` and one `ed.shake` on the biggest action beat.
- **Frame 0 of a moving shot**: `travel/orbita/mao` place the camera on the cut itself (before 2026-11-07 the first frame
  after a cut still showed the old angle: the "rosto fora do quadro" one-frame audit hits).
- Keep her arms down (`K.bracos(noob, nil, ...)`) before any shot whose camera passes on her right (+X) side: her reaching
  arm fills the frame.
