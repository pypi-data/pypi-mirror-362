import os
import sys
import pathlib
import shutil
import time
import polars
import datetime
import pandas
import matplotlib.pyplot as plt
import typing
import warnings

sys.path.insert(0, '../src/FinToolsAP/')

import LocalDatabase
import Decorators
import LaTeXBuilder
import UtilityFunctions

# set printing options
pandas.set_option('display.max_rows', None)
pandas.set_option('display.max_columns', None)
pandas.set_option('display.width', shutil.get_terminal_size()[0])
pandas.set_option('display.float_format', lambda x: '%.3f' % x)

warnings.simplefilter(action = 'ignore', category = FutureWarning)

# directory for loacl wrds database 

# linux
LOCAL_WRDS_DB = pathlib.Path('/home/andrewperry/Documents')

PATH_TO_DATA = pathlib.Path('/home/andrewperry/Desktop/')

@Decorators.Performance
def query_CRSP_performance(DB):
    return(DB.queryDB(DB.DBP.FullMutualFundData, all_vars = True, start_date = '1980-01-01', return_type = 'polars'))

                    

def main():

    DB = LocalDatabase.LocalDatabase(save_directory = PATH_TO_DATA, 
                                     database_name = 'MutualFundData'
                                    )

    df = query_CRSP_performance(DB)

    print(df.head())
    

if __name__ == "__main__":
    main()
