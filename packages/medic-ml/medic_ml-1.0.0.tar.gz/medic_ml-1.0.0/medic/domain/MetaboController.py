import os
import pickle
from typing import Generator, Tuple, Union

import pandas as pd

from . import MetaboExperiment
from .MetaboExperimentDTO import MetaboExperimentDTO
from .Results import *
from ..service import init_logger

ROOT_PATH = os.path.dirname(__file__)
DUMP_PATH = os.path.join(ROOT_PATH, os.path.join("dumps", "splits"))


class MetaboController:
    """
    Bottleneck class to interface between backend and frontend
    """
    def __init__(self, metabo_experiment: MetaboExperiment = None):
        self._logger = init_logger()
        if metabo_experiment is None:
            self._metabo_experiment = MetaboExperiment()
        else:
            self._metabo_experiment = metabo_experiment

    def set_metadata(self, filename: str, data=None, from_base64=True) -> None:
        """
        Set the metadata informations for the experiment
        filename: the filename of metadata
        data: matrix of information contained in the file
        from_base64: specify encoding
        """
        self._metabo_experiment.set_metadata_with_dataframe(filename=filename, data=data, from_base64=from_base64)

    def set_data_matrix_from_path(self, path_data_matrix, data=None, from_base64=True):
        """
        Set the data from file for the experiment
        path_data_matrix: filename or path of the file
        data: matrix of data
        from_base64: specify encoding
        """
        return self._metabo_experiment.set_data_matrix(path_data_matrix, data=data, from_base64=from_base64)

    def get_metadata_columns(self) -> list:
        """
        Retrieve the names of the columns in the metadata matrix
        """
        return self._metabo_experiment.get_metadata_columns()

    def get_unique_targets(self) -> list:
        """
        Retrieve a list of unique targets by applying a "set()" function to the complete list of targets.
        """
        return self._metabo_experiment.get_unique_targets()

    def add_classification_design(self, classes_design: dict):
        """
        add an classification design to the experience
        classes_design: which target.s against which for the prediction, and the names (classes) of the groups of target.s
        """
        self._metabo_experiment.add_classification_design(classes_design)

    def get_classification_designs(self):
        """
        Retrieve all classification designs for an experience.
        """
        return self._metabo_experiment.get_classification_designs()

    def all_classification_designs_names(self) -> Generator[Tuple[str, str], None, None]:
        """
        Retrieve all classification designs names for an experience.
        """
        return self._metabo_experiment.all_classification_designs_names()

    def get_all_classification_designs_names(self) -> List[Tuple[str, str]]:
        """
        Retrieve a list of classification designs names for an experience.
        """
        return list(self._metabo_experiment.all_classification_designs_names())

    def reset_classification_designs(self):
        """
        Delete all existing classification designs.
        """
        self._metabo_experiment.reset_classification_designs()

    def remove_classification_design(self, name: str):
        """
        !!! --- NOT USED --- !!!
        Remove an classification design
        """
        self._metabo_experiment.remove_classification_design(name)

    def get_samples_id_from_splits(self, nbr_split_list, design):
        """
        !!! --- NOT USED --- !!!
        Retrieve sample identification in each split from file
        nbr_split_list: nbr of splits
        design:
        """
        samples_list = []
        for s in nbr_split_list:
            with open(os.path.join(DUMP_PATH, design + "_split_{}.p".format(s)), "rb") as split_file:
                samples_list.append(pickle.load(split_file)[:2])  # append list of X_train & X_test samples names
        return samples_list

    def set_id_column(self, id_column: str):
        """
        Set the id_column attribute of the MetaData object
        It is the column in the metadata used to have a unique id for each line/item/sample
        id_column: string of the name of the column
        """
        self._metabo_experiment.set_id_column(id_column)

    def validate_id_column(self) -> bool:
        """
        Ensure all values in the data index column (unique_ids) are in the the metadata id_column
        """
        return self._metabo_experiment.validate_id_column()

    def set_selected_models(self, selected_models: list):
        """
        Set the self._selected_models attribute of MetaboExperiment with the list given in argument
        and for each Classification Design object initialize basics of Results instances
        selected_models: list of models to run during the experiment
        """
        self._metabo_experiment.set_selected_models(selected_models)

    def learn(self):  # TODO: Come back to put this function in the diagram, suspect its to big for now
        self._metabo_experiment.learn()

    def get_results(self, design_name: str, algo: str):
        """
        Retrieve the results of a specific algorithm for a specific classification design
        design_name: classification design's name
        algo: specific algo for which we want the results
        """
        return self._metabo_experiment.classification_designs[design_name].results[algo].results

    def get_all_results(self):
        """
        Retrieve, for each classification design that is done, the results dict corresponding
        """
        return self._metabo_experiment.get_all_updated_results()

    def add_custom_model(self, model_name: str, needed_imports: str, params_grid: dict, importance_attribute: str):
        """
        Add the information needed to run a custom model
        model_name: the name of the model
        needed_imports: the modules needed to run this model
        params_grid: the hyperparameters grid with which hyperparameters to test and for which values
        importance_attribute: the attribute of the model to use to measure the importance of features
        """
        self._metabo_experiment.add_custom_model(model_name, needed_imports, params_grid, importance_attribute)

    def get_all_algos_names(self) -> list:
        """
        Retrieve the list of names from default (supported) models and custom models
        """
        ret = self._metabo_experiment.get_all_algos_names()
        self._logger.info(f"get_all_algos_names: {ret}")
        return ret

    def set_cv_type(self, cv_type: str):
        """
        Set the type of Cross-Validation (cv) for the experiment
        """
        self._metabo_experiment.set_cv_type(cv_type)

    def get_cv_types(self) -> List[str]:
        """
        Retrieve the dict of possible cross-validation types supported by the MeDIC
        """
        return self._metabo_experiment.get_cv_types()

    def get_selected_cv_type(self) -> str:
        """
        Return the type of CV selected for this experiment
        """
        return self._metabo_experiment.get_selected_cv_type()

    def generate_save(self) -> MetaboExperimentDTO:
        """
        Return an object MetaboExperimentDTO
        (which is a holder of some MetaboExperiment attributes)
        """
        return self._metabo_experiment.generate_save()

    def is_save_safe(self, saved_metabo_experiment_dto: MetaboExperimentDTO) -> bool:
        """
        Verify that the hash from the saved MetaboExperimentDTO is the same from the current object
        """
        return self._metabo_experiment.is_save_safe(saved_metabo_experiment_dto)

    def full_restore(self, saved_metabo_experiment_dto: MetaboExperimentDTO):
        """
        Restore an experiment from a saving (always? from file)
        """
        self._metabo_experiment.full_restore(saved_metabo_experiment_dto)

    def partial_restore(self, saved_metabo_experiment_dto: MetaboExperimentDTO, filename_data: str, filename_metadata: str,
                        data=None, from_base64_data: bool = True, metadata=None, from_base64_metadata=True,):
        """
        Restore only the parameters of an experiment
        It allows the use of identical parameters for different sets of data and metadata
        """
        self._metabo_experiment.partial_restore(saved_metabo_experiment_dto, filename_data, filename_metadata, data,
                                                from_base64_data, metadata, from_base64_metadata,)

    def load_results(self, saved_metabo_experiment_dto: MetaboExperimentDTO):
        """
        Init a new experiment (new metadata and data_matrix) and load saved results
        """
        self._metabo_experiment.load_results(saved_metabo_experiment_dto)

    def get_target_column(self) -> str:
        """
        Retrieve the _target_column attribute of metadata
        """
        return self._metabo_experiment.get_target_column()

    def get_id_column(self) -> str:
        """
        Retrieve the _id_column attribute of metadata
        """
        return self._metabo_experiment.get_id_column()

    def set_number_of_splits(self, number_of_splits: int):
        """
        Set the value of the MetaboExpe attribute _number_of_splits
        """
        self._metabo_experiment.set_number_of_splits(number_of_splits)

    def get_number_of_splits(self) -> int:
        """
        Retrieve the value of the attribute _number_of_splits
        """
        return self._metabo_experiment.get_number_of_splits()

    def set_train_test_proportion(self, train_test_proportion: float):
        """
        Set the value of the MetaboExpe attribute _train_test_proportion
        """
        self._metabo_experiment.set_train_test_proportion(train_test_proportion)

    def get_train_test_proportion(self) -> float:
        """
        Retrieve the value of the attribute _train_test_proportion
        """
        return self._metabo_experiment.get_train_test_proportion()

    def create_splits(self) -> None:
        """
        Check that Experiment parameters are set and then : create an instance of SplitGroup for each classification Design
        (The init of SplitGroup triggers the _compute_splits function)
        If test_split_seed is provided, then only this test split seed is computed.
        """
        self._metabo_experiment.create_splits()

    def create_test_split_from_seed(self, test_split_seed: int) -> None:
        """
        Check that Experiment parameters are set and then : create an instance of SplitGroup
        having one test split from provided seed for each classification Design
        (The init of SplitGroup triggers the _compute_splits function)
        """
        self._metabo_experiment.create_splits(test_split_seed)

    def get_selected_models(self) -> List[str]:
        """
        Retrieve the name of the selected models to use for the experiment
        """
        return self._metabo_experiment.get_selected_models()

    def is_progenesis_data(self) -> bool:
        """
        Return the bool indicating if the data given is of the progenesis format
        """
        return self._metabo_experiment.is_progenesis_data()

    def get_pairing_group_column(self) -> str:
        """
        Retrieve the name of the column to use for pairing the samples
        """
        return self._metabo_experiment.get_pairing_group_column()

    def set_pairing_group_column(self, pairing_group_column: str):
        """
        Set the value of the MetaboExpe attribute _pairing_group_column
        """
        self._metabo_experiment.set_pairing_group_column(pairing_group_column)

    def is_data_raw(self) -> Union[bool, None]:
        """
        return the bool indicating to use either raw or normalized data
        """
        return self._metabo_experiment.is_data_raw()

    def set_raw_use_for_data(self, use_raw_data: bool):
        """
        Set the bool value of whether to use the raw data from a progenesis matrix or the normalized data
        """
        self._metabo_experiment.set_raw_use_for_data(use_raw_data)

    def get_data_matrix_remove_rt(self) -> bool:
        """
        return the value of the _remove_rt attribute
        (if true, remove the features detected before 1 minute of Retention Time)
        """
        return self._metabo_experiment.get_data_matrix_remove_rt()

    def set_data_matrix_remove_rt(self, remove_rt: bool):
        """
        set the value of the _remove_rt attribute
        (if true, remove the features detected before 1 minute of Retention Time)
        """
        self._metabo_experiment.set_data_matrix_remove_rt(remove_rt)

    def get_cv_folds(self) -> int:
        """
        Return the attribute of MetaboExperiment of the number of Cross Validation folds
        Default is 5
        """
        return self._metabo_experiment.get_cv_folds()

    def set_cv_folds(self, cv_folds: int):
        """
        Set the number of Cross Validation folds, must be >=2
        """
        self._metabo_experiment.set_cv_folds(cv_folds)

    def update_classification_designs_with_selected_models(self):
        self._metabo_experiment.update_classification_designs_with_selected_models()

    def is_the_data_matrix_corresponding(self, data: str) -> bool:
        return self._metabo_experiment.is_the_data_matrix_corresponding(data)

    def is_the_metadata_corresponding(self, metadata: str) -> bool:
        return self._metabo_experiment.is_the_metadata_corresponding(metadata)

    def get_final_targets_values(self):
        return self._metabo_experiment.get_final_targets_values()

    def set_final_targets_values(self, targets_columns: List[str]):
        self._metabo_experiment.set_final_targets_values(targets_columns)

    def add_final_targets_col_to_dataframe(self):
        self._metabo_experiment.add_final_targets_col_to_dataframe()

    def data_is_set(self) -> bool:
        return self._metabo_experiment.data_is_set()

    def metadata_is_set(self) -> bool:
        return self._metabo_experiment.metadata_is_set()

    def set_target_columns(self, target_cols: List[str]) -> None:
        self._metabo_experiment.set_target_columns(target_cols)

    def set_multithreading(self, activate_multithreading: bool):
        self._metabo_experiment.set_multithreading(activate_multithreading)

    def get_cv_algorithm_configuration(self) -> list:
        return self._metabo_experiment.get_cv_algorithm_configuration()

    def set_cv_algorithm_configuration(self, cv_algorithm_configuration: list):
        self._metabo_experiment.set_cv_algorithm_configuration(cv_algorithm_configuration)

    def get_samples_id(self):
        """
        Samples name from data file
        """
        return self._metabo_experiment.get_samples_id()

    def get_classes_repartition_for_all_experiment(self) -> dict:
        return self._metabo_experiment.get_classes_repartition_for_all_experiment()

    def get_balance_correction_for_all_experiment(self) -> dict:
        return self._metabo_experiment.get_balance_correction_for_all_experiment()

    def set_balance_correction_for_experiment(self, classification_design_name: str, balance_correction: int) -> None:
        self._metabo_experiment.set_balance_correction_for_experiment(classification_design_name, balance_correction)

    def display_splits(self) -> None:
        """
        Display the classes repartition for each split of each classification design.

        This can be used for debugging purposes from the automate.py script for example.

        The output will be something like:
            classification design 'first_design' details:
                Data set repartition: 'B': 96 (84%) vs 'C': 18 (16%) (Balance corr=34%).
                Classes 'B' vs 'C' repartition in splits (All | Train | Test):
                Split #00: All=[34 (65%) vs 18 (35%)] | Train=[14 (52%) vs 13 (48%)] | Test=[20 (80%) vs 5 (20%)]
                Split #01: All=[35 (66%) vs 18 (34%)] | Train=[15 (52%) vs 14 (48%)] | Test=[20 (83%) vs 4 (17%)]
                ...
        """
        self._metabo_experiment.display_splits()