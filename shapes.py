"""The pictures the prenormalizer is shown. Shapes are drawn in floating point (the world is analog) as unions of straight strips, each a segment
with a width and flat ends, and each pixel's value is how many of its 8 x 8 sub-points fall inside the shape: 0 to 64, light objects on a dark
ground, the way a transparency passes light. Only the disk of radius 64 around the center is kept, because the image turns inside the scanner."""
import math
import numpy as np
N, SUB, RADIUS = 128, 8, 64
_c = (np.arange(N * SUB) + 0.5) / SUB - N / 2
SX, SY = np.meshgrid(_c, _c)                          # every sub-point's x (along a row) and y (down a column); the field's center is (0, 0)
_p = np.arange(N) + 0.5 - N / 2
PX, PY = np.meshgrid(_p, _p)
DISK = PX ** 2 + PY ** 2 <= RADIUS ** 2               # pixel centers inside the scanner's field

def render(strips, fine=1):
    """The picture as integer pixels (fine=1), or each pixel read as fine x fine parts, each the count of its own (8/fine)^2 sub-points (amendment
    A3 reads fine=2). The same total light either way; the scanner's field is the same disk of whole pixels."""
    inside = np.zeros(SX.shape, bool); M = N * SUB
    for (x0, y0, x1, y1, w) in strips:
        dx, dy = x1 - x0, y1 - y0; length = math.hypot(dx, dy); ux, uy = dx / length, dy / length
        pad = w / 2 + 1.0                                     # only the sub-points in the strip's box (and a pixel more) can be inside it
        c0 = max(0, int(math.floor((min(x0, x1) - pad + N / 2) * SUB - 0.5))); c1 = min(M, int(math.ceil((max(x0, x1) + pad + N / 2) * SUB - 0.5)) + 1)
        r0 = max(0, int(math.floor((min(y0, y1) - pad + N / 2) * SUB - 0.5))); r1 = min(M, int(math.ceil((max(y0, y1) + pad + N / 2) * SUB - 0.5)) + 1)
        if c0 >= c1 or r0 >= r1:
            continue
        rx, ry = SX[r0:r1, c0:c1] - x0, SY[r0:r1, c0:c1] - y0
        along = rx * ux + ry * uy; across = ry * ux - rx * uy
        inside[r0:r1, c0:c1] |= (along >= 0) & (along <= length) & (np.abs(across) <= w / 2)
    if fine == 1:
        img = inside.reshape(N, SUB, N, SUB).sum(axis=(1, 3)).astype(np.int64)
        img[~DISK] = 0
        return img
    b = SUB // fine; assert b * fine == SUB
    img = inside.reshape(N * fine, b, N * fine, b).sum(axis=(1, 3)).astype(np.int64)
    img[~np.repeat(np.repeat(DISK, fine, 0), fine, 1)] = 0
    return img

def place(strips, turn_deg=0.0, dx=0.0, dy=0.0):
    """Turn a shape about the field's center, then move it."""
    c, s = math.cos(math.radians(turn_deg)), math.sin(math.radians(turn_deg))
    return [(c * x0 - s * y0 + dx, s * x0 + c * y0 + dy, c * x1 - s * y1 + dx, s * x1 + c * y1 + dy, w) for (x0, y0, x1, y1, w) in strips]

def railyard():
    """Eight parallel tracks 1.5 pixels wide and 5 pixels apart, their left ends on a ladder track at 45 degrees and their right ends even: a
    classification yard's fan. Its bounding box is -35..35 by -17.5..17.5, centered on (0, 0)."""
    w = 1.5
    strips = [(-35.0 + 5 * i, -17.5 + 5 * i, 35.0, -17.5 + 5 * i, w) for i in range(8)]
    strips.append((-35.0, -17.5, 0.0, 17.5, w))
    return strips


# ---- The four kinds of ground for P3 and P4 (DATA.md). Every shape is centered on its own box before it is turned and moved. ----

def _center(strips):
    xs = [v for s in strips for v in (s[0], s[2])]; ys = [v for s in strips for v in (s[1], s[3])]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    return [(x0 - cx, y0 - cy, x1 - cx, y1 - cy, w) for (x0, y0, x1, y1, w) in strips]

def radius(strips):
    """The farthest corner of any strip from the center of the shape."""
    r = 0.0
    for (x0, y0, x1, y1, w) in strips:
        length = math.hypot(x1 - x0, y1 - y0); nx, ny = -(y1 - y0) / length, (x1 - x0) / length
        for px, py in ((x0, y0), (x1, y1)):
            for sg in (-1, 1):
                r = max(r, math.hypot(px + sg * nx * w / 2, py + sg * ny * w / 2))
    return r

