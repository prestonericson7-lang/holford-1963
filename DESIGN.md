# Design choices, fixed before the analyzer read any picture

Written at 2:48 PM on November 22, 2026, after the predictions were filed and before any code here had run on a picture. US patent 3,508,065
leaves the choices below open. Each one is mine, and each is written here so it can be argued with. Nothing here changes after a result is
seen; a change would go beside, with its time.

**What is borrowed, unchanged.** From conflex-1965 (commit eb43e6f): shapes.py (the pictures: strips drawn in floating point, read as integer
pixels 0 to 64, a field of radius 64), the scanner in prenorm.py, and conflex.py (CONFLEX I). The four kinds of ground and their 240
pictures are DATA.md's, drawn from the same seeds, so they are the same pictures, pixel for pixel. The railyard, its 12 turns and its 13
shifts are conflex-1965's DESIGN.md's.

**The scan** (the patent's FIG. 6: "thirty-nine reflective grid lines"). 39 grid lines a turn, one on the picture at a time, so each gives one
pulse: the picture's line integrals at 360k/39 degrees. Each line is 2 bands wide (conflex-1965's amendment A1), so one sample per pixel
represents the video. In code: prenorm.scan(img, strip=2, strips=39), 129 samples a pulse.

**The first level: the property filters** (bank 66). Each pulse, padded with zeros to 256 samples, goes through a 256-point discrete Fourier
transform in integers (Q14 cosines and sines, as in cloud-screener-1970), and its power at each frequency is Re^2 + Im^2. Seven band-pass
filters an octave wide cover the whole band but its two ends: band b holds frequencies 2^b to 2^(b+1) - 1 (in cycles per 256 samples), b
= 0 to 6, leaving out the steady part (0) and the very top (128). Each band's lamp is its power summed over the 39 pulses: the rectified output, added up over one turn. Band 6 is the finest.

**The coarse gain control** (circuit 64). Each lamp is read as its share of all seven: lamp x 2^20 // (the sum of the seven), so a brighter
or bigger picture of the same shape lights the lamps in the same proportions.

**The second level: circular harmonics** (detector 76, bank 80). For each band, its power in each of the 39 pulses, as a share of that band's
power over the turn (x 2^16, floor), makes a sequence of 39 numbers: how the band rises and falls over one turn. A 39-point discrete Fourier
transform in integers (Q14) gives its harmonics, 1 to 19 a turn. Five second-level filters group them: 1, 2, 3 to 4, 5 to 8, and 9 to 19 a
turn. Each second-level lamp is its group's power, as a share of the band's steady power (x 2^20 // |E(0)|^2). 7 x 5 = 35 lamps. "The
strongest circular harmonic" (H3, H4) is the harmonic from 1 to 19 with the most power in band 6; a tie goes to the lower harmonic.

**The ten-spoked wheel** (H3). Ten spokes 1.5 pixels wide, from 3 pixels out to R, 36 degrees apart, no rim. Wheel i (i = 0 to 11): R = 20
+ 2.5 i pixels, turned 7 i degrees, its hub moved by 3 (i mod 3) pixels toward 30 i degrees, so every wheel stays inside the field.

**CONFLEX** (H5, H6). All 42 lamps (7 first-level, 35 second-level) as on/off cells, each a 16-cell thermometer as in conflex-1965's
DATA.md (cell j on when the lamp is at least lo + j (hi - lo) / 17, lo and hi from the teaching pictures; a lamp with lo = hi gives cells
that are always off): 672 S-cells. Then conflex-1965's CONFLEX unchanged: 4,000 D-cells, A = N = 5, the M-sequence wiring from seed
0x1F2E3D4C, one M-field per kind, taught once on the 120 teaching pictures in the order drawn. Graded on the 120 held-out pictures. Reported
beside, not graded: the first level's 7 lamps alone; six wirings; the plain nearest-mean rule on log10(1 + lamp).

**Randomness.** None in the analyzer. The pictures are DATA.md's (PCG64 seeds 1965 and 1966); CONFLEX's wiring is its M-sequence.
