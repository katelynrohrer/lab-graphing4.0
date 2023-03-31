from datafile import DataFile
import math
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
        df = pd.DataFrame(columns=["Motion", "Subject", "Run", "Speed", "offset","correlation","average angle delta", "rmse"])
        MOCA_col = "angles"
        BS_col = "gyro disp y (deg)"

        def corr_offset(s1, s2, of):
            s1, s2 = offset(s1, s2, of)
            corr = s1.corr(s2)
            return corr

        for mc in self.data:
            corresponding_file = mc.info.corresponding_bs()
            if corresponding_file is None:
                print(f"No corresponding file found for {mc.filename}")
                continue
            bs = DataFile(mc.info.corresponding_bs())
            if MOCA_col not in mc.df.columns:
                print(f"Column {MOCA_col} not found in {mc.filename}")
                continue
            if BS_col not in bs.df.columns:
                print(f"Column {BS_col} not found in {bs.filename}")
                continue
            mc.resample()
            mc.offset_zero(MOCA_col)
            bs.resample()
            s1 = mc.df[MOCA_col]
            s2 = bs.df[BS_col]

            a = -len(bs.df)//3
            b = len(mc.df)//2

            corr,best_offset = maximize(lambda x: corr_offset(s1,s2,x), a, b)

            s1, s2 = offset(s1, s2, best_offset)

            deltas = s1 - s2
            avg_delta = deltas.mean()
            rmse_data = (s1 - s2)**2
            rmse = math.sqrt(rmse_data.mean())
            print(f"Results for {mc.info}")
            print("  Best offset:      {}".format(best_offset))
            print("  Best correlation: {}".format(corr))
            print("  Avg angle delta:  {}".format(avg_delta))
            df.loc[len(df)] = [*mc.info.csv_string(), best_offset, corr, avg_delta, rmse]

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
