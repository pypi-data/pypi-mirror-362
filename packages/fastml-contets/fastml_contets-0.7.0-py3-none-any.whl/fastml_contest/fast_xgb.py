import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import KFold
from sklearn.metrics import roc_auc_score, f1_score, roc_curve

def ks_score(y_true, y_prob):
    fpr, tpr, _ = roc_curve(y_true, y_prob)
    return max(tpr - fpr)

def evaluate_metrics(y_true, y_prob, threshold=0.5):
    y_pred = (y_prob > threshold).astype(int)
    ks = ks_score(y_true, y_prob)
    auc = roc_auc_score(y_true, y_prob)
    f1 = f1_score(y_true, y_pred)
    return ks, auc, f1

def train_with_cv(train_df, test_df, label_col='label', cate_cols=None, n_splits=10):
    """
    使用 XGBoost 进行 10 折交叉验证训练，并在测试集上预测。
    """
    # 准备数据
    X = train_df.drop(columns=[label_col])
    y = train_df[label_col].values
    X_test = test_df.drop(columns=[label_col], errors='ignore')
    y_test = test_df[label_col] if label_col in test_df.columns else None

    # 类别列转换为 string（或自行做 one-hot/target encoding）
    if cate_cols is None:
        cate_cols = X.select_dtypes(include='object').columns.tolist()
    for col in cate_cols:
        X[col] = X[col].astype(str)
        X_test[col] = X_test[col].astype(str)

    # 使用 one-hot 编码（也可以改成 target encoding）
    X = pd.get_dummies(X, columns=cate_cols)
    X_test = pd.get_dummies(X_test, columns=cate_cols)
    X_test = X_test.reindex(columns=X.columns, fill_value=0)

    skf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    test_preds = np.zeros(len(X_test))
    ks_list, auc_list, f1_list, model_list = [], [], [], []

    for fold, (train_idx, valid_idx) in enumerate(skf.split(X, y)):
        print(f"\n📦 Fold {fold + 1}")

        X_train, X_valid = X.iloc[train_idx], X.iloc[valid_idx]
        y_train, y_valid = y[train_idx], y[valid_idx]

        dtrain = xgb.DMatrix(X_train, label=y_train)
        dvalid = xgb.DMatrix(X_valid, label=y_valid)
        dtest = xgb.DMatrix(X_test)

        params = {
            'objective': 'binary:logistic',
            'eval_metric': 'auc',
            'learning_rate': 0.1,
            'max_depth': 5,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'seed': 42,
            'verbosity': 1,
        }

        evals = [(dtrain, 'train'), (dvalid, 'valid')]
        model = xgb.train(
            params,
            dtrain,
            num_boost_round=2000,
            evals=evals,
            early_stopping_rounds=100,
            verbose_eval=100
        )

        valid_prob = model.predict(dvalid)
        ks, auc, f1 = evaluate_metrics(y_valid, valid_prob)
        print(f"✅ Fold {fold+1} - KS: {ks:.4f}, AUC: {auc:.4f}, F1: {f1:.4f}")

        ks_list.append(ks)
        auc_list.append(auc)
        f1_list.append(f1)
        model_list.append(model)

        test_prob = model.predict(dtest)
        test_preds += test_prob / n_splits

    # 平均交叉验证指标
    print("\n📊 平均交叉验证指标:")
    print(f"Mean KS  = {np.mean(ks_list):.4f}")
    print(f"Mean AUC = {np.mean(auc_list):.4f}")
    print(f"Mean F1  = {np.mean(f1_list):.4f}")

    # 测试集评估（如果有标签）
    if y_test is not None:
        ks, auc, f1 = evaluate_metrics(y_test, test_preds)
        print("\n🧪 测试集评估指标:")
        print(f"Test KS  = {ks:.4f}")
        print(f"Test AUC = {auc:.4f}")
        print(f"Test F1  = {f1:.4f}")

    return model_list, test_preds