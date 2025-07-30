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
import pandas.tseries.offsets

import dateutil.relativedelta
import wrds
import linearmodels

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

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

FIG_SAVE_DIR = pathlib.Path('/home/andrewperry/Dropbox/Research/Research/Asset Pricing Optimal Contracting/slides/slidesv3/figures')

SLACK_NOTIFY = False

# Weighted average
# can be used with groupby:  df.groupby('col1').apply(wavg, 'avg_name', 'weight_name')
# ML: corrected by ML to allow for missing values
def wavg(group, avg_name, weight_name=None):
    """ http://stackoverflow.com/questions/10951341/pandas-dataframe-aggregate-function-using-multiple-columns
    In rare instance, we may not have weights, so just return the mean. Customize this if your business case
    should return otherwise.
    """
    if weight_name==None:
        return group[avg_name].mean()
    else:
        x = group[[avg_name,weight_name]].dropna()
        try:
            return (x[avg_name] * x[weight_name]).sum() / x[weight_name].sum()
        except ZeroDivisionError:
            return group[avg_name].mean()

def single_group_avg(df, gr, vr, wt, vw: bool = True):
        if(vw):
            res = df.groupby(gr).apply(wavg, vr, wt)
        else:
            res = df.groupby(gr).mean(numeric_only = True)[vr]
        res = res.to_frame().reset_index().rename(
            columns = {0: vr}
        )
        return(res)

def main():

    DB = QueryWRDS.QueryWRDS('andrewperry', LOCAL_WRDS_DB)

    start_date = datetime.datetime(1900, 1, 1)
    end_date = datetime.datetime(2100, 1, 1)

    bank = DB.query_Bank(start_date, end_date, freq = 'A')
    bank['jdate'] = bank.datadate
    bank.jdate += pandas.tseries.offsets.YearEnd(0)

    comp_crsp_link = DB.query_link_table()

    # data
    call_reports = pd.read_stata('test_data/call_report.dta')
    WRDS_db = wrds.Connection(username = 'andrewperry')
    corp_link_table = WRDS_db.raw_sql('''SELECT * FROM WRDSAPPS.BONDCRSP_LINK''')
    corp_bond = pd.read_csv('test_data/corp_bond.csv', low_memory = False)
    #rssid_permco_link = pd.read_csv('test_data/rssid_permco.csv')
    rf_df = pd.read_csv('test_data/DGS5.csv')
    rf_df.DGS5 /= 100
    sp500_ret = pd.read_csv('test_data/sp500.csv')
    sp500_ret['date'] = sp500_ret.caldt
    sp500_ret.date = pd.to_datetime(sp500_ret.date, format = '%Y-%m-%d')
    sp500_ret = sp500_ret.set_index('date')

    # data types and names
    corp_link_table.permno = corp_link_table.permno.astype('Int64')
    corp_link_table.permco = corp_link_table.permco.astype('Int64')
    corp_bond.DATE = pd.to_datetime(corp_bond.DATE, format = '%Y-%m-%d')
    corp_bond.MATURITY = pd.to_datetime(corp_bond.MATURITY, format = '%Y-%m-%d')
    corp_bond.OFFERING_DATE = pd.to_datetime(corp_bond.OFFERING_DATE, format = '%Y-%m-%d')
    corp_bond = corp_bond.rename(columns = {'CUSIP': 'cusip'})
    corp_bond = corp_bond.rename(columns = {'DATE': 'date'})
    rf_df = rf_df.rename(columns = {'DATE': 'date'})
    rf_df.date = pd.to_datetime(rf_df.date, format = '%Y-%m-%d')
    rf_df.date += pandas.tseries.offsets.MonthEnd(0)
    #rssid_permco_link.dt_start = pd.to_datetime(rssid_permco_link.dt_start, format = '%Y%m%d')
    #rssid_permco_link.dt_end = pd.to_datetime(rssid_permco_link.dt_end, format = '%Y%m%d')
    #rssid_permco_link = rssid_permco_link.rename(columns = {'entity': 'idrssd'})

    corp_bond['T_Volume'] = corp_bond['T_Volume'].apply(
        lambda x: x.replace('$','')
    ).apply(
        lambda x: x.replace(',','')
    ).astype(np.float64)

    corp_bond['RET_EOM'] = corp_bond['RET_EOM'].str.rstrip('%').astype(np.float64) / 100
    corp_bond['T_Spread'] = corp_bond['T_Spread'].str.rstrip('%').astype(np.float64) / 100
    corp_bond['YIELD'] = corp_bond['YIELD'].str.rstrip('%').astype(np.float64) / 100

    corp_bond['tenor'] = (corp_bond.MATURITY - corp_bond.OFFERING_DATE).dt.days / 365
    corp_bond.tenor = corp_bond.tenor.round()
    corp_bond.tenor = corp_bond.tenor.astype('Int16')

    INVEST_GRADE = ['A', 'A-', 'A+', 'AA-', 'BBB+', 'AA', 'BBB', 'AA+', 'AAA', 'BBB-']
    corp_bond['invest_grade'] = [1 if v in INVEST_GRADE else 0 for v in corp_bond.R_SP]



    # merging
    bank = bank.merge(comp_crsp_link, how = 'left', on = ['gvkey'])

    # only US banks
    bank = bank[bank.fic == 'USA']

    # set link date bounds
    bank = bank[(bank.jdate >= bank.linkdt) & (bank.jdate <= bank.linkenddt)]

    corp_bond = corp_bond.merge(corp_link_table, how = 'inner', on = ['cusip'])
    corp_bond = corp_bond[(corp_bond.date >= corp_bond.link_startdt) & (corp_bond.date <= corp_bond.link_enddt)]
    corp_bond['jdate'] = corp_bond.date + pandas.tseries.offsets.MonthEnd(0)
    
    bank_permcos = bank.permco.unique()
    bank_bonds = corp_bond[corp_bond.permco.isin(bank_permcos)]

    # split into large and small banks 5 years before GFC
    size_of_sector = bank.groupby(by = ['jdate'])['at'].sum().reset_index().rename(columns = {'at': 'sector_size'})
    bank = bank.merge(size_of_sector, how = 'inner', on = ['jdate'])
    bank['share_of_market'] = bank['at'] / bank.sector_size
    
    ## large banks
    #plt.figure(1)
    #banks2003 = bank[bank.jdate == datetime.datetime(2003, 12, 31)].share_of_market.nlargest(10)
    #banks2003 = bank[bank.gvkey.isin(list(bank[bank.index.isin(banks2003.index)].gvkey))].set_index('jdate')
    #banks2003.groupby(by = ['conm']).share_of_market.plot(legend = True)
    #plt.xlabel('Year')
    #plt.ylabel('Share')
    #plt.savefig(FIG_SAVE_DIR / 'share_2003.png')
    #
    #plt.figure(2)
    #banks2021 = bank[bank.jdate == datetime.datetime(2021, 12, 31)].share_of_market.nlargest(10)
    #banks2021 = bank[bank.gvkey.isin(list(bank[bank.index.isin(banks2021.index)].gvkey))].set_index('jdate')
    #banks2021.groupby(by = ['conm']).share_of_market.plot(legend = True)
    #plt.xlabel('Year')
    #plt.ylabel('Share')
    #plt.savefig(FIG_SAVE_DIR / 'share_2021.png')
