def do_flaml(X_train, y_train):
    """
        from flaml import AutoML
    automl = AutoML()
    automl_settings = {
        "time_budget": -1,
        "metric": 'roc_auc',
        "task": 'classification',
        "estimator_list":['lgbm', 'rf', 'catboost', 'xgboost',  'lrl1'],
            "sample": True,  # 启用采样
        "eval_method": 'holdout',  # 使用验证集代替交叉验证
        "split_ratio": 0.2,  # 更小的验证集比例
        "ensemble": True,  # 启用模型集成
        "hpo_method": 'cfo'  # 使用贝叶斯优化
    #"include_preprocess": True
    #    "verbose": 4  # 详细日志
    #**`skip_transform`** (bool, 默认值: False)
    # - 是否跳过 AutoML 内置的预处理（如缺失值填充、编码）。设为 `True` 可手动预处理数据
    }
    automl.fit(df.drop(['id','default'], axis=1), df['default'], **automl_settings)

    y_pred_proba = automl.predict_proba(X_test)[:,1]

    ##############2#################
    from flaml import AutoML
    automl = AutoML()
    X_train, y_train = load_iris(return_X_y=True)
    automl.fit(X_train, y_train)
    starting_points = automl.best_config_per_estimator
        
    new_automl = AutoML()
    new_automl.fit(X_train, y_train, starting_points=starting_points)
    """

    return True
