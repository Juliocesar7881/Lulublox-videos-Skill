"""Splits ONE ElevenLabs take that contains all the lines of a video (one paragraph per line) into
falas/fala-01.mp3, fala-02.mp3, ... One generation per video instead of one per line: fewer browser steps and a
consistent voice. Whisper (word timestamps) finds where each script line ends; the cut goes in the middle of the
silence between two lines (laughs or gasps from an emotion tag stay with their own line).

    python dividir_falas.py PROJECT TAKE.mp3 [--modelo small]

Then run alinhar_falas.py as usual. Exits with an error if a line cannot be found in the take."""
import argparse
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def norm(t):
    t = unicodedata.normalize('NFKD', t)
    t = ''.join(c for c in t if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]', '', t.lower())


def palavras_do_texto(t):
    t = re.sub(r'\[[^\]]*\]', ' ', t)
    return [norm(w) for w in t.split() if norm(w)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('projeto')
    ap.add_argument('take')
    ap.add_argument('--modelo', default='small')
    a = ap.parse_args()
    proj = Path(a.projeto).resolve()
    rot = json.loads((proj / 'roteiro.json').read_text(encoding='utf-8'))
    linhas = [palavras_do_texto(f['texto']) for f in rot['falas']]

    from faster_whisper import WhisperModel
    import numpy as np
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', a.take, '-f', 'f32le', '-ac', '1', '-ar', '16000', '-'],
                         capture_output=True, check=True).stdout
    audio = np.frombuffer(raw, np.float32)
    dur = len(audio) / 16000
    m = WhisperModel(a.modelo, device='cpu', compute_type='int8')
    prompt = ' '.join(re.sub(r'\[[^\]]*\]', '', f['texto']).strip() for f in rot['falas'])
    segs, _ = m.transcribe(audio, language='en', beam_size=5, word_timestamps=True, initial_prompt=prompt)
    ws = [(norm(w.word), w.start, w.end) for s in segs for w in s.words if norm(w.word)]

    # Sequence alignment (difflib) between the script words and the heard words: each line spans from its first to
    # its last heard word that matched (a greedy prefix match broke on "rock" vs "Rocky").
    import difflib
    roteiro = [(n, w) for n, lin in enumerate(linhas) for w in lin]
    sm = difflib.SequenceMatcher(None, [w for _, w in roteiro], [w for w, _, _ in ws], autojunk=False)
    mapa = {}
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            mapa[blk.a + k] = blk.b + k
    faixa = []
    for n in range(len(linhas)):
        idx = [mapa[i] for i, (m, _) in enumerate(roteiro) if m == n and i in mapa]
        if not idx:
            raise SystemExit(f'line {n + 1} ("{" ".join(linhas[n])}") not found in the take: {[w for w, _, _ in ws]}')
        faixa.append((min(idx), max(idx)))

    # Energy (10 ms frames). Between two lines the cut goes at the start of the LONGEST silence (a gasp or laugh
    # from the next line's tag is sound, so it stays with its line); each piece is then trimmed of its
    # leading/trailing silence (keeping 40 ms before the sound and 150 ms after it).
    fr = 160
    rms = np.sqrt(np.convolve(audio ** 2, np.ones(fr) / fr, 'same')[::fr])
    lim = max(0.006, float(np.percentile(rms, 95)) * 0.06)
    silencio = rms < lim

    def maior_silencio(t0, t1):
        a, b = int(t0 * 100), max(int(t0 * 100) + 1, int(t1 * 100))
        melhor, ini, k = (0, None), None, a
        for k in range(a, min(b, len(silencio))):
            if silencio[k] and ini is None:
                ini = k
            if (not silencio[k] or k == b - 1) and ini is not None:
                if k - ini > melhor[0]:
                    melhor = (k - ini, ini)
                ini = None
        return (melhor[1] + 3) / 100 if melhor[1] is not None and melhor[0] >= 4 else (t0 + t1) / 2

    cortes = [0.0]
    for n in range(len(linhas) - 1):
        fim = ws[faixa[n][1]][2]
        prox = ws[faixa[n + 1][0]][1]
        cortes.append(round(maior_silencio(min(fim, prox) - 0.1, max(prox, fim + 0.1)), 3))
    cortes.append(round(dur, 3))

    # Trimming uses a much lower threshold than the cut: soft consonants ("s" of "sandcastle" at -42 dB) are sound.
    quieto = rms < lim / 5

    def aparar(ini, fim):
        a, b = int(ini * 100), max(int(ini * 100) + 1, int(fim * 100))
        som = np.nonzero(~quieto[a:b])[0]
        if not len(som):
            return ini, fim
        return max(ini, (a + som[0]) / 100 - 0.04), min(fim, (a + som[-1] + 1) / 100 + 0.15)

    pasta = proj / 'falas'
    pasta.mkdir(exist_ok=True)
    for k in range(len(linhas)):
        ini, fim = aparar(cortes[k], cortes[k + 1])
        saida = pasta / f'fala-{k + 1:02d}.mp3'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{ini:.3f}', '-to', f'{fim:.3f}', '-i', a.take,
                        '-af', 'afade=t=in:d=0.01,areverse,afade=t=in:d=0.04,areverse', '-codec:a', 'libmp3lame',
                        '-b:a', '160k', str(saida)], check=True)
        print(f'{saida.name}: {ini:.2f}-{fim:.2f}s')


if __name__ == '__main__':
    main()