#
    #plt.figure(3)
    #GSIBS_2012 = ['002968', '007647', '002019', '010035', '008007']
    #banksGSIB = bank[bank.gvkey.isin(GSIBS_2012)].set_index('jdate')
    #banksGSIB.groupby(by = ['conm']).share_of_market.plot(legend = True)
    #plt.xlabel('Year')
    #plt.ylabel('Share')
    #plt.savefig(FIG_SAVE_DIR / 'share_GSIB2022.png')
#
    #bank_bonds.T_Yld_Pt /= 100
#
#
    #mkt_spreads_vw = single_group_avg(bank_bonds, ['date', 'tenor'], 'T_Spread', 'T_Volume', vw = True)
    #mkt_spreads_eq = single_group_avg(bank_bonds, ['date', 'tenor'], 'T_Spread', 'T_Volume', vw = False)
    #mkt_spreads_eq = mkt_spreads_eq.set_index('date')
    #mkt_spreads_vw = mkt_spreads_vw.set_index('date')
#
    #TENORS_TO_PLOT = [1, 2, 5, 7, 10]
#
    #plt.figure(4)
    #mkt_spreads_eq[mkt_spreads_eq.tenor.isin(TENORS_TO_PLOT)].groupby(by = ['tenor'])['T_Spread'].plot(legend = True)
    #plt.xlabel('Date')
    #plt.ylabel('Bid/Ask Spread (equally weighted)')
    #plt.savefig(FIG_SAVE_DIR / 'mkt_eq_bidask.png')
#
    #plt.figure(5)
    #mkt_spreads_vw[mkt_spreads_vw.tenor.isin(TENORS_TO_PLOT)].groupby(by = ['tenor'])['T_Spread'].plot(legend = True)
    #plt.xlabel('Date')
    #plt.ylabel('Bid/Ask Spread (volume weighted)')
    #plt.savefig(FIG_SAVE_DIR / 'mkt_vw_bidask.png')
#
    #plt.figure(6)
    #volume = bank_bonds.groupby(by = ['date', 'tenor'])['T_Volume'].sum().reset_index(drop = False)
    #volume = volume.set_index('date')
    #volume[volume.tenor.isin(TENORS_TO_PLOT)].groupby(by = ['tenor'])['T_Volume'].plot(legend = True)
    #plt.xlabel('Date')
    #plt.ylabel('Total Volume [$]')
    #plt.savefig(FIG_SAVE_DIR / 'mkt_tenor_volume.png')
