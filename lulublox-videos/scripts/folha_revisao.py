"""Contact sheets of a rendered Short for the review pass (2 frames per second, 6 x 4 tiles of 180 px).

    python folha_revisao.py PROJECT [--fim SECONDS]

Writes PROJECT/revisao/folha-1.png, folha-2.png... plus PROJECT/revisao/fim.png (a full-size frame 1.9 s before the
end, the payoff shot). Read them against the beat table in gerar_cena.py: is every "must be visible" item visible,
whole, not behind her arm and not cut at the frame edge?"""
import subprocess
import sys
from pathlib import Path

proj = Path(sys.argv[1]).resolve()
mp4 = sorted((proj / 'final-en').glob('*.mp4'))
if not mp4:
    raise SystemExit(f'no final-en/*.mp4 in {proj}')
mp4 = mp4[0]
out = proj / 'revisao'
out.mkdir(exist_ok=True)
for f in out.glob('folha-*.png'):
    f.unlink()
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(mp4), '-vf', 'fps=2,scale=180:-2,tile=6x4:padding=4:color=white',
                str(out / 'folha-%d.png')], check=True)
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(mp4)],
                           capture_output=True, text=True).stdout.strip() or 0)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{max(0, dur - 1.9):.2f}', '-i', str(mp4), '-frames:v', '1',
                '-vf', 'scale=540:-2', str(out / 'fim.png')], check=True)
print('sheets:', sorted(p.name for p in out.glob('folha-*.png')), '+ fim.png')
