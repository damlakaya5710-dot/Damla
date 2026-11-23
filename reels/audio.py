"""Damla Isı Pompası Reels — prosedürel müzik + ses efektleri (15 sn, 48 kHz stereo).
Kullanım: python3 audio.py cikti.wav
"""
import sys, wave
import numpy as np

SR = 48000
INS0, D = 9.85, 2.2   # sıcak su sahnesi (görüntüyle aynı ekleme)
DUR = 15.0 + D
N = int(SR * DUR)
t = np.arange(N) / SR
rng = np.random.default_rng(7)
L = np.zeros(N); Rr = np.zeros(N)

def add(sig, start, pan=0.0, gain=1.0, raw=False):
    if not raw and start >= INS0: start += D
    i0 = int(start * SR)
    if i0 >= N: return
    sig = sig[: N - i0] * gain
    l = np.cos((pan + 1) * np.pi / 4); r = np.sin((pan + 1) * np.pi / 4)
    L[i0:i0 + len(sig)] += sig * l * 1.414
    Rr[i0:i0 + len(sig)] += sig * r * 1.414

def env_adsr(n, a, d, s, r_):
    e = np.ones(n) * s
    na, nd, nr = int(a * SR), int(d * SR), int(r_ * SR)
    e[:na] = np.linspace(0, 1, na)
    e[na:na + nd] = np.linspace(1, s, nd)
    if nr > 0: e[-nr:] *= np.linspace(1, 0, nr)
    return e

def onepole_lp(x, fc):
    """fc: sabit ya da örnek başına dizi (Hz)."""
    fc = np.broadcast_to(np.asarray(fc, float), x.shape)
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x); z = 0.0
    for i in range(len(x)):
        z = (1 - a[i]) * x[i] + a[i] * z; y[i] = z
    return y

def bandnoise(dur, f0, f1, q=2.0):
    n = int(dur * SR); x = rng.standard_normal(n)
    fc = np.geomspace(f0, f1, n)
    lp = onepole_lp(onepole_lp(x, fc * q), fc * q)
    hp = lp - onepole_lp(lp, fc / q)
    return hp / (np.abs(hp).max() + 1e-9)

def note(f): return 440.0 * 2 ** ((f - 69) / 12)

# ---------- pad (akorlar) ----------
chords = [  # hikâye zamanı (başlangıç, bitiş, midi notaları) — arpej için
    (0.0, 5.05, [38, 50, 57, 64, 65, 72]),     # Dm9 — merak
    (5.05, 7.6, [34, 46, 53, 57, 62, 69]),     # Bbmaj7 — sıcak
    (7.6, 9.85, [43, 55, 58, 62, 65, 69]),     # Gm9 — serin
    (9.85, 12.88, [45, 57, 62, 64, 69, 71]),   # Asus — gerilim
    (12.88, 15.0, [38, 50, 57, 62, 66, 69, 76]),  # D(add9) — çözülme / logo
]
WCH = [41, 53, 57, 60, 64, 67]                 # Fmaj9 — sıcak su
pads = [(0.0, 5.05, chords[0][2]), (5.05, 7.6, chords[1][2]), (7.6, INS0, chords[2][2]),
        (INS0, INS0 + D, WCH), (INS0 + D, 12.88 + D, chords[3][2]), (12.88 + D, DUR, chords[4][2])]
for (a, b, notes) in pads:
    dur = b - a + 0.6
    n = int(dur * SR); tt = np.arange(n) / SR
    sig = np.zeros(n)
    for k, m in enumerate(notes):
        f = note(m)
        for det in (-0.12, 0.0, 0.12):
            ff = f * 2 ** (det / 12)
            ph = rng.random() * 2 * np.pi
            saw = 2 * ((ff * tt + ph / (2 * np.pi)) % 1) - 1
            sig += (0.55 * saw + 0.45 * np.sin(2 * np.pi * ff * tt + ph)) / (1 + 0.15 * k)
    cutoff = 900 + 700 * np.sin(np.pi * np.clip(tt / dur, 0, 1))
    if a >= 12.88 + D: cutoff = 1800 + 1500 * np.exp(-tt * 1.5)
    sig = onepole_lp(onepole_lp(sig, cutoff), cutoff)
    sig *= env_adsr(n, 0.25 if a > 0 else 0.05, 0.3, 0.85, 0.6) / len(notes)
    add(sig, a, pan=0.0, gain=0.55 if a < 12.88 + D else 0.7, raw=True)

