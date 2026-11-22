"""CONFLEX I, rebuilt from M. R. Uffelman, "CONFLEX I - A Conditioned Reflex System" (1962 IRE International Convention Record, Part 4, p. 132) and
US patent 3,295,103 (Driese, Gerig, Uffelman and Williams, assignors to Scope Incorporated; filed August 16, 1962).

S-field: Ns binary sensory cells. D-field: Nd D-cells ("The D-cells are majority decision gates"), each with A affirmative and N negative inputs chosen at
random from the S-field ("once the connections are selected they remain fixed"); its output is +1, 0 or -1 as the affirmative sum is greater
than, equal to, or less than the negative sum. M-fields: one per class; "The gain of each M-cell is changed by the amount of the associated
D-cell's output" for every teaching stimulus of its class. Test: each M-field's sum of M-cell gain times D-cell output (a dot product); the
comparator names the largest. The random wiring comes from a maximal-length shift register, as the patent's sequential version did.
"""
import numpy as np

class MSequence:
    """A 31-stage maximal-length linear feedback shift register (x^31 + x^28 + 1): a pseudo-random bit stream that repeats every 2^31 - 1."""
    def __init__(self, seed=0x1F2E3D4C):
        self.s = seed & 0x7FFFFFFF or 1
    def bit(self):
        b = ((self.s >> 30) ^ (self.s >> 27)) & 1
        self.s = ((self.s << 1) | b) & 0x7FFFFFFF
        return b
    def below(self, m):
        """An integer in [0, m), from fresh bits, by rejection (so every value is equally likely)."""
        k = max(1, (m - 1).bit_length())
        while True:
            v = 0
            for _ in range(k):
                v = (v << 1) | self.bit()
            if v < m:
                return v

class Conflex:
    def __init__(self, ns, nd, a=5, n=5, classes=2, seed=0x1F2E3D4C):
        self.ns, self.nd, self.a, self.n = ns, nd, a, n
        g = MSequence(seed); aff = np.zeros((nd, a), np.int64); neg = np.zeros((nd, n), np.int64)
        for j in range(nd):
            picked = []
            while len(picked) < a + n:                      # A + N distinct S-cells per D-cell
                v = g.below(ns)
                if v not in picked:
                    picked.append(v)
            aff[j], neg[j] = picked[:a], picked[a:]
        self.aff, self.neg = aff, neg
        self.m = np.zeros((classes, nd), np.int64)          # the M-fields' gains

    def d(self, s):
        """The D-field's outputs (+1, 0, -1) for a binary stimulus s of Ns cells."""
        s = np.asarray(s, np.int64)
        return np.sign(s[self.aff].sum(1) - s[self.neg].sum(1))

    def condition(self, s, cls):
        self.m[cls] += self.d(s)

    def scores(self, s):
        return self.m @ self.d(s)

    def classify(self, s):
        return int(np.argmax(self.scores(s)))              # ties go to the lowest class number

def p_zero(b, y):
    """The 1962 paper's equation (21): the chance a D-cell with A = N = B inputs outputs 0, for a stimulus covering a fraction y of the S-field."""
    from math import comb
    return sum(comb(b, k) ** 2 * y ** (2 * k) * (1 - y) ** (2 * b - 2 * k) for k in range(b + 1))
