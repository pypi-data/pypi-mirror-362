import base64
import hashlib
import importlib
import os
import pickle
from typing import Union
import re

import pickle as pkl
from typing import List, Dict, Tuple

import numpy
import numpy as np
import pandas as pd
import sklearn

PACKAGE_ROOT_PATH = os.sep.join(os.path.dirname(__file__).split(os.sep)[:-1])
DUMP_PATH = os.path.join(PACKAGE_ROOT_PATH, "domain", "dumps")
DUMP_EXPE_PATH = os.path.join(DUMP_PATH, "save.mtxp")

DEFAULT_IMPORTANCE_ATTRIBUTE = "feature_importances_"


def dump_metabo_expe(obj, expe_file_path: str=DUMP_EXPE_PATH):
    with open(expe_file_path, "w+b") as expe_file:
        pkl.dump(obj, expe_file)

        
def get_dumped_metabo_experiment_path() -> str:
    return DUMP_EXPE_PATH


def get_metabo_experiment_path(expe_filename: str="save", is_date: bool=True) -> str:
    """Get the metabo experiment path.
        - optionaly add the date (if is_date is True).
        - add the ".mtxp" extension if expe_filename don't have one.

    Args:
        expe_filename (str, optional): filename to use as template. Defaults to "save".
        is_date (bool, optional): True to add the date and time in the filename. Defaults to True.

    Returns:
        str: The full path to the filename
    """
    _, name_ext = os.path.splitext(expe_filename)
    if not name_ext:
        expe_filename = expe_filename + ".mtxp"
    
    saves_dir = get_medic_subdir("saves")
    
    new_filename = insert_datetime(expe_filename) if is_date else expe_filename
    return os.path.join(saves_dir, new_filename)


def get_medic_subdir(subdir_name: str) -> str:
    """Returns the path to provided subdirectory of '~/medic_files/' main medic directory.

    Args:
        subdir_name (str): subdir to get (and create if it doesn't exist)

    Returns:
        str: the subdir full path
    """
    home_dir_path: str = os.path.expanduser("~")
    subdir_path: str = os.path.join(home_dir_path, "medic_files", subdir_name)
    
    if not os.path.exists(subdir_path):
        os.makedirs(subdir_path)
        
    if not os.path.exists(subdir_path):
        subdir_path = os.getcwd()
    
    return subdir_path


from datetime import datetime

def insert_datetime(expe_filename: str) -> str:
    current_datetime = datetime.now().strftime("_%Y%m%d_%H%M%S")
    name_root, name_ext = os.path.splitext(expe_filename)
    return name_root + current_datetime + name_ext


def load_metabo_expe(path):
    if os.path.isfile(DUMP_EXPE_PATH):
        with open(path, "rb") as expe_file:
            return pkl.load(expe_file)
    else:
        return None


def retrieve_data_from_sample_name(names_list, dataframe):
    """

    :param names_list: list of samples name
    :param dataframe: a dataframe with each sample as a line identified by the samples' name
    :return: list of data
    """
    print("retrieving data from name")
    data_list = []
    for n in names_list:
        d = dataframe.loc[n, :]
        data_list.append(d.tolist())
    # print("data list : {}".format(data_list[0]))
    print("data from name retrieved")
    # print("data 2nd element : {}".format(data_list[1]))
    return data_list


def list_filler(liste):
    """
    (NA or "")
    Complete the NA values of a list with the last non NA value from left to right.
    If the first value is NA, then leave it like this.
    :param liste: list to fill
    :return: new list filled
    """
    l = []
    current = ""
    for idx, j in enumerate(liste):
        if j != "":
            current = j
        l.append(current)
    return l