def railyard_random(rng):
    """6 to 10 parallel tracks 4 to 6 pixels apart, 1.2 to 1.8 wide; the longest 55 to 75 long; left ends on a ladder track spanning 30 to 60
    percent of the longest, right ends even."""
    n = int(rng.integers(6, 11)); s = rng.uniform(4, 6); w = rng.uniform(1.2, 1.8); lmax = rng.uniform(55, 75); f = rng.uniform(0.3, 0.6)
    ys = [(i - (n - 1) / 2) * s for i in range(n)]; xl = [-lmax / 2 + f * lmax * i / (n - 1) for i in range(n)]
    strips = [(xl[i], ys[i], lmax / 2, ys[i], w) for i in range(n)] + [(xl[0], ys[0], xl[-1], ys[-1], w)]
    return _center(strips), {"tracks": n, "spacing": s, "width": w, "longest": lmax, "ladder_span": f}

def airfield(rng):
    """2 runways crossing at 40 to 90 degrees (55 to 85 long, each moved along itself by up to a quarter of its length), or 3 runways in a
    triangle (lines 120 degrees apart, each turned up to 8 degrees, 8 to 14 pixels from the center, 50 to 75 long); 3.5 to 6 wide."""
    k = int(rng.integers(2, 4)); w = rng.uniform(3.5, 6.0); strips = []
    if k == 2:
        lens = rng.uniform(55, 85, 2); th = [0.0, rng.uniform(40, 90)]; off = rng.uniform(-0.25, 0.25, 2)
        for i in range(2):
            c, s = math.cos(math.radians(th[i])), math.sin(math.radians(th[i])); cx, cy = off[i] * lens[i] * c, off[i] * lens[i] * s
            strips.append((cx - lens[i] / 2 * c, cy - lens[i] / 2 * s, cx + lens[i] / 2 * c, cy + lens[i] / 2 * s, w))
    else:
        lens = rng.uniform(50, 75, 3); th = [120 * i + rng.uniform(-8, 8) for i in range(3)]; d = rng.uniform(8, 14, 3)
        for i in range(3):
            c, s = math.cos(math.radians(th[i])), math.sin(math.radians(th[i])); cx, cy = -s * d[i], c * d[i]
            strips.append((cx - lens[i] / 2 * c, cy - lens[i] / 2 * s, cx + lens[i] / 2 * c, cy + lens[i] / 2 * s, w))
    return _center(strips), {"runways": k, "width": w}

def road_grid(rng):
    """3 to 5 roads each way, 10 to 16 pixels apart, 1.5 to 2.5 wide; the second set leaning up to 15 degrees off square; each road runs 2 to 6
    pixels past the last crossing."""
    m, n = int(rng.integers(3, 6)), int(rng.integers(3, 6)); sx, sy = rng.uniform(10, 16, 2); w = rng.uniform(1.5, 2.5)
    lean = math.radians(rng.uniform(0, 15)); over = rng.uniform(2, 6)
    X, Y = (n - 1) / 2 * sx, (m - 1) / 2 * sy; dxl, dyl = math.sin(lean), math.cos(lean)
    strips = [(-X - over, (j - (m - 1) / 2) * sy, X + over, (j - (m - 1) / 2) * sy, w) for j in range(m)]
    t = Y / dyl + over
    strips += [((i - (n - 1) / 2) * sx - t * dxl, -t * dyl, (i - (n - 1) / 2) * sx + t * dxl, t * dyl, w) for i in range(n)]
    return _center(strips), {"roads": [m, n], "width": w}

def patchwork(rng):
    """A grid of 3 to 5 by 3 to 5 fields, each 10 to 15 pixels on a side; each field lit (a crop) with chance one half, at least 3 lit and at
    least 2 dark; a lit field is drawn 1 pixel in from each edge, so the paths between fields stay dark."""
    a, b = int(rng.integers(3, 6)), int(rng.integers(3, 6)); cw, ch = rng.uniform(10, 15, 2)
    while True:
        lit = rng.random((a, b)) < 0.5
        if 3 <= lit.sum() <= a * b - 2:
            break
    strips = [((i - a / 2) * cw + 1, (j - b / 2 + 0.5) * ch, (i - a / 2 + 1) * cw - 1, (j - b / 2 + 0.5) * ch, ch - 2)
              for i in range(a) for j in range(b) if lit[i, j]]
    return _center(strips), {"fields": [a, b], "lit": int(lit.sum())}

KINDS = ["railyard", "airfield", "road grid", "patchwork"]
_GEN = [railyard_random, airfield, road_grid, patchwork]

def example(kind, rng):
    """One picture: a shape of the kind (drawn again while its farthest corner is over 58 pixels out), turned uniformly at random and moved
    to a uniformly random point of the disk of radius 60 minus its own radius, so all of it stays inside the field."""
    while True:
        strips, params = _GEN[kind](rng); r = radius(strips)
        if r <= 58:
            break
    turn = rng.uniform(0, 360); rho = (60 - r) * math.sqrt(rng.random()); phi = rng.uniform(0, 2 * math.pi)
    dx, dy = rho * math.cos(phi), rho * math.sin(phi)
    return place(strips, turn, dx, dy), {**params, "kind": KINDS[kind], "turn": turn, "shift": [dx, dy], "radius": r}
