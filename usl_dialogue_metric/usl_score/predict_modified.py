# import json
import os
import argparse
from os import walk
import pandas as pd
from tqdm import tqdm
from scorer import Scorer

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='USL-H inference script')
    parser.add_argument('--df-dir', type=str, required=True, help='Path to df in gzip that stores the dialogue_histories and preds')
    parser.add_argument('--weight-dir', type=str, required=True, help='Path to directory that stores the weight')

    args = parser.parse_args()
    scorer = Scorer(args)

    evals = ['fteval_wow_tdhkn_\\nsep_prs_spktokenTrue_!pad_3dhcount_nb10_sampleFalse_k50_p1_numseq10_0ngoldinprompt_10-80genlen_4bs_0seed_temp1.0_typp1.0_nbeamgr1_divp0.0_tokentype_False/',
             'fteval_wow_tdhkn_\\nsep_prs_spktokenTrue_!pad_3dhcount_nb1_sampleTrue_k50_p0.3_numseq10_0ngoldinprompt_10-80genlen_8bs_0seed_temp1.0_typp1.0_nbeamgr1_divp0.0_tokentype_False/',
             'fteval_wow_tdhkn_\\nsep_prs_spktokenTrue_!pad_3dhcount_nb1_sampleTrue_k3_p1_numseq10_0ngoldinprompt_10-80genlen_8bs_0seed_temp1.0_typp1.0_nbeamgr1_divp0.0_tokentype_False/',
             ]

    for eval in tqdm(evals):

        gzips = []
        eval_path = os.path.join(args.df_dir, eval)
        for (dirpath, dirnames, filenames) in walk(eval_path):
            for filename in filenames:
                if '_analysed.gzip' in filename:
                    gzips.append(filename)

        if len(gzips) > 0:
            for filename in gzips:
                filepath = os.path.join(eval_path, filename)
                print('Now processing USL-H for ', filepath)
                df = pd.read_csv(filepath, compression='gzip')
                df.fillna('', inplace=True)

                if 'USL-HS' not in df.columns:

                    contexts = df['dialogue_histories'].tolist()
                    responses = df['preds'].tolist()

                    _, scores = scorer.get_scores(contexts, responses, normalize=True)
                    df_scores = pd.DataFrame(scores)
                    # df = df.merge(df_scores, left_index=True, right_index=True)
                    df_scores.to_csv(filepath[:-5]+'_uslhs.gzip', compression='gzip', index=False)
                    
                    
                    
    df = pd.read_csv(filepath, compression='gzip')
    df.fillna('', inplace=True)

    if 'USL-HS' not in df.columns:

        contexts = df['dialogue_histories'].tolist()
        responses = df['preds'].tolist()

        _, scores = scorer.get_scores(contexts, responses, normalize=True)
        df_scores = pd.DataFrame(scores)
        # df = df.merge(df_scores, left_index=True, right_index=True)
        df_scores.to_csv(filepath[:-5]+'_uslhs.gzip', compression='gzip', index=False)