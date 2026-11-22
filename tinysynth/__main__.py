"""python -m tinysynth demo [outdir]  |  python -m tinysynth bed SECONDS out.wav [--shift N]"""
import sys
from pathlib import Path
import numpy as np
from . import SR, bed, sfx, KINDS, write_wav


def main(argv):
    if len(argv) >= 1 and argv[0] == "demo":
        out = Path(argv[1] if len(argv) > 1 else "demo"); out.mkdir(exist_ok=True)
        write_wav(out / "bed.wav", bed(24) * .6)
        for k in KINDS:
            x = sfx(k); write_wav(out / f"sfx_{k}.wav", x / max(np.abs(x).max(), 1e-9) * .8)
        print("wrote", out)
    elif len(argv) >= 3 and argv[0] == "bed":
        shift = int(argv[argv.index("--shift") + 1]) if "--shift" in argv else 0
        write_wav(argv[2], bed(float(argv[1]), shift) * .6); print("wrote", argv[2])
    else:
        print(__doc__); return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
