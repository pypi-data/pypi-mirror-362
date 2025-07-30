import pandas as pd
from functools import cached_property
from universal_timeseries_transformer import PricesMatrix
from timeseries_performance_calculator import (
    get_table_total_performance,
    get_table_period_returns,
    get_table_yearly_returns,
    get_table_monthly_returns,
    get_tables_monthly_relative,
    get_dfs_tables_year,
)
from fund_insight_engine.fund_data_retriever.fund_configuration import (
    get_df_fund_info,
    get_df_fund_fee,
    get_df_fund_numbers,
)
from fund_insight_engine.fund_data_retriever.timeseries.timeseries_utils import get_df_menu8186_by_fund
from fund_insight_engine.fund_data_retriever.portfolio import Portfolio
from fund_insight_engine.fund_data_retriever.portfolio.portfolio_utils import get_dfs_by_asset
from .fund_consts import COLS_FOR_CONSISE_INFO
from .fund_utils import (
    get_corrected_prices_with_indices,
    get_price,
    get_nav,
    get_aum,
    get_units,  
    get_stock_proportion,
    get_bond_proportion,
    get_proportions,
)

class Fund:
    """    
    Cached Properties:
        corrected_prices: Corrected prices DataFrame
        prices: Prices DataFrame
        returns: Returns DataFrame
        cumreturns: Cumulative returns DataFrame
        _obj_prices_matrix: PricesMatrix object
        _obj_portfolio: Portfolio object
        info: Info DataFrame
        fee: Fee DataFrame
        numbers: Numbers DataFrame
        portfolio: Portfolio DataFrame
        raw_portfolio: Raw Portfolio DataFrame
        total_performance: Total Performance DataFrame
        period_returns: Period Returns DataFrame
        yearly_returns: Yearly Returns DataFrame
        monthly_returns: Monthly Returns DataFrame
        monthly_relative: Monthly Relative DataFrame
    
    Manual Cache Properties:
        cumreturns_ref: Reference-based cumulative returns DataFrame (needs invalidation)
    """

    def __init__(self, fund_code: str, start_date: str=None, end_date: str=None, date_ref: str=None, benchmark: str=None):
        self.fund_code = fund_code
        self.start_date = start_date
        self.end_date = end_date
        self.date_ref = self.set_date_ref(date_ref)        
        self.benchmark = self.set_benchmark(benchmark)

    def set_date_ref(self, date_ref: str=None) -> str:
        return date_ref if date_ref else self.end_date

    def set_benchmark(self, benchmark: str=None) -> str:
        return self.info_concise.loc['BM1: 기준'][0] if benchmark is None else benchmark

    @cached_property
    def corrected_prices(self) -> pd.DataFrame:
        return get_corrected_prices_with_indices(self.fund_code, self.start_date, self.end_date, option_indices=self.benchmark)
    
    @cached_property
    def prices(self) -> pd.DataFrame:
        return self.corrected_prices.loc[self.start_date:, :]

    @cached_property
    def pm(self) -> PricesMatrix:
        return PricesMatrix(self.corrected_prices)

    @cached_property
    def returns(self) -> pd.DataFrame:
        return self.pm.returns.loc[self.start_date:, :]

    @cached_property
    def cumreturns(self) -> pd.DataFrame:
        return self.pm.cumreturns.loc[self.start_date:, :]

    @cached_property
    def q(self) -> pd.DataFrame:
        return self.prices.iloc[:,[0]]

    @cached_property
    def v(self) -> pd.DataFrame:
        return self.returns.iloc[:,[0]]

    @cached_property
    def raw_timesries(self) -> pd.DataFrame:
        return get_df_menu8186_by_fund(fund_code=self.fund_code, start_date=self.start_date, end_date=self.end_date)

    @cached_property
    def total_performance(self) -> pd.DataFrame:
        return get_table_total_performance(prices=self.corrected_prices)
    
    @cached_property
    def period_returns(self) -> pd.DataFrame:
        return get_table_period_returns(prices=self.corrected_prices)
    
    @cached_property
    def yearly_returns(self) -> pd.DataFrame:
        return get_table_yearly_returns(prices=self.corrected_prices)
    
    @cached_property
    def monthly_returns(self) -> pd.DataFrame:
        return get_table_monthly_returns(prices=self.corrected_prices)
    
    @cached_property
    def monthly_relative(self) -> pd.DataFrame:
        return get_tables_monthly_relative(prices=self.corrected_prices)
    
    @cached_property
    def dfs_relative(self) -> pd.DataFrame:
        return get_dfs_tables_year(prices=self.corrected_prices)

    @cached_property
    def info(self) -> pd.DataFrame:
        return get_df_fund_info(fund_code=self.fund_code, date_ref=self.date_ref)
    
    @cached_property
    def info_concise(self) -> pd.DataFrame:
        return self.info.T[COLS_FOR_CONSISE_INFO].T
    
    @cached_property
    def fee(self) -> pd.DataFrame:
        return get_df_fund_fee(fund_code=self.fund_code, date_ref=self.date_ref)
    
    @cached_property
    def numbers(self) -> pd.DataFrame:
        return get_df_fund_numbers(fund_code=self.fund_code, date_ref=self.date_ref)
    
    @cached_property
    def portfolio(self) -> Portfolio:
        return Portfolio(fund_code=self.fund_code, date_ref=self.date_ref)

    @cached_property
    def dfs_portfolio(self) -> dict:
        return get_dfs_by_asset(self.portfolio.raw)

    @cached_property
    def raw_portfolio(self) -> pd.DataFrame:
        return self.portfolio.raw

    @cached_property
    def price(self) -> pd.DataFrame:
        return get_price(fund_code=self.fund_code, start_date=self.start_date, end_date=self.end_date)
    
    @cached_property
    def nav(self) -> pd.DataFrame:
        return get_nav(fund_code=self.fund_code, start_date=self.start_date, end_date=self.end_date)
    
    @cached_property
    def aum(self) -> pd.DataFrame:
        return get_aum(fund_code=self.fund_code, start_date=self.start_date, end_date=self.end_date)
    
    @cached_property
    def units(self) -> pd.DataFrame:
        return get_units(fund_code=self.fund_code, start_date=self.start_date, end_date=self.end_date)
    
    @cached_property
    def stock_proportion(self) -> pd.DataFrame:
        return get_stock_proportion(fund_code=self.fund_code, start_date=self.start_date, end_date=self.end_date)
    
    @cached_property
    def bond_proportion(self) -> pd.DataFrame:
        return get_bond_proportion(fund_code=self.fund_code, start_date=self.start_date, end_date=self.end_date)
    
    @cached_property
    def proportions(self) -> pd.DataFrame:
        return get_proportions(fund_code=self.fund_code, start_date=self.start_date, end_date=self.end_date)
    
    @cached_property
    def prices_and_proportions(self) -> pd.DataFrame:
        return self.prices.join(self.proportions).bfill()

    def get_cumreturns_ref(self, index_ref: str=None) -> pd.DataFrame:
        return self.pm.get_cumreturns_ref(index_ref=index_ref)
    