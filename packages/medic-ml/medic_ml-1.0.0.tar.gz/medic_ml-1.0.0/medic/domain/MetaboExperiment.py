from typing import Generator, Tuple, List, Dict, Union

import sklearn

from . import ClassificationDesign
from . import MetaData, MetaboModel
from .DataMatrix import DataMatrix
from .MetaboExperimentDTO import MetaboExperimentDTO
from .ModelFactory import ModelFactory
from ..conf.SupportedCV import CV_ALGORITHMS
from ..service import Utils
from ..service import init_logger

X_TRAIN_INDEX = 0
X_TEST_INDEX = 1
y_TRAIN_INDEX = 2
y_TEST_INDEX = 3

DEFAULT_NJOB = 1


class MetaboExperiment:
    def __init__(self):
        self._model_factory = ModelFactory()

        self._data_matrix = DataMatrix()
        self._is_progenesis_data = False
        self._metadata = MetaData()
        self._unique_ids = None

        self._number_of_splits = 25
        self._train_test_proportion = 0.2
        self._pairing_group_column = ""
        self._cv_folds = 5
        self._activate_multithreading = True

        self.classification_designs: Dict[str, ClassificationDesign] = {}

        self._supported_models = self._model_factory.create_supported_models("GS")
        self._custom_models = {}
        self._selected_models = []
        self._cv_algorithms = CV_ALGORITHMS
        self._selected_cv_type = list(self._cv_algorithms.keys())[0]
        
        self._logger = init_logger(__name__)

    def init_metadata(self):
        """
        Create an instance of MetaData for the attribute of metadata
        """
        self._metadata = MetaData()

    def get_metadata(self) -> MetaData:
        return self._metadata

    def get_final_targets_values(self):
        return self._metadata.get_final_targets_values()

    def set_final_targets_values(self, columns: List[str]):
        self._metadata.set_final_targets_values(columns)

    def add_final_targets_col_to_dataframe(self):
        self._metadata.add_final_targets_col_to_dataframe()

    def init_data_matrix(self):
        """
        Create an instance of DataMatrix for the attribute of data_matrix
        """
        self._data_matrix = DataMatrix()

    def set_metadata_with_dataframe(self, filename, data=None, from_base64=True):
        """
        Create an instance of MetaData and then fill it by reading and storing the content
        of the metadata file provided
        """
        self.init_metadata()
        self._metadata.read_format_and_store_metadata(filename, data=data, from_base64=from_base64)

    def set_data_matrix(self, path_data_matrix: str, data=None, from_base64: bool = True):
        """
        set metadata from progenesis data file while handling progenesis data file
        it creates a "fake" metadata structure from the retrieved id and classes of progenesis
        And formats it with the targets column
        """
        self._data_matrix.reset_file()
        # self._data_matrix handles itself to store data, and it also creates a "fake" metadata dataframe to keep
        # the same metadata format as if it was given by a metadata file
        # it returns None if it is not a progenesis file
        metadata_df, self._unique_ids = self._data_matrix.read_format_and_store_data(path_data_matrix, data=data, from_base64=from_base64)

        # format the metadata df (in case progenesis is given)
        self._is_progenesis_data = metadata_df is not None
        if metadata_df is not None:
            self._metadata = MetaData(metadata_df)
            self._metadata.set_id_column("sample_names")
            self._metadata.set_target_columns(["labels"])

    def get_data_matrix(self) -> DataMatrix:
        return self._data_matrix

    def get_train_test_proportion(self) -> float:
        """
        Retrieve the value of the attribute _train_test_proportion
        """
        return self._train_test_proportion

    def get_number_of_splits(self) -> int:
        """
        Retrieve the value of the attribute _number_of_splits
        """
        return self._number_of_splits

    def set_number_of_splits(self, number_of_splits: int):
        """
        Set the value of the MetaboExpe attribute _number_of_splits
        """
        self._number_of_splits = number_of_splits

    def set_train_test_proportion(self, train_test_proportion: float):
        """
        Set the value of the MetaboExpe attribute _train_test_proportion
        """
        self._train_test_proportion = train_test_proportion

    def create_splits(self, test_split_seed: int|None=None) -> None:
        """
        Check that Experiment parameters are set and then : create an instance of SplitGroup for each Classification Design
        (The init of SplitGroup triggers the _compute_splits function).
        If test_split_seed is provided, then only this test split seed is computed.
        """
        if self._number_of_splits is None:
            raise ValueError("Number of splits not set")
        if self._train_test_proportion is None:
            raise ValueError("Train test proportion not set")
        if self._pairing_group_column is None:
            raise ValueError("Pairing group column not set")
        if self._metadata is None:
            raise ValueError("Metadata not set")
        for _, classification_design in self.classification_designs.items():
            classification_design.set_split_parameter_and_compute_splits(self._train_test_proportion,
                                                                       self._number_of_splits, self._metadata,
                                                                       self._pairing_group_column, self._unique_ids, 
                                                                       test_split_seed)

    def get_pairing_group_column(self) -> str:
        """
        Retrieve the name of the column to use for pairing the samples
        """
        return self._pairing_group_column

    def set_pairing_group_column(self, pairing_group_column: str):
        """
        Set the value of the MetaboExpe attribute _pairing_group_column
        """
        if pairing_group_column not in self._metadata.get_columns():
            raise RuntimeError("Column {} is not in the metadata".format(pairing_group_column))
        self._pairing_group_column = pairing_group_column

    def get_classification_designs(self) -> Dict[str, ClassificationDesign]:
        """
        Retrieve all Classification Designs for an experience
        """
        return self.classification_designs

    def _raise_if_classes_design_is_not_valid(self, classes_design: dict) -> None:
        if "" in list(classes_design.keys()):
            raise ValueError("Empty label(s) is not allowed")
        if len(classes_design) < 2:
            raise ValueError("Labels must have different names")
        items = [inner_val for val in classes_design.values() for inner_val in val]
        if 0 in items:
            raise ValueError(
                "You need to select at least one class. If no class appears, "
                "please upload a data matrix and, if necessary, a metadata file"
            )
        if len(set(items)) != len(items):
            raise ValueError("Duplicate class name is not allowed")

    def add_classification_design(self, classes_design: dict):
        """
        add a Classification Design to the experience, creates an object ClassificationDesign each time
        classes_design: which target.s against which for the prediction, and the names (classes) of the groups of target.s
        """
        self._raise_if_classes_design_is_not_valid(classes_design)
        classification_design = ClassificationDesign(classes_design)
        self.classification_designs[classification_design.get_name()] = classification_design

    def remove_classification_design(self, name: str):
        """
        Remove a Classification Design, but not used
        """
        self.classification_designs.pop(name)

    def add_custom_model(self, model_name: str, needed_imports: str, params_grid: dict, importance_attribute: str):
        """
        Add the information needed to run a custom model
        model_name: the name of the model
        needed_imports: the modules needed to run this model
        params_grid: the hyperparameters grid with which hyperparameters to test and for which values
        importance_attribute: the attribute of the model to use to measure the importance of features
        """
        model_index = model_name.strip()
        model_index = "Custom" + model_index

        index = 1
        model_index = model_index + "0"
        # Check if model name already exists, if yes, get the next available index
        # This system make the addition of identical algorithm with different hyperparameters grid possible
        while model_index in self._custom_models:
            model_index = model_index[:-1]
            model_index = model_index + str(index)
            index += 1
        self._custom_models[model_index] = self._model_factory.create_custom_model(model_name, needed_imports,
                                                                                   params_grid, importance_attribute)

    def get_custom_models(self) -> dict:
        return self._custom_models

    def set_selected_models(self, selected_models: list):
        """
        Set the self._selected_models attribute with the list given in argument
        and for each Classification Design object initialize basics of Results instances
        selected_models: list of models to run during the experiment
        """
        if self.classification_designs == {}:
            raise ValueError("You must define at least one classification design before selecting models.")
        self._selected_models = selected_models
        for _, classification_design in self.classification_designs.items():
            classification_design.set_selected_models_name(selected_models)

    def update_classification_designs_with_selected_models(self):
        """

        """
        for _, classification_design in self.classification_designs.items():
            classification_design.set_selected_models_name(self._selected_models)

    def get_selected_models(self) -> list:
        """
        Retrieve the name of the selected models to use for the experiment
        """
        return self._selected_models

    def get_metadata_columns(self) -> list:
        """
        Retrieve the names of the columns in the metadata matrix
        """
        if self._metadata is None:
            raise RuntimeError("Metadata is not set.")
        return self._metadata.get_columns()

    def set_id_column(self, id_column: str):
        """
        Set the id_column attribute of the MetaData object
        It is the column in the metadata used to have a unique id for each line/item/sample
        id_column: string of the name of the column
        """
        if self._metadata is None:
            raise RuntimeError("Metadata is not set.")
        self._metadata.set_id_column(id_column)

    def validate_id_column(self) -> bool:
        """
        Ensure all values in the data index column (unique_ids) are in the the metadata id_column
        """
        if not self._is_progenesis_data and self._metadata is None:
            raise RuntimeError("Metadata is not set.")
        if self._unique_ids is None:
            return False
        return self._metadata.validate_id_column(self._is_progenesis_data, self._unique_ids)

    def get_unique_targets(self) -> list:
        """
        Retrieve a list of unique targets by applying a "set()" function to the complete list of targets.
        """
        try:
            return self._metadata.get_unique_targets()
        except RuntimeError:
            return []

    def get_model_from_name(self, model_name: str) -> MetaboModel:
        if model_name in self._supported_models.keys():
            return self._supported_models[model_name]
        elif model_name in self._custom_models.keys():
            return self._custom_models[model_name]
        else:
            raise RuntimeError(
                "The model '"
                + model_name
                + "' has not been found neither in supported and custom lists."
            )

    def _check_classification_design(self):
        error_message = "Train test proportion, number of splits and metadata need to be set before start learning: "
        if self._number_of_splits is None:
            raise RuntimeError(error_message + "missing number of splits")
        if self._train_test_proportion is None:
            raise RuntimeError(error_message + "missing train test proportion")
        if self._metadata is None:
            raise RuntimeError(error_message + "missing metadata")

    def all_classification_designs_names(self) -> Generator[Tuple[str, str], None, None]:
        """
        Retrieve all Classification Designs names for an experience.
        """
        for name, classification_design in self.classification_designs.items():
            yield name, classification_design.get_full_name()

    def reset_classification_designs(self):
        """
        Delete all existing Classification Designs.
        """
        self.classification_designs = {}

    def _raise_if_value_for_learning_not_setted(self):
        if self._data_matrix is None:
            raise RuntimeError("Data matrix not set")
        if self._metadata is None:
            raise RuntimeError("Metadata not set")
        if self._pairing_group_column is None:
            raise RuntimeError("Pairing group column not set")
        if self._train_test_proportion is None:
            raise RuntimeError("Train test proportion not set")
        if self._number_of_splits is None:
            raise RuntimeError("Number of splits not set")
        if self._selected_models is None:
            raise RuntimeError("Selected models not set")
        if self._cv_folds is None:
            raise RuntimeError("CV folds not set")
        if self.classification_designs == {}:
            raise RuntimeError(
                "You must define at least one classification design before learning."
            )

    def learn(self):
        self._raise_if_value_for_learning_not_setted()
        cv_algorithm_constructor = self.get_cv_algorithm_constructor()
        cv_algorithm_config = self.get_cv_algorithm_configuration()
        self._check_classification_design()
        self._data_matrix.load_data()
        assert(self._data_matrix.data is not None)
        if not self._data_matrix.data.index.isin(self._metadata.get_metadata()[self._metadata.get_id_column()]).all():
            raise ValueError(f"'{self._metadata.get_id_column()}' seen not to be as valid name of the unique id column.")
        params = []
        for _, classification_design in self.classification_designs.items():
            self._logger.info("-> Classification design loop ")
            selected_targets_name = classification_design.get_selected_targets_name()
            (selected_targets, selected_ids,) = self._metadata.get_selected_targets_and_ids(selected_targets_name)
            classes = Utils.load_classes_from_targets(
                classification_design.get_classes_design(), selected_targets
            )
            for split_index, split in classification_design.all_splits():
                for model_name in self._selected_models:
                    x_train = self._data_matrix.load_samples_corresponding_to_IDs_in_splits(
                        split[X_TRAIN_INDEX]
                    )
                    x_test = self._data_matrix.load_samples_corresponding_to_IDs_in_splits(
                        split[X_TEST_INDEX]
                    )
                    params.append(
                        (model_name, classification_design.get_name(), split_index, split, x_train, x_test,
                         cv_algorithm_constructor, cv_algorithm_config, selected_ids, classes)
                    )
        self.run_learning(params)
        self._data_matrix.unload_data()


    def run_learning(self, params: List[tuple]):
        self._logger.info("-> run_learning function beginning")
        # launch the run_on_model function with the params
        result_params = [self.run_on_model(*param) for param in params]

        for result_param in result_params:
            (
                classification_design_name, 
                model_name, 
                best_model, 
                scaled_data, 
                importance_attribute, 
                classes, 
                y_train,
                y_train_pred,
                y_test,
                y_test_pred,
                split_index,
                X_train,
                X_test
            ) = result_param
            results = self.classification_designs[classification_design_name].get_results()
            results[model_name].set_feature_names(X_train) # called multiple times but it's ok
            results[model_name].design_name = classification_design_name
            results[model_name].add_results_from_one_algo_on_one_split(
                best_model, scaled_data, importance_attribute, 
                classes, y_train, y_train_pred, y_test, y_test_pred,
                split_index, X_train.index, X_test.index
            )

        for classification_design_name, classification_design in self.classification_designs.items():
            results = classification_design.get_results()
            _, selected_sample_id = self._metadata.get_selected_targets_and_ids(
                classification_design.get_selected_targets_name())
            for model_name, result in results.items():
                self._logger.info(f"-> Compute remaining results for {model_name} of {classification_design_name} design")
                result.compute_remaining_results_on_all_splits(selected_sample_id)
            classification_design.set_is_done(True)


    def run_on_model(self, model_name, classification_design_name, split_index, split, x_train, x_test,
                     cv_algorithm_constructor, cv_algorithm_config, selected_ids, classes):
        self._logger.info(f"-> Split : {split_index}")
        self._logger.info(f"-> Model : {model_name}")

        metabo_model = self.get_model_from_name(model_name)

        # When set n_processes is set to -1, all processors are used.
        n_processes = -1 if self._activate_multithreading else DEFAULT_NJOB
        best_model = metabo_model.train(
            self._cv_folds,
            x_train,
            split[y_TRAIN_INDEX],
            cv_algorithm_constructor,
            cv_algorithm_config,
            n_processes,
            seed=split_index
        )
        y_train_pred = best_model.predict(x_train)
        y_test_pred = best_model.predict(x_test)
        return (
            classification_design_name,
            model_name,
            best_model,
            self._data_matrix.get_scaled_data(selected_ids),
            metabo_model.get_importance_attribute(),
            classes,
            split[y_TRAIN_INDEX],
            y_train_pred,
            split[y_TEST_INDEX],
            y_test_pred,
            str(split_index),
            x_train,
            x_test
        )

    def get_results(self, classes_design: str, algo_name) -> dict:
        return self.classification_designs[classes_design].get_results()[algo_name]

    def get_all_updated_results(self) -> dict:
        """
        Retrieve, for each Classification Design that is done, the results dict corresponding
        """
        results = {}
        for name in self.classification_designs:
            if self.classification_designs[name].get_is_done():
                results[name] = self.classification_designs[name].get_results()
        return results

    def get_all_algos_names(self) -> list:
        """
        Concatenate the list of names from default (supported) models and custom models
        """
        return list(self._supported_models.keys()) + list(self._custom_models.keys())

    def set_cv_type(self, cv_type: str):
        """
        Set the type of Cross-Validation (cv) for the experiment
        """
        if cv_type not in self._cv_algorithms:
            raise ValueError(f"CV type '{cv_type}' is not supported. Choices are : {list(self._cv_algorithms.keys())}")

        if cv_type == "GridSearchCV":
            self._supported_models = self._model_factory.create_supported_models("GS")
        elif cv_type == "RandomizedSearchCV":
            self._supported_models = self._model_factory.create_supported_models("RS")

        self._selected_cv_type = cv_type

    def get_selected_cv_type(self) -> str:
        """
        Return the type of CV selected for this experiment
        """
        return self._selected_cv_type

    def get_cv_algorithm_constructor(self) -> sklearn.model_selection:
        return self._cv_algorithms[self._selected_cv_type]["constructor"]

    def get_cv_algorithm_configuration(self) -> list:
        return self._cv_algorithms[self._selected_cv_type]["params"]

    def set_cv_algorithm_configuration(self, cv_algorithm_configuration: list):
        config_index = 0
        for param_index, params in enumerate(self._cv_algorithms[self._selected_cv_type]["params"]):
            if not params["constant"]:
                self._cv_algorithms[self._selected_cv_type]["params"][param_index]["value"] = \
                    cv_algorithm_configuration[config_index]
                config_index += 1

    def get_cv_types(self) -> List[str]:
        """
        Retrieve the dict of possible cross-validation types supported by the MeDIC
        """
        return list(self._cv_algorithms.keys())

    def generate_save(self) -> MetaboExperimentDTO:
        """
        Create an object MetaboExperimentDTO
        (which is a holder of some MetaboExperiment attributes)
        """
        return MetaboExperimentDTO(self)

    def full_restore(self, saved_metabo_experiment_dto: MetaboExperimentDTO):
        """
        Restore an experiment from a saving (always? from file)
        Data and parameters
        """
        self._metadata = saved_metabo_experiment_dto.metadata
        self._data_matrix = saved_metabo_experiment_dto.data_matrix
        self._static_restore_for_partial(saved_metabo_experiment_dto)

    def _static_restore_for_partial(self, saved_metabo_experiment_dto: MetaboExperimentDTO):
        """
        ??? STATIC vs partial_restore ???
        Restore attributes from a MetaboExperimentDTO object
        a "Partial" restore means it only brings back parameters and no data
        """
        self._number_of_splits = saved_metabo_experiment_dto.number_of_splits
        self._train_test_proportion = saved_metabo_experiment_dto.train_test_proportion
        self.classification_designs = saved_metabo_experiment_dto.classification_designs
        self._custom_models = saved_metabo_experiment_dto.custom_models
        self._selected_models = saved_metabo_experiment_dto.selected_models
        self._selected_cv_type = saved_metabo_experiment_dto.selected_cv_type

    def partial_restore(self, saved_metabo_experiment_dto: MetaboExperimentDTO, filename_data: str, filename_metadata: str,
                        data=None, from_base64_data: bool = True, metadata=None, from_base64_metadata=True,):
        """
        ??? STATIC vs partial_restore ???
        Do a partial restore of an experiment
        """
        self._data_matrix.set_raw_use(saved_metabo_experiment_dto.data_matrix.is_raw())
        self._data_matrix.set_remove_rt(saved_metabo_experiment_dto.data_matrix.get_remove_rt())
        self.set_data_matrix(filename_data, data=data, from_base64=from_base64_data,)
        self.set_metadata_with_dataframe(filename_metadata, data=metadata, from_base64=from_base64_metadata)
        self._static_restore_for_partial(saved_metabo_experiment_dto)

    def load_results(self, saved_metabo_experiment_dto: MetaboExperimentDTO):
        """
        Init a new experiment (new metadata and data_matrix) and load saved results
        """
        self.init_metadata()
        self.init_data_matrix()
        self._static_restore_for_partial(saved_metabo_experiment_dto)

    def is_save_safe(self, saved_metabo_experiment_dto: MetaboExperimentDTO) -> bool:
        """
        Verify that the hash from the saved MetaboExperimentDTO is the same from the current object
        """
        return (self._metadata.get_hash() == saved_metabo_experiment_dto.metadata.get_hash()
                and self._data_matrix.get_hash() == saved_metabo_experiment_dto.data_matrix.get_hash())

    def is_the_data_matrix_corresponding(self, data: str) -> bool:
        return self._data_matrix.get_hash() == Utils.compute_hash(data)

    def is_the_metadata_corresponding(self, metadata: str) -> bool:
        return self._metadata.get_hash() == Utils.compute_hash(metadata)

    def get_target_column(self) -> str:
        """
        Retrieve the _target_column attribute of metadata
        """
        return self._metadata.get_target_column()

    def get_id_column(self) -> str:
        """
        Retrieve the _id_column attribute of metadata
        """
        return self._metadata.get_id_column()

    def is_progenesis_data(self) -> bool:
        """
        Return the bool indicating if the data given is of the progenesis format
        """
        return self._is_progenesis_data

    def is_data_raw(self) -> Union[bool, None]:
        """
        return the bool indicating to use either raw or normalized data
        """
        return self._data_matrix.is_raw()

    def set_raw_use_for_data(self, use_raw: bool):
        """
        Set the bool value of whether to use the raw data from a progenesis matrix or the normalized data
        """
        self._data_matrix.set_raw_use(use_raw)

    def get_data_matrix_remove_rt(self) -> bool:
        """
        return the value of the _remove_rt attribute
        (if true, remove the features detected before 1 minute of Retention Time)
        """
        return self._data_matrix.get_remove_rt()

    def set_data_matrix_remove_rt(self, remove_rt: bool):
        """
        set the value of the _remove_rt attribute
        (if true, remove the features detected before 1 minute of Retention Time)
        """
        self._data_matrix.set_remove_rt(remove_rt)

    def get_cv_folds(self) -> int:
        """
        Return the number of Cross Validation folds
        """
        return self._cv_folds

    def set_cv_folds(self, cv_folds: int):
        """
        Set the number of Cross Validation folds
        """
        if cv_folds < 2:
            raise ValueError("CV folds must be greater than or equal to 2.")
        self._cv_folds = cv_folds

    def data_is_set(self) -> bool:
        return self._data_matrix.data_is_set()

    def metadata_is_set(self) -> bool:
        return self._metadata.metadata_is_set()

    def set_target_columns(self, target_cols: List[str]) -> None:
        self._metadata.set_target_columns(target_cols)

    def set_multithreading(self, activate_multithreading: bool):
        self._activate_multithreading = activate_multithreading

    def get_samples_id(self):
        """
        This used to return self._metadata.get_samples_id(), thus sourcing samples name from metadata file.
        It has been adjusted to account for the situation of metadata containing more information
        than the samples studied by the provided data file
        """
        if self._unique_ids is None:
            return []
        return self._unique_ids
    
    def get_classes_repartition_for_all_experiment(self) -> dict:
        classes_repartition = {}
        for classification_design_name in self.classification_designs:
            class_design = self.classification_designs[classification_design_name].get_classes_design()
            classes_repartition[classification_design_name] = \
                self._metadata.get_classes_repartition_based_on_design(class_design)
        return classes_repartition

    def get_balance_correction_for_all_experiment(self) -> dict:
        balance_correction = {}
        for classification_design_name in self.classification_designs:
            balance_correction[classification_design_name] = \
                self.classification_designs[classification_design_name].get_balance_correction()
        return balance_correction

    def set_balance_correction_for_experiment(self, classification_design_name: str, balance_correction: int) -> None:
        if classification_design_name not in self.classification_designs:
            raise ValueError("Classification design name not found")
        self.classification_designs[classification_design_name].set_balance_correction(balance_correction)

    def display_splits(self) -> None:
        """
        Display the classes repartition for each split of each Classification Design.
        See more détail in the MetaboController.display_splits() method description.
        """
        from collections import Counter

        def display_classes_repartition(target_classes: list) -> str:
            return ' vs '.join([f"{cnt} ({int(round(cnt*100 / len(target_classes))):02d}%)" for _, cnt in sorted(Counter(target_classes).items())])

        for key,classification_design in self.classification_designs.items():
            balance_corr: int = classification_design.get_balance_correction()
            experimental_classes_repartition: dict = self._metadata.get_classes_repartition_based_on_design(classification_design.get_classes_design())
            total_cnt: int = sum(value for value in experimental_classes_repartition.values())

            debug_lines = []
            for split_index, split_group in classification_design.all_splits():
                if split_index == 0:
                    class_set = sorted(set(split_group[2]))
                    debug_lines.append(f"Classification Design '{key}' details:")
                    total_class_repartition: str = " vs ".join([f"'{cl}': {cnt:02d} ({int(round(cnt*100 / total_cnt)):02d}%)"
                                                                for cl, cnt in sorted(experimental_classes_repartition.items())])
                    debug_lines.append(f"Data set repartition: {total_class_repartition} (Balance corr={balance_corr}%).")
                    debug_lines.append(f"Classes '{class_set[0]}' vs '{class_set[1]}' repartition in splits (All | Train | Test):")

                all_cls_cnt: str = display_classes_repartition(split_group[2] + split_group[3])
                train_cls_cnt: str = display_classes_repartition(split_group[2])
                test_cls_cnt: str = display_classes_repartition(split_group[3])
                debug_lines.append(f"Split #{split_index:02d}: All=[{all_cls_cnt}] | Train=[{train_cls_cnt}] | Test=[{test_cls_cnt}]")

            debug_message = "\n\t".join(debug_lines)
            self._logger.debug(debug_message)