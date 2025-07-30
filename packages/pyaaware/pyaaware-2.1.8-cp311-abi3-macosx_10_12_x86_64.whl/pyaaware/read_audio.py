from pathlib import Path

import numpy as np


def read_audio(name: str | Path) -> np.ndarray:
    """Read audio data from a file using soundfile

    :param name: File name
    :return: Array of time domain audio data
    """
    from .raw_read_audio import raw_read_audio
    from .resample import resample

    out, sample_rate = raw_read_audio(name)

    return resample(out, orig_sr=sample_rate, target_sr=16000, mode="soxr_hq")
