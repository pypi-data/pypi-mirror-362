from aws_s3_controller import load_csv_in_bucket, scan_files_in_bucket_by_regex
from financial_dataset_preprocessor import force_float
from fund_insight_engine.fund_data_retriever.portfolio.portfolio_consts import VALID_ASSETS
from fund_insight_engine.mongodb_retriever.menu2206_retriever.menu2206_utils import get_df_menu2206_snapshot


def get_full_holdings(date_ref=None):
    df = get_df_menu2206_snapshot(date_ref=date_ref)
    df_snapshot = df[df['자산'].isin(VALID_ASSETS)]
    COLS_TO_KEEP = ['펀드코드', '종목', '종목명', '원화 보유정보: 장부가액', '원화 보유정보: 평가액', '원화 보유정보: 수량']
    COLS_RENAMED = ['펀드코드', '종목코드', '종목명', '장부가', '평기액', '수량']
    MAPPING_RENAME = dict(zip(COLS_TO_KEEP, COLS_RENAMED))
    df_snapshot = df_snapshot[COLS_TO_KEEP].rename(columns=MAPPING_RENAME)
    return df_snapshot

def get_preprocessed_menu2820_snapshot(date_ref=None):
    regex = f'code000000-at{date_ref.replace("-", "")}' if date_ref else 'code000000'
    file_name = scan_files_in_bucket_by_regex(bucket='dataset-system', bucket_prefix='dataset-menu2820-snapshot', regex=regex)[-1]
    df = load_csv_in_bucket(bucket='dataset-system', bucket_prefix='dataset-menu2820-snapshot', regex=file_name)
    COLS_NUMBERS = ['수량', '취득액']
    df['종목'] = df['종목'].astype(str).str.zfill(6)
    for col in COLS_NUMBERS:
        df[col] = df[col].map(force_float)
    return df

def rename_columns_menu2820_snapshot(df):
    COLS_TO_KEEP = ['펀드', '종목', '종목명', '매매처', '매매구분', '수량', '취득액']
    COLS_RENAMED = ['펀드코드', '종목코드', '종목명', '매매처', '매매구분', '체결수량', '체결액']
    MAPPING_RENAME = dict(zip(COLS_TO_KEEP, COLS_RENAMED))
    df = df[COLS_TO_KEEP].rename(columns=MAPPING_RENAME)
    return df

def aggregate_menu2820_snapshot_by_fund(df):
    df_agg = df.groupby(['펀드코드', '종목코드', '매매구분'], as_index=False).agg({
        '종목명': 'first',
        '체결수량': 'sum',
        '체결액': 'sum'
    })
    return df_agg

def aggregate_menu2820_snapshot(df):
    df_agg = df.groupby(['종목코드', '매매구분'], as_index=False).agg({
        '종목명': 'first',
        '체결수량': 'sum',
        '체결액': 'sum'
    })
    return df_agg

def order_columns_df_agg(df):
    COLS_ORDERED = ['종목코드', '종목명', '매매구분', '체결수량', '체결액']
    df = df[COLS_ORDERED]
    return df

def order_columns_df_agg_by_fund(df):
    COLS_ORDERED = ['펀드코드', '종목코드', '종목명', '매매구분', '체결수량', '체결액']
    df = df[COLS_ORDERED]
    return df

def get_trade_executions(date_ref=None):
    df = get_preprocessed_menu2820_snapshot(date_ref=date_ref)
    return (
        df
        .copy()
        .pipe(rename_columns_menu2820_snapshot)
        .pipe(aggregate_menu2820_snapshot)
        .pipe(order_columns_df_agg)
    )

def get_trade_executions_by_fund(date_ref=None):
    df = get_preprocessed_menu2820_snapshot(date_ref=date_ref)
    return (
        df
        .copy()
        .pipe(rename_columns_menu2820_snapshot)
        .pipe(aggregate_menu2820_snapshot_by_fund)
        .pipe(order_columns_df_agg_by_fund)
    )
