"""Small sound effects. sfx(kind) -> mono float array. Kinds: pop whoosh ding chime buzz click blip."""
import numpy as np
from .core import SR, hz

KINDS = ("pop", "whoosh", "ding", "chime", "buzz", "click", "blip")


def sfx(kind, v=1.0, rng=None):
    rng = rng or np.random.default_rng(5)
    if kind == "pop":
        t = np.arange(int(.09 * SR)) / SR
        return v * .8 * np.sin(2 * np.pi * (700 + 900 * np.exp(-t * 60)) * t) * np.exp(-t * 45)
    if kind == "whoosh":
        n = int(.55 * SR)
        k = np.hanning(int(.004 * SR) * 2 + 1)
        x = np.convolve(rng.standard_normal(n), k / k.sum(), "same")
        return v * 1.2 * x * np.sin(np.pi * np.arange(n) / n) ** 2 * .6
    if kind == "ding":
        t = np.arange(int(.7 * SR)) / SR
        return v * .5 * (np.sin(2 * np.pi * 1318 * t) + .4 * np.sin(2 * np.pi * 2637 * t)) * np.exp(-t * 7)
    if kind == "chime":
        out = np.zeros(int(1.1 * SR))
        for j, m in enumerate([79, 83, 86]):
            s = int(j * .1 * SR)
            t = np.arange(len(out) - s) / SR
            out[s:] += .4 * np.sin(2 * np.pi * float(hz(m)) * t) * np.exp(-t * 6)
        return v * out
    if kind == "buzz":
        t = np.arange(int(.35 * SR)) / SR
        return v * .35 * np.sign(np.sin(2 * np.pi * 110 * t)) * np.exp(-t * 5) * np.minimum(t / .01, 1)
    if kind == "click":
        n = int(.05 * SR)
        t = np.arange(n) / SR
        return v * (.9 * rng.standard_normal(n) * np.exp(-t * 140) + .5 * np.sin(2 * np.pi * 180 * t) * np.exp(-t * 90))
    if kind == "blip":
        t = np.arange(int(.16 * SR)) / SR
        return v * .5 * np.sign(np.sin(2 * np.pi * (520 + 700 * (t > .07)) * t)) * np.exp(-t * 14)
    raise ValueError(f"unknown sfx {kind!r}; choose from {KINDS}")


def place(track, kind, t, v=1.0):
    """Mix sfx(kind) into `track` at time t seconds."""
    x, i = sfx(kind, v), int(t * SR)
    if 0 <= i < len(track):
        track[i:i + len(x)] += x[:len(track) - i]