# ---------- arpej (tempo hissi) ----------
step = 0.25
k = 0
s0 = 2.2
while s0 + k * step < 12.6:
    st = s0 + k * step
    ch = [c for c in chords if c[0] <= st < c[1]][0][2]
    m = ch[2:][(k * 3) % (len(ch) - 2)] + 12
    f = note(m); n = int(0.45 * SR); tt = np.arange(n) / SR
    pl = (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2 * f * tt)) * np.exp(-tt * 9)
    vel = 0.5 + 0.5 * ((k % 4) == 0)
    if 9.9 < st < 10.9: vel *= 0.35
    add(pl, st, pan=0.45 if k % 2 else -0.45, gain=0.10 * vel)
    k += 1
# sıcak su sahnesi arpeji
for j in range(int(D / step)):
    st = INS0 + j * step; m = WCH[2:][(j * 3) % 4] + 12
    f = note(m); n = int(0.45 * SR); tt = np.arange(n) / SR
    pl = (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2 * f * tt)) * np.exp(-tt * 9)
    add(pl, st, pan=0.45 if j % 2 else -0.45, gain=0.10 * (0.5 + 0.5 * (j % 4 == 0)), raw=True)
# ---------- sub vuruşlar ----------
def boom(f0=55, dec=2.2, dur=2.0, click=0.3):
    n = int(dur * SR); tt = np.arange(n) / SR
    f = f0 * (1 + 2.5 * np.exp(-tt * 30))
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-tt * dec)
    s += click * rng.standard_normal(n) * np.exp(-tt * 80)
    return np.tanh(s * 1.6)
for (st, g, f0) in [(0.0, 0.9, 46), (2.22, 0.45, 52), (5.06, 0.6, 50), (7.6, 0.7, 49), (10.95, 0.55, 55), (12.88, 1.0, 44)]:
    add(boom(f0), st, gain=g)

# ---------- whoosh / riser ----------
for (st, dur, f0, f1, g, pan) in [(1.95, 0.75, 300, 4000, 0.5, -0.3), (4.75, 0.6, 400, 6000, 0.55, 0.6),
                                  (7.35, 0.55, 500, 7000, 0.55, -0.6), (12.0, 0.9, 200, 9000, 0.8, 0.0)]:
    w = bandnoise(dur, f0, f1)
    n = len(w); e = np.sin(np.pi * np.linspace(0, 1, n)) ** 1.5
    if st == 12.0: e = np.linspace(0, 1, n) ** 2.5
    add(w * e, st, pan=pan, gain=g)

# fan dönüş sesi (0.3–2.4)
n = int(2.4 * SR); tt = np.arange(n) / SR
sp = np.clip(tt / 1.3, 0, 1) ** 0.6
hum_f = 60 + 160 * sp
hum = np.sin(2 * np.pi * np.cumsum(hum_f) / SR) * 0.5 + np.sin(2 * np.pi * np.cumsum(hum_f * 5) / SR) * 0.15
air = bandnoise(2.4, 500, 2500, 1.5)
fan = (hum + air * 0.8) * (sp * np.clip((2.4 - tt) / 0.6, 0, 1))
add(fan, 0.3, gain=0.18)

# ısıtma: sıcak yükselen ton
n = int(2.6 * SR); tt = np.arange(n) / SR
warm = sum(np.sin(2 * np.pi * note(m) * tt * (1 + 0.002 * np.sin(tt * 5))) for m in (58, 65, 70)) / 3
add(warm * env_adsr(n, 0.6, 0.4, 0.7, 0.8), 5.1, gain=0.10)

# soğutma: buz pırıltısı
for i in range(40):
    f = rng.uniform(3000, 9000); st = 7.6 + rng.uniform(0, 1.6)
    n = int(0.6 * SR); tt = np.arange(n) / SR
    add(np.sin(2 * np.pi * f * tt) * np.exp(-tt * rng.uniform(6, 14)), st, pan=rng.uniform(-0.8, 0.8), gain=0.035)
ice = bandnoise(0.9, 9000, 2000, 3)
add(ice * np.exp(-np.linspace(0, 5, len(ice))), 7.6, gain=0.35)

