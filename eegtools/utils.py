from pathlib import Path
import wave

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def read_wav(filename):
    ''' WAV ファイルの読み込み
    '''
    params = {}

    if isinstance(filename, Path) is True:
        filename = str(filename)
    with wave.open(filename, mode="rb") as wav_read:
        # print(wav_read.getnchannels())
        # print(wav_read.getparams())
        wav_params = wav_read.getparams()
        buf = wav_read.readframes(-1)
        # b = wav_read.readframes(5)

    if wav_params.sampwidth == 2:
        wav_dat_raw = np.frombuffer(buf, dtype='int16')
    elif wav_params.sampwidth == 4:
        wav_dat_raw = np.frombuffer(buf, dtype='int32')

    wav_time = np.arange(wav_params.nframes) / wav_params.framerate

    df = pd.DataFrame(wav_time, columns=['time'])

    for ch in range(wav_params.nchannels):
        ch_name = f'ch_{ch}'
        df[ch_name] = wav_dat_raw[ch::2]

    params['df'] = df
    params['path'] = filename
    params['fs'] = wav_params.framerate
    params['nchannels'] = wav_params.nchannels

    return params


def read_eeg(filename):
    ''' EEGファイルの読み込み

    Polymate の CSV フォーマットに対応
    '''
    params = {}

    df = pd.read_csv(filename, header=3)
    df.rename(columns={'TIME': 'TIME_str'}, inplace=True)
    fs = pd.read_csv(filename, header=None, nrows=1)[1][0]
    df['time'] = np.arange(df.shape[0]) / fs

    params['df'] = df
    params['path'] = filename
    params['fs'] = fs
    return params


