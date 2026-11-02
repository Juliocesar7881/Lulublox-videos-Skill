# Short format

Vertical 9:16, 20–30 s, 60 fps, Lulu as the star, word-by-word captions with the key word in yellow. Everything in English. The reasons for the length, the hook and the topics are in [what-performs.md](what-performs.md).

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
