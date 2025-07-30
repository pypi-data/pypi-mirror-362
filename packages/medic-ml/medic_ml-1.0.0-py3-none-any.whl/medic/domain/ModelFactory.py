import importlib
import os
from typing import List, Union

import sklearn

from .MetaboModel import MetaboModel
from ..conf.SupportedModels import LEARN_CONFIG
from ..service import Utils


# TODO: deals with methods names' that are used in Results (for example), how to retrieve features/importance/etc
class ModelFactory:
    def __init__(self):
        self._SEED = 42

    def create_supported_models(self, CV_type = "GS") -> dict:
        """
        CV_type: for now supports GS (gridsearch) and RS (randomsearch), the value will adapt the retrieval of the
        hyperparameter grid to explore.
        """
        supported_models = {}

        if CV_type == "GS":
            parameter_grid_value = "GridSearch"
        elif CV_type == "RS":
            parameter_grid_value = "RandomSearch"
        else:
            raise ValueError(f"Supported values are 'GS' and 'RS', given value is {CV_type}")

        for model_name, model_configuration in LEARN_CONFIG.items():
            supported_models[model_name] = MetaboModel(
                model_configuration["function"], model_configuration["ParamGrid"][parameter_grid_value],
                model_configuration["importance_attribute"]
            )
        return supported_models

    def create_custom_model(self, model_name: str, needed_imports: str, params_grid: dict,
                            importance_attribute: str = Utils.DEFAULT_IMPORTANCE_ATTRIBUTE) -> MetaboModel:
        """
        Create a custom model (not included by default) for the MeDIC to use
        """
        imports_list = needed_imports.split(".")
        model = Utils.get_model_from_import(imports_list, model_name)
        return MetaboModel(model, params_grid, importance_attribute)
