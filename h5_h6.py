"""H5 and H6: CONFLEX on Holford's 42 lamps, on conflex-1965's 240 pictures (DATA.md there; the same seeds, so the same pictures, checked here
against conflex-1965's own saved counts). Reported beside: the first level's 7 lamps alone, six wirings, a plain nearest-mean rule."""
import json, time
import numpy as np
import holford as H, prenorm as P, shapes as S
from conflex import Conflex
KN, PER, ND = 4, 30, 4000
import os
CONFLEX_COUNTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "conflex-1965", "results", "p3p4_counts.json")   # a conflex-1965 checkout beside this one

def draw(seed):
    rng = np.random.Generator(np.random.PCG64(seed)); out = []
    for k in range(KN):
        for _ in range(PER):
            strips, meta = S.example(k, rng); out.append((k, strips))
    return out

def thermo(teach, rows):
    lo, hi = teach.min(0), teach.max(0); nl = teach.shape[1]; X = np.zeros((len(rows), 16 * nl), np.int64)
    for i, c in enumerate(rows):
        for n in range(nl):
            if hi[n] > lo[n]:
                for j in range(1, 17):
                    X[i, 16 * n + j - 1] = int(17 * int(c[n]) >= 17 * int(lo[n]) + j * (int(hi[n]) - int(lo[n])))
    return X

def conflex_acc(Xt, yt, Xh, yh, seed=0x1F2E3D4C):
    cf = Conflex(Xt.shape[1], ND, 5, 5, classes=KN, seed=seed)
    for x, y in zip(Xt, yt): cf.condition(x, y)
    pred = np.array([cf.classify(x) for x in Xh]); table = np.zeros((KN, KN), int)
    for a, b in zip(yh, pred): table[a, b] += 1
    return float((pred == yh).mean()), table.tolist()

t0 = time.time(); rec = {}
for split, seed in (("teach", 1965), ("held", 1966)):
    rows = []
    for k, strips in draw(seed):
        img = S.render(strips); a = H.analyze(img)
        rows.append({"kind": k, "lamps": a["first"] + a["second"], "first_design_counts": P.counts(img)})
    rec[split] = rows
old = json.load(open(CONFLEX_COUNTS))
same = all(r["first_design_counts"] == o["first"] for s in ("teach", "held") for r, o in zip(rec[s], old[s]))
yt = np.array([r["kind"] for r in rec["teach"]]); yh = np.array([r["kind"] for r in rec["held"]])
Lt = np.array([r["lamps"] for r in rec["teach"]], dtype=object); Lh = np.array([r["lamps"] for r in rec["held"]], dtype=object)
Xt, Xh = thermo(Lt, Lt), thermo(Lt, Lh)
acc, table = conflex_acc(Xt, yt, Xh, yh)
acc1, table1 = conflex_acc(thermo(Lt[:, :7], Lt[:, :7]), yt, thermo(Lt[:, :7], Lh[:, :7]), yh)
wirings = [conflex_acc(Xt, yt, Xh, yh, sd)[0] for sd in (0x1F2E3D4C, 0x0BADF00D, 0x13579BDF, 0x2468ACE1, 0x5EED1965, 0x7FFFFFFF)]
lt, lh = np.log10(1 + Lt.astype(float)), np.log10(1 + Lh.astype(float)); mu, sd = lt.mean(0), lt.std(0); sd[sd == 0] = 1
means = np.array([((lt - mu) / sd)[yt == k].mean(0) for k in range(KN)])
nm = float(np.mean([int(np.argmin((((means - (z - mu) / sd)) ** 2).sum(1))) == y for z, y in zip(lh, yh)]))
out = {"same_pictures_as_conflex_1965": same, "seconds": None, "H5_accuracy": acc, "H5_table": table, "H5_held": acc >= 0.90,
       "H6_vs_first_design": 100 / 120, "H6_held": acc >= 100 / 120 - 1e-12, "first_level_only": acc1, "first_level_only_table": table1,
       "six_wirings": wirings, "nearest_mean": nm}
json.dump({**out, "rows": rec}, open("results/h5_h6.json", "w"))
print("same pictures as conflex-1965 (its first-design counts reproduced for all 240):", same, f"| {time.time() - t0:.1f} s")
print(f"H5 {'held' if out['H5_held'] else 'FAILED'}: CONFLEX on all 42 lamps names {round(acc * 120)} of 120 held-out pictures right ({100 * acc:.1f}%)")
for k, row in enumerate(table): print(f"    {S.KINDS[k]:>10} ->", row)
print(f"H6 {'held' if out['H6_held'] else 'FAILED'}: against the 1967 first design's 83.3%")
print(f"beside: first level alone {100 * acc1:.1f}%; six wirings " + ", ".join(f"{100 * w:.1f}" for w in wirings) + f"; nearest-mean rule {100 * nm:.1f}%")
