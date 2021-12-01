import pandas as pd


def find_ath(df, col):
    ndf = df
    done = False
    ath_idx = []
    while not done:
        idxmax = ndf[col].idxmax()
        ath_idx.append(idxmax)
        print(ndf.iloc[idxmax])
        if idxmax >= 1:
            ndf = ndf.loc[:idxmax-1]
        else:
            done = True
    return df.iloc[ath_idx]
