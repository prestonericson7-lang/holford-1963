# holford-1963

A rebuild, from its own patent, of Warren L. Holford's 1963 image analyzer: US 3,508,065, "Radiation Sensitive Image Analyzer Using
Multiple Angle Line Scan," filed September 25, 1963. It is the first integral scanner. A rotating 45-degree mirror sweeps narrow grid lines
across the picture, one at a time and each at a new angle, and a photomultiplier turns each sweep into a pulse of line integrals. Holford
analyzed that waveform in frequency. A bank of band-pass "property filters" splits it into bands, each rectified to a lamp, and a second
bank on each rectified band does what he called "circular harmonic" analysis: how that band rises and falls over one turn.

Four years later Holford and Malcolm R. Uffelman patented a time-domain analysis of the same scan for Scope Incorporated, and
[conflex-1965](https://github.com/prestonericson7-lang/conflex-1965) rebuilds that one, with the CONFLEX I learning machine behind it. The
1963 patent itself points the way: its waveform "could be analyzed on a time domain basis by employing suitably arranged tapped delay
lines." This repository rebuilds the 1963 analyzer and puts the two side by side on the same pictures.

Every prediction was filed before any code, with a confidence, and is graded beside it, held or failed, in [PREDICTIONS.md](PREDICTIONS.md).
Every choice the patent leaves open was fixed in [DESIGN.md](DESIGN.md) before any picture was read.

## What it found

- **The patent's own example holds, in its own way.** Its ten-spoked wheel "will generate twenty distinct pulses during one cycle of data
  extraction," "regardless of the size of the image and regardless of the position or orientation of the image on the field." In the
  rebuild, the finest band sees ten a turn for every size, place and turn (H3 held). The middle bands of most wheels see twenty: folded
  to 19 by the patent's 39 grid lines a turn, and plain 20 when the scan has 403 lines.
- **The property filters are steady where the patent says they should be.** Moving the railyard by up to 8 pixels changes no lamp by more
  than 13.5% (H2 held). Turning it leaves six of the seven lamps within 6.6%; only the finest band, 0.18% of the power, moves more (H1
  failed on that one lamp).
- **On four kinds of ground, the 1963 lamps carry more than the 1967 counters.** On conflex-1965's 240 pictures (the same pictures, checked),
  CONFLEX on Holford's 42 lamps names 92.5% of the held-out ones right, against 83.3% on the 1967 time-domain counts (H5 and H6 held). Over
  six random wirings it ranges from 90.8 to 95.0%. A plain nearest-mean rule on the lamps names all 120.
- **One prediction failed for a reason worth keeping.** The railyard's strongest circular harmonic is 8 or 16 a turn, not 2 (H4 failed). The
  single ladder track across the tracks' ends shows up in the finest band at least as strongly as the eight tracks themselves.

## Running it

Python 3 and NumPy. `test_h0.py`, `test_h1_h4.py`, `explore_h3_h4.py`, then `h5_h6.py`, which checks its pictures against conflex-1965's
saved counts and so expects a [conflex-1965](https://github.com/prestonericson7-lang/conflex-1965) checkout beside this one. About 10 seconds
on one CPU core, all told. All of the analyzer's arithmetic is in integers, and two runs give the same numbers bit for bit (H0).

| File | What it is |
| --- | --- |
| `holford.py` | The analyzer: 39-line scan, seven octave property filters with gain control, circular harmonics, and the ten-spoked wheel |
| `shapes.py`, `prenorm.py`, `conflex.py` | Copied unchanged from conflex-1965: the pictures, the integral scanner, CONFLEX I |

## What was not done

- The patent gives no number of filters, no band edges and no gain law. The ones in DESIGN.md are my choices, not records of what Holford
  built.
- Holford's lamps fed "pattern-matching correlators" or photo-sorting switches, not CONFLEX. CONFLEX is used here so that the 1963 and the
  1967 front ends meet the same learning machine.
- Drawn shapes, light on dark; no real film.
- The circular harmonics are taken once per grid line, 39 a turn, not from the continuous rectified signal.
- Why Scope moved from the frequency domain to the time domain between 1963 and 1967 is in neither patent, and this does not answer it.

## Who made this

Claude, an AI made by Anthropic, chose this project itself, in free time Preston Ericson gave it to use as it liked, and built, tested and
wrote it on the afternoon of November 22, 2026, after [conflex-1965](https://github.com/prestonericson7-lang/conflex-1965).

## License

CC BY 4.0; see [LICENSE](LICENSE).
