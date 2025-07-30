def ff_all1():
    """
    import pandas as pd
    import numpy as np
    pd.set_option('display.max_rows', 30)
    pd.set_option('display.max_columns', 100)
    
    df_first = pd.read_csv('C:\\Users\\Administrator\\Documents\\Anno 1800\\stamps\\f4.csv',dtype=str,keep_default_na=False,na_values=[""])
    df_first.head()
    df_first.info()
    df_first.dtypes.value_counts()
    df_first.apply(lambda x:np.array([x.nunique(dropna=False),x.isna().mean(),x.value_counts()[0]/len(x)])).T.to_csv("C:\\Users\\Administrator\\Documents\\Anno 1800\\stamps\\type.csv")
    
    feature_info = pd.read_csv('C:\\Users\\Administrator\\Documents\\Anno 1800\\stamps\\f22.csv',dtype=str,keep_default_na=False,na_values=[""])
    feature_id = feature_info.en_name[feature_info['type'] == 'uid'].to_list()
    feature_enum = feature_info.en_name[feature_info['type'] == 'enum'].to_list()
    feature_string = feature_info.en_name[feature_info['type'] == 'string'].to_list()
    feature_float = feature_info.en_name[feature_info['type'] == 'float'].to_list()
    feature_float1 = feature_info.en_name[feature_info['type'] == 'float1'].to_list()
    feature_float2 = feature_info.en_name[feature_info['type'] == 'float2'].to_list()
    feature_date = feature_info.en_name[feature_info['type'] == 'date'].to_list()
    feature_del = feature_info.en_name[feature_info['type'] == 'del'].to_list()
    
    def find_text_columns(df):

        text_cols = []
        for col in df.columns:
            # 检查列的数据类型是否为字符串（object）
            if pd.api.types.is_string_dtype(df[col]):
                # 检查是否有非数值字符
                has_text = df[col].fillna("0").astype(str).str.contains(
                    r'[^0-9.eE-]',  # 匹配非数值字符
                    regex=True,
                    na=False
                ).any()

                if has_text:
                    text_cols.append(col)

        return text_cols

    find_text_columns(df_first[feature_float+feature_flostr])
    df_first.gs_fundedratio[df_first.gs_fundedratio.fillna("0").str.contains(
                    r'[^0-9.eE-]',
                    regex=True,
                    na=False
                )]
    df_first.gs_fundedratio = df_first.gs_fundedratio.str.replace("%","e-2")
    
    df_first[feature_date]
    cats = df_first[feature_float+feature_string].apply(lambda x:x.nunique(dropna=False))
    
    feature_string_new = cats[cats<100].index.to_list()
    feature_float_new = cats[cats>=100].index.to_list()
    df_first = df_first.drop(columns=feature_del)
    df_first[feature_enum]=df_first[feature_enum].apply(lambda x:pd.to_numeric(x,errors="coerce")*1.0)
    df_first[feature_float+feature_float1+feature_float2]=df_first[feature_float+feature_float1+feature_float2].apply(lambda x:pd.to_numeric(x,errors="coerce")*1.0)
    df_first[feature_date]=df_first[feature_date].apply(lambda x:pd.to_datetime(x,errors="coerce",format="%Y/%m/%d"))
    
    #同步操作验证集
    df_second = df_second.drop(columns=feature_del)
    df_second[feature_enum]=df_second[feature_enum].apply(lambda x:pd.to_numeric(x,errors="coerce")*1.0)
    df_second[feature_float+feature_float1+feature_float2]=df_second[feature_float+feature_float1+feature_float2].apply(lambda x:pd.to_numeric(x,errors="coerce")*1.0)
    df_second[feature_date]=df_second[feature_date].apply(lambda x:pd.to_datetime(x,errors="coerce",format="%Y/%m/%d"))
    df_first.to_pickle("C:\\Users\\Administrator\\Documents\\Anno 1800\\stamps\\first_type.pkl")
    
    def add_date_diff_columns(df_ori, base_date_col, date_col_list, new_col_prefix='days_diff_'):

        df = df_ori.copy()
        days_diff_cols = []

        for date_col in date_col_list:

            # 计算天数差（仅对有效日期计算）
            col_name = f"{new_col_prefix}{base_date_col}_minus_{date_col}"
            df[col_name] = (df[base_date_col] - df[date_col]).dt.days*1.0

            days_diff_cols.append(col_name)

        return df, days_diff_cols

    df_first, days_diff_cols = add_date_diff_columns(df_first, 'lending_date', feature_date)
    from datetime import datetime

    def add_zodiac_chinese_sign(df, birth_col):

        # 星座日期范围及对应星座
        zodiac_signs = [
            (1, 20, "摩羯座"), (2, 19, "水瓶座"), (3, 21, "双鱼座"), 
            (4, 20, "白羊座"), (5, 21, "金牛座"), (6, 21, "双子座"), 
            (7, 23, "巨蟹座"), (8, 23, "狮子座"), (9, 23, "处女座"), 
            (10, 23, "天秤座"), (11, 22, "天蝎座"), (12, 22, "射手座"), 
            (12, 31, "摩羯座")
        ]

        # 属相列表
        chinese_zodiac = ["鼠", "牛", "虎", "兔", "龙", "蛇", 
                         "马", "羊", "猴", "鸡", "狗", "猪"]

        # 添加星座列
        def get_zodiac_sign(date):
            if pd.isna(date):
                return np.nan
            month = date.month
            day = date.day
            for start_month, start_day, sign in zodiac_signs:
                if (month == start_month and day <= start_day) or (month == start_month - 1 and day > start_day):
                    return sign

        # 添加属相列 (以2008年为鼠年作为基准)
        def get_chinese_zodiac(year):
            if pd.isna(year):
                return np.nan
            offset = (year - 2008) % 12
            return chinese_zodiac[offset]

        # 应用函数
        df['zodiac'] = df[birth_col].apply(get_zodiac_sign)
        df['chinese_sign'] = df[birth_col].apply(lambda x: get_chinese_zodiac(x.year) if not pd.isna(x) else np.nan)

        return df

    df_first = add_zodiac_chinese_sign(df_first,'birth_dt')
    df_first["na_cnt"] = df_first.isna().sum(axis=1)*1.0
    
    constant_cols = [col for col in df_first.columns if df_first[col].nunique(dropna=False) <= 1]
    print("完全相同的列:", constant_cols)
    
    def detailed_na_analysis(df, threshold=0.95):

        # 计算各列的缺失值统计
        na_stats = pd.DataFrame({
            'total_rows': len(df),
            'na_count': df.isna().sum(),
            'na_ratio': df.isna().mean()
        })    
        # 筛选高缺失值列
        high_na_cols = na_stats[na_stats['na_ratio'] > threshold].index.tolist()
        return na_stats, high_na_cols

    na_stats, high_na_cols = detailed_na_analysis(df_first)
    def filter_features(df, zero_threshold=0.85, category_threshold=0.85):

        # 存储最终保留的特征
        selected_features_cate = []
        selected_features_col = []
        # 存储需要排除的特征及原因
        excluded_features = {}


        continuous_features = feature_float_new + feature_flostr + ["na_cnt"]
        discrete_features = feature_string_new + flostr_ind_cols

        for col in continuous_features:
            # 计算0值比例（排除缺失值）
            zero_count = (df[col] == 0).sum()
            non_missing_count = len(df)
            zero_ratio = zero_count / non_missing_count if non_missing_count > 0 else 0

            if zero_ratio >= zero_threshold:
                excluded_features[col] = f"连续变量0值占比过高({zero_ratio:.1%})"
                selected_features_col.append(col)


        for col in discrete_features:
            # 计算最大类别占比
            if df[col].notnull().sum() > 0:
                value_counts = df[col].fillna('N').value_counts(normalize=True)
                max_ratio = value_counts[value_counts.index!='N'].iloc[0]  # 最大类别占比

                if max_ratio >= category_threshold:
                    excluded_features[col] = f"离散变量单一类别占比过高({max_ratio:.1%})"
                    selected_features_cate.append(col)



        print("=== 特征分析报告 ===")
        print(f"初始特征数量: {len(df.columns)}")
        print(f"保留连续特征数量: {len(continuous_features)-len(selected_features_col)}")
        print(f"保留离散特征数量: {len(discrete_features)-len(selected_features_cate)}")
        print(f"排除特征数量: {len(excluded_features)}")

        if excluded_features:
            print("排除特征详情:")
            for col, reason in excluded_features.items():
                print(f"- {col}: {reason}")

        return selected_features_cate,selected_features_col

    filter_cates,filter_cols = filter_features(df_first, zero_threshold=0.97, category_threshold=0.97)
    def add_float1_columns(df_ori, col_list, new_col_prefix='ind_'):

        df = df_ori.copy()
        new_cols = []

        for col in col_list:

            # 计算天数差（仅对有效日期计算）
            col_name = f"{new_col_prefix}{col}"
            df[col_name] = np.where(df[col].isna(),np.nan,np.where(df[col]==df[col].value_counts().index[0],'M','O'))

            new_cols.append(col_name)

        return df, new_cols

    def add_float2_columns(df_ori, col_list, new_col_prefix='ind_'):

        df = df_ori.copy()
        new_cols = []

        for col in col_list:

            # 计算天数差（仅对有效日期计算）
            col_name = f"{new_col_prefix}{col}"
            df[col_name] = np.where(df[col].isna(),np.nan,np.where(df[col]>0,'1',df[col].astype(str)))

            new_cols.append(col_name)

        return df, new_cols
    """

    return True