#
    #plt.figure(7)
    #num_trades = bank_bonds.groupby(by = ['date', 'tenor'])['tenor'].count().to_frame().rename(
    #    columns = {'tenor': 'counts'}
    #).reset_index().set_index('date')
    #num_trades[num_trades.tenor.isin(TENORS_TO_PLOT)].groupby(by = ['tenor'])['counts'].plot(legend = True)
    #plt.xlabel('Date')
    #plt.ylabel('Total Trades')
    #plt.savefig(FIG_SAVE_DIR / 'mkt_tenor_trades.png')
#
    #plt.figure(8)
    #num_trades_BT = bank_bonds.groupby(by = ['date', 'BOND_TYPE'])['BOND_TYPE'].count().to_frame().rename(
    #    columns = {'BOND_TYPE': 'counts'}
    #).reset_index().set_index('date')
    #num_trades_BT.groupby(by = ['BOND_TYPE'])['counts'].plot(legend = True)
    #plt.xlabel('Date')
    #plt.ylabel('Total Trades')
    #plt.savefig(FIG_SAVE_DIR / 'mkt_type_trades.png')
#
    #plt.figure(9)
    #volume_BT = bank_bonds.groupby(by = ['date', 'BOND_TYPE'])['T_Volume'].sum().reset_index().set_index('date')
    #volume_BT.groupby(by = ['BOND_TYPE'])['T_Volume'].plot(legend = True)
    #plt.xlabel('Date')
    #plt.ylabel('Volume [$]')
    #plt.savefig(FIG_SAVE_DIR / 'mkt_type_volume.png')
#
#
    ## 5 year corporate yield
    #bank_bonds5Y = bank_bonds[bank_bonds.tenor == 5]
    #yld5Y_vw = single_group_avg(bank_bonds5Y, ['date', 'BOND_TYPE'], 'T_Yld_Pt', 'T_Volume', vw = True)
    #yld5Y_eq = single_group_avg(bank_bonds5Y, ['date', 'BOND_TYPE'], 'T_Yld_Pt', 'T_Volume', vw = False)
    #yld5Y_vw = yld5Y_vw.set_index('date')
    #yld5Y_eq = yld5Y_eq.set_index('date')
#
    #plt.figure(10)
    #yld5Y_eq.groupby(by = ['BOND_TYPE'])['T_Yld_Pt'].plot(legend = True)
    #plt.xlabel('Date')
    #plt.ylabel('Yield (equally weighted)')
    #plt.savefig(FIG_SAVE_DIR / 'mkt_yield_type_eq.png')
#
    #plt.figure(11)
    #yld5Y_vw.groupby(by = ['BOND_TYPE'])['T_Yld_Pt'].plot(legend = True)
    #plt.xlabel('Date')
    #plt.ylabel('Yield (Volume weighted)')
    #plt.savefig(FIG_SAVE_DIR / 'mkt_yield_type_vw.png')
#
    #plt.figure(12)
    #yld5Y_eq[yld5Y_eq.BOND_TYPE.isin(['CDEB', 'CMTN'])].groupby(by = ['BOND_TYPE'])['T_Yld_Pt'].plot(legend = True)
    #plt.xlabel('Date')
    #plt.ylabel('Yield (equally weighted)')
    #plt.savefig(FIG_SAVE_DIR / 'mkt_yield_CDEBCMTN_eq.png')
#
    #plt.figure(13)
    #yld5Y_vw[yld5Y_vw.BOND_TYPE.isin(['CDEB', 'CMTN'])].groupby(by = ['BOND_TYPE'])['T_Yld_Pt'].plot(legend = True)
    #plt.xlabel('Date')
    #plt.ylabel('Yield (Volume weighted)')
    #plt.savefig(FIG_SAVE_DIR / 'mkt_yield_CDEBCMTN_vw.png')
#
#
    ## 5 year CDEB spread
    #yld5Y_vwCDEB = yld5Y_vw[yld5Y_vw.BOND_TYPE == 'CDEB']
    #yld5Y_vwCDEB = yld5Y_vwCDEB.merge(rf_df[['date', 'DGS5']], how = 'inner', on = ['date'])
    #yld5Y_vwCDEB['spread'] = yld5Y_vwCDEB.T_Yld_Pt - yld5Y_vwCDEB.DGS5
    #yld5Y_vwCDEB = yld5Y_vwCDEB.set_index('date')
#
    #plt.figure(14)
    #yld5Y_vwCDEB.T_Yld_Pt.plot(legend = True)
    #yld5Y_vwCDEB.DGS5.plot(legend = True)
    #plt.xlabel('Date')
    #plt.ylabel('Yield')
    #plt.savefig(FIG_SAVE_DIR / 'mkt_yield_corp_T.png')
#
    #plt.figure(15)
    #yld5Y_vwCDEB.spread.plot()
    #plt.xlabel('Date')
    #plt.ylabel('Yield Spread')
    #plt.savefig(FIG_SAVE_DIR / 'mkt_spread.png')
    ##plt.show()
