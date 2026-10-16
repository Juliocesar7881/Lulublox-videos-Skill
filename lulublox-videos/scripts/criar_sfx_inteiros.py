"""Original effects that end on their own (procedural synthesis, no third-party recording), so no effect ever has
to be cut in the middle:

  coracao-5s.mp3     heartbeat for the 5-4-3-2-1 countdown: lub-dub every second, speeding up a little, last beat
                     dies out before 5.0 s (category 'coracao_5s')
  vento-rajada.mp3   one gust of wind, 1.3 s, rises and fades out naturally (category 'vento_curto')
  deslize-curto.mp3  a quick slide/swish, 0.8 s, natural decay (category 'deslize')
  tremor-curto.mp3   a low rumble that shakes for 1.2 s and dies out (category 'tremor')

Written to efeitos/originais-livres/ of the roblox-video-editor library and registered in catalogo.json.

    python criar_sfx_inteiros.py
"""
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from criar_sfx_chuva import DESTINO, SR, registrar  # noqa: E402

rng = np.random.default_rng(1016)


def envelope_fim(sinal, fade):
    n = int(fade * SR)
    sinal[-n:] *= np.linspace(1, 0, n) ** 2
    return sinal


def normalizar(sinal, pico_db=-1.5):
    return sinal / np.max(np.abs(sinal)) * 10 ** (pico_db / 20)


def batida(dur=0.16, f0=58, f1=38):
    k = np.arange(int(dur * SR)) / SR
    f = f0 + (f1 - f0) * k / dur
    fase = 2 * np.pi * np.cumsum(f) / SR
    corpo = np.sin(fase) * np.exp(-k / 0.045)
    clique = sosfilt(butter(2, [150, 900], btype='band', fs=SR, output='sos'), rng.normal(0, 1, len(k))) * np.exp(-k / 0.008)
    return corpo + 0.25 * clique


def coracao(total=5.0):
    n = int(total * SR)
    s = np.zeros(n)
    t, periodo = 0.05, 1.0
    while t < total - 0.45:
        for atraso, ganho in ((0.0, 1.0), (0.24 * periodo, 0.7)):
            b = batida() * ganho
            i = int((t + atraso) * SR)
            if i + len(b) < n:
                s[i:i + len(b)] += b
        t += periodo
        periodo = max(0.62, periodo * 0.9)  # beats a bit faster as the countdown runs out
    s = sosfilt(butter(2, 220, btype='low', fs=SR, output='sos'), s)
    return envelope_fim(normalizar(s), 0.3)


def rajada(total=1.3):
    n = int(total * SR)
    t = np.arange(n) / SR
    ruido = rng.normal(0, 1, n)
    # A band-pass that sweeps up and back down (the "whoo" of a gust).
    centro = 350 + 650 * np.sin(np.pi * t / total)
    saida = np.zeros(n)
    bloco = 1024
    for i in range(0, n, bloco):
        c = float(centro[i])
        sos = butter(2, [c * 0.6, c * 1.6], btype='band', fs=SR, output='sos')
        saida[i:i + bloco] = sosfilt(sos, ruido[i:i + bloco])
    amp = np.sin(np.pi * np.clip(t / total, 0, 1)) ** 1.5
    return envelope_fim(normalizar(saida * amp), 0.15)


def deslize(total=0.8):
    n = int(total * SR)
    t = np.arange(n) / SR
    ruido = sosfilt(butter(2, [1500, 6000], btype='band', fs=SR, output='sos'), rng.normal(0, 1, n))
    amp = np.clip(t / 0.06, 0, 1) * np.exp(-np.clip(t - 0.06, 0, None) / 0.22)
    return envelope_fim(normalizar(ruido * amp), 0.08)


def tremor(total=1.2):
    n = int(total * SR)
    t = np.arange(n) / SR
    ruido = sosfilt(butter(3, 120, btype='low', fs=SR, output='sos'), rng.normal(0, 1, n))
    amp = np.clip(t / 0.05, 0, 1) * np.exp(-t / 0.4) * (0.7 + 0.3 * np.sin(2 * np.pi * 9 * t))
    return envelope_fim(normalizar(ruido * amp), 0.2)


def impacto(total=0.55):
    """A short cartoon thud: a low pitch-drop body plus a click, decaying to silence."""
    n = int(total * SR)
    t = np.arange(n) / SR
    f = 95 * np.exp(-t / 0.12) + 40
    corpo = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.11)
    ruido = sosfilt(butter(2, [200, 2500], btype='band', fs=SR, output='sos'), rng.normal(0, 1, n)) * np.exp(-t / 0.025)
    return envelope_fim(normalizar(corpo + 0.45 * ruido), 0.08)


