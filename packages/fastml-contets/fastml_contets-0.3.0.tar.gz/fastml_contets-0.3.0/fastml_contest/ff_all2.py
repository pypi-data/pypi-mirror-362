def ff_all2():
    """
    import pandas as pd
    import numpy as np

    # 设置显示所有行
    pd.set_option('display.max_rows', 30)
    pd.set_option('display.max_columns', 100)

    # matplotlib和seaborn用于画图 
    import matplotlib.pyplot as plt
    import seaborn as sns
    color = sns.color_palette()
    %matplotlib inline

    import warnings
    warnings.filterwarnings("ignore")

    feature_string = df_first.columns[df_first.dtypes == 'object'].to_list()
    feature_float = df_first.columns[df_first.dtypes == 'float64'].to_list()
    feature_date = df_first.columns[df_first.dtypes == 'datetime64[ns]'].to_list()
    feature_id = ["id"]
    feature_enum = ["label"]
    df_first[feature_date] = df_first[feature_date].apply(lambda x:x.astype(str))
    df_first["month_float"] = df_first[feature_date].apply(lambda x:x.str.slice(5,7).astype(float)*1.0)
    df_first["month_string"] = df_first[feature_date].apply(lambda x:x.str.slice(5,7))
    feature_string = [x for x in feature_string + ["month_string"] if x not in feature_id + feature_enum]
    feature_float = [x for x in feature_float + ["month_float"] if x not in feature_id + feature_enum]

    _ = df_first[feature_float].apply(lambda x:x.isna().sum())
    float_copy = _.index[_!=0]
    feature_float1 = [x+"_1" for x in feature_float if x in float_copy]
    feature_float2 = [x+"_2" for x in feature_float if x in float_copy]
    df_first[feature_float1] = df_first[float_copy]
    df_first[feature_float2] = df_first[float_copy]

    from sklearn.base import BaseEstimator,TransformerMixin
    from sklearn.experimental import enable_iterative_imputer
    from sklearn.impute import SimpleImputer,KNNImputer,IterativeImputer
    from sklearn.preprocessing import RobustScaler,OneHotEncoder,PolynomialFeatures
    from sklearn.pipeline import Pipeline
    from sklearn.compose import ColumnTransformer

    class DistributionTransformer(BaseEstimator,TransformerMixin):
        def __init__(self):
            pass

        def fit(self,array,y=None):
            return self

        def transform(self,array,y=None):
            return np.where(array>=0,np.log(array+1),-np.log(-array+1))

    def feature_pipe_init():
        float_impute_cons = Pipeline([('float_impute_cons',SimpleImputer(strategy='constant',fill_value=0))])
        float_impute_mean = Pipeline([('float_impute_mean',SimpleImputer(strategy='mean'))])
        #float_impute_model = Pipeline([('float_impute_model',IterativeImputer(estimator=RandomForestRegressor(n_estimators=5,verbose=2),max_iter=3,verbose=2))])
        float_impute = ColumnTransformer([('float_impute_cons',float_impute_cons,feature_float),
                                      ('float_impute_mean',float_impute_mean,feature_float1)])
        float_pipe = Pipeline([('float_impute',float_impute),
                              ('float_dist',DistributionTransformer()),
                              ('float_scaler',RobustScaler())])
        string_pipe = Pipeline([('string_impute',SimpleImputer(strategy='constant',fill_value='N')),
                               ('string_onehot',OneHotEncoder(sparse=False,handle_unknown='ignore',drop='first'))])
        feature_processor = ColumnTransformer([('float_pipe',float_pipe,feature_float+feature_float1),
                                      ('string_pipe',string_pipe,feature_string)])
        pipe = Pipeline([('feature_processor',feature_processor)])
        return pipe

    from sklearn.feature_selection import SelectKBest
    from sklearn.feature_selection import SelectFromModel
    from sklearn.feature_selection import f_classif,mutual_info_classif
    from sklearn.ensemble import RandomForestClassifier,RandomForestRegressor

    def select_pipe_init():
        pipe = Pipeline([('feature_select',SelectFromModel(RandomForestClassifier(n_estimators=20),threshold='1.5*mean'))])
        return pipe

    from sklearn.neural_network import MLPClassifier
    from sklearn.neighbors import KNeighborsClassifier
    from xgboost import XGBClassifier
    from catboost import CatBoostClassifier, Pool
    from catboost.metrics import BuiltinMetric
    from sklearn.ensemble import HistGradientBoostingClassifier

    def model_pipe_init():
        pipe = Pipeline([('model',HistGradientBoostingClassifier())])
        return pipe

    from sklearn.model_selection import GridSearchCV
    from sklearn.metrics import roc_auc_score,accuracy_score,roc_curve,make_scorer,f1_score,precision_recall_curve

    def get_model():
        feature_pipe = feature_pipe_init()
        select_pipe = select_pipe_init()
        model_pipe = model_pipe_init()
        pipe = Pipeline([feature_pipe.steps[0],select_pipe.steps[0],model_pipe.steps[0]])
        return pipe

    def ks_score(y_ture, y_pred):
        fpr, tpr, thresholds = roc_curve(y_ture, y_pred)
        return max(tpr - fpr)

    def result(y_test,y_pred,y_score):
        accuracy = accuracy_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_score)
        fpr, tpr, thresholds = roc_curve(y_test, y_score)
        print(accuracy, auc, max(tpr - fpr))
        return max(tpr - fpr)

    import itertools
    import time
    from copy import deepcopy

    def ks_metric(y_pred, y_ture,weights=None):
        fpr, tpr, thresholds = roc_curve(y_ture, y_pred)
        return max(tpr - fpr),True

    class KsMetric:
        def is_max_optimal(self):
            return True

        def evaluate(self,approxes,target,weight):
                # 获取不同阈值下的精确率、召回率
            precisions, recalls, thresholds = precision_recall_curve(target, approxes[0])

            # 计算每个阈值对应的F1分数
            f1_scores = 2 * (precisions[:-1] * recalls[:-1]) / (precisions[:-1] + recalls[:-1] + 1e-6)  # 避免除0
            best_idx = np.argmax(f1_scores)  # F1最大值的索引
            best_threshold = thresholds[best_idx]
            best_f1 = f1_scores[best_idx]
            fpr, tpr, thresholds = roc_curve(target, approxes[0])
            return 0.4*best_f1 + 0.3*(roc_auc_score(target,approxes[0])+max(tpr-fpr)),1

        def get_final_error(self,error,weight):
            return error

    df_first = df_first[feature_id+feature_enum+feature_string+feature_float+feature_float1+feature_float2]
    df_second = df_second[feature_id+feature_enum+feature_string+feature_float+feature_float1+feature_float2]

    def feature_pipe_init3():
        float_impute_cons = Pipeline([('float_impute_cons',SimpleImputer(strategy='constant',fill_value=0))])
        float_impute_mean = Pipeline([('float_impute_mean',SimpleImputer(strategy='mean'))])
        float_impute_model = Pipeline([('float_impute_model',IterativeImputer(estimator=RandomForestRegressor(n_estimators=20,verbose=2),max_iter=1,verbose=2))])
        float_impute = ColumnTransformer([('float_impute_cons',float_impute_cons,feature_float),
                                      ('float_impute_mean',float_impute_mean,feature_float1),
                                      ('float_impute_model',float_impute_model,feature_float2)])
        float_pipe = Pipeline([('float_impute',float_impute),
                              ('float_dist',DistributionTransformer()),
                              ('float_scaler',RobustScaler())])
        string_pipe = Pipeline([('string_impute',SimpleImputer(strategy='constant',fill_value='N')),
                               ('string_onehot',OneHotEncoder(sparse=False,handle_unknown='ignore',drop='first'))])
        feature_processor = ColumnTransformer([('float_pipe',float_pipe,feature_float+feature_float1+feature_float2),
                                      ('string_pipe',string_pipe,feature_string)])
        pipe = Pipeline([('feature_processor',feature_processor)])
        return pipe

    pipe = Pipeline([feature_pipe_init().steps[0],select_pipe_init().steps[0]])
    data = pd.concat([df_first,df_second],ignore_index=True)

    #pipe_para = {'feature_select':SelectFromModel(RandomForestClassifier(n_estimators=20),threshold='2*mean')}
    pipe_para = {'feature_select':'passthrough'}
    pipe.set_params(**pipe_para)
    data_deal = pipe.fit_transform(data,data.label)

    model = CatBoostClassifier(
        verbose=True,
        loss_function = FocalLossObjective(),
        eval_metric=KsMetric(),
        iterations=3000,
        learning_rate=0.03,
        depth=8,
        max_ctr_complexity=5,
        l2_leaf_reg=10,
        subsample=0.8,
        colsample_bylevel=0.8,
        early_stopping_rounds=200
    )
    model.fit(
        df_first_deal,df_first.label,
        eval_set = (df_second_deal,df_second.label),
        verbose = 50,
        plot=True
    )

    pipe_para = {'feature_select':SelectFromModel(RandomForestClassifier(n_estimators=20),threshold='mean')}
    #pipe_para = {'feature_select':'passthrough','feature_processor__float_pipe__float_dist':'passthrough'}
    #pipe_para = {'feature_select':SelectKBest(f_classif,k=180)}
    pipe.set_params(**pipe_para)
    data_deal = pipe.fit_transform(data,data.label)

    onehot_names = pipe.named_steps['feature_processor'].named_transformers_['string_pipe'].named_steps['string_onehot'].get_feature_names_out(input_features=feature_string).tolist()

    select_cols = pipe.named_steps['feature_select'].get_support()
    select_names = np.array(feature_float+feature_float1+onehot_names)[select_cols].tolist()

    pd.DataFrame(model.get_feature_importance(),columns=["value"],index=select_names).to_csv("C:\\Users\\Administrator\\Documents\\Anno 1800\\stamps\\value.csv")

    predict = df_second.label
    prob = model.predict_proba(df_second_deal)[:, 1].tolist()
    real = df_second.label
    result(real, predict, prob)

    def find_best_threshold(y_true, y_prob):
        # 获取不同阈值下的精确率、召回率
        precisions, recalls, thresholds = precision_recall_curve(y_true, y_prob)

        # 计算每个阈值对应的F1分数
        f1_scores = 2 * (precisions[:-1] * recalls[:-1]) / (precisions[:-1] + recalls[:-1] + 1e-6)  # 避免除0
        best_idx = np.argmax(f1_scores)  # F1最大值的索引
        best_threshold = thresholds[best_idx]
        best_f1 = f1_scores[best_idx]

        return best_threshold, best_f1

    best_thresh, best_f1 = find_best_threshold(real, prob)
    print(f"最佳阈值: {best_thresh:.32f}, 最大F1分数: {best_f1:.32f}")

    pipe = Pipeline([feature_pipe_init().steps[0],select_pipe_init().steps[0]])
    data = pd.concat([df_first,df_second],ignore_index=True)

    pipe_para = {'feature_select':SelectFromModel(RandomForestClassifier(n_estimators=20),threshold='mean')}
    #pipe_para = {'feature_select':'passthrough','feature_processor__float_pipe__float_dist':'passthrough'}
    #pipe_para = {'feature_select':SelectKBest(f_classif,k=180)}
    pipe.set_params(**pipe_para)
    data_deal = pipe.fit_transform(data,data.label)

    pipe = Pipeline([('model',CatBoostClassifier(
        verbose=True,
        loss_function = FocalLossObjective(),
        eval_metric=KsMetric(),
        iterations=1000,
        early_stopping_rounds=50
    ))])
    para = [{'model__learning_rate':[0.02,0.03],
        'model__depth':[6,8],
        'model__max_ctr_complexity':[3,5],
        'model__l2_leaf_reg':[6,10],
        'model__subsample':[0.6,0.8],
        'model__colsample_bylevel':[0.6,0.8]}]

    def evaluate(target,approxes):
            # 获取不同阈值下的精确率、召回率
        precisions, recalls, thresholds = precision_recall_curve(target, approxes)

        # 计算每个阈值对应的F1分数
        f1_scores = 2 * (precisions[:-1] * recalls[:-1]) / (precisions[:-1] + recalls[:-1] + 1e-6)  # 避免除0
        best_idx = np.argmax(f1_scores)  # F1最大值的索引
        best_threshold = thresholds[best_idx]
        best_f1 = f1_scores[best_idx]
        fpr, tpr, thresholds = roc_curve(target, approxes)
        return 0.4*best_f1 + 0.3*(roc_auc_score(target,approxes)+max(tpr-fpr)),[1 if x > best_threshold else 0 for x in approxes]

    def result(target,y_pred,approxes):
        precisions, recalls, thresholds = precision_recall_curve(target, approxes)

        # 计算每个阈值对应的F1分数
        f1_scores = 2 * (precisions[:-1] * recalls[:-1]) / (precisions[:-1] + recalls[:-1] + 1e-6)  # 避免除0
        best_idx = np.argmax(f1_scores)  # F1最大值的索引
        best_threshold = thresholds[best_idx]
        best_f1 = f1_scores[best_idx]
        fpr, tpr, thresholds = roc_curve(target, approxes)
        print(best_f1, roc_auc_score(target,approxes), max(tpr-fpr))

    from sklearn.base import clone

    def model_iter(train,test,pipe0,para):
        predict = []
        prob = []
        real = []
        grid_list = []
        for i in [1]:
            print(i)
            data_train = train
            data_test = test
            real_s = df_second.label.to_list()
            prob_m = []
            score_m = 0
            predict_m = []
            para_m = {}
            model_m = {}
            for d in para:
                combinations = list(itertools.product(*d.values()))
                combinations_as_dicts = [dict(zip(d.keys(),comb)) for comb in combinations]
                for comb in combinations_as_dicts:
                    print('---START---')
                    start_time = time.time()
                    pipe=clone(pipe0)
                    pipe.set_params(**comb)
                    pipe.fit(
        data_train,df_first.label,
        model__eval_set = (data_test,df_second.label),
        model__verbose = 50
    )
                    prob_s = pipe.predict_proba(data_test)[:, 1].tolist()
                    score_s,predict_s = evaluate(real_s, prob_s)
                    end_time = time.time()
                    print('---TIME---')
                    print(end_time - start_time)
                    for csk,csv in comb.items():
                        print(csk)
                        print(csv)
                    print(score_s)
                    if score_s > score_m:
                        score_m = score_s
                        predict_m = predict_s
                        prob_m = prob_s
                        para_m = comb
                        model_m = deepcopy(pipe)
            print('----------BEST:----------')
            for cmk,cmv in para_m.items():
                print(cmk)
                print(cmv)
            print(score_m)
            grid_list = grid_list + [model_m]
            predict = predict + predict_m
            prob = prob + prob_m
            real = real + real_s
        result(real, predict, prob)
        return grid_list

    model_iter(df_first_deal,df_second_deal,pipe,para)
    """
    return True