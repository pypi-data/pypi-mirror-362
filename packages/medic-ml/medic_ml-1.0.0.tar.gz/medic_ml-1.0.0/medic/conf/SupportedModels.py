import numpy as np
from pyscm.scm import SetCoveringMachineClassifier
from randomscm.randomscm import RandomScmClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

LEARN_CONFIG = {
    "DecisionTree": {
        "function": DecisionTreeClassifier,
        "ParamGrid": {
            "RandomSearch": {
                "max_depth": np.arange(2, 9, step=1, dtype=int),
                "min_samples_split": np.arange(2, 20, step=2, dtype=int),
                "max_features": ["sqrt", "log2"],
            },
            "GridSearch": {
                "max_depth": [2, 3, 4, 5, 6, 7],
                "min_samples_split": [2, 4, 6, 8, 10],
                "max_features": ["sqrt", "log2"],
                "class_weight": ["balanced"]
            }
        },
        "importance_attribute": "feature_importances_",
    },
    "RandomForest": {
        "function": RandomForestClassifier,
        "ParamGrid": {
            "RandomSearch" : {
                "n_estimators": np.arange(5, 300, step=10, dtype=int),
                "max_depth": np.arange(2, 6, step=1, dtype=int), #[1, 2, 3, 4, 5],
                "min_samples_split": np.arange(2, 20, step=2, dtype=int),
            },
            "GridSearch" : {
                "n_estimators": [5, 10, 30, 50, 70, 100, 200],
                "max_depth": [2, 3, 4, 5],
                "min_samples_split": [2, 4, 6, 8, 10],
            }
        },
        "importance_attribute": "feature_importances_",
    },
    "SCM": {
        "function": SetCoveringMachineClassifier,
        "ParamGrid": {
            "RandomSearch" : {
                "p": np.logspace(-2, 2, base=10, num=30),
                "max_rules": np.arange(1, 6, 1, dtype=int),
                "model_type": ["conjunction", "disjunction"],
            },
            "GridSearch" : {
                "p": np.logspace(-2, 2, base=10, num=7), #[0.01, 0.1, 1, 10],
                "max_rules": [1, 2, 3, 4, 5],
                "model_type": ["conjunction", "disjunction"],
            }
        },
        "importance_attribute": "feature_importances_",
    },
    "RandomSCM": {
        "function": RandomScmClassifier,
        "ParamGrid": {
            "RandomSearch" : {
                "p": np.logspace(-2, 2, base=10, num=30),
                "n_estimators": np.arange(5, 200, step=10, dtype=int),
                "model_type": ["conjunction", "disjunction"],
            },
            "GridSearch" : {
                "p": np.logspace(-2, 2, base=10, num=5),
                "n_estimators": [5, 10, 30, 50, 70, 100, 200],
                "model_type": ["conjunction", "disjunction"],
            },
        },
        "importance_attribute": "feature_importances_",
    },
}
