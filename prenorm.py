"""Scope Incorporated's time-domain prenormalizer (US patent 3,566,080, filed April 27, 1967), rebuilt in integers. The integral scanner turns
the image once while 64 mirror strips sweep across it; each strip gives one pulse, the image's line integrals at one angle. Six normalized
time-domain filters (NTDFs) correlate the last T samples of that video with fixed reference functions L0 to L5, and six counters count how
often each one's |correlation| rises above the threshold during one full turn. Every choice the patent leaves open is written in DESIGN.md."""
from functools import lru_cache
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
Q, K, N, T, GAP = 14, 64, 128, 16, 16
THETA_NUM, THETA_DEN = 4, 5                                     # the threshold, 4/5
_h = 2 * np.arange(N, dtype=np.int64) - (N - 1)               # pixel centers in half-pixel units; the field's center is 0
HX, HY = np.meshgrid(_h, _h)
_disk = (HX ** 2 + HY ** 2 <= (2 * 64) ** 2).ravel()           # the same disk as shapes.DISK
_hx, _hy = HX.ravel()[_disk], HY.ravel()[_disk]

@lru_cache(maxsize=None)
def bands(strips):
    """Each field pixel's one-pixel band for each of the strips, from Q14 integer cosines and sines of 360 k / strips degrees."""
    ang = 2 * np.pi * np.arange(strips) / strips
    ck = np.round((1 << Q) * np.cos(ang)).astype(np.int64); sk = np.round((1 << Q) * np.sin(ang)).astype(np.int64)
    b = np.stack([(((_hx * ck[k] + _hy * sk[k]) >> Q) >> 1) + N // 2 for k in range(strips)])
    assert b.min() >= 0 and b.max() < N
    return b
BANDS = bands(K)                                                # the design as first fixed: 64 strips
L = np.round(127 * np.cos(np.pi * np.outer(np.arange(1, 7), np.arange(T) + 0.5) / T)).astype(np.int64)   # L0..L5: cosines k = 1..6, integer weights

def _fine_grid(fine):
    """Part centers in units of 1 / (2 fine) pixel, the field's center at 0, kept where their whole pixel is in the field."""
    h = 2 * np.arange(N * fine, dtype=np.int64) + 1 - N * fine
    gx, gy = np.meshgrid(h, h)
    keep = np.repeat(np.repeat(_disk.reshape(N, N), fine, 0), fine, 1).ravel()
    return gx.ravel()[keep], gy.ravel()[keep], keep

def scan(img, strip=1, strips=K, fine=1):
    """One full turn of the integral scanner's video: one pulse per strip (64 as first fixed, 403 in amendment A2), each followed by 16 samples of dark spacer. With strip=1 (the design as first
    fixed) a pulse is the 128 one-pixel bands' line integrals; with strip=2 (amendment A1, the patent's 2T(omega)0 rule) each sample is the sum
    of two neighboring bands, 129 samples as the strip enters, crosses and leaves the field."""
    if fine == 1:
        v = np.asarray(img, np.int64).ravel()[_disk]; B = bands(strips); nb = N
    else:                                                       # amendment A3: each pixel read as fine x fine parts; one spare band each side
        gx, gy, keep = _fine_grid(fine); v = np.asarray(img, np.int64).ravel()[keep]; nb = N + 2
        ang = 2 * np.pi * np.arange(strips) / strips
        ck = np.round((1 << Q) * np.cos(ang)).astype(np.int64); sk = np.round((1 << Q) * np.sin(ang)).astype(np.int64)
        shift = int(np.log2(2 * fine)); assert 1 << shift == 2 * fine
    parts = []
    for k in range(strips):
        if fine == 1:
            bk = B[k]
        else:
            bk = (((gx * ck[k] + gy * sk[k]) >> Q) >> shift) + N // 2 + 1
            assert bk.min() >= 0 and bk.max() < nb
        pk = np.rint(np.bincount(bk, weights=v, minlength=nb)).astype(np.int64)     # float sums of integers below 2^53 are exact
        assert pk.sum() == v.sum()
        if strip > 1:
            pk = np.convolve(pk, np.ones(strip, np.int64)); assert pk.dtype == np.int64 and pk.sum() == strip * v.sum()
        parts += [pk, np.zeros(GAP, np.int64)]
    return np.concatenate(parts)

def ntdf_events(video):
    """For every window of the last T samples (column 0 the oldest), whether each NTDF's |Phi| exceeds 4/5. Phi = cov / sqrt(varV varL) with
    cov = T sum(v l) - sum(v) sum(l) and var = T sum(x^2) - (sum x)^2, so the test is exact in integers: 25 cov^2 > 16 varV varL, and varV > 0."""
    W = sliding_window_view(np.asarray(video, np.int64), T)
    sv = W.sum(1); svv = (W * W).sum(1); svl = W @ L.T
    sl = L.sum(1); sll = (L * L).sum(1)
    varV = T * svv - sv * sv; varL = T * sll - sl * sl
    cov = T * svl - sv[:, None] * sl[None, :]
    assert varV.max() * varL.max() * THETA_DEN ** 2 < 2 ** 63   # and cov^2 <= varV varL always, so nothing below overflows
    return (THETA_DEN ** 2 * cov * cov > THETA_NUM ** 2 * varV[:, None] * varL[None, :]) & (varV[:, None] > 0)

def counts_of_video(video):
    e = ntdf_events(video)
    rising = e & ~np.vstack([np.zeros((1, e.shape[1]), bool), e[:-1]])
    return [int(x) for x in rising.sum(0)]

def counts(img, strip=1, strips=K, fine=1):
    """The six counters after one full turn."""
    return counts_of_video(scan(img, strip, strips, fine))
