from typing import List, Tuple, Union

import pandas as pd
from sklearn.model_selection import train_test_split

from . import MetaData
from ..service import Utils, init_logger
import numpy as np


class SplitGroup:
    def __init__(self, metadata: MetaData, selected_targets: List[str], train_test_proportion: float,
                 number_of_splits: int, classes_design: dict, pairing_column: str, 
                 uniq_sample_id: List[str], balance_correction: int = 0,
                 classes_repartition: Union[dict, None] = None,
                 test_split_seed: Union[int,None] = None):
        self._logger = init_logger()
        self._metadata = metadata
        self._number_of_split = number_of_splits
        self._classes_design = classes_design
        self._splits = []
        self._compute_splits(train_test_proportion, number_of_splits, pairing_column, selected_targets,
                             uniq_sample_id, balance_correction, classes_repartition, test_split_seed)

    def _compute_splits(self, train_test_proportion: float, number_of_splits: int, pairing_column: str,
                        selected_targets: List[str],  uniq_sample_id: List[str], 
                        balance_correction: int = 0,
                        classes_repartition: Union[dict, None] = None,
                        test_split_seed: Union[int,None] = None) -> None:
        """
        Create the desired number of split for the experiment. It includes/hadles the train-test repartition, the class
        balancing, the pairing of samples, the classes design, etc.

        Args:
            train_test_proportion (float): Proportion of the dataset to include in the test split.
            number_of_splits (int): total number of splits
            pairing_column (str): Column to user of the pairing. When empty ("") not pairing is done.
            selected_targets (List[str]): The selection of classes done with the interface or the automate.py (the names of the
                selected classes/targets)
                We consider selected_targets that has targets coming from multiple columns, that they are separated
                by "__" i.e. "ali__A", "med__B", etc.
            balance_correction (int, optional): balance correction to adjust proportion between classes.
                Defaults to 0. (for no balancing)
            classes_repartition (Union[dict, None], optional): . Defaults to None.
            test_split_seed (int | None, optional): Split seed number. For test purpose only,
                to be used from automate.py to test one specific split. Defaults to None.
        """
        self._logger.info("_compute_split function beginning")

        # 1 - filter out the samples having a target not included in the classification design
        # retrieve metadata dataframe
        df_filter = self._metadata.get_metadata()
        # keep only the lines for which the value in the final_targets column is in selected_targets
        df_filter = df_filter[df_filter[self._metadata.get_target_column()].isin(selected_targets)]
        # keep only the lines that correspond to samples in data file
        # (handles the cases of a metadata file for multiple data files : where samples in 
        # the metadata having corresponding targets are not in the provided data file)
        df_filter = df_filter[df_filter[self._metadata.get_id_column()].isin(uniq_sample_id)]

        # 2 - select only one sample per entity
        if pairing_column != "":
            # sort the dataframe by the pairing_column values
            df_entity = df_filter.sort_values(pairing_column)
            # group samples by the pairing column and keep only the first row of each group (.nth(0) is more stable
            # than .first())
            # Carefull : the groupby function change the index of the dataframe to the column it groups by
            df_entity = df_entity.groupby(pairing_column).nth(0)
        else:
            df_entity = df_filter

        # 2.5 - extract ids and targets, transform targets to labels
        ids = df_entity[self._metadata.get_id_column()]
        targets = df_entity[self._metadata.get_target_column()]
        labels = Utils.load_classes_from_targets(self._classes_design, targets)

        # 3- procede with the train-test division on the selected samples        
        if test_split_seed is not None:
            self._logger.debug(f"Testing split seed #{test_split_seed}")
            split_indexes: list[int] = [test_split_seed] # Test only one split seed
        else:
            split_indexes = list(range(number_of_splits)) # All splits indexes
            
        for split_index in split_indexes:
            if pairing_column == "":
                X_train, X_test, y_train, y_test = train_test_split(ids, labels, test_size=train_test_proportion,
                                                                    random_state=split_index, stratify=labels)

                # 4- retrieve the paired samples corresponding to the one in train or test set
            else:
                # random shuffle initialisation for second shuffle of samples
                rng = np.random.default_rng(seed=split_index)
                # define the ids column as the index of the dataframe, so it can be extracted with groupby().groups
                df = df_filter.set_index(self._metadata.get_id_column())
                # groups is a dictionary with 'keys' as the pairing value and 'values' as the index of the lines corresponding to the pairing
                groups = df.groupby(pairing_column).groups
                # apply the train-test division on the pairing values / the entity
                # TODO : careful check if labels is in the right order with the data
                X_train_temp, X_test_temp, y_train_temp, y_test_temp = train_test_split(df_entity.index, labels,
                                                                                        test_size=train_test_proportion,
                                                                                        random_state=split_index,
                                                                                        stratify=labels)
                # retrieve the ids corresponding the to entities in train
                X_train = []
                for representative in X_train_temp:
                    represented_pairing_value = df_filter.loc[representative][pairing_column]
                    X_train.extend(groups[represented_pairing_value])
                # retrieve targets corresponding to ids and then convert to labels
                X_train = pd.Series(X_train)
                targets = df.loc[X_train][self._metadata.get_target_column()]
                y_train = Utils.load_classes_from_targets(self._classes_design, targets)

                training_data = list(zip(X_train, y_train))
                rng.shuffle(training_data)
                X_train, y_train = zip(*training_data)

                # retrieve the ids corresponding the to entities in test
                X_test = []
                for representative in X_test_temp:
                    represented_pairing_value = df_filter.loc[representative][pairing_column]
                    X_test.extend(groups[represented_pairing_value])
                # retrieve targets corresponding to ids and then convert to labels
                X_test = pd.Series(X_test)
                targets = df.loc[X_test][self._metadata.get_target_column()]
                y_test = Utils.load_classes_from_targets(self._classes_design, targets)

                testing_data = list(zip(X_test, y_test))
                rng.shuffle(testing_data)
                X_test, y_test = zip(*testing_data)

            if balance_correction > 0:
                X_train, y_train = Utils.remove_random_samples_from_class(X_train,
                                                                          y_train,
                                                                          balance_correction,
                                                                          classes_repartition)
            X_train = list(X_train)
            y_train = list(y_train)
            X_test = list(X_test)
            y_test = list(y_test)
            
            if not self._validate_split(y_train, y_test):
                raise RuntimeError(f"_compute_split step #4 aborted for the invalid split #{split_index}.")
            
            self._splits.append([X_train, X_test, y_train, y_test])
            
        self._number_of_split = len(self._splits) # Update the number of splits if some have been removed
        
        self._logger.info("_compute_split function done")

    def load_split_with_index(self, split_index: int) -> list:
        return self._splits[split_index]

    def get_number_of_splits(self):
        """
        Return the attribute of number of split
        """
        return self._number_of_split

    def filter_sample_with_pairing_group(self, pairing_column: str) -> Tuple[List[str], List[str]]:
        """
        Function only needs the name of the column used to pair samples together.
        It retrieves other informations from the attributes (object MetaData).
        Then it iterates over all the metadata dataframe to store only one sample of each entity (entity stands for a
        biological source, like an individual). Multiple samples can originate from one entity.
        """
        metadata_dataframe = self._metadata.get_metadata()
        id_column = self._metadata.get_id_column()
        target_column = self._metadata.get_target_column()
        filtered_id = []
        filtered_target = []
        already_selected_value = set()
        # TODO : might want to change the process to sorting all lines and then picking the first one
        for index, row in metadata_dataframe.iterrows():
            if row[pairing_column] not in already_selected_value:
                already_selected_value.add(row[pairing_column])
                filtered_id.append(row[id_column])
                filtered_target.append(row[target_column])
        return filtered_id, filtered_target

    def get_selected_targets_and_ids(self, selected_targets: List[str], samples_id: List[str],
                                     targets: List[str]) -> Tuple[Tuple[str], Tuple[str]]:
        """
        Function just filters out the target/id that are not in the selected_targets list
        """
        return tuple(zip(*[(target, id) for target, id in zip(targets, samples_id) if target in selected_targets]))
    
    def _validate_split(self, y_train: list, y_test: list) -> bool:
                    # Test and train validation: they must have at least 2 classes.
        nb_test_classes: int = len(set(y_test))
        nb_train_classes: int = len(set(y_train))
        
        if nb_test_classes < 2 or nb_train_classes < 2:
            error_msg: str = "At least 2 classes must be present in both train and test splits."
            if nb_test_classes < 2:
                error_msg += f" Test set contains only the class '{next(iter(set(y_test)))}'."
            if nb_train_classes < 2:
                error_msg += f" Train set contains only the class '{next(iter(set(y_train)))}'."
            
            self._logger.error(error_msg)
            return False

        return True

