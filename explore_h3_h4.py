"""Exploratory, after the H1 to H4 results and before their grades are written: what makes the railyard's band 6 peak at 8 and 16 a turn, and
does the wheels' 19 in the middle bands come from twenty a turn folded by 39 lines? (1) The railyard at a turn of 0: the pulses carrying most
of band 6's power, and their lines' angles to the yard. (2) The same wheels scanned with 403 lines instead of 39 (nothing folds below 201 a
turn): the strongest harmonic in each band."""
import json, math
import numpy as np
import holford as H, prenorm as P, shapes as S

def band_power_per_pulse(img, lines):
    v = P.scan(img, 2, lines).reshape(lines, H.PULSE + P.GAP)[:, :H.PULSE]
    ps = H.power_spectra(np.ascontiguousarray(v))
    return np.stack([ps[:, lo:hi + 1].sum(1) for lo, hi in H.BANDS], 1)

out = {}
bp = band_power_per_pulse(S.render(S.railyard()), 39)
b6 = bp[:, 6].astype(float); share = b6 / b6.sum()
order = np.argsort(-share)[:6]
out["railyard_band6_top_pulses"] = [{"line": int(k), "angle_deg": round(360 * k / 39, 1), "share": round(float(share[k]), 3)} for k in order]
print("railyard, turn 0, band 6: the six pulses with the most power (line angle in degrees, share of the band's power over the turn):")
for r in out["railyard_band6_top_pulses"]: print("   ", r)

def strongest(bp, lines):
    best = []
    for b in range(7):
        e = bp[:, b].astype(float); e = e / max(e.sum(), 1)
        h = np.abs(np.fft.rfft(e)) ** 2
        best.append(int(np.argmax(h[1:])) + 1)
    return best
out["wheels_403_lines_strongest_by_band"] = [strongest(band_power_per_pulse(S.render(H.wheel(i)), 403), 403) for i in range(12)]
print("wheels scanned with 403 lines, strongest harmonic a turn in bands 0..6:")
for i, r in enumerate(out["wheels_403_lines_strongest_by_band"]): print("   wheel", i, r)
json.dump(out, open("results/explore_h3_h4.json", "w"), indent=1)
