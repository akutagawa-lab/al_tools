from pathlib import Path
import wave

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def read_wav(filename):
    ''' WAV ファイルの読み込み

    Args:
        filename (str or Path): wav filename

    Returns:
        params (dict): result
            params['df'] (Pandas.DataFrame): audio data
                In case of multiple channel wav file, columns are named as
                'ch_1', 'ch_2', ...
                Time represented as second is stored in column named 'time'.
                i.e. params['df']['time'] represents time stamp of each row.
            params['path'] (str): wav filename
            params['fs'] (float): sampling frequency
            params['nchannels'] (int): number of channels
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


def read_eeg(filename, time_col='time'):
    ''' Polymate CSVファイルの読み込み

    Args:
        filename (str or Path): filename to be read.
        time_col (str): column name of time

    Returns:
        params (dict): result to read
        params['df'] (Pandas.DataFrame): eeg data
        params['path'] (str or Path): file path
        params['fs'] (float): sampling rate
        params['orig_columns'] (list): original column name
        params['df_head'] (Pandas.DataFrame): header information
            params['df_head'][<name>]['Type']: channel type
            params['df_head'][<name>]['Unit']: unit
    '''
    params = {}

    df = pd.read_csv(filename, header=3)
    df.rename(columns={'TIME': 'TIME_str'}, inplace=True)
    params['orig_columns'] = df.columns.to_list()

    # read sampling rate
    fs = pd.read_csv(filename, header=None, nrows=1)[1][0]
    df[time_col] = np.arange(df.shape[0]) / fs

    # read additional information for each column
    df_head = pd.read_csv(filename, header=None, skiprows=1, nrows=3)
    df_head = df_head.set_axis(df_head.iloc[2].to_list(), axis=1)
    df_head.rename(columns={'TIME': 'TIME_str'}, inplace=True)
    df_head.drop(df.index[[2]], inplace=True)
    df_head = df_head.set_axis(['Type', 'Unit'], axis=0)
    df_head['TIME_str']['Unit'] = 's'
    df_head['TIME_str']['Type'] = ''
    df_head[time_col] = ''
    df_head[time_col]['Type'] = ''
    df_head[time_col]['Unit'] = 's'
    params['df'] = df
    params['path'] = filename
    params['fs'] = fs
    params['df_head'] = df_head
    return params

