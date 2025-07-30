import os
import sys
import time
import shutil
import pathlib
import datetime
import functools
import knockknock
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# add source directory to path
sys.path.insert(0, '../src/FinToolsAP/')

import LocalDatabase
import PortfolioSorts
import LaTeXBuilder

# set printing options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', shutil.get_terminal_size()[0])
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# directory for loacl wrds database
LOCAL_WRDS_DB = pathlib.Path('/home/andrewperry/Documents')

SLACK_NOTIFY = True

def list_inter(list1: list, list2: list) -> list:
    res = [e for e in list1 if e in list2]
    return(res)

def main():

    desktop = pathlib.Path('/home/andrewperry/Desktop/')

    DB = LocalDatabase.LocalDatabase(save_directory = LOCAL_WRDS_DB, 
                                     database_name = 'WRDS'
                                    )
    
    df = DB.queryDB(DB.DBP.Factors, all_vars = True)
    df = df.set_index('date')
        
    save_dir = desktop / 'factors/'
    os.makedirs(save_dir, exist_ok = True)
    for factor in df.columns:
        fig, axs = plt.subplots(nrows = 1, ncols = 1)
        fig.suptitle(f'{factor}')
        df[factor].plot(ax = axs)
        fig.savefig(save_dir / f'{factor}.pdf')
        plt.close(fig)
    
    LaTeXBuilder.graph_document(save_dir)



    raise ValueError
    head_first = head.iloc[:, :9]
    head_second = head.iloc[:, 9:]
    
    desktop = pathlib.Path('/home/andrewperry/Desktop/')
    LaTeXBuilder.df_to_tex_file(head_first, desktop / 'head/head_first.tex', index = False)
    LaTeXBuilder.df_to_tex_file(head_second, desktop / 'head/head_second.tex', index = False)
    LaTeXBuilder.table_document(desktop / 'head')
    
    raise ValueError

    ccm = DB.query_DB(DB.DBP.CCM)
    ibes = DB.query_DB(DB.DBP.IBES_AVG, measure = ['EPS', 'BPS'], fpi = [0, 1, 2])
    ibes.measure = ibes.measure.str.lower()
    ibes['label'] = ibes.measure + ibes.fpi.astype(str)
    ibes = ibes.drop(columns = ['measure', 'fpi'])
    ibes = pd.pivot_table(ibes, index = ['cusip', 'ann_eom'], columns = 'label', values = 'est')
    ibes = ibes.reset_index(drop = False)
    ibes = ibes.sort_values(by = ['cusip', 'ann_eom'])
    ibes = ibes.rename(columns = {'ann_eom': 'date'})
        
    ccm = ccm.merge(ibes, how = 'left', on = ['date', 'cusip'])
    print(ccm[ccm.ticker == 'AAPL'])




if __name__ == '__main__':
    main()