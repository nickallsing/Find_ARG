#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 10:14:25 2022

@author: nallsing
"""
DESC = ("""This function combines multiple csv blast outputs into a hits csv and list csv. 
        It also outputs individual files for each sample with correct titles Please place in
        same directory as files.
        """)
import argparse
import glob
import pandas as pd
import os

def main():
    parser = arg_parser()
    args = parser.parse_args()
    os.mkdir(args.o)
    files = glob.glob(args.i)
    big_df = pd.DataFrame()
    df_dict = {}
    for file in files:
        df = pd.read_csv(file, sep=',', header=None)
        df.columns = ["query_acc.ver", "subject_acc.ver", "%_identity", "alignment_length", "mismatches", "gap_opens", "q._start", "q._end", "s._start", "s._end", "evalue", "bit_score"]
        name = str(args.o+"/"+file[:-4]+".csv")
        filename = file[:-10]
        df.to_csv(name)
        df[filename] = pd.Series([1 for x in range(len(df.index))])
        new_df = df[["subject_acc.ver",filename]]
        counted_df = new_df.groupby(by=["subject_acc.ver"]).sum()
        big_df = pd.concat([big_df, counted_df], axis=1)
        big_df = big_df.fillna(0)
        #sorted_df = counted_df.sort_values(by=filename, ascending=False)
        df_dict.update({filename:df["subject_acc.ver"]})
    df_2=pd.DataFrame.from_dict(df_dict,orient='index').transpose()
    big_df.to_csv(args.n)
    df_2.to_csv(args.l)
   

def arg_parser():
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument("-i", default="*.txt", help='Required. Input file(s). For multiple, format as "*.txt"')
    parser.add_argument("-n", default="ARG_hits.csv",help="Hits csv name. Default = ARG_hits.csv")
    parser.add_argument("-l", default="ARG_list.csv",help="List csv name. Default = ARG_list.csv")
    parser.add_argument('-o', default="ARG_hits_data",help="Out directory for sample csvs. Default = ARG_hits_data")

    return parser


if __name__ == "__main__":
    import sys
    sys.exit(main())