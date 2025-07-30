import pandas as pd
from xgboost import XGBRegressor
import xgboost as xgb, time
import numpy as np
import pandas as pd
import time
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import KFold

def preprocess_features(train, test, rmv_cols=["id", "label"], cardinality_threshold=9):
    """
    预处理特征：识别数值型与分类型变量，并进行factorize和类型转换。
    
    参数:
        train (pd.DataFrame): 训练集
        test (pd.DataFrame): 测试集
        rmv_cols (list): 要排除的列名，如"id"和"label"
        cardinality_threshold (int): 判定高基数分类变量的唯一值个数阈值，默认是9

    返回:
        train (pd.DataFrame): 处理后的训练集
        test (pd.DataFrame): 处理后的测试集
        cats (list): 分类特征名列表
        high_cardinality (list): 高基数特征名列表
        features (list): 特征名列表


    train, test, CATS, HIGH_CARDINALITY, FEATURES = preprocess_features(train, test)
    """
    FEATURES = [c for c in train.columns if c not in rmv_cols]
    combined = pd.concat([train, test], axis=0, ignore_index=True)

    CATS = []
    HIGH_CARDINALITY = []

    print(f"THE {len(FEATURES)} BASIC FEATURES ARE:")

    for c in FEATURES:
        ftype = "numerical"
        if combined[c].dtype == "object":
            CATS.append(c)
            combined[c] = combined[c].fillna("NAN")
            combined[c], _ = combined[c].factorize()
            combined[c] -= combined[c].min()
            ftype = "categorical"

        if combined[c].dtype == "int64":
            combined[c] = combined[c].astype("int32")
        elif combined[c].dtype == "float64":
            combined[c] = combined[c].astype("float32")

        n = combined[c].nunique()
        print(f"{c} ({ftype}) with {n} unique values")

        if n >= cardinality_threshold:
            HIGH_CARDINALITY.append(c)

    train_processed = combined.iloc[:len(train)].copy()
    test_processed = combined.iloc[len(train):].reset_index(drop=True).copy()

    print("\nTHE FOLLOWING HAVE 9 OR MORE UNIQUE VALUES:", HIGH_CARDINALITY)

    return train_processed, test_processed,combined, CATS, HIGH_CARDINALITY, FEATURES


def target_encode(train, valid, test, col, target="label", kfold=5, smooth=20, agg="mean"):

    train['kfold'] = ((train.index) % kfold)
    col_name = '_'.join(col)
    train[f'TE_{agg.upper()}_' + col_name] = 0.
    for i in range(kfold):
        
        df_tmp = train[train['kfold']!=i]
        if agg=="mean": mn = train[target].mean()
        elif agg=="median": mn = train[target].median()
        elif agg=="min": mn = train[target].min()
        elif agg=="max": mn = train[target].max()
        elif agg=="nunique": mn = 0
        df_tmp = df_tmp[col + [target]].groupby(col).agg([agg, 'count']).reset_index()
        df_tmp.columns = col + [agg, 'count']
        if agg=="nunique":
            df_tmp['TE_tmp'] = df_tmp[agg] / df_tmp['count']
        else:
            df_tmp['TE_tmp'] = ((df_tmp[agg]*df_tmp['count'])+(mn*smooth)) / (df_tmp['count']+smooth)
        df_tmp_m = train[col + ['kfold', f'TE_{agg.upper()}_' + col_name]].merge(df_tmp, how='left', left_on=col, right_on=col)
        df_tmp_m.loc[df_tmp_m['kfold']==i, f'TE_{agg.upper()}_' + col_name] = df_tmp_m.loc[df_tmp_m['kfold']==i, 'TE_tmp']
        train[f'TE_{agg.upper()}_' + col_name] = df_tmp_m[f'TE_{agg.upper()}_' + col_name].fillna(mn).values  
    
    df_tmp = train[col + [target]].groupby(col).agg([agg, 'count']).reset_index()
    if agg=="mean": mn = train[target].mean()
    elif agg=="median": mn = train[target].median()
    elif agg=="min": mn = train[target].min()
    elif agg=="max": mn = train[target].max()
    elif agg=="nunique": mn = 0
    df_tmp.columns = col + [agg, 'count']
    if agg=="nunique":
        df_tmp['TE_tmp'] = df_tmp[agg] / df_tmp['count']
    else:
        df_tmp['TE_tmp'] = ((df_tmp[agg]*df_tmp['count'])+(mn*smooth)) / (df_tmp['count']+smooth)
    df_tmp_m = valid[col].merge(df_tmp, how='left', left_on=col, right_on=col)
    valid[f'TE_{agg.upper()}_' + col_name] = df_tmp_m['TE_tmp'].fillna(mn).values
    valid[f'TE_{agg.upper()}_' + col_name] = valid[f'TE_{agg.upper()}_' + col_name].astype("float32")

    df_tmp_m = test[col].merge(df_tmp, how='left', left_on=col, right_on=col)
    test[f'TE_{agg.upper()}_' + col_name] = df_tmp_m['TE_tmp'].fillna(mn).values
    test[f'TE_{agg.upper()}_' + col_name] = test[f'TE_{agg.upper()}_' + col_name].astype("float32")

    train = train.drop('kfold', axis=1)
    train[f'TE_{agg.upper()}_' + col_name] = train[f'TE_{agg.upper()}_' + col_name].astype("float32")

    return(train, valid, test)



