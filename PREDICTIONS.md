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

## Grades of H0 to H4, 2:51 PM (MEASURED; results/h0.json and h1_h4.json; test_h0.py, test_h1_h4.py)

- **H0: HELD.** Three runs, each in a fresh Python, give the same digest of every lamp (SHA-256 de0e5769f279...). The integer transform's band
  powers lie within 0.088% of a floating-point one.
- **H1: FAILED, on one lamp.** Over the railyard's 12 turns, bands 0 to 5 stay within 6.6% of their means (bands 0 to 3 within
  0.4%); band 6, the finest, which holds 0.18% of the power, moves by 44.8%.
- **H2: HELD.** Over the 13 shifts every lamp stays within 13.5% of its mean, band 6 the most.
- **H3: HELD.** All 12 wheels, at every size, place and turn: the strongest circular harmonic in band 6 is 10 a turn, not the patent's twenty.
- **H4: FAILED.** The railyard's strongest circular harmonic in band 6 is 8 or 16 a turn at every one of its turns, never 2.

**What the grades leave out, said plainly** (exploratory, measured before these grades were written: explore_h3_h4.py,
results/explore_h3_h4.json). H4's reason is the ladder. At a turn of 0, the pulse carrying the most of band 6's power over the turn
(29%) is the grid line at 313.8 degrees, 1.2 degrees from lying along the ladder track (at 45 degrees, its lines meet
the scan along 135 and 315). The lines nearest lying along the tracks (92.3 and 267.7 degrees, 2.3 degrees off) carry
9.8% and 9.4%. The tracks twice a turn and the ladder twice, 45 degrees apart in pairs, make 8 and 16 a turn the strongest
harmonics. I counted the tracks and forgot the one line across their ends.

And the patent's twenty is real, in the middle bands. With 39 lines, band 3 peaks at 19 a turn for 8 of the 12 wheels and band 4 for
8: 19 is where twenty a turn lands when 39 lines a turn fold it. Scanned with 403 lines (nothing folds below 201 a turn), band 3
peaks at 20 a turn for 8 of the 12 wheels and band 4 for 7, while band 6 stays at 10 for all 12. So the patent's wheel gives
ten a turn in the finest band and twenty in the middle ones; why twenty there is my reading, not measured: a spoke lining up with the scan
and a spoke lying square to it take turns every 18 degrees.

## Grades of H5 and H6, 2:52 PM (MEASURED; results/h5_h6.json; h5_h6.py)

(Beside the H0 to H4 grades above, 2:52 PM: the two track shares are paired the wrong way round there. The line at 267.7 degrees carries 9.8%
and the one at 92.3 degrees 9.4%. The line is kept as written.)

The pictures are conflex-1965's own: the same code and seeds, and checked. The 1967 first design's six counts, computed here, match
conflex-1965's saved counts for every one of the 240.

- **H5: HELD.** CONFLEX on all 42 lamps names 111 of the 120 held-out pictures right, 92.5%. Railyards 30 of 30, road grids
  30 of 30, patchworks 27 of 30 (3 called road grids), airfields 24 of 30 (6 called road grids).
- **H6: HELD.** 92.5% against the 1967 first design's 83.3%, on the same pictures, with the same CONFLEX and the same wiring.

**Beside, not graded.** The first level's 7 lamps alone: 92.5%. Over six wirings: 90.8 to 95.0%. And the plain
nearest-mean rule on log10(1 + lamp): 120 of 120, every held-out picture right. On the 1967 counts, the same rule got 90.0%
(first design) and 89.2% (A2).

**What the grades leave out, said plainly.** On this ground, Holford's 1963 lamps carry more than the 1967 counters did. A rule as plain
as "nearest average" sorts every held-out picture, and the learning machine, not the lamps, is what holds the score to 92.5%. That is a
finding about these two rebuilds, each with my own choices (the 1967 one's six cosines and its threshold; this one's seven octave bands
and its gain control), on drawn shapes, not real film. Why Scope moved from the frequency domain to the time domain between 1963 and
1967 is in neither patent, and this does not answer it.
