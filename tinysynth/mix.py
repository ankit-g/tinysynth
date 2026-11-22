"""Duck music under a voice track and sum with SFX."""
import numpy as np
from .core import SR


def duck_gain(voice, hi=.20, lo=.07, thresh=.01, attack=.08, release=.6):
    """Per-sample music gain: `hi` in silence, sliding to `lo` while the voice is active."""
    k = int(.05 * SR)
    env = np.convolve(np.abs(voice), np.ones(k) / k, "same")
    act = (env > thresh).astype(float)
    a, r = 1 - np.exp(-1 / (attack * SR)), 1 - np.exp(-1 / (release * SR))
    g, x = np.empty(len(act)), 0.0
    for i, v in enumerate(act):
        x += (a if v > x else r) * (v - x)
        g[i] = x
    return hi - (hi - lo) * g


def mix(voice, music, sfx_track, sfx_level=.30, **duck):
    n = min(len(voice), len(music), len(sfx_track))
    out = voice[:n] + duck_gain(voice[:n], **duck) * music[:n] + sfx_level * sfx_track[:n]
    return np.clip(out, -1, 1) * .95
