''' グラフ描画関連の関数
'''
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class plotData():
    '''グラフ描画用のデータコンテナ

    時間軸が共通な複数チャネルの時系列

    STUBです。まだ使えません。
    '''

    def __init__(self, df):
        self.df = df


def plot_multi_dat(df_set, figfile=None, xlim=(0, 50),
                   figsize=(8, 6),
                   xlabel='time [s]',
                   lw=1,
                   dpi=300):
    ''' 複数の時間軸を持つDataFrameのプロット

    Args:
        df_set (list of dict):
            グラフを描くデータセット。リストの要素は以下の辞書。
            'df' (Pandas.DataFrame) : プロットするデータ
            'cols' (list of str) : プロットするカラム
            'ylim' (list) : y軸の範囲 (最小値，最大値)
            'ylabel' (str) : y軸のラベル
            'toffset' (float) : 時間軸のオフセット
            'tcol' (str) : df の時間が格納されたカラム。デフォルトは'SECONDS'
            'keymap' (dict) : カラム名から凡例表示用テキストへのマップ
        figfile (str): 出力ファイル名
        xlim (list): 描画範囲 (from, to)
        figsize (list): グラフサイズ (width, height)
        xlabel (str): 横軸のラベル
        lw (float): 線の太さ
        dpi (float): DPI

    Examples:
        
        import eegtools

        eegtools.plot_multi_dat([
                    { 'df': df_eeg,
                      'cols': [' Fp1', ' Fp2', 'SNS'],
                      'ylim': [-100, 100],
                      'ylabel': '[uV]',
                      'tcol': 'time',
                      'keymap': {'SNS': 'Sensor signal'} },
                    { 'df': df_audio,
                      'cols': ['left', 'right'],
                      'ylabel': '[au]',
                      'tcol': 'sec' }
                 ],
                 figfile='subject-1.pdf',
                 xlim=[5, 10])

        df_eeg と df_audio の2つのpd.DataFrameを使ってグラフを描く。
        df_eeg からは時間が'time'，振幅が' Fp1'，' Fp2'，'SNS'の
        3枚のグラフを描く。
        y軸の範囲は-100から100。
        凡例はそれぞれ' Fp1'，' Fp2', 'Sensor signal'
        （'SNS'はkeymapの指定で置き換えられる）

        df_audio からは時間が'sec'，振幅が'left'と'right'の2枚のグラフを描く
        y軸の範囲は自動
        合計4枚のグラフで横軸は5から10秒。
        また 'subject-1.pdf' というPDFファイルを出力する。
        ここで，'subject-1.png' とすると PNG ファイルを出力できる。
    '''

    n_plots = 0
    for i in range(len(df_set)):
        n_plots += len(df_set[i]['cols'])

        if 'ylabel' not in df_set[i]:
            df_set[i]['ylabel'] = '[uV]'
        if 'toffset' not in df_set[i]:
            df_set[i]['toffset'] = 0.0
        if 'tcol' not in df_set[i]:
            df_set[i]['tcol'] = 'SECONDS'
        if 'keymap' not in df_set[i]:
            df_set[i]['keymap'] = {}

    print(f"{n_plots} plots")

    plt.rcParams["figure.figsize"] = figsize
    fig, ax = plt.subplots(n_plots, 1, layout=None, sharex=True)
    plt.subplots_adjust(wspace=.0, hspace=0.0001)
    plot_idx = 0

    for a_set in df_set:
        tim = a_set['df'][a_set['tcol']] - a_set['toffset']
        for c in a_set['cols']:
            if c in a_set['keymap']:
                label = a_set['keymap'][c]
            else:
                label = c
            ax[plot_idx].plot(tim, a_set['df'][c], label=label, lw=lw)
            ax[plot_idx].set_ylabel(a_set['ylabel'])
            if 'ylim' in a_set:
                ax[plot_idx].set_ylim(a_set['ylim'][0], a_set['ylim'][1])
            if xlim is not None:
                ax[plot_idx].set_xlim(xlim[0], xlim[1])
                ax[plot_idx].annotate(label, (1, 0.5),
                                      xycoords='axes fraction',
                                      verticalalignment='center')
#             ax[plot_idx].legend(bbox_to_anchor=(1.00, 1),
#                                 loc='upper left',
#                                 borderaxespad=0,
#                                 fontsize=9)
            plot_idx += 1

    ax[n_plots-1].set_xlabel(xlabel)

    plt.show()

    if figfile is not None:
        plt.savefig(figfile, dpi=dpi)

    return fig, ax
