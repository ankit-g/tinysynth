import numpy as np
from tinysynth import SR, hz, bed, sfx, KINDS, mix, write_wav, read_wav


def test_a4():
    assert abs(float(hz(69)) - 440) < 1e-9


def test_bed_length_and_peak():
    b = bed(5)
    assert len(b) == 5 * SR and abs(np.abs(b).max() - 1) < 1e-9


def test_shift_changes_audio():
    assert not np.allclose(bed(4, 0), bed(4, 3))


def test_all_sfx_finite_nonempty():
    for k in KINDS:
        x = sfx(k)
        assert len(x) > 0 and np.isfinite(x).all() and np.abs(x).max() > 0


def test_ducking_lowers_music_under_voice():
    voice = np.zeros(SR * 3); voice[SR:2 * SR] = .3 * np.sin(2 * np.pi * 200 * np.arange(SR) / SR)
    m = np.ones(len(voice)); s = np.zeros(len(voice))
    from tinysynth.mix import duck_gain
    g = duck_gain(voice)
    assert g[int(1.8 * SR)] < g[int(.5 * SR)] - .05
    assert np.abs(mix(voice, m, s)).max() <= .95


def test_wav_roundtrip(tmp_path):
    x = bed(1) * .5; write_wav(tmp_path / "a.wav", x)
    y, sr = read_wav(tmp_path / "a.wav")
    assert sr == SR and np.allclose(x, y, atol=1e-3)
