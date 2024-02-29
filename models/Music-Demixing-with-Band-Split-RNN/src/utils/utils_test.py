import numpy as np
import torch
from museval.metrics import bss_eval
import typing as tp


def compute_uSDR(
        y_hat: np.ndarray,
        y_tgt: np.ndarray,
        delta: float = 1e-7,
) -> float:
    """
    Computes SDR metric as in https://arxiv.org/pdf/2108.13559.pdf.
    Taken and slightly rewritten from
    https://github.com/AIcrowd/music-demixing-challenge-starter-kit/blob/master/evaluator/music_demixing.py
    """
    # compute SDR for one song
    num = np.sum(np.square(y_tgt), axis=(1, 2))
    den = np.sum(np.square(y_tgt - y_hat), axis=(1, 2))
    num += delta
    den += delta
    return 10 * np.log10(num / den)


def compute_SDRs(
        y_hat: torch.Tensor, y_tgt: torch.Tensor
) -> tp.Tuple[float, float]:
    """
    Computes cSDR and uSDR as defined in paper
    """
    y_hat = y_hat.T.unsqueeze(0).numpy()
    y_tgt = y_tgt.T.unsqueeze(0).numpy()
    
    # START OF EDIT
    # DEBUG PRINTING
    # print('--------------------before manipulation---------------')
    # print('y_hat:', y_hat)
    # print('y_hat shape: ', y_hat.shape)

    # print('y_tgt:', y_tgt)
    # print('y_tgt shape: ', y_tgt.shape)

    # print('--------------------manipulation---------------')
    
    # Get the shapes of both arrays
    hat_shape = y_hat.shape
    tgt_shape = y_tgt.shape

    # Get the shapes of the second dimension
    hat_dim = hat_shape[1]
    tgt_dim = tgt_shape[1]

    if hat_dim > tgt_dim:
        pad_width = ((0, 0), (0, hat_dim - tgt_dim), (0, 0))
        y_tgt_padded = np.pad(y_tgt, pad_width, mode='constant', constant_values=0)
        y_tgt = y_tgt_padded
    elif tgt_dim > hat_dim:
        pad_width = ((0, 0), (0, tgt_dim - hat_dim), (0, 0))
        y_hat_padded = np.pad(y_hat, pad_width, mode='constant', constant_values=0)
        y_hat = y_hat_padded

    # print('--------------------after manipulation---------------')
    # print('y_hat:', y_hat)
    # print('y_hat shape: ', y_hat.shape)

    # print('y_tgt:', y_tgt)
    # print('y_tgt shape: ', y_tgt.shape)
    # END OF EDIT

    # bss_eval way
    cSDR, *_ = bss_eval(
        y_tgt,
        y_hat
    )
    cSDR = np.nanmedian(cSDR)

    # as in music demixing challenge
    uSDR = compute_uSDR(
        y_hat,
        y_tgt
    )
    return cSDR, uSDR
