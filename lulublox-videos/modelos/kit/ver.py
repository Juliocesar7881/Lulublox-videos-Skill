"""ver.py NN NN ...: junta 9 quadros de cada vídeo numa linha (revisao/ver-XXX.png) para revisar vários de uma vez."""
import subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw
L = Path(__file__).resolve().parent
W, H, N = 112, 199, 10
ns = sys.argv[1:]
out = Image.new('RGB', (W * N + 30, H * len(ns)), 'white')
d = ImageDraw.Draw(out)
for r, n in enumerate(ns):
    p = next(L.glob(f'{n}-*'))
    m = sorted((p / 'final-en').glob('*.mp4'))
    d.text((3, r * H + 90), n, fill='black')
    if not m:
        continue
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(m[0])], capture_output=True, text=True).stdout)
    for i in range(N):
        t = dur * (i + 0.5) / N
        f = L / '_tmp.png'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.2f}', '-i', str(m[0]), '-frames:v', '1', '-vf', f'scale={W}:{H}', str(f)])
        out.paste(Image.open(f), (30 + i * W, r * H))
out.save(L / 'ver.png')
print(out.size)