def read_Progenesis_compounds_table(fileName, with_raw=True):
    datatable = pd.read_csv(fileName, header=2, index_col=0)
    header = pd.read_csv(fileName, nrows=1, index_col=0)
    start_normalized = header.columns.tolist().index("Normalised abundance")

    labels_array = np.array(header.iloc[0].tolist())
    possible_labels = labels_array[labels_array != "nan"]

    if with_raw:
        start_raw = header.columns.tolist().index("Raw abundance")
        sample_names = datatable.iloc[:, start_normalized:start_raw].columns
        possible_labels = possible_labels[0: int(len(possible_labels) / 2)]
    else:
        sample_names = datatable.iloc[:, start_normalized:].columns

    labels = [""] * len(sample_names)
    start_label = possible_labels[0]
    labels_array = labels_array.tolist()
    for next_labels in possible_labels[1:]:
        index_s = labels_array.index(start_label) - start_normalized
        index_e = labels_array.index(next_labels) - start_normalized
        labels[index_s:index_e] = [start_label] * (index_e - index_s)
        start_label = next_labels
    labels[index_e:] = [start_label] * (len(labels) - index_e)

    labels_dict = {sample_names[i]: j for i, j in enumerate(labels)}

    if with_raw:
        datatable_compoundsInfo = datatable.iloc[:, 0:start_normalized]
        datatable_normalized = datatable.iloc[:, start_normalized:start_raw]
        datatable_raw = datatable.iloc[:, start_raw:]
        datatable_raw.columns = [
            i.rstrip(".1") for i in datatable_raw.columns
        ]  # Fix the columns names

        datatable_normalized = datatable_normalized.T
        datatable_raw = datatable_raw.T
        datatable_compoundsInfo = datatable_compoundsInfo.T
        datatable_normalized.rename(columns={"Compound": "Sample"})
        datatable_raw.rename(columns={"Compound": "Sample"})
        return (
            datatable_compoundsInfo,
            datatable_normalized,
            datatable_raw,
            labels,
            sample_names,
        )
    else:
        datatable_compoundsInfo = datatable.iloc[:, 0:start_normalized]
        datatable_normalized = datatable.iloc[:, start_normalized:]
        datatable_normalized = datatable_normalized.T
        datatable_compoundsInfo = datatable_compoundsInfo.T
        datatable_normalized.rename(columns={"Compound": "Sample"})
        return datatable_compoundsInfo, datatable_normalized, labels, sample_names


def filter_sample_based_on_labels(data, labels, labels_to_keep):
    """
    function not used
    """
    labels_filter = np.array([i in labels_to_keep for i in labels])
    d = data.iloc[labels_filter]
    l = np.array(labels)[labels_filter]
    return d, l


def get_group_to_class(classes):
    """
    function not used
    """
    group_to_class = {}
    for class_name in classes:
        for subgroup in classes[class_name]:
            group_to_class[subgroup] = class_name
    return group_to_class


def reverse_dict(dictionnary: dict) -> dict:
    """
    Create a reverse dict to easily retrieve the label associate to a target.
    example
    input dict is in shape {label1 : [target1, target2], label2 : [target3, target4]}
    output dict would be {target1 : label1, target2 : label1, target3 : label2, target4 : label2}
    """
    reversed_dict = {}
    for key, value in dictionnary.items():
        if type(value) is list:
            for val in value:
                reversed_dict[val] = key
        else:
            reversed_dict[value] = key
    return reversed_dict


def load_classes_from_targets(classes_design: dict, targets: Tuple[str]) -> List[str]:
    """
    Create a list of targets to be predicted according to the class design, kind of a "traduction" of labels.
    !!! There is some confusion between class/label/target, it results from their use as synonyms in general in
    the litterature. We tried to established a distinction because we need 3 different terms to name 3 slightly different 
    things. However, even for us it got mixed up during the development. Hence the sometime confusing naming of variables.
    Always refer to the documentation for the proper meaning. !!!
    example
    Argument 'targets' is (class3, class1, class4, class4, class2, class1)
    classes_design would be something like {label1 : [class1, class2], label2 : [class3, class4]}
    reverse_classes_design would be {class1 : label1, class2 : label1, class3 : label2, class4 : label2}
    'classes' that is returned would be [label2, label1, label2, label2, label1, label1]
    """
    reverse_classes_design = reverse_dict(classes_design)
    classes = []
    for target in targets:
        if target not in reverse_classes_design:
            raise ValueError("Target {} not found in classes_design".format(target))
        classes.append(reverse_classes_design[target])
    if len(classes) != len(targets):
        raise ValueError("Some targets were not found in classes_design")
    return classes


# TODO: need to support multi-classification
def get_binary(list_to_convert: List[str], classes: List[str]) -> List[int]:
    return [classes.index(value) for value in list_to_convert]


def compute_hash(data: str) -> str:
    """
    Compute a hash for a data string
    """
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def is_save_safe(saved_metabo_experiment_dto) -> bool:
    return (
            saved_metabo_experiment_dto.metadata.is_data_the_same()
            and saved_metabo_experiment_dto.data_matrix.is_data_the_same()
    )


def format_list_for_checklist(list_to_format: List[str]) -> List[Dict[str, str]]:
    return [{"label": value, "value": value} for value in list_to_format]


def check_if_column_exist(datatable: pd.DataFrame, column_name: str) -> bool:
    return column_name in datatable.columns


