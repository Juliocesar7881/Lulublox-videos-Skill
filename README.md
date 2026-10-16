# Lulublox Videos Skill

A Claude Code skill that makes animated Roblox Shorts for kids starring **Lulu**, a charismatic and cute girl avatar. Everything is in English: script, voice, captions, titles and descriptions.

Lulu's look:
- peach skin and long chestnut hair with side-swept bangs and a pink bow;
- big violet eyes with lashes, and blush;
- a pink top with puffy sleeves, a purple pleated skirt that moves with her legs, and white sneakers;
- her signature move: a wink.

What the skill does, from one idea:

1. Writes an original kid-friendly script (for example "Which slide is the fastest? Pick fast! 5-4-3-2-1" plus a silly twist) and checks it against the log of past videos.
2. Generates Lulu's voice with the free ElevenLabs default voice Jessica (Playful, Bright, Warm; model Eleven v4).
3. Builds and animates the scene in Roblox Studio through the official command line (`-task RunScript`), with no clicks. It runs collision and camera audits, then records only the Studio window.
4. Edits the final 1080×1920 Short with karaoke captions, sound effects and licensed music, and checks loudness, the transcript and the frames.

## Install

```bash
git clone https://github.com/Juliocesar7881/Lulublox-videos-Skill.git
cd Lulublox-videos-Skill
python install.py
```

It needs the sibling skill [roblox-video-editor](https://github.com/Juliocesar7881/roblox-video-editor-skill), which provides the renderer and the audio library. It also needs Roblox Studio and Python 3.11+ on Windows.

## Use

In Claude Code: `/lulublox-videos` followed by your idea, for example "Lulu tries to bake the biggest cake".

## Layout

- `lulublox-videos/SKILL.md`: the workflow.
- `lulublox-videos/references/`: production rules, Short format and AnimKit reference.
- `lulublox-videos/luau/AnimKit.lua`: Lulu's model, face, reactive skirt, animation, camera, audits.
- `lulublox-videos/modelos/base/`: scene and edit helpers to copy into each project.
- `lulublox-videos/scripts/`: Studio pipeline, window capture, voice alignment, captions, one-command producer.

## License

MIT. Voices are generated with ElevenLabs; check their terms for commercial use.
