# Predictions, filed before any code

Filed at 2:47 PM on November 22, 2026, before a line of this repository's code existed and before its design was fixed. Confidences are
ESTIMATES. Grades go below, beside each; nothing above a grade is changed after it is filed.

## What is being rebuilt

Warren L. Holford's "Radiation Sensitive Image Analyzer Using Multiple Angle Line Scan," US patent 3,508,065, filed September 25, 1963
(patented April 21, 1970): the first integral scanner, the one Scope Incorporated's 1967 time-domain prenormalizer (US 3,566,080, by Malcolm
R. Uffelman and Holford) was built on. Its scan is the same: a rotating 45-degree mirror sweeps narrow grid lines across the picture, one at a
time, each line at a new angle ("thirty-nine reflective grid lines" in one embodiment). Its analysis is not. A bank of band-pass filters
spans the whole waveform, each band rectified to a lamp: the "property filters," meant to read the same wherever the picture sits and however
it is turned. A second bank on each rectified band measures how that band rises and falls over one turn, which Holford called "circular
harmonic" analysis. The patent's own worked example: "a ten-spoked wheel on the image field 10 will generate twenty distinct pulses during
one cycle of data extraction," "regardless of the size of the image and regardless of the position or orientation of the image on the field."
The pictures and the learning machine come from conflex-1965 (its shapes.py, its DATA.md pictures and its CONFLEX), so the 1963 and the 1967
front ends can be compared on the same ground.

## Predictions

**H0 (99%).** Every run gives the same numbers, bit for bit: the scan and the filters are integer arithmetic.

**H1 (45%).** The first-level lamps for conflex-1965's railyard at its 12 turns (every 30 degrees) each stay within 15% of their mean.

**H2 (75%).** The same railyard at conflex-1965's 13 shifts (up to 8 pixels): each first-level lamp within 15% of its mean.

**H3 (50%).** A wheel of ten thin spokes, drawn at 12 different sizes, positions and turns: in the finest band, the strongest circular
harmonic is 10 per turn every time, not the patent's twenty. Opposite spokes lie on one line and meet the scan together, and 39 grid lines a
turn cannot tell twenty a turn from nineteen.

**H4 (70%).** The railyard's strongest circular harmonic in the finest band is 2 per turn at every one of its 12 turns: parallel tracks look
the same twice a turn.

**H5 (55%).** CONFLEX on all of the lamps, both levels, names at least 90% of conflex-1965's 120 held-out pictures right.

**H6 (50%).** CONFLEX on the 1963 lamps does at least as well on those 120 pictures as it did on the 1967 prenormalizer's first-design counts
(83.3%).