def decode_pickle_from_base64(encoded_object: str):
    return pickle.loads(base64.b64decode(encoded_object.split(",")[1]))


def are_files_corresponding_to_dto(
        data: str, metadata: str, metabo_experiment_dto
) -> bool:
    return is_data_the_same(data, metabo_experiment_dto) and is_metadata_the_same(
        metadata, metabo_experiment_dto
    )


def reset_file(file_path: str):
    """
    Reset the content of a file ?
    """
    open(file_path, "w+b").close()


# TODO : function to probably delete
def restore_ids_and_targets_from_pairing_groups(filtered_samples: List[str], dataframe: pd.DataFrame, id_column: str,
                                                paired_column: str, target_column: str, classes_design: dict,) -> Tuple[List[str], List[str]]:

    pairing_values = dataframe.loc[dataframe[id_column].isin(filtered_samples)][paired_column].tolist()
    ids = dataframe[dataframe[paired_column].isin(pairing_values)][id_column].tolist()
    targets = dataframe.loc[dataframe[id_column].isin(ids)][target_column].tolist()
    duo = list(zip(ids, targets))
    restored_ids = []
    restored_targets = []
    for d in duo:
        if d[1] in np.concatenate(list(classes_design.values())):
            restored_ids.append(d[0])
            restored_targets.append(d[1])
    return restored_ids, load_classes_from_targets(classes_design, restored_targets)


def convert_str_to_list_of_lists(str_to_convert: str) -> List[List[Union[str, float, int]]]:
    first_level = []
    for find in re.findall(r'\[((([\w\'".]+,? ?)+))\] ?,?', str_to_convert):
        tmp = find[0].split(',')
        second_level = []
        for element in tmp:
            element = element.strip()
            try:
                element = int(element)
            except ValueError:
                pass
            try:
                element = float(element)
            except ValueError:
                pass
            second_level.append(element)

        first_level.append(second_level)
    return first_level


def is_data_the_same(data: str, metabo_experiment_dto) -> bool:
    return metabo_experiment_dto.data_matrix.get_hash() == compute_hash(data)


def is_metadata_the_same(metadata: str, metabo_experiment_dto) -> bool:
    return metabo_experiment_dto.metadata.get_hash() == compute_hash(metadata)


def get_model_from_import(imports_list: list, model_name: str) -> sklearn:
    """
    Import a "custom" model from sklearn
    """
    last_import = importlib.import_module("." + imports_list[0], package="sklearn")

    for next_import in imports_list[1:]:
        last_import = getattr(last_import, next_import)

    model = getattr(last_import, model_name)
    return model


def get_model_parameters(model) -> List[Tuple[str, str]]:
    parameters = vars(model()).keys()
    parameters = [(parameter, _get_type(parameter, model())) for parameter in parameters if parameter not in ["self", "random_state"]]
    return parameters


def _get_type(attribute: str, owner_instance) -> str:
    return str(type(getattr(owner_instance, attribute)).__name__)


def _parameter_is_relevant(parameter: str, model: object) -> bool:
    return parameter not in get_model_parameters(model) and parameter.endswith("_") and not parameter.startswith("_")


def _parameter_is_collection(parameter: str, trained_model: sklearn) -> bool:
    try:
        attribute = getattr(trained_model, parameter)
    except AttributeError:
        print("Attribute {} not found in model".format(parameter))
        return False
    if type(attribute) in (list, tuple, set, dict, pd.DataFrame, pd.Series, numpy.ndarray):
        if len(attribute) == 3:
            return True
        try:
            # TODO: manual test on the web app
            if len(attribute[0]) == 3 and len(attribute) == 1:
                return True
        except (KeyError, TypeError, IndexError):
            pass
    return False


def get_model_parameters_after_training(model: sklearn) -> List[Tuple[str, str]]:
    trained_model = model()
    trained_model.fit([[1, 2, 3], [4, 5, 6]], [1, 2])

    attributes = dir(trained_model)
    parameters = []
    for attribute in attributes:
        if _parameter_is_collection(attribute, trained_model) and \
                _parameter_is_relevant(attribute, model):
            parameters.append((attribute, _get_type(attribute, trained_model)))
    if DEFAULT_IMPORTANCE_ATTRIBUTE in attributes:
        default_tuple = (DEFAULT_IMPORTANCE_ATTRIBUTE, _get_type(DEFAULT_IMPORTANCE_ATTRIBUTE, trained_model))
        parameters.remove(default_tuple)
        parameters.insert(0, default_tuple)
    return parameters


