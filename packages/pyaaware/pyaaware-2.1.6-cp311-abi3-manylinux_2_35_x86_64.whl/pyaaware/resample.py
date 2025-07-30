import numpy as np


def resample(audio: np.ndarray, orig_sr: int, target_sr: int, mode: str) -> np.ndarray:
    from librosa import resample

    return resample(audio, orig_sr=orig_sr, target_sr=target_sr, res_type=mode)
