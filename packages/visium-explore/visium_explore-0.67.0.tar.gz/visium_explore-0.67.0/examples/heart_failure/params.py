"""Parameters for the heart failure DVC pipeline."""


class SplitParams:
    """Parameters for the split stage of the heart failure DVC pipeline."""

    SEED = 42
    TEST_PROPORTION = 0.25


class TrainEvalParams:
    """Parameters for the train and eval stages of the heart failure DVC pipeline."""

    model_config = {
        "LogisticRegression": {
            "model_import": "sklearn.linear_model.LogisticRegression",
            "seed": 42,
            "model_file": "log_reg.pkl",
            "metrics_file": "eval_metrics_log_reg.json",
        },
        "DecisionTreeClassifier": {
            "model_import": "sklearn.tree.DecisionTreeClassifier",
            "max_depth": 10,
            "model_file": "decision_tree.pkl",
            "metrics_file": "eval_metrics_decision_tree.json",
        },
        "KNeighborsClassifier": {
            "model_import": "sklearn.neighbors.KNeighborsClassifier",
            "n_neighbors": 8,
            "model_file": "knn.pkl",
            "metrics_file": "eval_metrics_knn.json",
        },
    }
