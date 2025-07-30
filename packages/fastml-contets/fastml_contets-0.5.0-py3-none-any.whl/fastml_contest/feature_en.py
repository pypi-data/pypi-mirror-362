import pandas as pd
from scipy import stats



def add_time_features(df, time_col, prefix=None):
    """
    根据指定的时间列生成时间衍生变量，并返回新增的列名列表

    参数：
        df: pd.DataFrame，包含时间列的数据框
        time_col: str，时间列名
        prefix: str，可选，衍生变量的前缀（默认使用时间列名）

    返回：
        df: 修改后的 DataFrame
        new_cols: List[str]，新增的列名

    train_data, new_dt_cols = add_time_features(train_data, 'loan_dt')
test_data, new_dt_cols = add_time_features(test_data, 'loan_dt')
print("新增列名：", new_dt_cols)
    """
    if prefix is None:
        prefix = time_col

    df[time_col] = pd.to_datetime(df[time_col], errors='coerce')

    new_cols = [
        f'{prefix}_year',
        f'{prefix}_month',
        f'{prefix}_day',
        f'{prefix}_weekday',
        f'{prefix}_is_weekend',
        f'{prefix}_hour',
        f'{prefix}_minute',
        f'{prefix}_second'
    ]

    df[new_cols[0]] = df[time_col].dt.year
    df[new_cols[1]] = df[time_col].dt.month
    df[new_cols[2]] = df[time_col].dt.day
    df[new_cols[3]] = df[time_col].dt.weekday
    df[new_cols[4]] = df[new_cols[3]].isin([5, 6]).astype(int)
    df[new_cols[5]] = df[time_col].dt.hour
    df[new_cols[6]] = df[time_col].dt.minute
    df[new_cols[7]] = df[time_col].dt.second

    return df, new_cols



# 新增行维度统计值特征
def get_valid_numeric_columns(df, exclude_cols=None, na_threshold=0.0):
    """
    筛选出数值型且缺失比例不超过阈值的列
    
    参数：
        df: pd.DataFrame
        exclude_cols: list，排除的列（如 id, target 等）
        na_threshold: float，缺失值比例上限，默认 0（即完全无缺失）

    返回：
        valid_cols: list，筛选后的列名

    valid_cols = get_valid_numeric_columns(train_data.drop(columns=['label','id']))

    base_stats = [np.mean, np.prod, np.std, stats.skew, stats.kurtosis, sharpe]
    quantile_stats = [np.min, quantile01, quantile02, np.median, quantile08, quantile09, np.max, IQR, np.ptp, mode]
    all_stats = base_stats + quantile_stats

    range_count = 23

    for df in [train_data, test_data]:
        
        #base stats
        for fun in all_stats:
            df[f"Agg_Feature_{fun.__name__}"] = fun(
                    (df.loc[:, valid_cols].values), axis=1)
            
        # count stats
        for i in np.arange(0, range_count):
            df[f"count_{i}"] = (df[valid_cols] == i).sum(axis=1)
    """
    if exclude_cols is None:
        exclude_cols = []

    numeric_cols = df.select_dtypes(include=["int", "float"]).columns
    valid_cols = [
        col for col in numeric_cols 
        if col not in exclude_cols and df[col].isna().mean() <= na_threshold
    ]
    return valid_cols


import pandas as pd, numpy as np



def IQR(x, axis):
    return np.quantile(x, 0.75, axis=axis) - np.quantile(x, 0.25, axis=axis)

def sharpe(x, axis):
    return np.mean(x, axis=axis) / np.std(x, axis=axis)

def mode(x, axis):
    return stats.mode(x, axis=axis, keepdims=False).mode

def quantile01(a, axis):
    return np.quantile(a, q=0.1, axis=axis)

def quantile02(a, axis):
    return np.quantile(a, q=0.2, axis=axis)

def quantile08(a, axis):
    return np.quantile(a, q=0.8, axis=axis)

def quantile09(a, axis):
    return np.quantile(a, q=0.9, axis=axis)

def derive_na_flags_train_test(train_df, test_df, threshold=0.1, suffix="_is_na", inplace=False, return_cols=False):
    """
    对 train 中 NA 比例超过阈值的列，在 train 和 test 中衍生是否为 NA 的变量。

    参数：
    - train_df: 训练集 DataFrame
    - test_df: 测试集 DataFrame
    - threshold: float，缺失比例阈值（如 0.1 表示 10%）
    - suffix: str，派生列名后缀
    - inplace: bool，是否原地修改 train_df 和 test_df
    - return_cols: bool，是否返回新加的列名列表

    返回：
    - (train_new, test_new) or (train_new, test_new, added_cols)

    train_data, test_data, added_cols = derive_na_flags_train_test(train_data, test_data, threshold=0.1, return_cols=True)
print(train_data)
print(test_data)
    """
    na_ratio = train_df.isna().mean()
    target_cols = na_ratio[na_ratio > threshold].index.tolist()
    derived_cols = [f"{col}{suffix}" for col in target_cols]

    if not inplace:
        train_df = train_df.copy()
        test_df = test_df.copy()

    for col, new_col in zip(target_cols, derived_cols):
        train_df[new_col] = train_df[col].isna().astype(int)
        test_df[new_col] = test_df[col].isna().astype(int)

    if return_cols:
        return train_df, test_df, derived_cols
    return train_df, test_df





