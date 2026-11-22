"""Slow, sparse chiptune background bed: 72 bpm, one chord per bar, optional key shift."""
import numpy as np
from .core import SR, note

CHORDS = [[60, 64, 67, 71], [57, 60, 64, 67], [53, 57, 60, 64], [55, 59, 62, 67]]  # Cmaj7 Am7 Fmaj7 G
ROOTS = [36, 33, 41, 43]
LEAD = [[76, None, 79, None], [72, None, 76, None], [77, None, 72, None], [74, None, 71, None]]


def bed(seconds, shift=0, bpm=72, fade=2.0):
    """Return a mono music bed of the given length, transposed by `shift` semitones, normalised to peak 1."""
    buf = np.zeros(int(seconds * SR))
    beat = 60 / bpm
    bar = 4 * beat
    for b in range(int(seconds / bar) + 1):
        c, t0, phrase = b % 4, b * bar, (b // 4) % 4
        for m in CHORDS[c][:3]:                                   # soft pad
            note(buf, "tri", m + shift, t0, bar * .95, .06, decay=1.2)
        note(buf, "tri", ROOTS[c] + shift, t0, 2 * beat, .28, decay=2)         # bass
        note(buf, "tri", ROOTS[c] + shift, t0 + 2 * beat, 2 * beat, .2, decay=2)
        if phrase != 3:                                           # arpeggio
            for k, i in enumerate([0, 1, 2, 1]):
                note(buf, "sq", CHORDS[c][i] + 12 + shift, t0 + k * beat, beat * .8, .05, duty=.25, decay=5)
        if phrase in (1, 2):                                      # melody
            for k, m in enumerate(LEAD[c]):
                if m:
                    note(buf, "sq", m + shift, t0 + k * beat, beat * 1.8, .045, decay=3, vib=.004)
        if b % 2 == 0:                                            # soft kick
            n, i0 = int(.14 * SR), int(t0 * SR)
            if i0 + n < len(buf):
                t = np.arange(n) / SR
                buf[i0:i0 + n] += .16 * np.sin(2 * np.pi * (50 * t + 90 * (1 - np.exp(-25 * t)) / 25)) * np.exp(-28 * t)
    f = min(int(fade * SR), len(buf) // 2)
    if f:
        buf[:f] *= np.linspace(0, 1, f)
        buf[-f:] *= np.linspace(1, 0, f)
    peak = np.abs(buf).max()
    return buf / peak if peak else buf
