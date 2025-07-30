import os
import sys
import pathlib
import shutil
import time
import datetime
import functools
import pandas as pd
import knockknock
import matplotlib.pyplot as plt

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

    CCM_df = DB.query_CCM(start_date, end_date)
    
    MF_df = DB.query_TFNMF(start_date, end_date, 
                     id_type = 'cusip', 
                     ids = list(CCM_df.cusip.unique()))
    
    CCM_df['jdate'] = CCM_df.date
    MF_df['jdate'] = MF_df.rdate

    CCM_MF_df = MF_df.merge(CCM_df, how = 'inner', on = ['cusip', 'jdate'])

    lst = [CCM_df, MF_df]
    del CCM_df, MF_df
    del lst

    CCM_MF_df['me_port'] = CCM_MF_df.prc * CCM_MF_df.shares

    print(CCM_MF_df.head())

    raise ValueError

    characteristics = ['dp', 'be', 'bm', 'ffbm', 'ep', 'ffep', 'cfp', 'ffcfp', 
                       'inv', 'op', 'pr2_12', 'pr1_1', 'pr13_60', 'beta', 'ac', 
                       'nsi']
    
    df_lst = []
    for char in characteristics:
        wdf = util_funcs.group_avg(CCM_MF_df, 'fundno', 'jdate', char, 'me')
        edf = util_funcs.group_avg(CCM_MF_df, 'fundno', 'jdate', char, 'me', vw = False)
        edf = edf.add_suffix('_ew')
        edf = edf.rename(columns = {'fundno_ew': 'fundno', 'jdate_ew': 'jdate'})
        df_lst.append(wdf)
        df_lst.append(edf)

    MF_chars_df = functools.reduce(lambda x, y: pd.merge(x, y, on = ['fundno', 'jdate']), df_lst)
    MF_chars_df = MF_chars_df.sort_values(by = ['fundno', 'jdate'])

    print(MF_chars_df.head(100))



    

    



    
WEBHOOK_URL = 'https://hooks.slack.com/services/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'
@knockknock.slack_sender(webhook_url = WEBHOOK_URL,
                         channel = 'test',
                         user_mentions = ['U01DNFEHKEV'])
def TEST_query_MF():
    main()

if __name__ == "__main__":
    if(os.getlogin() == 'andrewperry'):
        TEST_query_MF()
    else:
        main()