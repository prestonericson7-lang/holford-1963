"""Warren L. Holford's 1963 image analyzer (US patent 3,508,065), rebuilt in integers: the integral scan with 39 grid lines a turn, a first
bank of seven octave band-pass "property filters" with coarse gain control, and a second bank of "circular harmonic" filters on each rectified
band. Every choice the patent leaves open is in DESIGN.md."""
import math
import numpy as np
import prenorm as P

Q = 14
LINES, PULSE, NFFT = 39, 129, 256
BANDS = [(1 << b, (1 << (b + 1)) - 1) for b in range(7)]              # band b: frequencies 2^b .. 2^(b+1) - 1, in cycles per 256 samples
GROUPS = [(1, 1), (2, 2), (3, 4), (5, 8), (9, 19)]                      # the second level's five filters, in harmonics a turn

def _shift(a):
    return (a + (1 << (Q - 1))) >> Q

def _tables(n, nf):
    ang = 2 * np.pi * np.outer(np.arange(nf), np.arange(n)) / n
    return np.round((1 << Q) * np.cos(ang)).astype(np.int64), np.round((1 << Q) * np.sin(ang)).astype(np.int64)

C256, S256 = _tables(NFFT, NFFT // 2 + 1)                               # 129 frequencies x 256 samples
C39, S39 = _tables(LINES, LINES // 2 + 1)                               # 20 harmonics (0 to 19) x 39 grid lines

def pulses(img):
    """The 39 pulses of one turn, 129 samples each (2-band lines; the dark between them dropped)."""
    v = P.scan(img, 2, LINES).reshape(LINES, PULSE + P.GAP)[:, :PULSE]
    return np.ascontiguousarray(v)

def power_spectra(pls):
    """Each pulse padded to 256 samples: its power at frequencies 0 to 128, by an integer Q14 Fourier transform."""
    x = np.zeros((pls.shape[0], NFFT), np.int64); x[:, :PULSE] = pls
    re = _shift(x @ C256.T); im = _shift(x @ S256.T)
    return re * re + im * im

def analyze(img):
    """Both banks of lamps for one picture, and the strongest circular harmonic of each band."""
    ps = power_spectra(pulses(img))
    bp = np.stack([ps[:, lo:hi + 1].sum(1) for lo, hi in BANDS], 1)       # each pulse's power in each band: 39 x 7
    tot = [int(x) for x in bp.sum(0)]; total = sum(tot)
    first = [(t << 20) // total if total else 0 for t in tot]          # coarse gain control: each lamp as a share of all seven
    second, strongest = [], []
    for b in range(7):
        share = np.array([(int(p) << 16) // tot[b] if tot[b] else 0 for p in bp[:, b]], np.int64)
        re = _shift(C39 @ share); im = _shift(S39 @ share); hp = re * re + im * im          # harmonics 0 .. 19 a turn
        e0 = int(hp[0])
        second += [(int(hp[lo:hi + 1].sum()) << 20) // e0 if e0 else 0 for lo, hi in GROUPS]
        strongest.append(int(np.argmax(hp[1:])) + 1)                    # 1 .. 19; a tie goes to the lower harmonic
    return {"first": first, "second": second, "strongest": strongest, "band_power": tot}

def wheel(i):
    """DESIGN.md's wheel i: ten spokes 1.5 pixels wide, from 3 pixels out to R = 20 + 2.5 i, 36 degrees apart, turned 7 i degrees, the hub
    moved 3 (i mod 3) pixels toward 30 i degrees."""
    R, turn, d, a = 20 + 2.5 * i, 7 * i, 3 * (i % 3), math.radians(30 * i)
    dx, dy = d * math.cos(a), d * math.sin(a); out = []
    for s in range(10):
        th = math.radians(36 * s + turn)
        out.append((3 * math.cos(th) + dx, 3 * math.sin(th) + dy, R * math.cos(th) + dx, R * math.sin(th) + dy, 1.5))
    return out
