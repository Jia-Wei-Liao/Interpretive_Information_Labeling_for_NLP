import os
import argparse
import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize


SUBMISSION_FILE = 'submission'

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--df_files', type=str,
        default=[
        't5_small_qr_q_qr_r_bs4_beam1.csv',
        't5_base_qr_q_qr_r_bs4_beam1.csv',
        ],
    nargs='+')

    return parser.parse_args()


def read_csv_file(df_files):
    return [pd.read_csv(os.path.join(SUBMISSION_FILE, df)) for df in df_files]


def compute_len(df):
    df['q_len'] = df['q'].map(lambda x: len(word_tokenize(x)))
    df['r_len'] = df['r'].map(lambda x: len(word_tokenize(x)))

    return df


def compute_df_list_len(df_list):
    return [compute_len(df) for df in df_list]


def aggregate(df_list):
    id_list = df_list[0]['id']
    q_list = []
    r_list = []
    n_seq = len(df_list[0])

    for i in range(n_seq):
        q_index = np.argmax([df.iloc[i]['q_len'] for df in df_list])
        r_index = np.argmax([df.iloc[i]['r_len'] for df in df_list])
        q_list.append(df_list[q_index].iloc[i]['q'])
        r_list.append(df_list[r_index].iloc[i]['r'])

    aggregation_df = pd.DataFrame({'id': id_list, 'q': q_list, 'r': r_list})

    return aggregation_df


if __name__ == '__main__':
    args = parse_arguments()
    df_list = read_csv_file(args.df_files)
    df_files = compute_df_list_len(df_list)
    aggregation_df = aggregate(df_files)
    aggregation_df.to_csv(os.path.join(SUBMISSION_FILE, 'ensemble.csv'), index=False)
