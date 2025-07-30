import sys
import pathlib
import pandas as pd
import shutil
from pandas.tseries.offsets import *
import datetime
import matplotlib.pyplot as plt

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
    # load data
    ff_me = pd.read_csv('FFBreakpoints/ME_Breakpoints.CSV')
    ff_bm = pd.read_csv('FFBreakpoints/BM_Breakpoints.CSV')
    ff_cfp = pd.read_csv('FFBreakpoints/CFP_Breakpoints.CSV')
    ff_dp = pd.read_csv('FFBreakpoints/DP_Breakpoints.CSV')
    ff_ep = pd.read_csv('FFBreakpoints/EP_Breakpoints.CSV')
    ff_inv = pd.read_csv('FFBreakpoints/INV_Breakpoints.CSV')
    ff_op = pd.read_csv('FFBreakpoints/OP_Breakpoints.CSV')
    ff_pr = pd.read_csv('FFBreakpoints/PR2-12_Breakpoints.CSV')
    
    # convert dates to datetimes
    ff_me.date = pd.to_datetime(ff_me.date, format = '%Y%m')
    ff_bm.date = pd.to_datetime(ff_bm.date, format = '%Y')
    ff_cfp.date = pd.to_datetime(ff_cfp.date, format = '%Y')
    ff_dp.date = pd.to_datetime(ff_dp.date, format = '%Y%m')
    ff_ep.date = pd.to_datetime(ff_ep.date, format = '%Y')
    ff_inv.date = pd.to_datetime(ff_inv.date, format = '%Y')
    ff_op.date = pd.to_datetime(ff_op.date, format = '%Y')
    ff_pr.date = pd.to_datetime(ff_pr.date, format = '%Y%m')
    
    # adjust to end of the month or year
    ff_me.date += MonthEnd(0)
    ff_bm.date += YearEnd(0)
    ff_cfp.date += YearEnd(0)
    ff_dp.date += YearEnd(0)
    ff_ep.date += YearEnd(0)
    ff_inv.date += YearEnd(0)
    ff_op.date += YearEnd(0)
    ff_pr.date += MonthEnd(0)
    ff_me = ff_me.set_index('date').sort_index()
    ff_bm = ff_bm.set_index('date').sort_index()
    ff_cfp = ff_cfp.set_index('date').sort_index()
    ff_cfp /= 100
    ff_dp = ff_dp.set_index('date').sort_index()
    ff_dp /= 100
    ff_ep = ff_ep.set_index('date').sort_index()
    ff_ep /= 100
    ff_inv = ff_inv.set_index('date').sort_index()
    ff_inv /= 100
    ff_op = ff_op.set_index('date').sort_index()
    ff_op /= 100
    ff_pr = ff_pr.set_index('date').sort_index()
    ff_pr /= 100
    # compute my breakpoints
    DB = QueryWRDS.QueryWRDS('andrewperry', LOCAL_WRDS_DB)
    FF = FamaFrench.FamaFrench('andrewperry', LOCAL_WRDS_DB)
    start_date = datetime.date(1900, 6, 30)
    end_date = datetime.date(2100, 6, 30)
    ccm_df = DB.query_CCM(start_date, end_date)
    nyse_df = ccm_df[(ccm_df.years_in >= 2) & (ccm_df.exchcd == '1')]
    ap_me = FF.breakpoint_ts_new(nyse_df, vars = ['me'])
    ap_bm = FF.breakpoint_ts_new(nyse_df, vars = ['ffbm'])
    ap_cfp = FF.breakpoint_ts_new(nyse_df, vars = ['ffcfp'])
    ap_dp = FF.breakpoint_ts_new(nyse_df, vars = ['dp'])
    ap_ep = FF.breakpoint_ts_new(nyse_df, vars = ['ffep'])
    ap_inv = FF.breakpoint_ts_new(nyse_df, vars = ['inv'])
    ap_op = FF.breakpoint_ts_new(nyse_df, vars = ['op'])    
    ap_pr = FF.breakpoint_ts_new(nyse_df, vars = ['pr2_12'])
    ap_me = ap_me.set_index('date').sort_index()
    ap_bm = ap_bm.set_index('date').sort_index()
    ap_cfp = ap_cfp.set_index('date').sort_index()
    ap_dp = ap_dp.set_index('date').sort_index()
    ap_ep = ap_ep.set_index('date').sort_index()
    ap_inv = ap_inv.set_index('date').sort_index()
    ap_op = ap_op.set_index('date').sort_index()
    ap_pr = ap_pr.set_index('date').sort_index()
    ap_me = ap_me[ap_me.index >= datetime.datetime(1970, 1, 1)]
    ap_bm = ap_bm[ap_bm.index >= datetime.datetime(1970, 1, 1)]
    ap_cfp = ap_cfp[ap_cfp.index >= datetime.datetime(1970, 1, 1)]
    ap_dp = ap_dp[ap_dp.index >= datetime.datetime(1970, 1, 1)]
    ap_ep = ap_ep[ap_ep.index >= datetime.datetime(1970, 1, 1)]
    ap_inv = ap_inv[ap_inv.index >= datetime.datetime(1970, 1, 1)]
    ap_op = ap_op[ap_op.index >= datetime.datetime(1970, 1, 1)]
    ap_pr = ap_pr[ap_pr.index >= datetime.datetime(1970, 1, 1)]
    ff_me = ff_me.loc[ff_me.index >= ap_me.index.min()]
    ff_me = ff_me.loc[ff_me.index <= ap_me.index.max()]
    ff_bm = ff_bm.loc[ff_bm.index >= ap_bm.index.min()]
    ff_bm = ff_bm.loc[ff_bm.index <= ap_bm.index.max()]
    ff_cfp = ff_cfp.loc[ff_cfp.index >= ap_cfp.index.min()]
    ff_cfp = ff_cfp.loc[ff_cfp.index <= ap_cfp.index.max()]
    ff_dp = ff_dp.loc[ff_dp.index >= ap_dp.index.min()]
    ff_dp = ff_dp.loc[ff_dp.index <= ap_dp.index.max()]
    ff_ep = ff_ep.loc[ff_ep.index >= ap_ep.index.min()]
    ff_ep = ff_ep.loc[ff_ep.index <= ap_ep.index.max()]
    ff_inv = ff_inv.loc[ff_inv.index >= ap_inv.index.min()]
    ff_inv = ff_inv.loc[ff_inv.index <= ap_inv.index.max()]
    ff_op = ff_op.loc[ff_op.index >= ap_op.index.min()]
    ff_op = ff_op.loc[ff_op.index <= ap_op.index.max()]
    ff_pr = ff_pr.loc[ff_pr.index >= ap_pr.index.min()]
    ff_pr = ff_pr.loc[ff_pr.index <= ap_pr.index.max()]
    
    fig, ax = plt.subplots(3, 1, figsize = (32, 18))
    fig.suptitle('TS of Market Equity Breakpoints')
    ax[0].plot(ff_me['30.00%'], label = 'ff')
    ax[0].plot(ap_me['me_30%'], label = 'mine')
    ax[0].set_ylabel('30th Percentile')
    ax[1].plot(ff_me['50.00%'], label = 'ff')
    ax[1].plot(ap_me['me_50%'], label = 'mine')
    ax[1].set_ylabel('50th Percentile')
    ax[2].plot(ff_me['70.00%'], label = 'ff')
    ax[2].plot(ap_me['me_70%'], label = 'mine')
    ax[2].set_ylabel('70th Percentile')
    plt.legend()
    fig, ax = plt.subplots(3, 1, figsize = (32, 18))
    fig.suptitle('TS of Book-to-Market Breakpoints')
    ax[0].plot(ff_bm['30.00%'], label = 'ff')
    ax[0].plot(ap_bm['ffbm_30%'], label = 'mine')
    ax[0].set_ylabel('30th Percentile')
    ax[1].plot(ff_bm['50.00%'], label = 'ff')
    ax[1].plot(ap_bm['ffbm_50%'], label = 'mine')
    ax[1].set_ylabel('50th Percentile')
    ax[2].plot(ff_bm['70.00%'], label = 'ff')
    ax[2].plot(ap_bm['ffbm_70%'], label = 'mine')
    ax[2].set_ylabel('70th Percentile')
    plt.legend()
    fig, ax = plt.subplots(3, 1, figsize = (32, 18))
    fig.suptitle('TS of Cash-Flow to Price Breakpoints')
    ax[0].plot(ff_cfp['30.00%'], label = 'ff')
    ax[0].plot(ap_cfp['ffcfp_30%'], label = 'mine')
    ax[0].set_ylabel('30th Percentile')
    ax[1].plot(ff_cfp['50.00%'], label = 'ff')
    ax[1].plot(ap_cfp['ffcfp_50%'], label = 'mine')
    ax[1].set_ylabel('50th Percentile')
    ax[2].plot(ff_cfp['70.00%'], label = 'ff')
    ax[2].plot(ap_cfp['ffcfp_70%'], label = 'mine')
    ax[2].set_ylabel('70th Percentile')
    plt.legend()
    fig, ax = plt.subplots(3, 1, figsize = (32, 18))
    fig.suptitle('TS of Dividend-to-Price Breakpoints')
    ax[0].plot(ff_dp['30.00%'], label = 'ff')
    ax[0].plot(ap_dp['dp_30%'], label = 'mine')
    ax[0].set_ylabel('30th Percentile')
    ax[1].plot(ff_dp['50.00%'], label = 'ff')
    ax[1].plot(ap_dp['dp_50%'], label = 'mine')
    ax[1].set_ylabel('50th Percentile')
    ax[2].plot(ff_dp['70.00%'], label = 'ff')
    ax[2].plot(ap_dp['dp_70%'], label = 'mine')
    ax[2].set_ylabel('70th Percentile')
    plt.legend()
    fig, ax = plt.subplots(3, 1, figsize = (32, 18))
    fig.suptitle('TS of Earnings-to-Price Breakpoints')
    ax[0].plot(ff_ep['30.00%'], label = 'ff')
    ax[0].plot(ap_ep['ffep_30%'], label = 'mine')
    ax[0].set_ylabel('30th Percentile')
    ax[1].plot(ff_ep['50.00%'], label = 'ff')
    ax[1].plot(ap_ep['ffep_50%'], label = 'mine')
    ax[1].set_ylabel('50th Percentile')
    ax[2].plot(ff_ep['70.00%'], label = 'ff')
    ax[2].plot(ap_ep['ffep_70%'], label = 'mine')
    ax[2].set_ylabel('70th Percentile')
    plt.legend()
    fig, ax = plt.subplots(3, 1, figsize = (32, 18))
    fig.suptitle('TS of Investment Breakpoints')
    ax[0].plot(ff_inv['30.00%'], label = 'ff')
    ax[0].plot(ap_inv['inv_30%'], label = 'mine')
    ax[0].set_ylabel('30th Percentile')
    ax[1].plot(ff_inv['50.00%'], label = 'ff')
    ax[1].plot(ap_inv['inv_50%'], label = 'mine')
    ax[1].set_ylabel('50th Percentile')
    ax[2].plot(ff_inv['70.00%'], label = 'ff')
    ax[2].plot(ap_inv['inv_70%'], label = 'mine')
    ax[2].set_ylabel('70th Percentile')
    plt.legend()
    fig, ax = plt.subplots(3, 1, figsize = (32, 18))
    fig.suptitle('TS of Operating Profitability Breakpoints')
    ax[0].plot(ff_op['30.00%'], label = 'ff')
    ax[0].plot(ap_op['op_30%'], label = 'mine')
    ax[0].set_ylabel('30th Percentile')
    ax[1].plot(ff_op['50.00%'], label = 'ff')
    ax[1].plot(ap_op['op_50%'], label = 'mine')
    ax[1].set_ylabel('50th Percentile')
    ax[2].plot(ff_op['70.00%'], label = 'ff')
    ax[2].plot(ap_op['op_70%'], label = 'mine')
    ax[2].set_ylabel('70th Percentile')
    plt.legend()
    fig, ax = plt.subplots(3, 1, figsize = (32, 18))
    fig.suptitle('TS of Prior 2-12 Return Breakpoints')
    ax[0].plot(ff_pr['30.00%'], label = 'ff')
    ax[0].plot(ap_pr['pr2_12_30%'], label = 'mine')
    ax[0].set_ylabel('30th Percentile')
    ax[1].plot(ff_pr['50.00%'], label = 'ff')
    ax[1].plot(ap_pr['pr2_12_50%'], label = 'mine')
    ax[1].set_ylabel('50th Percentile')
    ax[2].plot(ff_pr['70.00%'], label = 'ff')
    ax[2].plot(ap_pr['pr2_12_70%'], label = 'mine')
    ax[2].set_ylabel('70th Percentile')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()