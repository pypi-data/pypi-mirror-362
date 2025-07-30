import base64
import io
import os.path
from typing import List, Tuple, Dict

import pandas as pd

from ..service import compute_hash
from ..service import init_logger

ROOT_PATH = os.path.dirname(__file__)
DUMP_PATH = os.path.join(ROOT_PATH, os.path.join("dumps", "metadata"))
DUMP_METADATA_PATH = os.path.join(DUMP_PATH, "metadata.p")
DUMP_METADATA_COLUMNS_PATH = os.path.join(DUMP_PATH, "metadata_columns.p")
DUMP_SAMPLES_ID_PATH = os.path.join(DUMP_PATH, "samples_id.p")
DUMP_TARGETS_PATH = os.path.join(DUMP_PATH, "targets.p")


class MetaData:
    def __init__(self, metadata_dataframe: pd.DataFrame = None):
        self._logger = init_logger()
        self._dataframe = metadata_dataframe

        self._id_column = None
        self._target_column = None
        self._final_targets_values = []

        self._hash = None

    def get_final_targets_values(self):
        """
        get the value of the attribute
        """
        return self._final_targets_values

    def set_final_targets_values(self, columns: List[str]):
        """
        compute the list of new strings (unite targets str with '__') and
        modify the value of the attribute with the list of values
        """
        if len(columns) > 1:
            df = self._dataframe.loc[:, columns].astype(str)
            final = list(df.apply(lambda row: "__".join(row), axis=1))
        else:
            final = self._dataframe[columns[0]].tolist()
        self._final_targets_values = final

    def add_final_targets_col_to_dataframe(self):
        """
        modify the attribute _dataframe to add the column of unified targets values
        """
        self._dataframe["final_targets"] = self._final_targets_values

    def add_final_targets_col_to_dump(self):
        """
        modify the temporary save of metadata (dump)
        """
        return None

    def read_format_and_store_metadata(self, path, data=None, from_base64=True):
        """
        Read the file to get a dataframe and compute a hash on it
        Store de obtained metadata dataframe in the attribute
        """
        df = self._load_and_format(path, data=data, from_base64=from_base64)
        if data is not None:
            self._hash = compute_hash(data)
        self._dataframe = df

    def get_hash(self) -> str:
        return self._hash

    def _load_and_format(self, filename, data=None, from_base64=True) -> pd.DataFrame:
        """
        Read the file and decode it to put it in the pd.Dataframe format
        """
        if from_base64:
            data_type, data_string = data.split(",")
            data = base64.b64decode(data_string)
            # print("data decoded :{}")
            # print(data[:200])
        else:
            data = filename

        if "csv" in filename:
            # Assume that the user uploaded a CSV file
            if from_base64:
                data = io.StringIO(data.decode("utf-8"))
            df = pd.read_csv(data, sep=None, na_filter=False, engine="python")
        elif "xls" in filename:
            if from_base64:
                data = io.BytesIO(data)
            # Assume that the user uploaded an excel file
            df = pd.read_excel(data, na_filter=False)
        else:
            raise TypeError("The input file is not of the right type, must be excel or csv.")
        return df

    def get_metadata(self) -> pd.DataFrame:
        """
        Getter for the metadata DataFrame
        """
        if self._dataframe is None:
            raise RuntimeError("Try to access the metadata before setting it.")
        return self._dataframe

    def get_columns(self) -> List[str]:
        """
        Retrieve the names of the columns in the metadata matrix as a list
        """
        if self._dataframe is None:
            self._logger.info("MetaData get_columns self._dataframe is None")
            return []
        return self._dataframe.columns.tolist()

    def get_unique_targets(self) -> List[str]:
        """
        Retrieve a list of unique targets by applying a "set()" function to the complete list of targets.
        eg: [0, 1, 1, 0, 0, 0, 1, 0, 2] will return [0, 1, 2]
        """
        targets = self.get_targets()
        return list(set(targets))

    def set_id_column(self, id_column: str) -> None:
        """
        Set the id_column attribute of the MetaData object
        It is the column in the metadata used to have a unique id for each line/item/sample
        id_column: string of the name of the column
        """
        if id_column not in self.get_columns():
            raise ValueError(f"'{id_column}' is not a column of the metadata. The columns are: {self.get_columns()}")
        self._id_column = id_column

    def validate_id_column(self, is_progenesis_data: bool, unique_ids: List[str]) -> bool:
        """
        Ensure all values in the data index column (unique_ids) are in the the metadata id_column
        """
        df = self._dataframe
        if self._dataframe is None:
            return False
        try:
            ids = df[self._id_column]
        except KeyError as e:
            self._logger.error(f"Error: column '{self._id_column}' does not exist")
            return False
        except TypeError as e:
            self._logger.error(f"Error: values in column '{self._id_column}' are not comparable")
            return False
        
        if is_progenesis_data:
            return ids.isin(unique_ids).all()
        else:
            # 'ids' represents the sample names in the metadata
            # 'unique_ids' represents sample names in the data
            # some experiments could have one metadata file for multiple data files, so we should check 
            # if the unique_ids of the data file are all contained in the metadata file.
            return set(ids) >= set(unique_ids)

    def set_target_column(self, target_column: List[str]) -> None:
        """
        Define which of the metadata columns is the targets column
        """
        if target_column not in self.get_columns():
            raise ValueError(f"'{target_column}' is not a column of the metadata. The columns are: {self.get_columns()}")
        self._target_column = target_column

    def get_target_column(self) -> List[str]:
        """
        Provide the _target_column attribute
        """
        return self._target_column

    def get_id_column(self) -> str:
        """
        Provide the _id_column attribute
        """
        return self._id_column

    def get_targets(self) -> List[str]:
        """
        return a list of all the targets
        either just the targets indicated in the column
        or "__".join() of the multiple target column selected
        """
        if self._target_column is None:
            self._logger.warning("Accessing targets before setting the column")
            return []
        return self._dataframe.loc[:, self._target_column]

    def get_selected_targets_and_ids(self, selected_targets: List[str]) -> Tuple[Tuple[str], Tuple[str]]:
        return tuple(zip(*[(target, id) for target, id in zip(self.get_targets(), self.get_samples_id()) if target in selected_targets]))

    def get_selected_targets(self, selected_targets: List[str]) -> List[str]:
        if selected_targets is None or len(selected_targets) == 0:
            raise ValueError("No target selected")
        return [target for target in self.get_targets() if target in selected_targets]

    def get_samples_id(self) -> List[str]:
        if self._id_column is None:
            self._logger.warning("Accessing samples id before setting the column")
            return []
        return self._dataframe[self._id_column].tolist()

    def metadata_is_set(self) -> bool:
        return self._dataframe is not None

    def set_target_columns(self, target_cols: List[str]) -> None:
        """
        Create the new targets and add them to the metadata dataframe
        """
        # Create the new targets from the given metadata informations (NAME__NAME)
        self.set_final_targets_values(target_cols)
        # Add the values of the final (new) targets to the dataframe of metadata (in memory)
        self.add_final_targets_col_to_dataframe()
        # Define the name of the column of targets as final_targets
        self.set_target_column("final_targets")

    def get_classes_repartition_based_on_design(self, classes_design: Dict[str, List[str]]) -> Dict[str, int]:
        """
        Retrieve the number of target for each class
        Which can be used to display the ratio of each classes in the experiment/design
        """
        target_repartition = self._dataframe["final_targets"].value_counts().to_dict()
        classes_repartition = {}
        for class_name in classes_design:
            classes_repartition[class_name] = sum([target_repartition[target] for target in classes_design[class_name]])
        return classes_repartition

# TODO: join sampleId and target in same pickle file
