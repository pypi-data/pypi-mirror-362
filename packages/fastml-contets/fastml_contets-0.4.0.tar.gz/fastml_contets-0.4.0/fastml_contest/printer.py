def print_hello():
    """
    以下是更详细的 CatBoost、LightGBM 和 XGBoost 参数解析，按功能分类展开，并附示例说明：

1. CatBoost 参数详解
核心参数
iterations

作用：决策树的总数量（即训练轮数）。

默认值：1000

注意事项：实际迭代可能因早停而减少。

learning_rate

作用：控制梯度下降的步长，影响模型收敛速度和精度。

默认值：0.03

调参建议：小学习率需配合更大的iterations。

depth

作用：单棵树的深度，直接影响模型复杂度。

默认值：6

注意：CatBoost 的对称树结构可能比其他算法更耗资源。

loss_function

可选值：

分类：Logloss（二分类）、MultiClass（多分类）

回归：RMSE、MAE、Quantile

示例：loss_function='MultiClass'

训练控制
early_stopping_rounds

作用：验证集指标在指定轮数内未提升时停止训练。

依赖：需通过eval_set提供验证集。

示例：early_stopping_rounds=50

eval_metric

常用指标：

分类：Accuracy、AUC、F1

回归：RMSE、R2

注意：与loss_function不同，仅用于监控不影响训练。

正则化与鲁棒性
l2_leaf_reg

作用：L2正则化系数，惩罚叶子权重的平方和。

默认值：3.0

调参建议：值越大模型越保守。

random_strength

作用：在分裂评分中添加随机噪声，增强多样性。

默认值：1.0

适用场景：防止过拟合或数据噪声较多时。

border_count

作用：数值特征分桶的数量，影响训练速度和精度。

默认值：254（GPU）或128（CPU）

类别特征处理
cat_features

作用：指定类别特征的列索引，CatBoost会自动编码。

示例：cat_features=[0, 2] 表示第0列和第2列为类别特征。

优势：无需手动编码，支持高基数类别。

2. LightGBM 参数详解
核心参数
boosting_type

可选值：

gbdt：传统的梯度提升树（默认）

dart：引入Dropout防止过拟合

goss：基于梯度的单边采样，加速训练

示例：boosting_type='dart'

num_leaves

作用：每棵树的最大叶子数，直接影响模型复杂度。

默认值：31

注意：需与max_depth协调（num_leaves <= 2^max_depth）。

objective

常用选项：

分类：binary、multiclass（需指定num_class）

回归：regression、regression_l1

排序：lambdarank

训练控制
n_estimators

作用：树的数量，与learning_rate共同控制训练轮次。

默认值：100

调参建议：大学习率可减少此值。

early_stopping_rounds

依赖：需通过eval_set和eval_metric配合使用。

示例：

python
model.fit(X_train, y_train, eval_set=[(X_val, y_val)], early_stopping_rounds=20)
正则化与采样
min_child_samples

作用：叶子节点所需的最小样本数，防止过拟合小数据。

默认值：20

调参建议：数据量小时增大此值。

feature_fraction

作用：每轮随机选择特征的比例（类似随机森林）。

默认值：1.0（不采样）

示例：feature_fraction=0.8 表示使用80%特征。

bagging_fraction

作用：样本采样比例（需bagging_freq >0启用）。

默认值：1.0

注意：与goss不兼容。

类别特征处理
categorical_feature

指定方式：列名列表或索引列表。

示例：categorical_feature=['category_col', 1]

内部处理：LightGBM使用特殊的分割算法（按直方图统计）。

3. XGBoost 参数详解
核心参数
booster

可选值：

gbtree：基于树的模型（默认）

gblinear：线性模型

dart：引入Dropout的树模型

eta（等价于learning_rate）

作用：收缩每棵树的权重，防止过拟合。

默认值：0.3

调参范围：通常设为0.01~0.2。

objective

常用选项：

二分类：binary:logistic

多分类：multi:softmax（需指定num_class）

回归：reg:squarederror

训练控制
max_depth

作用：树的最大深度，控制模型复杂度。

默认值：6

注意：与LightGBM的num_leaves不同，XGBoost严格限制深度。

subsample

作用：每轮训练使用的样本比例（行采样）。

默认值：1.0

示例：subsample=0.8 表示使用80%样本。

正则化与优化
gamma

作用：分裂所需的最小损失减少量（越大模型越保守）。

默认值：0

调参建议：常用范围0.1~0.5。

colsample_bytree

作用：每棵树列采样的比例。

默认值：1.0

扩展参数：

colsample_bylevel：每层级的列采样

colsample_bynode：每个节点的列采样

类别特征处理
传统方法：需手动编码（如One-Hot或Label Encoding）。

实验性支持：

设置enable_categorical=True（需数据为pandas.Categorical类型）。

示例：

python
X_train['category_col'] = X_train['category_col'].astype('category')
model = XGBClassifier(enable_categorical=True)
关键差异总结
类别特征处理：

CatBoost原生支持，无需预处理；

LightGBM需指定列但自动优化分割；

XGBoost依赖手动编码或实验性功能。

树结构控制：

CatBoost的depth对称树可能更耗内存；

LightGBM通过num_leaves灵活控制叶子数；

XGBoost的max_depth严格限制深度。

速度优化：

LightGBM的goss和histogram优化最快；

XGBoost的gpu_hist支持GPU加速；

CatBoost在类别特征多时效率更高。

示例调参片段（LightGBM）：
    """
    print("hello?????")