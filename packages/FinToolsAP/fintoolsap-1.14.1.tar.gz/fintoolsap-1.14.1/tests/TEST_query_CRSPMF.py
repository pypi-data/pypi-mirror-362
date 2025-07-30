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
import pandas.tseries.offsets
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

SLACK_NOTIFY = True

def main():
    
    DB = QueryWRDS.QueryWRDS('andrewperry', LOCAL_WRDS_DB, update_all_tables = False)

    raise ValueError

    start_date = datetime.datetime(1900, 1, 1)
    end_date = datetime.datetime.now()

    crsp = DB.query_CRSPMF(start_date, end_date, vars = ['crsp_portno', 'report_dt'])
    portmap = DB.query_CRSPPortnoMap(vars = ['crsp_portno', 'crsp_fundno', 'begdt', 'enddt'])
    link_df = DB.query_MFLinks(start_date, end_date, vars = ['crsp_fundno', 'wficn', 'rdate', 'fundno'])

    crsp['jdate'] = crsp.report_dt + pandas.tseries.offsets.QuarterEnd(0)
    link_df['jdate'] = link_df.rdate + pandas.tseries.offsets.QuarterEnd(0)

    crsp = crsp.merge(portmap, how = 'inner', on = ['crsp_portno'])
    crsp = crsp[(crsp.jdate >= crsp.begdt) & (crsp.jdate <= crsp.enddt)]
    crsp = crsp.merge(link_df, how = 'inner', on = ['crsp_fundno', 'jdate'])


    print(crsp.head())
    raise ValueError


    df = DB.query_TFNMF(start_date, end_date, vars = ['fundno', 'rdate'])
    df['jdate'] = df.rdate + pandas.tseries.offsets.QuarterEnd(0)
    df = df.merge(link_df, how = 'inner', on = ['fundno', 'jdate'])

    plt.figure(1)
    crsp.groupby(by = ['jdate'])['wficn'].nunique().plot()
    df.groupby(by = ['jdate'])['wficn'].nunique().plot()
    plt.legend(['CRSP', 'TFN'])
    plt.show()


WEBHOOK_URL = 'https://hooks.slack.com/services/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'
@knockknock.slack_sender(webhook_url = WEBHOOK_URL,
                         channel = 'test',
                         user_mentions = ['U01DNFEHKEV'])
def TEST_query_CRSPMF(): # change to name of file
    main()

if __name__ == '__main__':
    if(os.getlogin() == 'andrewperry' and SLACK_NOTIFY):
        TEST_query_CRSPMF() # change to name of file
    else:
        main()