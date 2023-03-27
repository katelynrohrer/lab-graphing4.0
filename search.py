from datafile import DataFile
from glob import glob
from utils import *
import time
import progressbar

class Search:
    def __init__(self, *terms, csv_only=True):
        terms = list(terms)
        if csv_only:
            terms.append(".csv")

        files = glob("./**", recursive=True)
        files = filter_for_terms(files, *terms)
        self.files = files

        self.data = []
        for i in progressbar.progressbar(range(len(files))):
            self.data.append(DataFile(files[i]))
        print(f"{len(self.files)} file(s) loaded.")

    def filter(self, *terms):
        self.files = filter_for_terms(self.files, *terms)
        self.data = [df for df in self.data if df.filename in self.files]
        print(f"{len(self.files)} file(s) loaded.")


    def ls(self):
        print(f"{len(self.files)} file(s) loaded:")
        for f in self.files:
            print(f)

    def a(self, methodToRun, *args, verbose=False):
        for i in progressbar.progressbar(range(len(self.data))):
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
