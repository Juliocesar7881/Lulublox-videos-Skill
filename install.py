"""Install the Lulublox Videos skill in Claude Code (no GitHub credentials needed).

    python install.py              # into ~/.claude/skills
    python install.py --project .  # into ./.claude/skills

The skill renders with the sibling skill `roblox-video-editor` (renderer, SFX/music library and stickers).
If it is missing, install it first from https://github.com/Juliocesar7881/roblox-video-editor-skill
(`python install.py` in that repository).
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

SKILL = 'lulublox-videos'
MARCA = '.installed-by-lulublox-videos'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--project', type=Path, help='Install into this project instead of the user skills folder')
    ap.add_argument('--skip-deps', action='store_true', help='Use the Python packages already installed')
    args = ap.parse_args()
    repo = Path(__file__).resolve().parent
    base = (args.project.resolve() if args.project else Path.home()) / '.claude' / 'skills'
    dest = base / SKILL
    if dest.exists() and not (dest / MARCA).exists():
        raise SystemExit(f'Existing skill not managed by this installer: {dest}. Back it up before installing.')
    if not args.skip_deps:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--disable-pip-version-check', '-r',
                        str(repo / 'requirements.txt')], check=True)
    shutil.copytree(repo / SKILL, dest, dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    (dest / MARCA).write_text('Portable install; updates keep local files.\n', encoding='utf-8')
    print(f'Skill installed: {dest}')
    if not (base / 'roblox-video-editor').exists():
        print('Missing dependency: roblox-video-editor. Install it from '
              'https://github.com/Juliocesar7881/roblox-video-editor-skill (python install.py).')
    print('In Claude Code: /lulublox-videos + your Short idea.')


if __name__ == '__main__':
    main()