#
    #BAC_GSIB_YEARS = [2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 3]
    #BNY_GSIB_YEARS = [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    #CIT_GSIB_YEARS = [4, 3, 3, 3, 4, 3, 3, 3, 3, 3, 3]
    #GSC_GSIB_YEARS = [2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2]
    #JPM_GSIB_YEARS = [4, 4, 4, 4, 4, 4, 4, 4, 3, 4, 4]
    #MGS_GSIB_YEARS = [2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1]
    #STS_GSIB_YEARS = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    #WFC_GSIB_YEARS = [1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1]
#
    # create index spreads for >250B, >100B, <100B
    # the first stress test was in 2012
    #bank_post2012 = bank[bank.jdate >= datetime.datetime(2012, 1, 1)]
#
    #bank_less_100 = bank_post2012[bank_post2012['at'] < 100000]
    #bank_grtr_100 = bank_post2012[(bank_post2012['at'] >= 100000) & (bank_post2012['at'] < 250000)]
    #bank_grtr_250 = bank_post2012[bank_post2012['at'] >= 250000]
#
    #fig, (ax1, ax2) = plt.subplots(2, 1)
    #num_less_100B_banks = bank_less_100.groupby(by = ['jdate'])['gvkey'].nunique()
    #num_less_100B_banks.plot()
    #plt.ylabel('Number of Banks')
    #plt.xlabel('Date')
    #plt.title('<100B')
#
    #plt.figure(17)
    #num_grtr_100B_banks = bank_grtr_100.groupby(by = ['jdate'])['gvkey'].nunique()
    #num_grtr_100B_banks.plot()
    #plt.ylabel('Number of Banks')
    #plt.xlabel('Date')
    #plt.title('>250B')
#
    #plt.figure(18)
    #num_grtr_250B_banks = bank_grtr_250.groupby(by = ['jdate'])['gvkey'].nunique()
    #num_grtr_250B_banks.plot()
    #plt.ylabel('Number of Banks')
    #plt.xlabel('Date')
    #plt.title('>250B')
#
    ## get bond datd for each groups
    #bond_less_100 = bank_bonds[bank_bonds.permco.isin(bank_less_100.permco.unique())] #57
    #bond_grtr_100 = bank_bonds[bank_bonds.permco.isin(bank_grtr_100.permco.unique())] #18
    #bond_grtr_250 = bank_bonds[bank_bonds.permco.isin(bank_grtr_250.permco.unique())] #8
#
    ## investment grade, 5 year maturity, positive yield
    ## 16
    #bond_less_100 = bond_less_100[(bond_less_100.invest_grade == 1) & 
    #                              (bond_less_100.tenor == 5) & 
    #                              (bond_less_100.YIELD > 0)]
    #
    ## 12
    #bond_grtr_100 = bond_grtr_100[(bond_grtr_100.invest_grade == 1) & 
    #                              (bond_grtr_100.tenor == 5) & 
    #                              (bond_grtr_100.YIELD > 0)]
    #
    ## 8
    #bond_grtr_250 = bond_grtr_250[(bond_grtr_250.invest_grade == 1) & 
    #                              (bond_grtr_250.tenor == 5) & 
    #                              (bond_grtr_250.YIELD > 0)]
#
    ## weighted yield index
    #wyield_less_100 = single_group_avg(bond_less_100, ['date'], 'YIELD', 'T_Volume', vw = True)
    #wyield_less_100 = wyield_less_100.rename(columns = {'YIELD': 'less_100'})
    #wyield_grtr_100 = single_group_avg(bond_grtr_100, ['date'], 'YIELD', 'T_Volume', vw = True)
    #wyield_grtr_100 = wyield_grtr_100.rename(columns = {'YIELD': 'grtr_100'})
    #wyield_grtr_250 = single_group_avg(bond_grtr_250, ['date'], 'YIELD', 'T_Volume', vw = True)
    #wyield_grtr_250 = wyield_grtr_250.rename(columns = {'YIELD': 'grtr_250'})
#
    #yields_by_group = wyield_grtr_250.merge(wyield_grtr_100, how = 'inner', on = ['date'])
    #yields_by_group = yields_by_group.merge(wyield_less_100, how = 'inner', on = ['date'])
    #yields_by_group = yields_by_group.merge(rf_df[['date', 'DGS5']], how = 'inner', on = ['date'])
    #yields_by_group = yields_by_group.set_index('date')
#
    ## credit spreads over treasury
    #spreads_over_T = pd.DataFrame()
    #spreads_over_T['grtr_250_T'] = yields_by_group.grtr_250 - yields_by_group.DGS5
    #spreads_over_T['grtr_100_T'] = yields_by_group.grtr_100 - yields_by_group.DGS5
    #spreads_over_T['less_100_T'] = yields_by_group.less_100 - yields_by_group.DGS5
    #spreads_over_T.index = yields_by_group.index
    #spreads_over_T *= 100
