from datafile import DataFile
import pandas as pd
from glob import glob
from utils import *
from progressbar import progressbar
from scipy.optimize import minimize_scalar



class Search:
    def __init__(self, *terms, csv_only=True):
        terms = list(terms)
        if csv_only:
            terms.append(".csv")

        files = glob("./**", recursive=True)
        files = filter_for_terms(files, *terms)
        self.files = files

        self.data = []
        for i in progressbar(range(len(files)), redirect_stdout=True):
            self.data.append(DataFile(files[i]))
        print(f"{len(self.files)} file(s) loaded.")

    def filter(self, *terms):
        self.files = filter_for_terms(self.files, *terms)
        self.data = [df for df in self.data if df.filename in self.files]
        print(f"{len(self.files)} file(s) loaded.")

    def find_angle_corr(self):
        df = pd.DataFrame()
        df.loc[len(df)] = ["Motion", "Subject", "Run", "Speed"]
        MOCA_col = "angles"
        BS_col = "gyro disp y (deg)"

        def corr_offset(s1, s2, offset):
            if offset >= 0:
                s1 = s1.iloc[offset:].reset_index(drop=True)
                s2 = s2.iloc[:len(s1)]
            else:
                s2 = s2.iloc[-offset:].reset_index(drop=True)
                s1 = s1.iloc[:len(s2)]

            corr = -s1.corr(s2)
            return corr

        for mc in self.data:
            bs = DataFile(mc.info.corresponding_bs())
            mc.resample()
            mc.offset_zero(MOCA_col)
            bs.resample()
            s1 = mc.df[MOCA_col]
            s2 = bs.df[BS_col]

            a = -0.5*len(bs)
            b = 0.5*len(mc)

            res = minimize_scalar(lambda x: corr_offset(s1,s2,x), bracket=(a, b), method='bounded')
            best_offset = res.x

            if best_offset >= 0:
                s1 = s1.iloc[best_offset:].reset_index(drop=True)
                s2 = s2.iloc[:len(s1)]
            else:
                s2 = s2.iloc[-best_offset:].reset_index(drop=True)
                s1 = s1.iloc[:len(s2)]

            deltas = s1.subtract(s2)
            avg_delta = deltas.mean()

            print(f"Results for {mc.info}")
            print("  Best offset:      {}".format(res.x))
            print("  Best correlation: {}".format(res.fun))
            print("  Avg angle delta:  {}".format(avg_delta))
            df.loc[len(df)] = [*mc.info.csv_string(), res.x, res.fun, avg_delta]

        return df



    

    def ls(self):
        print(f"{len(self.files)} file(s) loaded:")
        for f in self.files:
            print(f)

    def a(self, methodToRun, *args, verbose=False):
        for i in progressbar(range(len(self.data)), redirect_stdout=True):
            df = self.data[i]
            if verbose:
                print(f"Applying {methodToRun.__name__} on {df.info.title_str()}")
            methodToRun(df, *args)
        print(f"Applied {methodToRun.__name__} on {len(self.files)} file(s).")

    def w(self, verbose=False):
        self.a(DataFile.write, verbose=verbose)

    def r(self, verbose=False):
        self.a(DataFile.reset, verbose=verbose)

    # print data
    def pd(self):
        print(f"{len(self.data)} DataFile(s) loaded:")
        for item in self.data:
            print(item)

    def __getitem__(self, index):
        return self.data[index]