def explosao(total=0.75):
    """A small cartoon blast: noise burst with a falling low-pass and a low boom, gone by the end."""
    n = int(total * SR)
    t = np.arange(n) / SR
    ruido = rng.normal(0, 1, n)
    saida = np.zeros(n)
    bloco = 512
    for i in range(0, n, bloco):
        corte = float(4500 * np.exp(-t[i] / 0.18) + 250)
        saida[i:i + bloco] = sosfilt(butter(2, corte, btype='low', fs=SR, output='sos'), ruido[i:i + bloco])
    boom = np.sin(2 * np.pi * np.cumsum(60 * np.exp(-t / 0.3) + 30) / SR) * np.exp(-t / 0.16)
    amp = np.clip(t / 0.006, 0, 1) * np.exp(-t / 0.17)
    return envelope_fim(normalizar(saida * amp + 0.8 * boom), 0.1)


def brilho(total=0.6):
    """A quick magic sparkle: four bell notes going up, each ringing out."""
    n = int(total * SR)
    s = np.zeros(n)
    for k, nota in enumerate((1568, 1976, 2349, 3136)):
        i = int(k * 0.07 * SR)
        m = n - i
        tt = np.arange(m) / SR
        s[i:] += (np.sin(2 * np.pi * nota * tt) + 0.3 * np.sin(2 * np.pi * nota * 2.01 * tt)) * np.exp(-tt / 0.11)
    return envelope_fim(normalizar(s), 0.08)


def apito_sobe(total=0.6):
    """A slide whistle going up, with a soft start and end."""
    n = int(total * SR)
    t = np.arange(n) / SR
    f = 600 + 1300 * (t / total) ** 1.3
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * (1 + 0.04 * np.sin(2 * np.pi * 6 * t))
    amp = np.clip(t / 0.04, 0, 1) * np.clip((total - t) / 0.12, 0, 1)
    return normalizar(s * amp)


def fogo(total=0.8):
    """A whoosh of fire: band noise swelling fast and crackling as it dies out."""
    n = int(total * SR)
    t = np.arange(n) / SR
    ruido = sosfilt(butter(2, [300, 3500], btype='band', fs=SR, output='sos'), rng.normal(0, 1, n))
    estalos = (rng.random(n) > 0.9993) * rng.normal(0, 3, n)
    estalos = sosfilt(butter(2, 2500, btype='high', fs=SR, output='sos'), estalos)
    amp = np.clip(t / 0.08, 0, 1) * np.exp(-np.clip(t - 0.08, 0, None) / 0.25)
    return envelope_fim(normalizar((ruido + estalos) * amp), 0.1)


def gravar(nome, sinal, categoria, tags):
    destino = DESTINO / nome
    with tempfile.TemporaryDirectory() as pasta:
        wav = Path(pasta) / 'x.wav'
        wavfile.write(wav, SR, (sinal * 32767).astype(np.int16))
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(wav), '-codec:a', 'libmp3lame', '-b:a', '160k',
                        str(destino)], check=True)
    e = registrar(destino, categoria, tags)
    print(f"{e['path']}: {e['duration_seconds']} s")


if __name__ == '__main__':
    gravar('coracao-5s.mp3', coracao(), 'coracao_5s', ['Heartbeat', 'Countdown', 'Tension'])
    gravar('vento-rajada.mp3', rajada(), 'vento_curto', ['Wind', 'Gust', 'Whoosh'])
    gravar('deslize-curto.mp3', deslize(), 'deslize', ['Slide', 'Swish'])
    gravar('tremor-curto.mp3', tremor(), 'tremor', ['Rumble', 'Shake', 'Impact'])
    gravar('impacto-curto.mp3', impacto(), 'impacto_curto', ['Impact', 'Thud', 'Landing'])
    gravar('explosao-curta.mp3', explosao(), 'explosao_curta', ['Explosion', 'Blast', 'Boom'])
    gravar('brilho-curto.mp3', brilho(), 'brilho_curto', ['Sparkle', 'Magic', 'Chime'])
    gravar('apito-sobe-curto.mp3', apito_sobe(), 'apito_sobe_curto', ['Slide whistle', 'Up', 'Cartoon'])
    gravar('fogo-curto.mp3', fogo(), 'fogo_curto', ['Fire', 'Whoosh', 'Burst'])