def xgb_cv_train_predict(
    train, test, combined, FEATURES, HIGH_CARDINALITY, lists2,
    folds=3, seed=42, model_params=None, verbose=50
):
    """
    使用交叉验证训练 XGBoost 模型并进行特征工程、预测、AUC 打分。

    参数:
        train (pd.DataFrame): 含 label 的训练数据
        test (pd.DataFrame): 测试集数据
        combined (pd.DataFrame): 用于编码的 train+test 合并数据
        FEATURES (list): 基础特征列
        HIGH_CARDINALITY (list): 高基数特征列名
        lists2 (list of list): 特征组合编码用的列组合
        folds (int): 交叉验证折数
        seed (int): 随机种子
        model_params (dict): 传给 XGBClassifier 的参数
        verbose (int): 训练时的日志间隔

    返回:
        oof (np.ndarray): OOF 预测概率
        pred (np.ndarray): 测试集预测概率（平均）
        model_list (list): 每折训练好的模型
    
    import warnings
    warnings.filterwarnings('ignore')
    oof, pred, models = xgb_cv_train_predict(
        train=train,
        test=test,
        combined=combined,
        FEATURES=FEATURES,
        HIGH_CARDINALITY=HIGH_CARDINALITY,
        lists2=lists2,
        folds=3
)
    """
    if model_params is None:
        model_params = {
            "max_depth": 8,
            "colsample_bytree": 0.9,
            "subsample": 0.9,
            "n_estimators": 2000,
            "learning_rate": 0.1,
            "early_stopping_rounds": 100,
            "eval_metric": "auc",
            "use_label_encoder": False
        }

    oof = np.zeros(len(train))
    pred = np.zeros(len(test))
    model_list = []

    kf = KFold(n_splits=folds, shuffle=True, random_state=seed)

    for i, (train_index, test_index) in enumerate(kf.split(train)):
        print("#" * 25)
        print(f"### Fold {i+1}")
        print("#" * 25)

        x_train = train.loc[train_index, FEATURES + ["label"]].copy()
        y_train = train.loc[train_index, "label"]
        x_valid = train.loc[test_index, FEATURES].copy()
        y_valid = train.loc[test_index, "label"]
        x_test = test[FEATURES].copy()

        start = time.time()
        print(f"FEATURE ENGINEER {len(FEATURES)} COLUMNS and {len(lists2)} GROUPS: ", end="")

        for j, f in enumerate(FEATURES + lists2):
            c = [f] if j < len(FEATURES) else f
            print(f"({j+1}){c}", ", ", end="")

            # 目标编码
            x_train, x_valid, x_test = target_encode(x_train, x_valid, x_test, c, smooth=20, agg="mean")
            x_train, x_valid, x_test = target_encode(x_train, x_valid, x_test, c, smooth=0, agg="median")

            # HIGH CARDINALITY FEATURES - TE MIN, MAX, NUNIQUE and CE
            if (j>=len(FEATURES)) | (c[0] in HIGH_CARDINALITY):
                x_train, x_valid, x_test = target_encode(x_train, x_valid, x_test, c, smooth=0, agg="min")
                x_train, x_valid, x_test = target_encode(x_train, x_valid, x_test, c, smooth=0, agg="max")
                x_train, x_valid, x_test = target_encode(x_train, x_valid, x_test, c, smooth=0, agg="nunique")
        
                # COUNT ENCODING (USING COMBINED TRAIN TEST)
                tmp = combined.groupby(c).label.count()
                nm = f"CE_{'_'.join(c)}"; tmp.name = nm
                x_train = x_train.merge(tmp, on=c, how="left")
                x_valid = x_valid.merge(tmp, on=c, how="left")
                x_test = x_test.merge(tmp, on=c, how="left")
                x_train[nm] = x_train[nm].fillna(-1).astype("int32")
                x_valid[nm] = x_valid[nm].fillna(-1).astype("int32")
                x_test[nm]  = x_test[nm].fillna(-1).astype("int32")
                # x_train[nm] = x_train[nm].astype("int32")
                # x_valid[nm] = x_valid[nm].astype("int32")
                # x_test[nm] = x_test[nm].astype("int32")

        end = time.time()
        print(f"\nFeature engineering took {end - start:.1f} seconds")

        x_train = x_train.drop("label", axis=1)

        # 训练模型
        model = XGBClassifier(**model_params)
        model.fit(
            x_train, y_train,
            eval_set=[(x_valid, y_valid)],
            verbose=verbose
        )

        # OOF 和测试集预测
        oof[test_index] = model.predict_proba(x_valid)[:, 1]
        pred += model.predict_proba(x_test)[:, 1]

        auc_score = roc_auc_score(y_valid, oof[test_index])
        print(f" => Fold {i+1} AUC = {auc_score:.5f}")
        model_list.append(model)

    pred /= folds
    return oof, pred, model_list


