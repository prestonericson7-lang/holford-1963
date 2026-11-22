"""A third check, by different arithmetic: the findings recomputed with floating-point Fourier transforms (NumPy's) in place of the integer Q14
ones, sharing nothing with holford.analyze but the scan and the band edges. (1) The strongest circular harmonic in each band for the 12 wheels and
the railyard's 12 turns. (2) Every lamp, with the same gain control in floating point, for conflex-1965's 240 pictures, and the plain
nearest-mean rule on them."""
import json, os
import numpy as np
import holford as H, prenorm as P, shapes as S

def band_powers(img):
    v = P.scan(img, 2, H.LINES).reshape(H.LINES, H.PULSE + P.GAP)[:, :H.PULSE].astype(float)
    ps = np.abs(np.fft.rfft(np.pad(v, ((0, 0), (0, H.NFFT - H.PULSE))), axis=1)) ** 2
    return np.stack([ps[:, lo:hi + 1].sum(1) for lo, hi in H.BANDS], 1)

def lamps_and_strongest(img):
    bp = band_powers(img); tot = bp.sum(0); first = tot / tot.sum(); second = []; strongest = []
    for b in range(7):
        share = bp[:, b] / tot[b] if tot[b] > 0 else np.zeros(H.LINES)
        hp = np.abs(np.fft.rfft(share)) ** 2
        second += [hp[lo:hi + 1].sum() / hp[0] if hp[0] > 0 else 0.0 for lo, hi in H.GROUPS]
        strongest.append(int(np.argmax(hp[1:])) + 1)
    return np.concatenate([first, second]), strongest

ints = json.load(open("results/h1_h4.json"))
wheels = [lamps_and_strongest(S.render(H.wheel(i)))[1] for i in range(12)]
turns = [lamps_and_strongest(S.render(S.place(S.railyard(), d)))[1] for d in range(0, 360, 30)]
out = {"wheels_band6_float": [w[6] for w in wheels], "wheels_band6_integer": ints["H3"]["strongest_band6"],
       "turns_band6_float": [t[6] for t in turns], "turns_band6_integer": ints["H4"]["strongest_band6"],
       "all_bands_same_as_integer": [w for w in wheels] == ints["H3"]["all_strongest_by_band"] and [t for t in turns] == ints["H4"]["all_strongest_by_band"]}

rng = lambda s: np.random.Generator(np.random.PCG64(s))
def lamps_of(seed):
    g = rng(seed); X, y = [], []
    for k in range(4):
        for _ in range(30):
            strips, _ = S.example(k, g); X.append(lamps_and_strongest(S.render(strips))[0]); y.append(k)
    return np.array(X), np.array(y)
Xt, yt = lamps_of(1965); Xh, yh = lamps_of(1966)
lt, lh = np.log10(1 + Xt * 2 ** 20), np.log10(1 + Xh * 2 ** 20); mu, sd = lt.mean(0), lt.std(0); sd[sd == 0] = 1
means = np.array([((lt - mu) / sd)[yt == k].mean(0) for k in range(4)])
pred = np.array([int(np.argmin(((means - (z - mu) / sd) ** 2).sum(1))) for z in lh])
out["nearest_mean_float"] = int((pred == yh).sum())
json.dump(out, open("results/verify_float.json", "w"), indent=1)
print("wheels, band 6, float:  ", out["wheels_band6_float"], "\n         integer:", out["wheels_band6_integer"])
print("railyard, band 6, float:", out["turns_band6_float"], "\n         integer:", out["turns_band6_integer"])
print("every band's strongest harmonic the same in float as in integers, wheels and turns:", out["all_bands_same_as_integer"])
print("plain nearest-mean rule on float lamps:", out["nearest_mean_float"], "of 120")
