import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

# 1. 生成模拟数据（替换为你的实际数据）
X, _ = make_blobs(n_samples=1000, centers=4, n_features=2, random_state=42)

# 2. 遍历K值计算SSE
sse = []
k_range = range(1, 11)  # 测试K从1到10

for k in k_range:
    kmeans = KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=42)
    kmeans.fit(X)
    sse.append(kmeans.inertia_)  # inertia_即SSE

# 3. 绘制手肘图
plt.figure(figsize=(10, 6))
plt.plot(k_range, sse, 'bo-', linewidth=2, markersize=8)
plt.title('Elbow Method for Optimal K')
plt.xlabel('Number of clusters (K)')
plt.ylabel('SSE (Inertia)')
plt.grid(True)
plt.xticks(k_range)
plt.show()

# 4. 计算SSE变化率（辅助识别拐点）
sse_diff = np.diff(sse)  # 一阶差分
sse_diff_ratio = [sse_diff[i] / sse_diff[i-1] if i>0 else 0 for i in range(len(sse_diff))]

# 打印变化率（观察下降速度突变点）
print("SSE变化率:", [f'{x:.2f}' for x in sse_diff_ratio])

cluster_features = [
    "LotArea",
    "TotalBsmtSF",
    "FirstFlrSF",
    "SecondFlrSF",
    "GrLivArea",
]


def cluster_labels(df, features, n_clusters=20):

    """ 
    # 1. 识别字符串列
    string_cols = result_df.select_dtypes(include=['object']).columns
    print("\n字符串列:", list(string_cols))
    result_total=pd.concat([result_df,result_df_test],axis=0)
    # 2. 为字符串列创建哑变量
    dummy_df_total = pd.get_dummies(result_total, columns=string_cols)
    # print("\n转换后的 DataFrame:")
    # print(dummy_df_total)

    from sklearn.ensemble import RandomForestClassifier
    #2. 模型选择（基于随机森林的特征重要性）
    clf = RandomForestClassifier()
    clf.fit(df3.drop(['target'], axis=1), df3['target'])
    importance = clf.feature_importances_
    importance = pd.DataFrame(importance, index=df3.drop(['target'], axis=1).columns, columns=["Importance"])
    importance = importance.sort_values(by='Importance', ascending=True)
    print(importance.sort_values(by='Importance', ascending=False))
    #导出相关系数大于阀值的变量
    tree_importance_select = importance[importance['Importance'] >0.0001].index.tolist()
    importance.to_csv("data_var_rf_importance.csv")

    #3.
    iv_df = toad.quality(df4, 'target', iv_only=True)
    # selected_features = iv_df[(iv_df['iv'] > 0.01) & (iv_df['iv'] < 0.8)].index.tolist()
    selected_features = iv_df[iv_df['iv'] > 0.01].index.tolist()
    # 计算WOE转换器
    transformer = toad.transform.WOETransformer()
    transformer.fit(
        combiner.transform(train_df),  # 用训练数据分箱结果
        train_df['target'],  # 目标变量
        exclude=['target']  # 排除目标列
    )

    # 保存规则（分箱器和转换器）
    with open('woe_rules.pkl', 'wb') as f:
        pickle.dump({'combiner': combiner, 'transformer': transformer}, f)

    # 4. 转换训练数据（演示）
    train_woe = transformer.transform(combiner.transform(train_df))
    from sklearn.metrics import roc_auc_score
    # 计算KS值
    fpr, tpr, thresholds = roc_curve(y_test, y_test_prob)
    ks_value = np.max(np.abs(tpr - fpr))

    # 计算AUC
    auc_value = roc_auc_score(y_test, y_test_prob)

    # 计算F1值（默认阈值0.5）
    y_pred = (y_test_prob >= 0.5).astype(int)
    f1 = f1_score(y_test, y_pred)

    print(f"KS值: {ks_value:.4f}")
    print(f"AUC: {auc_value:.4f}")
    print(f"F1值: {f1:.4f}")

    """ 



    X = df.copy()
    X_scaled = X.loc[:, features]
    X_scaled = (X_scaled - X_scaled.mean(axis=0)) / X_scaled.std(axis=0)
    kmeans = KMeans(n_clusters=n_clusters, n_init=50, random_state=0)
    X_new = pd.DataFrame()
    X_new["Cluster"] = kmeans.fit_predict(X_scaled)
    return X_new


def cluster_distance(df, features, n_clusters=20):
    X = df.copy()
    X_scaled = X.loc[:, features]
    X_scaled = (X_scaled - X_scaled.mean(axis=0)) / X_scaled.std(axis=0)
    kmeans = KMeans(n_clusters=20, n_init=50, random_state=0)
    X_cd = kmeans.fit_transform(X_scaled)
    # Label features and join to dataset
    X_cd = pd.DataFrame(
        X_cd, columns=[f"Centroid_{i}" for i in range(X_cd.shape[1])]
    )
    return X_cd
