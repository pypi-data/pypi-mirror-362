import os
import sys
import time
import shutil
import pathlib
import datetime
import functools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# add source directory to path
sys.path.insert(0, '../src/FinToolsAP/')

import LocalDatabase
import FamaFrench

# set printing options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', shutil.get_terminal_size()[0])
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# directory for loacl wrds database
LOCAL_WRDS_DB = pathlib.Path('/home/andrewperry/Documents')

SLACK_NOTIFY = True

def main():
    DB = LocalDatabase.LocalDatabase(LOCAL_WRDS_DB, database_name = 'WRDS')
    treasury_df = DB.query_DB(DB.DBP.TREASURY)
    print(treasury_df.head())
    exit()

    fisd_banks = DB.query_DB(DB.DBP.Mergent.FISD_MERGED, sic_code = [6021, 6022, 6029])
    print(fisd_banks.head())

    issue_id_banks = list(fisd_banks.issue_id.unique())

    fisd_tsale = DB.query_DB(DB.DBP.Mergent.TSALES, issue_id = issue_id_banks)
    print(fisd_tsale.shape)
    print(fisd_tsale.head())


if __name__ == '__main__':
    main()
