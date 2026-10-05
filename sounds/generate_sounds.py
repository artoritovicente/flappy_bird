"""Generate simple WAV sound effects and background music."""

import array
import math
import os
import wave

SAMPLE_RATE = 44100


def _write_wav(path: str, samples: array.array, channels: int = 1) -> None:
    with wave.open(path, "w") as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(samples.tobytes())


def _sine_wave(frequency: float, duration: float, volume: float = 0.4) -> array.array:
    count = int(SAMPLE_RATE * duration)
    samples = array.array("h")
    for i in range(count):
        t = i / SAMPLE_RATE
        envelope = 1.0 - (i / count) * 0.3
        value = int(volume * 32767 * envelope * math.sin(2 * math.pi * frequency * t))
        samples.append(value)
    return samples


def _background_music(duration: float = 8.0, volume: float = 0.18) -> array.array:
    melody = [
        (392, 0.35), (440, 0.35), (494, 0.35), (440, 0.35),
        (392, 0.35), (330, 0.35), (392, 0.35), (440, 0.5),
        (392, 0.35), (440, 0.35), (494, 0.35), (587, 0.35),
        (494, 0.35), (440, 0.35), (392, 0.35), (330, 0.5),
    ]
    samples = array.array("h")
    total = int(SAMPLE_RATE * duration)
    pos = 0
    note_index = 0

    while pos < total:
        freq, note_dur = melody[note_index % len(melody)]
        note_samples = int(SAMPLE_RATE * note_dur)
        for i in range(note_samples):
            if pos >= total:
                break
            t = i / SAMPLE_RATE
            fade = min(1.0, i / (SAMPLE_RATE * 0.02), (note_samples - i) / (SAMPLE_RATE * 0.02))
            value = int(volume * 32767 * fade * math.sin(2 * math.pi * freq * t))
            samples.append(value)
            pos += 1
        note_index += 1

    return samples


def generate_all(output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)

    sounds = {
        "flap.wav": _sine_wave(520, 0.08, 0.35),
        "score.wav": _sine_wave(880, 0.12, 0.35),
        "hit.wav": _sine_wave(180, 0.35, 0.45),
        "menu.wav": _sine_wave(660, 0.06, 0.25),
        "bg_music.wav": _background_music(),
    }

    for filename, samples in sounds.items():
        _write_wav(os.path.join(output_dir, filename), samples)


if __name__ == "__main__":
    generate_all(os.path.dirname(os.path.abspath(__file__)))
