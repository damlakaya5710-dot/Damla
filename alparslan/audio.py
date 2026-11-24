"""ALPARSLAN — "Ağrı burada, peki ya kaynağı?" için prosedürel fon müziği (19 sn, 48 kHz stereo).
Tamamen sentez, telifsiz. Görüntüdeki zamanlamayla eşleşik:
  0–8.3  merak: Dm(add9) pad + ağrının nabzıyla eş kalp atışı, yakın planda kristal tınılar
  7.4    yükselen nefes (riser) → 8.6 derin vuruş: kamera geri çekilir, Bbmaj7 açılımı + arpej
  12.9   ana mesaj: sade Gm9, nabız susar
  16.5   marka: D(add9) çözülme çanı
Kullanım: python3 audio.py cikti.wav
"""
import sys, wave
import numpy as np

SR = 48000
DUR = 20.0
N = int(SR * DUR)
rng = np.random.default_rng(11)
L = np.zeros(N); R = np.zeros(N)


def add(sig, start, pan=0.0, gain=1.0):
    i0 = int(start * SR)
    if i0 >= N: return
    sig = sig[: N - i0] * gain
    l = np.cos((pan + 1) * np.pi / 4); r = np.sin((pan + 1) * np.pi / 4)
    L[i0:i0 + len(sig)] += sig * l * 1.414
    R[i0:i0 + len(sig)] += sig * r * 1.414


def tt(dur): return np.arange(int(dur * SR)) / SR
def hz(m): return 440.0 * 2 ** ((m - 69) / 12)


def fft_lp(x, fc):
    """Sabit kesimli yumuşak alçak geçiren (FFT ile, hızlı)."""
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X / np.sqrt(1 + (f / fc) ** 4), len(x))


def sweep_noise(dur, f0, f1):
    """Bant geçiren gürültü; merkez frekansı f0→f1 kayar (kısa bloklarla)."""
    n = int(dur * SR); x = rng.standard_normal(n); out = np.zeros(n); B = 2048
    for i in range(0, n, B):
        fc = f0 * (f1 / f0) ** (i / n)
        seg = x[max(0, i - B): i + B]
        X = np.fft.rfft(seg); f = np.fft.rfftfreq(len(seg), 1 / SR)
        y = np.fft.irfft(X * np.exp(-((np.log2(f + 1) - np.log2(fc)) ** 2) / 0.5), len(seg))
        k = i - max(0, i - B); out[i:i + B] = y[k:k + B][: len(out[i:i + B])]
    return out / (np.abs(out).max() + 1e-9)


# ---------------- pad (akorlar, yavaş çapraz geçiş) ----------------
def pad(notes, start, end, gain, bright=1200, xf=1.4):
    d = end - start + xf; t = tt(d); s = np.zeros_like(t)
    for j, m in enumerate(notes):
        f = hz(m)
        for det in (-0.07, 0.0, 0.07):           # hafif koro (detune)
            ph = rng.uniform(0, 2 * np.pi)
            s += np.sin(2 * np.pi * f * (1 + det / 100) * t + ph) * 0.6
            s += np.sin(2 * np.pi * 2 * f * (1 + det / 100) * t + ph) * 0.12 * (bright / 2000)
    lfo = 0.85 + 0.15 * np.sin(2 * np.pi * 0.13 * t + rng.uniform(0, 6))
    e = np.minimum(1, t / xf) * np.minimum(1, (d - t) / xf)
    s = fft_lp(s * lfo * e, bright) / len(notes)
    add(s, start, pan=-0.25, gain=gain); add(np.roll(s, 900), start, pan=0.25, gain=gain)


pad([38, 45, 52, 53, 57, 64], 0.0, 8.6, 0.22, bright=700)          # Dm(add9) — merak
pad([34, 46, 50, 53, 57, 62, 69], 8.6, 12.9, 0.24, bright=1500)    # Bbmaj7 — genişleyen bakış
pad([31, 43, 50, 53, 57, 58, 62], 12.9, 16.5, 0.2, bright=1000)    # Gm9 — düşündüren mesaj
pad([38, 45, 50, 54, 57, 64, 66], 16.5, DUR, 0.23, bright=1600)    # D(add9) — çözülme / marka

# derin drone (sub)
t = tt(DUR)
drone = np.sin(2 * np.pi * hz(26) * t) * 0.5 + np.sin(2 * np.pi * hz(38) * t + 1) * 0.3
drone *= np.minimum(1, t / 3) * (1 - 0.6 * np.clip((t - 8.6) / 1.5, 0, 1)) * np.minimum(1, (DUR - t) / 1.5)
add(drone, 0, gain=0.16)

