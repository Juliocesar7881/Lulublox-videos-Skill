# Short format

Vertical 9:16, 25–35 s, 60 fps, Lulu as the star, word-by-word captions with the key word in yellow. Everything in English.

## Main structure (~25–30 s): "Which one…? Pick fast!"

| Time | Block | What happens |
|---|---|---|
| 0–2 s | Hook | A direct question with the challenge: "Which slide is the fastest?". Medium close-up on Lulu, already reacting (surprised, curious). |
| 2–6 s | Options | "The red one, the blue one… or the giant yellow one?". One quick cut per option, on the word that names it. Ends with "**Pick fast!**". |
| 6–11 s | Countdown | Badge 5→4→3→2→1 (1 s each) on a wide shot of the options; Lulu looking from one to the other (`scared`/`nervous`, no shaking). Tick on every number. |
| 11–22 s | Attempts | She picks one ("The red one! It's the shortest!"), something unexpected happens, big reaction. She may try a second one. |
| 22–30 s | Twist | An ending that breaks the expectation, light and silly. The last frame is a strong reaction or her `wink`. |

The video does not end with a goodbye: it ends at the peak of the joke (it helps replays). Lines of 2–6 words, one idea per line.

Other formats that fit Lulu (always original): a tiny "how not to…" story, "1 vs 10 vs 100" escalation, "guess what's inside", a helping-a-friend story or a pet adventure.

## Visual language

- Cuts every 1–2.5 s, alternating wide (set + options), medium (body) and close-up (face). Low camera (below the eyes) makes Lulu and the objects look grand.
- The face always reacts and the pupils look at what she names.
- Colorful, saturated sets with big simple objects and a clear sky. No Roblox interface on screen.
- On-screen signs and numbers in English (1, 2, 3 or strong colors) so kids can choose along.

## Audio

- Lulu's voice (ElevenLabs, the chosen female voice) clear and in front; lively background music, low.
- SFX on almost every event: whoosh on cuts, pop on reaction captions, tick/ding on every countdown number, impact/boing on falls, applause or an "error" sound on the twist. Every effect plays to its end.

## Script (`roteiro.json`)

```json
{
  "titulo": "WHICH SLIDE IS THE FASTEST?",
  "idiomas": ["en"],
  "arquivo": "which-slide-is-the-fastest.mp4",
  "vozes": {"lulu": "Jessica"},
  "destaques": ["FASTEST", "RED", "BLUE", "YELLOW", "PICK FAST"],
  "falas": [
    {"id": "01", "personagem": "lulu", "tag": "curious", "texto": "Which slide is the fastest?"},
    {"id": "02", "personagem": "lulu", "tag": "excited", "texto": "The red one, the blue one... or the giant yellow one?"},
    {"id": "03", "personagem": "lulu", "tag": "excited", "texto": "Pick fast!"}
  ],
  "planos": [
    {"fala": "01", "camera": "low close-up on Lulu", "rosto": "surprised", "acao": "looks up"}
  ]
}
```

`titulo_youtube`, `descricao`, `hashtags` and `tags` also go in English (kid-friendly SEO: "roblox", "roblox shorts", "roblox for kids", "lulu roblox", the topic words).
