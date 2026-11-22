# tinysynth

A tiny, numpy-only chiptune synth for explainer videos. It makes the background music and sound effects used in the TokenMachines videos: a slow, sparse music bed, seven small sound effects, and automatic ducking so the music sits under a narration track.

```python
import numpy as np
from tinysynth import SR, bed, place, mix, read_wav, write_wav

voice, sr = read_wav("voice.wav")            # 48 kHz mono 16-bit
music = bed(len(voice) / SR, shift=-3)       # bed in a different key
fx = np.zeros(len(voice))
place(fx, "whoosh", 0.05, .6)                # kinds: pop whoosh ding chime buzz click blip
place(fx, "ding", 4.2)
write_wav("mix.wav", mix(voice, music, fx))  # music ducks 0.20 -> 0.07 while the voice speaks
```

Try it: `python -m tinysynth demo` writes `demo/bed.wav` and one file per effect. `python -m tinysynth bed 60 bed.wav --shift 2` writes a 60 s bed.

Install: `pip install -e .` (needs numpy). Tests: `pytest`.

## What is in it
- `core.py`: MIDI to Hz, square/triangle/saw/sine oscillators, `note()`, WAV read/write.
- `music.py`: `bed(seconds, shift)`, 72 bpm, Cmaj7 / Am7 / Fmaj7 / G, pad + bass + arpeggio + melody + soft kick, faded in and out.
- `sfx.py`: `sfx(kind)` and `place(track, kind, t)`.
- `mix.py`: `duck_gain()` and `mix()`.

MIT licensed.