#
    ## credit spreads over banks
    #spreads_over_250 = pd.DataFrame()
    #spreads_over_250['grtr_100_250'] = yields_by_group.grtr_100 - yields_by_group.grtr_250
    #spreads_over_250['less_100_250'] = yields_by_group.less_100 - yields_by_group.grtr_250
    #spreads_over_250.index = yields_by_group.index
    #spreads_over_250 *= 100
#
    #fig, ax = plt.subplots()
    #spreads_over_T.plot(ax = ax, legend = True)
    #plt.xlabel('Date')
    #plt.title('Spread over Treasury [bps]')
    #ax.legend(['SR', 'LR', 'NR'])
    #plt.savefig(FIG_SAVE_DIR / 'spread_over_T.png')
#
#
    #plt.figure(19)
    #spreads_over_250.plot(legend = True)
    #plt.xlabel('Date')
    #plt.title('Spread over other Banks [bps]')
    #plt.savefig(FIG_SAVE_DIR / 'spread_over_bank.png')
#
    ## create regulatory factor
    # combine >100B and >250B groups into regulatory factor
    # every year sort them into groups
    bank['reg_status'] = np.where(bank['at'] < 100000, 'NR', 'LR')
    bank['reg_status'] = np.where(bank['at'] >= 250000, 'SR', bank.reg_status)
    bank['regulated'] = np.where(bank['at'] < 100000, 'NR', 'R')
    bank['year'] = bank.jdate.dt.year
    bank_bonds['year'] = bank_bonds.date.dt.year

    bank_bonds = bank_bonds[(bank_bonds.invest_grade == 1) & 
                            (bank_bonds.tenor == 5) & 
                            (bank_bonds.YIELD > 0)]
    bonds_regstatus = bank_bonds.merge(bank[['year', 'permco', 'reg_status', 'regulated', 'at']], how = 'left', on = ['year', 'permco'])

    bonds_regstatus_drop = bonds_regstatus.dropna(subset = ['reg_status'])
    rets_vw = bonds_regstatus_drop.groupby(
        by = ['date', 'reg_status']
    ).apply(wavg, 'YIELD', 'T_Volume').to_frame().reset_index().rename(
        columns = {0: 'YIELD'}
    )
    
    rets_eq = bonds_regstatus_drop.groupby(
        by = ['date', 'reg_status']
    ).mean(numeric_only = True)['YIELD'].to_frame().reset_index().rename(
        columns = {0: 'YIELD'}
    )

    firm = bonds_regstatus_drop.groupby(
        by = ['date', 'reg_status']
    )['permco'].nunique().reset_index().rename(
        columns = {'permco': 'num_banks'}
    )

    bonds_regulated_drop = bonds_regstatus.dropna(subset = ['regulated'])
    rets_vw_reg = bonds_regulated_drop.groupby(
        by = ['date', 'regulated']
    ).apply(wavg, 'YIELD', 'T_Volume').to_frame().reset_index().rename(
        columns = {0: 'YIELD'}
    )
    
    rets_eq_reg = bonds_regulated_drop.groupby(
        by = ['date', 'regulated']
    ).mean(numeric_only = True)['YIELD'].to_frame().reset_index().rename(
        columns = {0: 'YIELD'}
    )

    firm_reg = bonds_regulated_drop.groupby(
        by = ['date', 'regulated']
    )['permco'].nunique().reset_index().rename(
        columns = {'permco': 'num_banks'}
    )

    rets_vw = rets_vw.pivot(index = 'date', columns = 'reg_status', values = 'YIELD')
    rets_eq = rets_eq.pivot(index = 'date', columns = 'reg_status', values = 'YIELD')
    firm = firm.pivot(index = 'date', columns = 'reg_status', values = 'num_banks')
    rets_vw = rets_vw.merge(rf_df[['date', 'DGS5']], how = 'inner', on = ['date'])
    rets_vw = rets_vw.set_index('date')

    rets_vw_reg = rets_vw_reg.pivot(index = 'date', columns = 'regulated', values = 'YIELD')
    rets_eq_reg = rets_eq_reg.pivot(index = 'date', columns = 'regulated', values = 'YIELD')
    firm_reg = firm_reg.pivot(index = 'date', columns = 'regulated', values = 'num_banks')

    rets_vw_reg = rets_vw_reg.merge(rf_df[['date', 'DGS5']], how = 'inner', on = ['date'])
    rets_vw_reg = rets_vw_reg.set_index('date')

    rets_vw_reg['RMT'] = rets_vw_reg.R - rets_vw_reg.DGS5
    rets_vw_reg['NMT'] = rets_vw_reg.NR - rets_vw_reg.DGS5
    rets_vw_reg['NMR'] = rets_vw_reg.NR - rets_vw_reg.R
    rets_eq_reg['NMR'] = rets_eq_reg.NR - rets_eq_reg.R

    fig, (ax1, ax2) = plt.subplots(2, 1)
    fig.tight_layout(h_pad = 3)
    rets_vw_reg_plt = rets_vw_reg * 100
    rets_vw_reg_plt[['R', 'NR']].plot(legend = True, ax = ax1)
    ax1.set_title('Offered Yield for Regulated and Non Regulated Banks')
    ax1.set_xlabel('')
    ax1.set_ylabel('Yield [%]')

    rets_vw_reg_plt[['RMT', 'NMT']].plot(legend = True, ax = ax2)
    ax2.set_title('Credit Spread for Regulated and Non Regulated Banks over Treasury')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Spread [bps]')
    ax2.legend(['R', 'NR'])
    ax2.set_ylim([-1, 4])
    fig.savefig(FIG_SAVE_DIR / 'reg_not_yield_spread.png', bbox_inches = 'tight', dpi = 600)

    fig, (ax1, ax2) = plt.subplots(2, 1)
    fig.tight_layout(h_pad = 3)
    rets_vw_reg_plt[['NMR']].plot(legend = False, ax = ax1)
    ax1.set_title('NMR')
    ax1.set_xlabel('')
    ax1.set_ylabel('Spread [bps]')

    firm_reg[['R', 'NR']].plot(legend = True, ax = ax2)
    ax2.set_title('Number of Regulated and Non-Regulated Banks')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Number')
    ax2.legend(['R', 'NR'])
    fig.savefig(FIG_SAVE_DIR / 'NMR.png', bbox_inches = 'tight', dpi = 600)
