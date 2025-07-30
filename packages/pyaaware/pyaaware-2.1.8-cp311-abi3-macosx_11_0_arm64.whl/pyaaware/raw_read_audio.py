from pathlib import Path

import numpy as np


def raw_read_audio(name: str | Path) -> tuple[np.ndarray, int]:
    import soundfile
    from pydub import AudioSegment

    from .env_vars import tokenized_expand

    expanded_name, _ = tokenized_expand(name)

    try:
        if expanded_name.endswith(".mp3") or expanded_name.endswith(".m4a"):
            if expanded_name.endswith(".mp3"):
                sound = AudioSegment.from_mp3(expanded_name)
            else:
                sound = AudioSegment.from_file(expanded_name)
            raw = np.array(sound.get_array_of_samples()).astype(np.float32).reshape((-1, sound.channels))
            norm_factor = 1.0 / 2.0 ** (sound.sample_width * 8 - 1)
            raw = raw * norm_factor
            sample_rate = sound.frame_rate
        else:
            raw, sample_rate = soundfile.read(expanded_name, always_2d=True, dtype="float32")
    except Exception as e:
        if name != expanded_name:
            raise OSError(f"Error reading {name} (expanded: {expanded_name}): {e}") from e
        else:
            raise OSError(f"Error reading {name}: {e}") from e

    return np.squeeze(raw[:, 0].astype(np.float32)), sample_rate
