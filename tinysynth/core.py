"""Core synth: oscillators, ADSR-ish note rendering, WAV I/O. numpy only."""
import wave
import numpy as np

SR = 48000


def hz(midi):
    """MIDI note number -> frequency in Hz (A4 = 69 = 440 Hz)."""
    return 440.0 * 2 ** ((np.asarray(midi, dtype=float) - 69) / 12)


def osc(kind, f, t, duty=0.5):
    """Waveform at frequency f (scalar or array) over times t. kind: sq | tri | saw | sin."""
    phase = np.cumsum(np.broadcast_to(f, t.shape)) / SR if np.ndim(f) else f * t
    ph = phase % 1
    if kind == "sq":
        return np.where(ph < duty, 1.0, -1.0)
    if kind == "tri":
        return 4 * np.abs(ph - 0.5) - 1
    if kind == "saw":
        return 2 * ph - 1
    if kind == "sin":
        return np.sin(2 * np.pi * ph)
    raise ValueError(f"unknown oscillator {kind!r}")


def note(buf, kind, midi, start, dur, amp, duty=0.5, decay=4.0, vib=0.0):
    """Mix one note into buf in place. start/dur in seconds; decay is an exponential rate over dur."""
    i0, n = int(start * SR), int(dur * SR)
    if i0 >= len(buf) or n <= 0:
        return
    n = min(n, len(buf) - i0)
    t = np.arange(n) / SR
    f = hz(midi)
    f = f * (1 + vib * np.sin(2 * np.pi * 5 * t)) if vib else float(f)
    env = np.minimum(t / 0.01, 1) * np.exp(-decay * t / max(dur, 1e-3)) * np.clip((dur - t) / 0.04, 0, 1)
    buf[i0:i0 + n] += amp * env * osc(kind, f, t, duty)


def write_wav(path, x, sr=SR):
    """Write mono float audio in [-1, 1] as 16-bit PCM."""
    x = np.clip(np.asarray(x, dtype=float), -1, 1)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((x * 32767).astype("<i2").tobytes())


def read_wav(path):
    """Read a 16-bit mono (or first channel of stereo) WAV -> (float array, sample rate)."""
    with wave.open(str(path)) as w:
        ch, sr = w.getnchannels(), w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(float) / 32768
    return (x[::ch] if ch > 1 else x), sr