# ---------------- kalp atışı: görüntüdeki nabızla eşleşik ----------------
# ağrının parlaklığı sin(5.7 t) ile atıyor → tepe anları 0.2756 + k·1.1023 sn
def thump(f0=55, dur=0.35, g=1.0):
    t = tt(dur); f = f0 * (1 + 1.4 * np.exp(-t * 30))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 11) * g


per = 2 * np.pi / 5.7
k = 0
while True:
    tb = (np.pi / 2) / 5.7 + k * per - 0.05
    k += 1
    if tb > 12.7: break
    if tb < 1.7: continue
    amp = min(1, (tb - 1.7) / 1.2) * (1 - 0.65 * np.clip((tb - 8.6) / 0.4, 0, 1)) * (1 - np.clip((tb - 11.5) / 1.2, 0, 1))
    add(thump(52, g=1.0), tb, gain=0.55 * amp)
    add(thump(60, g=0.6), tb + 0.24, gain=0.55 * amp)

# ---------------- kristal tınılar (bağlantılar çizilirken) ----------------
def bell(m, dur=2.6):
    t = tt(dur); f = hz(m)
    s = (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 3) + 0.2 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 6))
    return s * np.exp(-t * 2.2) * np.minimum(1, t / 0.004)


scale_dm = [62, 64, 65, 69, 72, 74, 76, 77, 81]
for i, st in enumerate([4.05, 4.5, 4.95, 5.35, 5.8, 6.3, 6.85, 7.3]):    # yakın plan: seyrek, sorgulayan
    add(bell(scale_dm[(i * 3) % len(scale_dm)]), st, pan=rng.uniform(-.7, .7), gain=0.07)
arp = [74, 77, 81, 84, 86, 81, 77, 74, 72, 77, 81, 86]                     # geri çekiliş: açılan ağ
for i in range(22):
    st = 8.7 + i * 0.19
    add(bell(arp[i % len(arp)] - (0 if i < 12 else 2), 1.8), st, pan=np.sin(i * 1.3) * .8, gain=0.05 * (1 - i / 30))

# ---------------- riser + derin vuruş (8.6 sn) ----------------
rs = sweep_noise(1.3, 300, 6000); e = np.linspace(0, 1, len(rs)) ** 2.2
add(rs * e, 7.3, pan=-.2, gain=0.22); add(rs[::-1] * e, 7.3, pan=.2, gain=0.12)
t = tt(3.0); boom = np.sin(2 * np.pi * np.cumsum(38 * (1 + 1.5 * np.exp(-t * 9))) / SR) * np.exp(-t * 1.6)
add(boom, 8.6, gain=0.75)
air = sweep_noise(2.2, 5000, 900); add(air * np.exp(-np.linspace(0, 4, len(air))), 8.6, gain=0.14)

# mesaj girişi: yumuşak "nefes"
br = sweep_noise(1.5, 700, 2500); add(br * np.sin(np.pi * np.linspace(0, 1, len(br))) ** 2, 12.3, gain=0.08)

# ---------------- marka çanı (16.5 sn) ----------------
for j, m in enumerate([62, 69, 74, 78, 81]):
    add(bell(m, 3.5), 16.55 + j * 0.06, pan=(j - 2) * .3, gain=0.09)
t = tt(2.5); add(np.sin(2 * np.pi * hz(38) * t) * np.exp(-t * 2.2), 16.5, gain=0.4)


# ---------------- reverb ----------------
def reverb(x, seconds=3.2, seed=1):
    r = np.random.default_rng(seed); n = int(seconds * SR); t = np.arange(n) / SR
    ir = fft_lp(r.standard_normal(n) * np.exp(-t * 2.4), 4500); ir /= np.sqrt((ir ** 2).sum())
    m = len(x) + n; nfft = 1 << (m - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, nfft) * np.fft.rfft(ir, nfft), nfft)[: len(x)]


L2 = L + 0.45 * reverb(L, seed=1); R2 = R + 0.45 * reverb(R, seed=2)
st = np.stack([L2, R2], 1); st /= np.abs(st).max()
st = np.tanh(st * 1.3) / np.tanh(1.3) * 10 ** (-1.0 / 20)
fade = np.ones(N); fo = int(0.6 * SR); fade[-fo:] = np.linspace(1, 0, fo) ** 1.5
st *= fade[:, None]
with wave.open(sys.argv[1] if len(sys.argv) > 1 else 'muzik.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
print('ok')
