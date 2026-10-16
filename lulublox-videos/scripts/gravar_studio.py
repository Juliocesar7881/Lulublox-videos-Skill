"""Record a Roblox Studio cutscene from the screen and turn it into a clean vertical clip.

  gravar     grava a tela inteira (Desktop Duplication + NVENC) por N segundos
  processar  acha o flash magenta de sincronia que o AnimKit mostra no inicio, usa-o para
             descobrir a area do viewport e o instante zero, recorta, desvira a camera
             deitada (modo vertical) e exporta 1080x1920 sem audio.
"""
import argparse, json, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'roblox-video-editor' / 'scripts'))
from media_utils import ffmpeg, probe  # noqa: E402

MAGENTA = (255, 0, 255)


def gravar(args):
    ff = ffmpeg()
    enc = ['-c:v', 'h264_nvenc', '-preset', 'p5', '-tune', 'hq', '-rc', 'vbr', '-cq', '14', '-b:v', '0']
    probe_enc = subprocess.run([ff, '-hide_banner', '-encoders'], capture_output=True, text=True).stdout
    if 'h264_nvenc' not in probe_enc:
        enc = ['-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '12']
    cmd = [ff, '-hide_banner', '-v', 'error', '-y', '-f', 'lavfi',
           '-i', f'ddagrab=output_idx={args.monitor}:framerate={args.fps}:draw_mouse=0',
           '-t', str(args.segundos), *enc, str(args.saida)]
    print('gravando', args.segundos, 's ->', args.saida, flush=True)
    subprocess.run(cmd, check=True)
    print('ok', flush=True)


def frames(ff, video, fps, scale_w):
    """Yield (time, rgb bytes, w, h) at a fixed frame rate from a small decode."""
    info = probe(video)
    w = scale_w; h = round(info['height'] * scale_w / info['width'] / 2) * 2
    p = subprocess.Popen([ff, '-v', 'error', '-i', str(video), '-vf', f'fps={fps},scale={w}:{h}:flags=neighbor',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    n = 0; size = w * h * 3
    while True:
        buf = p.stdout.read(size)
        if len(buf) < size:
            break
        yield n / fps, buf, w, h
        n += 1
    p.wait()


def is_magenta(px):
    r, g, b = px
    return r > 235 and g < 25 and b > 235  # only the pure flash (Lulu wears saturated pink)


def magenta_share(buf, w, h):
    step = 7; hit = tot = 0
    for i in range(0, w * h, step):
        tot += 1
        hit += is_magenta(buf[i * 3:i * 3 + 3])
    return hit / tot


def find_markers(ff, video, fps):
    """Return start times of each magenta flash (the viewport is >=25% of the screen)."""
    marks, on = [], False
    for t, buf, w, h in frames(ff, video, fps, 320):
        m = magenta_share(buf, w, h) > 0.25
        if m and not on:
            marks.append(t)
        on = m
    return marks


def viewport_box(ff, video, t):
    """Bounding box of magenta pixels at full resolution, at time t."""
    info = probe(video)
    W, H = info['width'], info['height']
    raw = subprocess.run([ff, '-v', 'error', '-ss', f'{t + 0.05:.3f}', '-i', str(video), '-frames:v', '1',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    xs, ys = [], []
    for y in range(0, H, 2):
        row = raw[y * W * 3:(y + 1) * W * 3]
        for x in range(0, W, 2):
            if is_magenta(row[x * 3:x * 3 + 3]):
                xs.append(x); ys.append(y)
    if not xs:
        raise SystemExit('Flash magenta nao encontrado no quadro; o viewport estava visivel?')
    x0, x1, y0, y1 = min(xs), max(xs) + 2, min(ys), max(ys) + 2
    # Even sizes for the encoder.
    return x0, y0, (x1 - x0) // 2 * 2, (y1 - y0) // 2 * 2


def processar(args):
    ff = ffmpeg()
    marks = find_markers(ff, args.bruto, args.fps_busca)
    if not marks:
        raise SystemExit('Nenhum flash de sincronia encontrado. A cena chamou AnimKit.rodar()?')
    t_mark = marks[0]
    x, y, w, h = viewport_box(ff, args.bruto, t_mark)
    start = t_mark + args.atraso
    duration = args.duracao or ((marks[1] - start) if len(marks) > 1 else probe(args.bruto)['duration'] - start)
    vf = [f'crop={w}:{h}:{x}:{y}']
    if args.vertical == 'deitada':
        # The AnimKit rolls the camera 90 deg so a 9:16 shot uses the full landscape viewport.
        vf.append('transpose=2')
        w, h = h, w
    # Centre-crop to exact 9:16 then scale to the delivery size.
    tw, th = (w, round(w * 16 / 9 / 2) * 2) if h * 9 >= w * 16 else (round(h * 9 / 16 / 2) * 2, h)
    vf += [f'crop={tw}:{th}', f'scale={args.largura}:{round(args.largura*16/9/2)*2}:flags=lanczos', f'fps={args.fps}', 'setsar=1', 'format=yuv420p']
    subprocess.run([ff, '-hide_banner', '-v', 'error', '-y', '-ss', f'{start:.3f}', '-i', str(args.bruto), '-t', f'{duration:.3f}',
                    '-vf', ','.join(vf), '-an', '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', str(args.saida)], check=True)
    rel = {'flashes': [round(m, 3) for m in marks], 'inicio': round(start, 3), 'duracao': round(duration, 3),
           'viewport': {'x': x, 'y': y, 'w': w if args.vertical != 'deitada' else h, 'h': h if args.vertical != 'deitada' else w},
           'saida': str(args.saida)}
    print(json.dumps(rel, ensure_ascii=False, indent=1))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    g = sub.add_parser('gravar')
    g.add_argument('saida', type=Path)
    g.add_argument('--segundos', type=float, required=True)
    g.add_argument('--fps', type=int, default=60)
    g.add_argument('--monitor', type=int, default=0)
    p = sub.add_parser('processar')
    p.add_argument('bruto', type=Path)
    p.add_argument('saida', type=Path)
    p.add_argument('--vertical', choices=['deitada', 'recorte'], default='deitada',
                   help='deitada: camera girada 90 graus no AnimKit (melhor nitidez); recorte: corta o centro')
    p.add_argument('--atraso', type=float, default=0.8, help='segundos entre o flash e o t=0 da timeline (AnimKit.ATRASO)')
    p.add_argument('--duracao', type=float, help='padrao: ate o flash final')
    p.add_argument('--largura', type=int, default=1080)
    p.add_argument('--fps', type=int, default=60)
    p.add_argument('--fps-busca', type=int, default=60)
    args = ap.parse_args()
    {'gravar': gravar, 'processar': processar}[args.cmd](args)


if __name__ == '__main__':
    main()
