from pandas.errors import InvalidIndexError
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
        tlist = []
        for t in terms:
            tlist += t.split()
        files = filter_for_terms(files, *tlist)
        self.files = files

        self.data = []
        for i in progressbar(range(len(files)), redirect_stdout=True):
            self.data.append(DataFile(files[i]))
        print(f"{len(self.files)} file(s) loaded.")

    def filter(self, *terms):
        self.files = filter_for_terms(self.files, *terms)
        self.data = [df for df in self.data if df.filename in self.files]
        print(f"{len(self.files)} file(s) loaded.")

    def find_angle_corr(self, verbose=False):
        df = pd.DataFrame(columns=["Motion", "Subject", "Run", "Speed", "offset","correlation","average angle delta", "rmse"])
        # MOCA_col = "angles"
        # BS_col = "gyro disp y (deg)"

        for i in progressbar(range(len(self.data)), redirect_stdout=True):
            mc = self.data[i]
            other_filename = mc.info.corresponding_bs()
            if other_filename is None:
                print(f"No corresponding file found for {mc.filename}")
                continue
            try:
                data = mc.get_angle_cor()
                if verbose: print(f"Processed {mc.info}:\n    Offset: {data[0]}\n    Correlation: {data[1]}\n    RMSE: {data[3]}")
                df.loc[len(df)] = [*mc.info.csv_string(), *data]
            except InvalidIndexError:
                continue

        return df

    def ls(self):
        print(f"{len(self.files)} file(s) loaded:")
        for f in self.files:
            print(f)

    def a(self, methodToRun, *args, verbose=False):
        for i in progressbar(range(len(self.data)), redirect_stdout=True):
            df = self.data[i]
            if verbose:
                print(f"Applying {methodToRun.__name__} on {df.info}")
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
