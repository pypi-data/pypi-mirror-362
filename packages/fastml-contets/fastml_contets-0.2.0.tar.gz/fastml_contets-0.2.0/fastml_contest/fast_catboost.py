import pandas as pd
import numpy as np
from catboost import CatBoostClassifier, Pool
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, roc_curve

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
    使用 CatBoost 进行 10 折交叉验证训练，并在测试集上预测。
    """
    # 准备数据
    X = train_df.drop(columns=[label_col])
    y = train_df[label_col].values
    X_test = test_df.drop(columns=[label_col], errors='ignore')
    y_test = test_df[label_col] if label_col in test_df.columns else None

    # 类别列转为字符串
    if cate_cols is None:
        cate_cols = X.select_dtypes(include='object').columns.tolist()
    for col in cate_cols:
        X[col] = X[col].astype(str)
        X_test[col] = X_test[col].astype(str)

    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

    test_preds = np.zeros(len(X_test))
    ks_list, auc_list, f1_list, model_list = [], [], [], []

    for fold, (train_idx, valid_idx) in enumerate(skf.split(X, y)):
        print(f"\n📦 Fold {fold + 1}")

        X_train, X_valid = X.iloc[train_idx], X.iloc[valid_idx]
        y_train, y_valid = y[train_idx], y[valid_idx]

        model = CatBoostClassifier(
            iterations=2000,
            loss_function=FocalLossObjective(),
            eval_metric='AUC',
            random_seed=42,
            learning_rate=0.1,
            depth=5,
            colsample_bylevel=0.8,
            bootstrap_type='Bayesian',
            early_stopping_rounds=100,
            verbose=100
        )

        model.fit(
            X_train, y_train,
            eval_set=(X_valid, y_valid),
            cat_features=cate_cols,
            use_best_model=True
        )

        # 验证集评估
        valid_prob = model.predict_proba(X_valid)[:, 1]
        ks, auc, f1 = evaluate_metrics(y_valid, valid_prob)
        print(f"✅ Fold {fold+1} - KS: {ks:.4f}, AUC: {auc:.4f}, F1: {f1:.4f}")

        ks_list.append(ks)
        auc_list.append(auc)
        f1_list.append(f1)
        model_list.append(model)

        # 测试集预测
        test_prob = model.predict_proba(X_test)[:, 1]
        test_preds += test_prob / n_splits

        # print(f"✅ Fold {fold+1}\n🧪 测试集评估指标:")
        # print(f"Test KS  = {test_ks:.4f}")
        # print(f"Test AUC = {test_auc:.4f}")
        # print(f"Test F1  = {test_f1:.4f}")
        # # === 计算自定义指标 ===
        # ks_metric = KsMetric()
        # custom_score, _ = ks_metric.evaluate([test_prob], y_test.values, None)

        # print(f"Test Custom Score = {custom_score:.4f}  # 0.4*F1 + 0.3*AUC + 0.3*KS")

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
