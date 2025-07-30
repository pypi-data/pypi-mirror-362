import os
import sys
import time
import scipy
import shutil
import seaborn
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
import util_funcs

# set printing options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', shutil.get_terminal_size()[0])
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# directory for loacl wrds database
LOCAL_WRDS_DB = pathlib.Path('/home/andrewperry/Documents/wrds_database/WRDS.db')

def main():
    
    DB = QueryWRDS.QueryWRDS('andrewperry', LOCAL_WRDS_DB)

    start_date = datetime.datetime(1900, 1, 1)
    end_date = datetime.datetime(2100, 12, 31)

    IH_df = DB.query_IH(start_date, end_date, typecode = '1')
    CCM_df = DB.query_CCM(start_date, end_date, 
                          cusip = list(IH_df.cusip.unique()))
    
    CCM_df['jdate'] = CCM_df.date
    IH_df['jdate'] = IH_df.rdate
    
    M_df = IH_df.merge(CCM_df, how = 'inner', on = ['cusip', 'jdate'])

    M_df['me_port'] = M_df.shares * M_df.prc.abs()

    # list largest equity holdings
    df = M_df.groupby(
        by = ['mgrno', 'date']
    ).agg({'me_port': 'sum'}).reset_index() 

    df = df.set_index('date')
    #df.groupby(by = ['mgrno'])['me_port'].plot(legend = False)

    last_date = df.index.max()

    last_date_size = df[df.index == last_date].sort_values(by = ['me_port'])

    IHnames_df = DB.query_IH(datetime.datetime(2021, 1, 1), end_date, vars = ['mgrno', 'mgrname', 'country'])
    IHnames_df = IHnames_df[IHnames_df.country == 'UNITED STATES']

    IHnames_df = IHnames_df.drop(columns = ['rdate'])
    IHnames_df = IHnames_df.drop_duplicates(subset = 'mgrno')

    last_date_size = last_date_size.drop_duplicates()

    last_date_size = last_date_size.merge(IHnames_df, how = 'inner', on = ['mgrno'])

    last_date_size = last_date_size.sort_values(by = ['me_port'], ascending = False)
    print(last_date_size)

    print(np.percentile(last_date_size.me_port, q = [0.9, 0.95, 0.99]))
    
    port_returns = util_funcs.double_group_avg(M_df, 'mgrno', 'date', 'adjret', 'me_port')

    port_returns = port_returns.set_index('date')
    #port_returns.groupby(by = ['mgrno'])['adjret'].plot(legend = False)

    print(scipy.stats.skew(port_returns['adjret']))
    print(scipy.stats.skewtest(port_returns['adjret']))

    port_returns.hist('adjret', bins = 100)
















    plt.show()
    













WEBHOOK_URL = 'https://hooks.slack.com/services/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'
@knockknock.slack_sender(webhook_url = WEBHOOK_URL,
                         channel = 'test',
                         user_mentions = ['U01DNFEHKEV'])
def filename(): # change to name of file
    main()

if __name__ == '__main__':
    if(os.getlogin() == 'andrewperry'):
        filename() # change to name of file
    else:
        main()