# verim: 1 kıvılcım + 4 çan
n = int(0.6 * SR); tt = np.arange(n) / SR
add(np.sin(2 * np.pi * np.cumsum(300 + 2500 * (tt / 0.6) ** 2) / SR) * np.sin(np.pi * tt / 0.6) * 0.5, 10.4, gain=0.25)
def bell(f, dur=2.5):
    n = int(dur * SR); tt = np.arange(n) / SR
    s = (np.sin(2 * np.pi * f * tt) * np.exp(-tt * 2.2) + 0.5 * np.sin(2 * np.pi * f * 2.76 * tt) * np.exp(-tt * 4)
         + 0.25 * np.sin(2 * np.pi * f * 5.4 * tt) * np.exp(-tt * 7))
    return s * np.minimum(1, tt * 400)
for i, m in enumerate([74, 76, 78, 81]):
    add(bell(note(m)), 10.95 + i * 0.2, pan=(-0.5 + i / 3), gain=0.16)
# logo çanı
for m, d in [(78, 0.0), (81, 0.04), (86, 0.08)]:
    add(bell(note(m), 2.0), 13.4 + d, gain=0.13)
add(bell(note(90), 1.6), 14.3, gain=0.06)

# su: whoosh, damla "plip", sıçrama, kabarcıklar, buhar
w = bandnoise(0.6, 400, 6000); add(w * np.sin(np.pi * np.linspace(0, 1, len(w))) ** 1.5, INS0 - 0.25, pan=0.5, gain=0.45, raw=True)
n = int(0.25 * SR); tt = np.arange(n) / SR
add(np.sin(2 * np.pi * np.cumsum(700 + 1800 * (tt / 0.25) ** 0.5) / SR) * np.exp(-tt * 18), INS0 + 0.5, gain=0.35, raw=True)
add(boom(60, dec=4, dur=1.0, click=0.15), INS0 + 0.5, gain=0.35, raw=True)
sp = bandnoise(0.5, 6000, 1500, 2); add(sp * np.exp(-np.linspace(0, 6, len(sp))), INS0 + 0.5, gain=0.3, raw=True)
for i in range(28):
    st = INS0 + 0.6 + rng.uniform(0, 1.3); n = int(0.08 * SR); tt = np.arange(n) / SR
    f0 = rng.uniform(500, 1400)
    add(np.sin(2 * np.pi * np.cumsum(f0 * (1 + 3 * tt / 0.08)) / SR) * np.exp(-tt * 50), st, pan=rng.uniform(-.6, .6), gain=0.06, raw=True)
stm = bandnoise(1.4, 3000, 1200, 1.2); add(stm * np.sin(np.pi * np.linspace(0, 1, len(stm))), INS0 + 0.9, gain=0.12, raw=True)
w = bandnoise(0.55, 500, 6000); add(w * np.sin(np.pi * np.linspace(0, 1, len(w))) ** 1.5, INS0 + 1.65, pan=-0.5, gain=0.4, raw=True)


# ---------- reverb (gürültü tepkisi ile konvolüsyon) ----------
def reverb(x, seconds=2.6, seed=1):
    r = np.random.default_rng(seed)
    n = int(seconds * SR); tt = np.arange(n) / SR
    ir = r.standard_normal(n) * np.exp(-tt * 3.2)
    ir = onepole_lp(ir, 5000); ir /= np.sqrt((ir ** 2).sum())
    m = len(x) + n
    nfft = 1 << (m - 1).bit_length()
    y = np.fft.irfft(np.fft.rfft(x, nfft) * np.fft.rfft(ir, nfft), nfft)[: len(x)]
    return y
wetL, wetR = reverb(L, seed=1), reverb(Rr, seed=2)
L2 = L + 0.35 * wetL; R2 = Rr + 0.35 * wetR

# ---------- mastering ----------
st = np.stack([L2, R2], 1)
st /= np.abs(st).max()
st = np.tanh(st * 1.4) / np.tanh(1.4)
st *= 10 ** (-1.0 / 20)
fade = np.ones(N); fo = int(0.25 * SR); fade[-fo:] = np.linspace(1, 0, fo)
st *= fade[:, None]
pcm = (st * 32767).astype(np.int16)
with wave.open(sys.argv[1] if len(sys.argv) > 1 else 'audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok')
