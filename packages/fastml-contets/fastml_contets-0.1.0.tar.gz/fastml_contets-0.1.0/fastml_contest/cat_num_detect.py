import pandas as pd

def auto_detect_variable_types(df, cat_threshold=10, nunique_ratio_threshold=0.05):
    """
    自动划分分类变量和数值变量
    
    参数:
        df: pandas DataFrame
        cat_threshold: 对于数值型变量，若唯一值少于该值认为是分类变量
        nunique_ratio_threshold: 对于数值型变量，若唯一值占比小于该比例，也认为是分类变量
    
    返回:
        categorical_vars: 分类变量列表
        numerical_vars: 数值变量列表
    """
    categorical_vars = []
    numerical_vars = []
    total_rows = len(df)

    for col in df.columns:
        dtype = df[col].dtype
        nunique = df[col].nunique(dropna=True)
        ratio = nunique / total_rows
        
        if dtype == 'object' or dtype.name == 'category':
            categorical_vars.append(col)
        elif pd.api.types.is_bool_dtype(df[col]):
            categorical_vars.append(col)
        elif pd.api.types.is_numeric_dtype(df[col]):
            if nunique < cat_threshold or ratio < nunique_ratio_threshold:
                categorical_vars.append(col)
            else:
                numerical_vars.append(col)
        else:
            # 其它类型暂时归为分类
            categorical_vars.append(col)
    
    return categorical_vars, numerical_vars