def transform_params_to_cross_validation_dict(params: List[Tuple[str, str]], param_types: dict) -> dict:
    cross_validation_params = {}
    error = []
    for param, value in params:
        values = re.split(r" *, *", value)
        param_type = param_types[param]
        if param_type == "float":
            try:
                cross_validation_params[param] = [float(val) for val in values]
            except ValueError:
                error.append(f"{param} must be decimal numbers (with '.')")
        elif param_type == "int":
            try:
                cross_validation_params[param] = [int(val) for val in values]
            except ValueError:
                error.append(f"{param} must be integers")
        else:
            try:
                values = int(value)
            except ValueError:
                try:
                    values = float(value)
                except ValueError:
                    pass
            try:
                values = [int(val) for val in values]
            except ValueError:
                try:
                    values = [float(val) for val in values]
                except ValueError:
                    pass

            cross_validation_params[param] = values
    if error:
        raise ValueError(error)
    return cross_validation_params


def get_closest_integer_steps(slider_size):
    max_number_of_steps = 5

    if slider_size <= 0:
        return []
    step = slider_size // max_number_of_steps
    steps = [step * i for i in range(0, max_number_of_steps + 1)]
    if slider_size % max_number_of_steps != 0:
        # steps.pop(-1)
        steps.append(slider_size)
    return [int(i) for i in steps if i <= slider_size]


def remove_random_samples_from_class(X: pd.Series, y: List[str], balance_correction: int,
                                     classes_repartition: dict, seed: int = 42)-> Tuple[pd.Series, list]:
    """
    Function to adjust proportion between classes, to make it more balanced, or as balanced as possible
    Supposed to be provided by user (how much to adjust)
    """

    samples_ids_and_targets = pd.DataFrame({"id": X, "final_classes": y})
    balance_correction = balance_correction / 100

    if len(classes_repartition) > 2:
        raise ValueError("Balance correction is not supported for multiclassification")

    class_A_name, class_B_name = tuple(classes_repartition.keys())
    total_number_of_samples = classes_repartition[class_A_name] + classes_repartition[class_B_name]
    class_A_repartition = classes_repartition[class_A_name] / total_number_of_samples
    class_B_repartition = classes_repartition[class_B_name] / total_number_of_samples

    # Naming trick to ensure that the "A" class is always the one with the higher number of examples
    if class_B_repartition > class_A_repartition:
        class_A_name, class_B_name = class_B_name, class_A_name
        class_A_repartition, class_B_repartition = class_B_repartition, class_A_repartition

    class_A_lines = samples_ids_and_targets[samples_ids_and_targets["final_classes"] == class_A_name]

    class_A_number_of_samples = len(class_A_lines)
    class_B_number_of_samples = len(samples_ids_and_targets[samples_ids_and_targets["final_classes"] == class_B_name])

    # --- PROOF OF THE FORMULA ---
    # new_proportion_A = trimmed_classe_A_samples / (trimmed_classe_A_samples + class_B_samples)
    # proportion_A - correction = trimmed_classe_A_samples / (trimmed_classe_A_samples + class_B_samples)
    # (proportion_A - correction) * (trimmed_classe_A_samples + class_B_samples) = trimmed_classe_A_samples
    # proportion_A * trimmed_classe_A_samples - correction * trimmed_classe_A_samples + proportion_A * class_B_samples - correction * class_B_samples = trimmed_classe_A_samples
    # proportion_A * class_B_samples - correction * class_B_samples = trimmed_classe_A_samples - proportion_A * trimmed_classe_A_samples + correction * trimmed_classe_A_samples
    # proportion_A * class_B_samples - correction * class_B_samples = trimmed_classe_A_samples * (1 - proportion_A + correction)
    # trimmed_classe_A_samples = class_B_samples * (proportion_A - correction) / (1 - proportion_A + correction)

    new_class_A_number_of_samples = class_B_number_of_samples * (class_A_repartition - balance_correction) / \
                                    (1 - class_A_repartition + balance_correction)
    # Considering class A is always bigger than or equal to class B, to get a more balanced repartition,
    # "new_class_A_number_of_samples" should be a smaller number than "class_A_number_of_samples"
    number_of_samples_to_remove = class_A_number_of_samples - new_class_A_number_of_samples

    np.random.seed(seed)
    ids_to_remove = np.random.choice(class_A_lines.index, int(number_of_samples_to_remove), replace=False)
    samples_ids_and_targets = samples_ids_and_targets.drop(ids_to_remove)

    return samples_ids_and_targets["id"], samples_ids_and_targets["final_classes"].tolist()
