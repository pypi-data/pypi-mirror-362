import copy
from typing import List, Union

import numpy as np
from IPython.display import Audio

current_tones = []
SAMPLERATE = 44100  # sampling rate


class Ton:
    def __init__(self, tasten, dauer):
        self.tasten = tasten
        self.dauer = dauer


def to_list(i):
    if isinstance(i, list):
        return copy.copy(i)
    return [i]


def create_window(n_samples: int, start_duration: float = 0.02, end_duration: float = 0.02) -> np.ndarray:
    start_samples = int(start_duration * SAMPLERATE)
    end_samples = int(end_duration * SAMPLERATE)
    window = np.ones(n_samples, dtype=np.float32)

    start_samples = min(start_samples, n_samples // 2)
    end_samples = min(end_samples, n_samples - start_samples)

    window[:start_samples] = np.linspace(0.0, 1.0, start_samples, endpoint=False)
    window[-end_samples:] = np.linspace(1.0, 0.0, end_samples, endpoint=True)

    return window


def key_to_pitch(key: int) -> int:
    c_major_offsets = [0, 2, 4, 5, 7, 9, 11]  # C, D, E, F, G, A, B
    octave = key // 7 + 4
    degree = key % 7
    return 12 + octave * 12 + c_major_offsets[degree]


def create_sound(tasten: List[int], dauer):
    pitches = [key_to_pitch(t) for t in tasten]

    freqs = [440.0 * (2 ** ((p - 69) / 12)) for p in pitches]

    t = np.linspace(0, dauer, int(SAMPLERATE * dauer), False)
    sounds = [0.5 * np.sin(2 * np.pi * f * t) for f in freqs]
    window = create_window(len(t))
    sound = np.sum(sounds, axis=0)
    return sound * window


def ton(taste: Union[int, List[int]], dauer: float = 1.0):
    global current_tones

    if dauer > 1000:
        raise ValueError('Der Ton ist zu lang, da mach ich nicht mit. Maximal sind 1000 Sekunden erlaubt.')

    taste = to_list(taste)
    if len(taste) > 100:
        raise ValueError('Das sind mir zu viele Tasten, da mach ich nicht mit. Maximal sind 100 Tasten erlaubt.')

    for t in taste:
        if t < -13:
            raise ValueError('Die Taste ist mir zu tief, da mach ich nicht mit. Maximal sind -13 bis 29 erlaubt.')
        if t > 29:
            raise ValueError('Die Taste ist mir zu hoch, da mach ich nicht mit. Maximal sind -13 bis 29 erlaubt.')

    current_tones.append(Ton(taste, dauer))


def spiele():
    global current_tones
    if not current_tones:
        return None
    sounds = [create_sound(t.tasten, t.dauer) for t in current_tones]
    sound = np.concatenate(sounds)
    current_tones = []
    return Audio(sound, rate=SAMPLERATE, autoplay=True)