#
    #print('Full Sample')
    #print(rets_vw_reg_plt['NML'].corr(rets_vw_reg_plt['LMS']))
#
    #print('Pre 2007')
    #pre = rets_vw_reg_plt[rets_vw_reg_plt.index <= datetime.datetime(2007, 1, 1)]
    #print(pre['NML'].corr(pre['LMS']))
#
    #print('Post 2011')
    #post = rets_vw_reg_plt[rets_vw_reg_plt.index >= datetime.datetime(2011, 1, 1)]
    #print(post['NML'].corr(post['LMS']))
    #exit()


    ########################################################################################################################################
    # Reg status
    ########################################################################################################################################

    rets_vw['NMS'] = rets_vw.NR - rets_vw.SR
    rets_vw['NML'] = rets_vw.NR - rets_vw.LR
    rets_vw['LMS'] = rets_vw.LR - rets_vw.SR

    rets_eq['NMS'] = rets_eq.NR - rets_eq.SR
    rets_eq['NML'] = rets_eq.NR - rets_eq.LR

    rets_vw['NMT'] = rets_vw.NR - rets_vw.DGS5
    rets_vw['SMT'] = rets_vw.SR - rets_vw.DGS5
    rets_vw['LMT'] = rets_vw.LR - rets_vw.DGS5

    fig, (ax1, ax2) = plt.subplots(2, 1)
    fig.tight_layout(h_pad = 3)
    rets_vw_plt = rets_vw * 100
    rets_vw_plt[['SR', 'LR', 'NR']].plot(legend = True, ax = ax1)
    ax1.set_title('Offered Yield for Non, Lightly, and Strongly Regulated Banks')
    ax1.set_xlabel('')
    ax1.set_ylabel('Yield [%]')

    rets_vw_plt[['SMT', 'LMT', 'NMT']].plot(legend = True, ax = ax2)
    ax2.set_title('Credit Spread for Non, Lightly, and Strongly Regulated Banks over Treasury')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Spread [bps]')
    ax2.legend(['SR', 'LR', 'NR'])
    ax2.set_ylim([-1, 4])
    fig.savefig(FIG_SAVE_DIR / 'regstatus_not_yield_spread.png', bbox_inches = 'tight', dpi = 600)

    fig, (ax1, ax2) = plt.subplots(2, 1)
    fig.tight_layout(h_pad = 3)
    rets_vw_plt[['NML', 'LMS']].plot(legend = True, ax = ax1)
    ax1.set_title('NML & LMS')
    ax1.set_xlabel('')
    ax1.set_ylabel('Spread [bps]')

    firm[['SR', 'LR', 'NR']].plot(legend = True, ax = ax2)
    ax2.set_title('Number of Non, Lightly, and Strongly Regulated Banks')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Number')
    ax2.legend(['SR', 'LR', 'NR'])
    fig.savefig(FIG_SAVE_DIR / 'NML_LMS.png', bbox_inches = 'tight', dpi = 600)

    #print('Full Sample')
    #print(rets_vw_plt['NML'].corr(rets_vw_plt['LMS']))
#
    #print('Pre 2007')
    #pre = rets_vw_plt[rets_vw_plt.index <= datetime.datetime(2007, 1, 1)]
    #print(pre['NML'].corr(pre['LMS']))
