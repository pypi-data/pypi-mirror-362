from autogluon.core.metrics import make_scorer
from sklearn.metrics import f1_score, roc_auc_score
from scipy.stats import ks_2samp
import numpy as np

from sklearn.metrics import f1_score, precision_recall_curve

def find_optimal_threshold(y_true, y_pred_proba):
    """通过PR曲线找到最大化F1的阈值"""
    precision, recall, thresholds = precision_recall_curve(y_true, y_pred_proba)
    f1_scores = 2 * (precision * recall) / (precision + recall + 1e-9)
    optimal_idx = np.argmax(f1_scores)
    optimal_threshold = thresholds[optimal_idx]
    return optimal_threshold

def weighted_metric(y_true, y_pred_proba, sample_weight=None, **kwargs):
    # 找到最佳F1阈值
    optimal_threshold = find_optimal_threshold(y_true, y_pred_proba)
    y_pred_class = (y_pred_proba > optimal_threshold).astype(int)
    f1 = f1_score(y_true, y_pred_class)
    
    # 其余部分保持不变
    try:
        auc = roc_auc_score(y_true, y_pred_proba)
    except ValueError:
        auc = 0.5
        
    pos_scores = y_pred_proba[y_true == 1]
    neg_scores = y_pred_proba[y_true == 0]
    if len(pos_scores) > 0 and len(neg_scores) > 0:
        ks = ks_2samp(pos_scores, neg_scores).statistic
    else:
        ks = 0.0
    
    return 0.4 * f1 + 0.3 * auc + 0.3 * ks

# 创建AutoGluon scorer
weighted_scorer = make_scorer(
    name='weighted_metric',
    score_func=weighted_metric,
    optimum=1,  # 最佳可能得分
    greater_is_better=True,  # 分数越高越好
    needs_proba=True  # 需要预测概率而不是类别
)