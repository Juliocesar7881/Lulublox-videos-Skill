"""Original rain ambience (procedural synthesis, no third-party recording).

Writes efeitos/originais-livres/chuva-continua.mp3 (34 s) in the roblox-video-editor library and registers it in
catalogo.json (category 'chuva'): a steady rain bed (band-passed noise that breathes slowly) with thousands of
tiny random drops on top. It is a continuous texture: shorten it with 'dur' and a long fade.

    python criar_sfx_chuva.py
"""
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

LIB = Path.home() / '.claude' / 'skills' / 'roblox-video-editor' / 'assets' / 'biblioteca-audio'
DESTINO = LIB / 'efeitos' / 'originais-livres'
SR = 44100
rng = np.random.default_rng(2610)


def chuva(segundos):
    n = int(SR * segundos)
    t = np.arange(n) / SR
    # Bed: white noise band-passed (rain hiss), slowly breathing in level.
    ruido = rng.normal(0, 1, n)
    leito = sosfilt(butter(2, [700, 7000], btype='band', fs=SR, output='sos'), ruido)
    leito *= 0.75 + 0.25 * np.sin(2 * np.pi * 0.11 * t + 1.3) * np.sin(2 * np.pi * 0.047 * t)
    # Drops: short damped clicks at random times, bright and dull ones.
    gotas = np.zeros(n)
    for _ in range(int(segundos * 220)):
        i = rng.integers(0, n - 2000)
        dur = rng.integers(200, 900)
        f = rng.uniform(1800, 6500)
        k = np.arange(dur) / SR
        g = np.sin(2 * np.pi * f * k) * np.exp(-k / rng.uniform(0.002, 0.006)) * rng.uniform(0.2, 1.0)
        gotas[i:i + dur] += g
    gotas = sosfilt(butter(2, 1200, btype='high', fs=SR, output='sos'), gotas)
    sinal = leito / np.max(np.abs(leito)) * 0.55 + gotas / np.max(np.abs(gotas)) * 0.45
    rampa = int(0.6 * SR)
    sinal[:rampa] *= np.linspace(0, 1, rampa)
    sinal[-rampa:] *= np.linspace(1, 0, rampa)
    return sinal / np.max(np.abs(sinal)) * 10 ** (-1.5 / 20)


def registrar(destino, categoria, tags):
    cat_path = LIB / 'catalogo.json'
    cat = json.loads(cat_path.read_text(encoding='utf-8'))
    rel = destino.relative_to(LIB).as_posix()
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(destino)],
                               capture_output=True, text=True, check=True).stdout.strip())
    dados = destino.read_bytes()
    entrada = {'path': rel, 'duration_seconds': round(dur, 2), 'sha256': hashlib.sha256(dados).hexdigest(), 'bytes': len(dados),
               'type': 'sfx', 'origin': 'original procedural synthesis', 'license_status': 'original-generated',
               'commercial_allowed': True, 'content_review': 'instrumental', 'category': categoria, 'tags': tags}
    cat['assets'] = [a for a in cat['assets'] if a['path'] != rel] + [entrada]
    cat_path.write_text(json.dumps(cat, ensure_ascii=False, indent=1), encoding='utf-8')
    return entrada


if __name__ == '__main__':
    destino = DESTINO / 'chuva-continua.mp3'
    with tempfile.TemporaryDirectory() as pasta:
        wav = Path(pasta) / 'chuva.wav'
        wavfile.write(wav, SR, (chuva(34.0) * 32767).astype(np.int16))
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(wav), '-codec:a', 'libmp3lame', '-b:a', '160k',
                        str(destino)], check=True)
    e = registrar(destino, 'chuva', ['Rain', 'Ambience', 'Storm', 'Continuous'])
    print(f"{e['path']}: {e['duration_seconds']} s, {e['bytes']} bytes")