#
    #print('Post 2011')
    #post = rets_vw_plt[rets_vw_plt.index >= datetime.datetime(2011, 1, 1)]
    #print(post['NML'].corr(post['LMS']))
    #exit()
    

    # fama french regression
    X = single_group_avg(bonds_regstatus, ['date', 'permco'], 'YIELD', 'T_Volume', vw = True)
    X = X.merge(bonds_regstatus[['date', 'permco', 'reg_status', 'regulated']], how = 'inner', on = ['date', 'permco'])
    X = X.merge(rf_df[['date', 'DGS5']], how = 'inner', on = ['date'])
    X = X.merge(rets_vw[['NML', 'LMS']], how = 'inner', on = ['date'])
    X = X.merge(rets_vw_reg[['NMR']], how = 'inner', on = ['date'])
    X['rp'] = X.YIELD - X.DGS5

    X['indic_NR'] = np.where(X.reg_status == 'NR', 1, 0)
    X['indic_LR'] = np.where(X.reg_status == 'LR', 1, 0)

    # different time periods
    Xfull = X
    Xpre07 = X[X.date < datetime.datetime(2007, 1, 1)]
    Xpre12 = X[X.date < datetime.datetime(2011, 1, 1)]
    Xpst12 = X[X.date >= datetime.datetime(2011, 1, 1)]
    Xfull = Xfull.set_index(['permco', 'date'])
    Xpre07 = Xpre07.set_index(['permco', 'date'])
    Xpre12 = Xpre12.set_index(['permco', 'date'])
    Xpst12 = Xpst12.set_index(['permco', 'date'])

    # regulation status NMS, NML
    ff_full_regstatusM = linearmodels.panel.PanelOLS(dependent = Xfull['rp'], exog = Xfull[['NML', 'LMS']], entity_effects = True)
    ff_full_regstatusM_fit = ff_full_regstatusM.fit(cov_type = 'clustered', cluster_entity = True) 
    
    ff_pre07_regstatusM = linearmodels.panel.PanelOLS(dependent = Xpre07['rp'], exog = Xpre07[['NML', 'LMS']], entity_effects = True)
    ff_pre07_regstatusM_fit = ff_pre07_regstatusM.fit(cov_type = 'clustered', cluster_entity = True) 
    
    ff_pre12_regstatusM = linearmodels.panel.PanelOLS(dependent = Xpre12['rp'], exog = Xpre12[['NML', 'LMS']], entity_effects = True)
    ff_pre12_regstatusM_fit = ff_pre12_regstatusM.fit(cov_type = 'clustered', cluster_entity = True) 

    ff_pst12_regstatusM = linearmodels.panel.PanelOLS(dependent = Xpst12['rp'], exog = Xpst12[['NML', 'LMS']], entity_effects = True)
    ff_pst12_regstatusM_fit = ff_pst12_regstatusM.fit(cov_type = 'clustered', cluster_entity = True) 

    # regulated NMR
    ff_full_regulatedM = linearmodels.panel.PanelOLS(dependent = Xfull['rp'], exog = Xfull[['NMR']], entity_effects = True)
    ff_full_regulatedM_fit = ff_full_regulatedM.fit(cov_type = 'clustered', cluster_entity = True) 

    ff_pre07_regulatedM = linearmodels.panel.PanelOLS(dependent = Xpre07['rp'], exog = Xpre07[['NMR']], entity_effects = True)
    ff_pre07_regulatedM_fit = ff_pre07_regulatedM.fit(cov_type = 'clustered', cluster_entity = True) 

    ff_pre12_regulatedM = linearmodels.panel.PanelOLS(dependent = Xpre12['rp'], exog = Xpre12[['NMR']], entity_effects = True)
    ff_pre12_regulatedM_fit = ff_pre12_regulatedM.fit(cov_type = 'clustered', cluster_entity = True) 

    ff_pst12_regulatedM = linearmodels.panel.PanelOLS(dependent = Xpst12['rp'], exog = Xpst12[['NMR']], entity_effects = True)
    ff_pst12_regulatedM_fit = ff_pst12_regulatedM.fit(cov_type = 'clustered', cluster_entity = True) 

    compare_dic = {'Stat: 2002-2022': ff_full_regstatusM_fit, 
                   'Stat: 2002-2007': ff_pre07_regstatusM_fit,
                   'Stat: 2002-2011': ff_pre12_regstatusM_fit,
                   'Stat: 2011-2022': ff_pst12_regstatusM_fit,
                   'Reg: 2002-2022': ff_full_regulatedM_fit,
                   'Reg: 2002-2007': ff_pre07_regulatedM_fit,
                   'Reg: 2002-2011': ff_pre12_regulatedM_fit,
                   'Reg: 2011-2022': ff_pst12_regulatedM_fit}
    
    print(linearmodels.panel.compare(compare_dic, stars = True, precision = 'std_errors'))


    exit()

    plt.show()















    exit()

    macro_df = pd.read_excel('test_data/JSTdatasetR6.xlsx')

    macro_df.year = pd.to_datetime(macro_df.year, format = '%Y')
    macro_df.year += pandas.tseries.offsets.YearEnd(0)

    usa_df = macro_df[macro_df.iso == 'USA']
    usa_df = usa_df.set_index('year')

    # filter to data in compustat
    usa_df = usa_df[usa_df.index >= datetime.datetime(1960, 1, 1)]

    # fragility
    usa_df['fragility'] = usa_df.tloans / usa_df.gdp.shift(1)
    usa_df['fragility_dmean'] = usa_df.fragility - np.mean(usa_df.fragility)
    usa_df['fragility_gr'] = usa_df.fragility.pct_change()
    avg_frag_gr = np.mean(usa_df.fragility_gr)
    usa_df['fragility_gr_dmean'] = usa_df['fragility_gr'] - avg_frag_gr

    # average loan growth
    usa_df['tloan_gr'] = usa_df.tloans.pct_change()
    avg_tloan_gr = np.mean(usa_df.tloan_gr)
    usa_df['tloan_gr_dmean'] = usa_df.tloan_gr - avg_tloan_gr

    # gdp growth
    usa_df['gdp_gr'] = usa_df.gdp.pct_change()
    avg_gdp_gr = np.mean(usa_df.gdp_gr)
    usa_df['gdp_gr_dmean'] = usa_df.gdp_gr - avg_gdp_gr

    def get_variation(values: pd.Series) -> np.float64:
        base = values.iloc[0]  # first element in window iteration
        current = values.iloc[-1]  # last element in window iteration
        return (current - base) / base if base else 0  # avoid ZeroDivisionError

    # crisis
    lst_crisis = []
    crisis_dates = list(usa_df[usa_df.crisisJST == 1].index)
    for crisis in crisis_dates:
        crisis_df = usa_df[(usa_df.index >= crisis - dateutil.relativedelta.relativedelta(years = 5)) & (usa_df.index <= crisis + dateutil.relativedelta.relativedelta(years = 5))]
        crisis_df['crisis_delta'] = list(range(-5, 6))
        temp = crisis_df.tloan_gr_dmean.expanding(min_periods = 2).apply(get_variation)
        temp.name = 'gr_loan_tm5'
        crisis_df = crisis_df.merge(temp, right_index = True, left_index = True)
        temp = crisis_df.gdp_gr_dmean.expanding(min_periods = 2).apply(get_variation)
        temp.name = 'gr_gdp_tm5'
        crisis_df = crisis_df.merge(temp, right_index = True, left_index = True)
        lst_crisis.append(crisis_df)

    usa_crisis_df = pd.concat(lst_crisis)

    crisis_avg_gr_loan_tm5 = usa_crisis_df.groupby(by = ['crisis_delta'])['gr_loan_tm5'].mean()
    crisis_avg_frag_dmean = usa_crisis_df.groupby(by = ['crisis_delta'])['fragility_dmean'].mean()
    crisis_avg_frag_gr_dmean = usa_crisis_df.groupby(by = ['crisis_delta'])['fragility_gr_dmean'].mean()
    plt.figure(1)
    crisis_avg_frag_dmean.plot()
    plt.xlabel('Year')
    plt.ylabel('Differnce in Fragility from Average')
    plt.savefig('/home/andrewperry/Dropbox/Research/Research/Asset Pricing Optimal Contracting/slides/slidesv2/figures/frag.png')

    plt.figure(2)
    crisis_avg_frag_gr_dmean.plot()

    plt.figure(3)
    crisis_avg_gr_loan_tm5.plot()


    plt.show()
    exit()
    
    DB = QueryWRDS.QueryWRDS('andrewperry', LOCAL_WRDS_DB)

    start_date = datetime.datetime(1900, 1, 1)
    end_date = datetime.datetime(2100, 1, 1)

    df = DB.query_Bank(start_date, end_date, freq = 'A')
    
    df_us = df[df.fic == 'USA']

    # align dates to end of year
    df_us['year_end'] = df_us.datadate + pandas.tseries.offsets.YearEnd(0)

    # split into small and large banks


    df_us['tloans'] = df_us.lcacld + df_us.lcacrd
    df_us['loan_size'] = np.where(df_us['at'] != 0, df_us.tloans / df_us['at'], np.nan)

    size_of_sector = df_us.groupby(by = ['year_end'])['at'].sum()
    credit_of_sector = df_us.groupby(by = ['year_end'])['tloans'].sum()

    average_loan_to_size = df_us.groupby(by = ['year_end'])['loan_size'].mean()
    growth_avg_loan_size = average_loan_to_size.pct_change()

    df_us = df_us.set_index('year_end')

    df_us.groupby(by = ['gvkey'])['at'].plot(legend = False)

    plt.show()


WEBHOOK_URL = 'https://hooks.slack.com/services/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'
@knockknock.slack_sender(webhook_url = WEBHOOK_URL,
                         channel = 'test',
                         user_mentions = ['U01DNFEHKEV'])
def TEST_query_Bank(): # change to name of file
    main()

if __name__ == '__main__':
    if(os.getlogin() == 'andrewperry' and SLACK_NOTIFY):
        TEST_query_Bank() # change to name of file
    else:
        main()