import itertools
import os
from collections import Counter
from typing import List

import numpy as np
import pandas as pd
import sklearn
import umap
from sklearn.decomposition import PCA
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    balanced_accuracy_score,
)

from ..service import Utils
from ..conf import parameters as cfg
from ..service import Utils, init_logger

ROOT_PATH = os.path.dirname(__file__)
DUMP_PATH = os.path.join(ROOT_PATH, os.path.join("dumps", "splits"))

MAX_CARDINALITY_FOR_COOCURENCE = 1000


class Results:
    """
    Contains all results of a classification design, is an attribute of class Classification_design, and gives info to class "Plotter".
    Has results of all algorithms for all splits on one classification design (so almost only numbers/floats/ints).
    Can be kept in RAM as it is not supposed to be too big, and prevents the reading/writing of models and splits files.
    """

    def __init__(self, splits_number: int):
        self._logger = init_logger()
        self.splits_number = [str(s) for s in range(splits_number)]
        self.results = {s: {} for s in self.splits_number}
        self.f_names = []
        self.best_acc = 0
        self.design_name = ""

        self.tmp = {"scaled_data": pd.DataFrame(), "y_train_true": [], "y_test_true": [], "classes": []}

    def add_results_from_one_algo_on_one_split(
            self,
            model: sklearn,
            scaled_data: pd.DataFrame,
            importance_attribute: str,
            classes: list,
            y_train_true: list,
            y_train_pred: list,
            y_test_true: list,
            y_test_pred: list,
            split_number: str,
            train_ids: List[str],
            test_ids: List[str],
    ):
        """
        Besoin modèle pour extraire features, features importance
        Besoin des y_true, des y_pred, des noms de samples pour le train et le test

        Fonction appelée à chq fois qu'un split a fini de rouler, pour stocker les info nécessaires à la production des
        graphique pour l'onglet résultat
        X : entièreté du dataset (autant train que test) c'est simplement pour voir le clustering de tous les individus
        """
        self.results[split_number]["y_test_true"] = y_test_true
        self.results[split_number]["y_test_pred"] = y_test_pred
        self.results[split_number]["y_train_true"] = y_train_true
        self.results[split_number]["y_train_pred"] = y_train_pred
        self.results[split_number]["train_accuracy"] = accuracy_score(
            y_train_true, y_train_pred
        )
        self.results[split_number]["test_accuracy"] = accuracy_score(
            y_test_true, y_test_pred
        )
        self.results[split_number]["balanced_train_accuracy"] = balanced_accuracy_score(
            y_train_true, y_train_pred
        )
        self.results[split_number]["balanced_test_accuracy"] = balanced_accuracy_score(
            y_test_true, y_test_pred
        )
        unique_classes = sorted(list(set(classes)))
        binary_y_train_true = Utils.get_binary(y_train_true, unique_classes)
        binary_y_train_pred = Utils.get_binary(y_train_pred, unique_classes)
        binary_y_test_true = Utils.get_binary(y_test_true, unique_classes)
        binary_y_test_pred = Utils.get_binary(y_test_pred, unique_classes)
        self.results[split_number]["train_precision"] = precision_score(
            binary_y_train_true, binary_y_train_pred
        )
        self.results[split_number]["test_precision"] = precision_score(
            binary_y_test_true, binary_y_test_pred
        )
        self.results[split_number]["train_recall"] = recall_score(
            binary_y_train_true, binary_y_train_pred
        )
        self.results[split_number]["test_recall"] = recall_score(
            binary_y_test_true, binary_y_test_pred
        )
        self.results[split_number]["train_f1"] = f1_score(
            binary_y_train_true, binary_y_train_pred
        )
        self.results[split_number]["test_f1"] = f1_score(
            binary_y_test_true, binary_y_test_pred
        )
        self.results[split_number]["train_roc_auc"] = roc_auc_score(
            binary_y_train_true, binary_y_train_pred
        )
        self.results[split_number]["test_roc_auc"] = roc_auc_score(
            binary_y_test_true, binary_y_test_pred
        )
        self.results[split_number][
            "failed_samples"
        ] = self.produce_always_wrong_samples(
            y_train_true,
            y_train_pred,
            y_test_true,
            y_test_pred,
            split_number,
            train_ids,
            test_ids,
        )
        self.results[split_number]["hyperparameters"] = model.get_params()
        if self.results[split_number]["test_accuracy"] > self.best_acc:
            self.best_acc = self.results[split_number]["test_accuracy"]
            self.results["best_model"] = model
        self.results[split_number][
            "feature_importances"
        ] = self._get_features_importance(model, importance_attribute)
        self.results[split_number]["Confusion_matrix"] = self._produce_conf_matrix(
            y_test_true, y_test_pred
        )
        self.update_tmp(scaled_data, y_train_true, y_test_true, classes)


    def compute_remaining_results_on_all_splits(self, samples_id: list):
        if len(samples_id) != len(self.tmp["classes"]):
            raise ValueError("samples_id and classes should have the same length")

        self.results["info_expe"] = self._produce_info_expe(
            self.tmp["y_train_true"], self.tmp["y_test_true"]
        )
        self.results["features_table"] = self.produce_features_importance_table()
        self.results["accuracies_table"] = self.produce_accuracy_plot_all()
        self.results["classes"] = self.tmp["classes"]
        self.results["umap_data"] = self._produce_UMAP(
            self.tmp["scaled_data"], self.results["features_table"]
        )
        self.results["3d_umap_data"] = self._produce_UMAP(
            self.tmp["scaled_data"], self.results["features_table"], n_components=3
        )
        self.results["pca_data"] = self._produce_PCA(
            self.tmp["scaled_data"], self.results["features_table"]
        )
        self.results["3d_pca_data"] = self._produce_PCA(
            self.tmp["scaled_data"], self.results["features_table"], n_components=3
        )
        self.results["metrics_table"] = self.produce_metrics_table()
        self.results[
            "features_stripchart"
        ] = self.features_strip_chart_abundance_each_class(
            self.results["features_table"], self.tmp["scaled_data"]
        )
        self.results["features_2d_and_3d"] = self.produce_features_2d_and_3d(
            self.results["features_table"], self.tmp["scaled_data"]
        )
        self.results["coocurence_matrix"] = self.produce_coocurence_matrix()
        self.results["samples_id"] = samples_id
            

    def set_feature_names(self, x: pd.DataFrame):
        """
        retrieve features name directly from datamatrix
        """
        self.f_names = list(x.columns)

    def format_name_and_associated_values(self, names, values):
        """
        Aggregate statistics for used features.
        """
        df = pd.DataFrame({"name": names, "value": values})
        # Replace 0 by Nans so we dont count them in the statistics
        df = df.replace(0, value=np.nan)
        df = df.groupby(by="name").agg(['count', 'mean', 'std']).reset_index()

        # Replace Nans back to zeros
        df = df.fillna(0)

        # This will get a dictionnary where keys are names and values is a list of [count, mean, std]
        aggregated_statistics = df.set_index("name").T.to_dict("list")

        return aggregated_statistics


    def _produce_conf_matrix(self, y_test_true: list, y_test_pred: list):
        labels = list(set(y_test_true))
        return labels, confusion_matrix(
            y_test_true, y_test_pred, labels=labels, normalize="true"
        )

    def _produce_UMAP(self, X: pd.DataFrame, features_df: pd.DataFrame, n_components: int = 2):
        features = cfg.features
        umaps = []
        for nbr in features:
            selected_feat = features_df["features"][:nbr]
            selected_x = X.loc[:, selected_feat]
            selected_x = selected_x.to_numpy()
            umap_data = umap.UMAP(n_components=n_components, init="random", random_state=13, n_jobs=1)
            umaps.append(umap_data.fit_transform(selected_x))

        # Do the umap for all used metrics
        selected_feat = features_df.loc[features_df["times_used"] > 0]["features"]
        if selected_feat.shape[0] < 3:
            selected_feat = features_df["features"][:3]
        selected_x = X.loc[:, selected_feat]
        selected_x = selected_x.to_numpy()
        umap_data = umap.UMAP(n_components=n_components, init="random", random_state=13, n_jobs=1)
        umaps.append(umap_data.fit_transform(selected_x))

        # Redo the umap but on all the data
        selected_x = X.to_numpy()
        umap_data = umap.UMAP(n_components=n_components, init="random", random_state=13, n_jobs=1)
        umaps.append(umap_data.fit_transform(selected_x))
        return umaps

    def _produce_PCA(self, X: pd.DataFrame, features_df: pd.DataFrame, n_components: int = 2):
        nbr_feat = cfg.features
        pcas = []
        labels = []

        for nbr in nbr_feat:
            selected_feat = features_df["features"][:nbr]
            x = X.loc[:, selected_feat]
            x = x.to_numpy()

            pca = PCA(n_components=n_components)
            pcas.append(pca.fit_transform(x))
            labels.append(
                {str(i): f"PC {i + 1} ({var:.1f}%)" for i, var in enumerate(pca.explained_variance_ratio_ * 100)})

        # Do the PCA for all used feature
        selected_feat = features_df.loc[features_df["times_used"] > 0]["features"]
        if selected_feat.shape[0] < 3:
            selected_feat = features_df["features"][:3]

        x = X.loc[:, selected_feat]
        pca = PCA(n_components=n_components)
        pcas.append(pca.fit_transform(x))
        labels.append({str(i): f"PC {i + 1} ({var:.1f}%)" for i, var in enumerate(pca.explained_variance_ratio_ * 100)})

        # Redo the PCA but on all the data
        x = X.to_numpy()
        pca = PCA(n_components=n_components)
        pcas.append(pca.fit_transform(x))
        labels.append({str(i): f"PC {i + 1} ({var:.1f}%)" for i, var in enumerate(pca.explained_variance_ratio_ * 100)})

        return pcas, labels

    def _produce_info_expe(self, y_train_true, y_test_true):
        """
        produce dataframe with basic information about the dataset/experiment, like number of samples and the train-test
        proprotion, the number of class, etc.
        """
        nbr_train = len(y_train_true)
        nbr_test = len(y_test_true)
        tot = nbr_train + nbr_test
        ratio_test = round(nbr_test / tot * 100)
        ratio_train = 100 - ratio_test
        nom_stats = ["Number of samples", "Number of splits", "Train-test repartition"]
        valeurs_stats = [str(tot)]
        valeurs_stats.append(len(self.splits_number))
        valeurs_stats.append(str(ratio_train) + "% - " + str(ratio_test) + "%")
        y = y_train_true + y_test_true
        c = Counter(y)
        for k in c.keys():
            nom_stats.append("Number of class {}".format(k))
            valeurs_stats.append("{}".format(c[k]))

        d = {"stats": nom_stats, "numbers": valeurs_stats}
        df = pd.DataFrame(data=d)
        return df

    def produce_features_importance_table(self):
        """
        Fonction qui réccupère les features et leurs importances de chq split sur le train et le test pour en faire un dataframe.
        Est donnée à la fonction de plotting correspondante (après que l'instance ait été complétée avec tous
        les résultats de splits)
        """
        (
            features,
            times_used_all_splits,
            importance_or_usage_or_,
            std
        ) = self._aggregate_features_info()
        # print("--> aggregating done, importances : {}".format(importance_or_usage_or_))

        d = {
            "features": features,
            "times_used": times_used_all_splits,
            "importance_usage": importance_or_usage_or_,
            "std": std
        }
        df = pd.DataFrame(data=d)
        df["times_used"] = pd.to_numeric(df["times_used"])
        df["importance_usage"] = pd.to_numeric(df["importance_usage"])
        df["std"] = pd.to_numeric(df["std"])
        df = df.sort_values(by=["importance_usage"], ascending=False)
        return df

    def produce_accuracy_plot_all(self):
        """
        Retrieve balanced accuracies from every splits on train and test to make a dataframe
        The return is used by corresponding ploting function
        """
        x_splits_num = []
        y_splits_acc = []
        traces = []
        for s in self.splits_number:
            x_splits_num.append(str(s))  # c'est normal
            x_splits_num.append(str(s))
            y_splits_acc.append(self.results[s]["balanced_train_accuracy"])
            traces.append("train")
            y_splits_acc.append(self.results[s]["balanced_test_accuracy"])
            traces.append("test")

        d = {"splits": x_splits_num, "balanced accuracies": y_splits_acc, "color": traces}
        df = pd.DataFrame(data=d)

        return df

    # TODO: faire une fonction qui produce metrics table pour tous les splits
    def produce_metrics_table(self):
        metrics = [
            "accuracy",
            "balanced accuracy",
            "precision",
            "recall",
            "f1",
            "roc_auc",
        ]
        trains_metrics = []
        tests_metrics = []
        acctrain = []
        acctest = []
        balacctrain = []
        balacctest = []
        precisiontrain = []
        precisiontest = []
        recalltrain = []
        recalltest = []
        f1train = []
        f1test = []
        roc_auc_train = []
        roc_auc_test = []
        for s in self.splits_number:
            acctrain.append(self.results[s]["train_accuracy"])
            acctest.append(self.results[s]["test_accuracy"])
            balacctrain.append(self.results[s]["balanced_train_accuracy"])
            balacctest.append(self.results[s]["balanced_test_accuracy"])
            precisiontrain.append(self.results[s]["train_precision"])
            precisiontest.append(self.results[s]["test_precision"])
            recalltrain.append(self.results[s]["train_recall"])
            recalltest.append(self.results[s]["test_recall"])
            f1train.append(self.results[s]["train_f1"])
            f1test.append(self.results[s]["test_f1"])
            roc_auc_train.append(self.results[s]["train_roc_auc"])
            roc_auc_test.append(self.results[s]["test_roc_auc"])

        trains_metrics.append(
            str(round(float(np.mean(acctrain)), 4))
            + " ("
            + str(round(float(np.std(acctrain)), 4))
            + ")"
        )
        trains_metrics.append(
            str(round(float(np.mean(balacctrain)), 4))
            + " ("
            + str(round(float(np.std(balacctrain)), 4))
            + ")"
        )
        trains_metrics.append(
            str(round(float(np.mean(precisiontrain)), 4))
            + " ("
            + str(round(float(np.std(precisiontrain)), 4))
            + ")"
        )
        trains_metrics.append(
            str(round(float(np.mean(recalltrain)), 4))
            + " ("
            + str(round(float(np.std(recalltrain)), 4))
            + ")"
        )
        trains_metrics.append(
            str(round(float(np.mean(f1train)), 4))
            + " ("
            + str(round(float(np.std(f1train)), 4))
            + ")"
        )
        trains_metrics.append(
            str(round(float(np.mean(roc_auc_train)), 4))
            + " ("
            + str(round(float(np.std(roc_auc_train)), 4))
            + ")"
        )

        tests_metrics.append(
            str(round(float(np.mean(acctest)), 4))
            + " ("
            + str(round(float(np.std(acctest)), 4))
            + ")"
        )
        tests_metrics.append(
            str(round(float(np.mean(balacctest)), 4))
            + " ("
            + str(round(float(np.std(balacctest)), 4))
            + ")"
        )
        tests_metrics.append(
            str(round(float(np.mean(precisiontest)), 4))
            + " ("
            + str(round(float(np.std(precisiontest)), 4))
            + ")"
        )
        tests_metrics.append(
            str(round(float(np.mean(recalltest)), 4))
            + " ("
            + str(round(float(np.std(recalltest)), 4))
            + ")"
        )
        tests_metrics.append(
            str(round(float(np.mean(f1test)), 4))
            + " ("
            + str(round(float(np.std(f1test)), 4))
            + ")"
        )
        tests_metrics.append(
            str(round(float(np.mean(roc_auc_test)), 4))
            + " ("
            + str(round(float(np.std(roc_auc_test)), 4))
            + ")"
        )

        metrics_table = pd.DataFrame(
            data={"metrics": metrics, "train": trains_metrics, "test": tests_metrics}
        )
        return metrics_table

    def features_strip_chart_abundance_each_class(self, feature_df, data):
        """
        store data for the 10 most important feature (mean of all split)
        as well as the class for each sample
        allows ploting the stripchart in Plots
        """
        number_of_used_features = len(feature_df[feature_df["importance_usage"] > 0])
        strip_charts = []
        n_features = cfg.features + [number_of_used_features]
        for ind in n_features:
            important_features = list(feature_df["features"])[:ind]
            df = data.loc[:, important_features]
            df["targets"] = self.results["classes"]
            strip_charts.append(df)
        return strip_charts

    def produce_always_wrong_samples(
            self,
            y_train_true,
            y_train_pred,
            y_test_true,
            y_test_pred,
            split_number,
            train_ids: List[str],
            test_ids: List[str],
    ):
        """
        return: two dicts with sample names as keys, and wrongly predicted as values (0:good pred, 1:bad pred)
        """

        train_samples = {t: 0 for t in train_ids}
        test_samples = {t: 0 for t in test_ids}

        labels = {l: idx for idx, l in enumerate(list(set(y_train_true)))}

        y_train_true = [labels[l] for l in y_train_true]
        y_train_pred = [labels[l] for l in y_train_pred]
        y_test_true = [labels[l] for l in y_test_true]
        y_test_pred = [labels[l] for l in y_test_pred]

        train_nbr = [sum(x) for x in list(zip(y_train_true, y_train_pred))]
        for i, n in enumerate(train_ids):
            if train_nbr[i] == 1:
                train_samples[n] += 1

        test_nbr = [sum(x) for x in list(zip(y_test_true, y_test_pred))]
        for i, n in enumerate(test_ids):
            if test_nbr[i] == 1:
                test_samples[n] += 1

        return train_samples, test_samples

    def produce_features_2d_and_3d(self, features_table: pd.DataFrame, scaled_data):
        selected_features = features_table[:3]["features"]
        return scaled_data.loc[:, selected_features]

    def update_tmp(self, scaled_data, y_train_true, y_test_true, classes):
        if self.tmp["scaled_data"].empty:
            self.tmp["scaled_data"] = scaled_data
        if not self.tmp["y_train_true"]:
            self.tmp["y_train_true"] = y_train_true
        if not self.tmp["y_test_true"]:
            self.tmp["y_test_true"] = y_test_true
        if not self.tmp["classes"]:
            self.tmp["classes"] = classes

    def _get_features_importance(self, model, importance_attribute):
        """
        retrieve features and their importance from a model to save it in the Results dict after each split
        """
        if self.f_names is None:
            raise RuntimeError("Features names are not retrieved yet")

        if hasattr(model, importance_attribute):
            importances = getattr(model, importance_attribute)
            if len(importances) == 1 and len(importances[0]) == len(self.f_names):
                importances = importances[0]
        elif hasattr(model, 'rule_importances_'):
            importances = [0] * len(self.f_names)
            for rule, f_importance in zip(model.model_.rules, model.rule_importances_):
                importances[rule.feature_idx] = f_importance
        zipped = zip(self.f_names, importances)
        return list(zipped)

    def _aggregate_features_info(self):
        """
        When all splits are done and saved, aggregate feature info from every split to compute stats
        from all splits, concatenate in the same list the name of features, and another list their importance
        """
        features = []
        imp = []
        # Get values of all splits in two lists
        for split in self.splits_number:
            f, i = list(zip(*self.results[split]["feature_importances"]))
            features.extend(f)
            imp.extend(i)

        # Store the mean importance, and the number of time used, per feature
        count_f = self.format_name_and_associated_values(features, imp)

        features = [f for f in count_f.keys()]
        times_used_all_splits = [count_f[f][0] for f in count_f.keys()]
        importance_or_usage_or_ = [count_f[f][1] for f in count_f.keys()]
        std = [count_f[f][2] for f in count_f.keys()]
        return features, times_used_all_splits, importance_or_usage_or_, std

    def produce_coocurence_matrix(self):

        features = list(zip(*self.results["0"]["feature_importances"]))[0]
        splits = [split for split in self.results.keys() if split.isdigit()]

        weight_matrix = pd.DataFrame(0, columns=features, index=splits)
        for split, values in self.results.items():
            if split.isdigit():
                for feature, weight in values['feature_importances']:
                    if weight > 0:
                        weight_matrix.loc[split, feature] = 1
        weight_matrix = weight_matrix.loc[:, (weight_matrix != 0).any(axis=0)]
        features = list(weight_matrix.columns)

        # Mean of importance for all features
        mean_importance = weight_matrix.mean(axis=0)
        number_of_nodes = len(mean_importance)
        cardinality = (number_of_nodes * (number_of_nodes - 1)) / 2
        if cardinality > MAX_CARDINALITY_FOR_COOCURENCE:
            return None, None, None, cardinality

        all_pairs = []
        for split in splits:
            split_features = weight_matrix.loc[split][weight_matrix.loc[split] == 1].index

            pairs = list(itertools.combinations(split_features, 2))
            all_pairs.extend(pairs)

        counter = Counter(all_pairs)
        return counter, mean_importance, len(splits), int(cardinality)

# Kept old classes for compatibility
class ResultsDT(Results):
    pass


class ResultsRF(Results):
    pass


class ResultsSCM(Results):
    pass


class ResultsRSCM(Results):
    pass
