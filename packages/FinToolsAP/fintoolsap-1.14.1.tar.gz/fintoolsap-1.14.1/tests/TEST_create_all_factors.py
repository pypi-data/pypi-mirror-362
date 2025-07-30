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

import QueryWRDS
import FamaFrench

# set printing options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', shutil.get_terminal_size()[0])
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# directory for loacl wrds database
LOCAL_WRDS_DB = pathlib.Path('/home/andrewperry/Documents/wrds_database/WRDS.db')

def main():
    
    DB = QueryWRDS.QueryWRDS('andrewperry', LOCAL_WRDS_DB)
    FF = FamaFrench.FamaFrench(data_base = DB)

    factors = FF.FF_factors()

    print(factors.head(300))

    


WEBHOOK_URL = 'https://hooks.slack.com/services/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'
@knockknock.slack_sender(webhook_url = WEBHOOK_URL,
                         channel = 'test',
                         user_mentions = ['U01DNFEHKEV'])
def TEST_create_all_factors(): # change to name of file
    main()

if __name__ == '__main__':
    if(os.getlogin() == 'andrewperry'):
        TEST_create_all_factors() # change to name of file
    else:
        main()