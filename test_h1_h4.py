"""H1 to H4: the railyard's first-level lamps over conflex-1965's 12 turns and 13 shifts; the strongest circular harmonic of band 6 for the 12
ten-spoked wheels and for the railyard's 12 turns. The sets are DESIGN.md's."""
import json, math
import numpy as np
import holford as H, shapes as S
ry = S.railyard()
turns = list(range(0, 360, 30))
shifts = [(0.0, 0.0)] + [(8 * math.cos(math.radians(a)), 8 * math.sin(math.radians(a))) for a in range(0, 360, 45)] \
         + [(4 * math.cos(math.radians(a)), 4 * math.sin(math.radians(a))) for a in range(0, 360, 90)]
A1 = [H.analyze(S.render(S.place(ry, d))) for d in turns]
A2 = [H.analyze(S.render(S.place(ry, 0.0, dx, dy))) for dx, dy in shifts]
W = [H.analyze(S.render(H.wheel(i))) for i in range(12)]
def steady(rows):
    C = np.array([r["first"] for r in rows], float); m = C.mean(0)
    dev = np.where(m > 0, np.abs(C - m).max(0) / np.where(m > 0, m, 1), 0.0)
    return {"mean_share": (m / 2 ** 20).round(4).tolist(), "worst_rel_dev": dev.round(4).tolist(), "held": bool((dev <= 0.15).all())}
out = {"H1": steady(A1), "H2": steady(A2),
       "H3": {"strongest_band6": [w["strongest"][6] for w in W], "all_strongest_by_band": [w["strongest"] for w in W]},
       "H4": {"strongest_band6": [a["strongest"][6] for a in A1], "all_strongest_by_band": [a["strongest"] for a in A1]},
       "rows": {"turns": A1, "shifts": A2, "wheels": W}}
out["H3"]["held"] = all(x == 10 for x in out["H3"]["strongest_band6"])
out["H4"]["held"] = all(x == 2 for x in out["H4"]["strongest_band6"])
json.dump(out, open("results/h1_h4.json", "w"), indent=1)
for k in ("H1", "H2"):
    print(k, "held" if out[k]["held"] else "FAILED", "| mean shares", out[k]["mean_share"], "| worst rel dev", out[k]["worst_rel_dev"])
print("H3", "held" if out["H3"]["held"] else "FAILED", "| wheels, strongest harmonic in band 6:", out["H3"]["strongest_band6"])
print("H4", "held" if out["H4"]["held"] else "FAILED", "| railyard turns, strongest harmonic in band 6:", out["H4"]["strongest_band6"])
print("wheels, strongest by band (0..6):"); [print("  ", r) for r in out["H3"]["all_strongest_by_band"]]
