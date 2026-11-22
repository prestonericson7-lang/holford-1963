"""H0: the same numbers on every run; and the integer Fourier transform against a floating-point one, for scale."""
import hashlib, json, subprocess, sys
import numpy as np
import holford as H, shapes as S

def digest():
    pics = [S.render(S.railyard()), S.render(H.wheel(0)), S.render(H.wheel(7))]
    return hashlib.sha256(json.dumps([H.analyze(p) for p in pics]).encode()).hexdigest(), pics

if len(sys.argv) > 1:
    print(digest()[0]); sys.exit()
runs = [subprocess.run([sys.executable, "test_h0.py", "--once"], capture_output=True, text=True, check=True).stdout.strip() for _ in range(2)]
d, pics = digest()
pls = H.pulses(pics[0]); ours = H.power_spectra(pls).astype(float)
x = np.zeros((pls.shape[0], H.NFFT)); x[:, :H.PULSE] = pls; ref = np.abs(np.fft.rfft(x, axis=1)) ** 2
band = lambda ps: np.stack([ps[:, lo:hi + 1].sum(1) for lo, hi in H.BANDS], 1)
rel = np.abs(band(ours) - band(ref)) / np.maximum(band(ref), 1)
out = {"run1": runs[0], "run2": runs[1], "here": d, "H0_held": runs[0] == runs[1] == d,
       "worst_band_power_rel_error_vs_float_fft": float(rel[band(ref) > 1e6].max())}
json.dump(out, open("results/h0.json", "w"), indent=1); print(json.dumps(out, indent=1))
