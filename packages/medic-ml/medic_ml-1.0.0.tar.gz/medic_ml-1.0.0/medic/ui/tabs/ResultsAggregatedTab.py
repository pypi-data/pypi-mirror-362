from collections import Counter

import dash_bootstrap_components as dbc
import numpy as np
from dash import html, dcc, Output, Input, State, dash, Dash

from .MetaTab import MetaTab
from ...service import Plots, init_logger, log_exceptions
from ...domain import MetaboController

CONFIG = {
    "toImageButtonOptions": {
        "format": "svg",  # one of png, svg, jpeg, webp
        "height": None,
        "width": None,
        "scale": 1,  # Multiply title/legend/axis/canvas sizes by this factor
    }
}


class ResultsAggregatedTab(MetaTab):
    def __init__(self, app: Dash, metabo_controller: MetaboController):
        super().__init__(app, metabo_controller)
        self._logger = init_logger()
        self.r = self.metabo_controller.get_all_results()
        self._plots = Plots("blues")

    def getLayout(self) -> dbc.Tab:
        _resultsMenuDropdowns = dbc.Card(
            className="results_menu_dropdowns",
            children=[
                dbc.CardBody(
                    [
                        html.Div(
                            className="dropdowns",
                            children=[
                                html.H6("Classification Design : "),
                                dbc.Select(
                                    id="design_dropdown_summary",
                                    className="form_select",
                                    options=[{"label": "None", "value": "None"}],
                                    value="None",
                                ),
                                dcc.Store(id='design_dropdown_summary_store', storage_type='session'),
                            ],
                        ),
                        dbc.Button(
                            "Load",
                            color="primary",
                            id="load_results_button",
                            className="custom_buttons",
                            n_clicks=0,
                        ),
                        html.Div(id="output_button_load_results"),
                    ],
                    id="all_algo_results",
                )
            ],
        )
        
        __currentExperimentInfo = dbc.Card(
            children=[
                dbc.CardBody(
                    children=[
                        html.H6(
                            "Current experiment info"
                        ),  
                        dcc.Loading(
                            id="loading_expe_table_summary",
                            children=html.Div(id="expe_table_summary", children=""),
                            type="circle",
                        ),
                    ]
                )
            ],
            className="w-25",
        )

        _resultsInfo = html.Div(
            className="Results_info",
            children=[
                _resultsMenuDropdowns,
                __currentExperimentInfo,
            ],
        )


        _heatmapUsedFeatures = html.Div(
            className="umap_plot_and_title",
            children=[
                html.Div(
                    className="title_and_help",
                    children=[
                        html.H6("Features Usage"),
                        dbc.Button(
                            "[?]",
                            className="text-muted btn-secondary popover_btn",
                            id="help_heatmapFeatures",
                        ),
                        dbc.Popover(
                            children=[dbc.PopoverBody("Blablabla wout wout")],
                            id="pop_help_heatmapFeatures",
                            is_open=False,
                            target="help_hHeatmapFeatures",
                        ),
                    ],
                ),
                dcc.Loading(
                    dcc.Graph(id="heatmapFeatures", config=CONFIG),
                    type="dot",
                    color="#13BD00",
                ),
                dcc.Slider(-3, 0, 0.1,
                           id='slider_heatmapFeatures',
                           marks={i: '{}'.format(10 ** i) for i in range(-3, 1, 1)},
                           value=-2,
                           updatemode='drag',
                           ),
            ],
        )

        _heatmapSamplesAlwaysWrong = html.Div(
            className="umap_plot_and_title",
            children=[
                html.Div(
                    className="title_and_help",
                    children=[
                        html.H6("Errors on samples in test"),
                        dbc.Button(
                            "[?]",
                            className="text-muted btn-secondary popover_btn",
                            id="help_heatmapSamples",
                        ),
                        dbc.Popover(
                            children=[dbc.PopoverBody("Blablabla wout wout")],
                            id="pop_help_heatmapSamples",
                            is_open=False,
                            target="help_heatmapSamples",
                        ),
                    ],
                ),
                dcc.Loading(
                    dcc.Graph(id="heatmapSamples", config=CONFIG),
                    type="dot",
                    color="#13BD00",
                ),
                # dcc.Slider(min=0, max=3, step=1, value=0, marks={0: "10", 1: "40", 2: "100", 3: "All"},
                #            id="features_stripChart_dropdown")
            ],
        )

        _barplotComparaisonAlgo = html.Div(
            className="umap_plot_and_title",
            children=[
                html.Div(
                    className="title_and_help",
                    children=[
                        html.H6("Comparaison of algorithms performances"),
                        dbc.Button(
                            "[?]",
                            className="text-muted btn-secondary popover_btn",
                            id="help_barplotAlgo",
                        ),
                        dbc.Popover(
                            children=[dbc.PopoverBody("Blablabla wout wout")],
                            id="pop_help_barplotAlgo",
                            is_open=False,
                            target="help_barplotAlgo",
                        ),
                    ],
                ),
                dcc.Loading(
                    dcc.Graph(id="barplotAlgo", config=CONFIG),
                    type="dot",
                    color="#13BD00",
                ),
            ],
        )

        return dbc.Tab(
            className="global_tab",
            label="Results aggregated",
            children=[
                _resultsInfo,
                html.Div(
                    className="fig_group",
                    children=[
                        _barplotComparaisonAlgo
                    ],
                ),
                html.Div(className="fig_group", children=[
                    _heatmapSamplesAlwaysWrong,
                    _heatmapUsedFeatures
                ]),
            ],
        )
        # html.Div(className="column_content",
        #          # WARNING !! : _infoFigure is not with the card, it's in a separate column
        #          children=[_heatmapSamplesAlwaysWrong])])])

    def _registerCallbacks(self) -> None:
        @self.app.callback(
            [
                Output("design_dropdown_summary", "options"),
                Output("design_dropdown_summary", "value"),
            ],
            Input("custom_big_tabs", "active_tab"),
            State('design_dropdown_summary_store', 'data'),
        )
        @log_exceptions(self._logger)
        def update_results_dropdown_design(active, stored_value):
            if active == "tab-4":
                try:
                    self.r = self.metabo_controller.get_all_results()
                    a = list(self.r.keys())
                    if stored_value is not None and stored_value in a:
                        return [{"label": i, "value": i} for i in a], stored_value
                    return [{"label": i, "value": i} for i in a], a[0]
                except:  # TODO: wrong practice ???
                    return dash.no_update, dash.no_update
            else:
                return dash.no_update, dash.no_update

        @self.app.callback(
            Output('design_dropdown_summary_store', 'data'),
            Input('load_results_button', 'n_clicks'),
            State('design_dropdown_summary', 'value')
        )
        def save_design_dropdown_summary_value(_, value):
            return value
        
        @self.app.callback(
            [
                Output("expe_table_summary", "children")
            ],
            [
                Input("load_results_button", "n_clicks")
            ],
            [
                State("design_dropdown_summary", "value")
            ],
        )
        @log_exceptions(self._logger)
        def get_experiment_statistics(_, design_name):
            if design_name == "None":
                return dash.no_update
            
            df = self.r[design_name][list(self.r[design_name].keys())[0]].results["info_expe"]
            table_body = self._plots.show_exp_info_all(df)
            table = dbc.Table(
                table_body, id="table_exp_info", borderless=True, hover=True
            )
            return [table]

        @self.app.callback(
            [
                Output("heatmapFeatures", "figure"),
            ],
            [Input("load_results_button", "n_clicks"),
             Input("slider_heatmapFeatures", "value")],
            [State("design_dropdown_summary", "value"),
             ],
        )
        @log_exceptions(self._logger)
        def show_heatmap_features_usage(n_clicks, log_importance_threshold, design):
            if n_clicks >= 1:

                importance_threshold = 10 ** log_importance_threshold

                algos = list(self.r[design].keys())
                global_df = None
                for a in algos:
                    if global_df is None:
                        self._logger.info("Global df is none")
                        global_df = self.r[design][a].results["features_table"]
                        global_df = global_df.loc[
                            :, ("features", "importance_usage")
                        ]  # reduce dataframe to 2 columns
                        global_df.rename(
                            columns={"importance_usage": a}, inplace=True
                        )  # rename column to identify algorithm
                    else:
                        self._logger.info(f"Global df not none, algo : {a}")
                        df = self.r[design][a].results[
                            "features_table"
                        ]  # retrieve features table of algo a
                        df = df.loc[
                            :, ("features", "importance_usage")
                        ]  # reduce dataframe to 2 columns
                        df.rename(
                            columns={"importance_usage": a}, inplace=True
                        )  # rename column to identify algorithm
                        global_df = global_df.merge(
                            df, how="outer", on="features"
                        )  # join data with global dataset

                global_df = global_df.set_index("features")
                global_df = global_df.fillna(0)

                global_df = global_df.loc[global_df.max(axis=1) >= importance_threshold]

                hm_fig = self._plots.show_heatmap_features_usage(global_df, importance_threshold)

                return [hm_fig]
            else:
                return dash.no_update

        @self.app.callback(
            Output("heatmapSamples", "figure"),
            [Input("load_results_button", "n_clicks")],
            State("design_dropdown_summary", "value"),
        )
        @log_exceptions(self._logger)
        def show_heatmap_samples_always_wrong(n_clicks, design):
            if n_clicks >= 1:
                algos = list(self.r[design].keys())

                data_train = []
                data_test = []
                all_samples = []

                for i, a in enumerate(algos):
                    data_train.append([])
                    data_test.append([])
                    train = []
                    test = []
                    for j, s in enumerate(self.r[design][a].splits_number):
                        train_d, test_d = self.r[design][a].results[s]["failed_samples"]
                        train.append(train_d)
                        test.append(test_d)

                    counter_train = Counter()
                    for d in train:
                        counter_train.update(d)

                    counter_test = Counter()
                    for d in test:
                        counter_test.update(d)

                    all_samples = list(counter_train.keys()) + list(counter_test.keys())
                    for s in all_samples:
                        if s in counter_train.keys():
                            data_train[i].append(counter_train[s])
                        else:
                            data_train[i].append(0)

                        if s in counter_test.keys():
                            data_test[i].append(counter_test[s])
                        else:
                            data_test[i].append(0)

                data_train = np.array(data_train).T
                data_test = np.array(data_test).T

                fig = self._plots.show_heatmap_wrong_samples(
                    data_train, data_test, all_samples, algos
                )

                return fig
            else:
                return dash.no_update

        @self.app.callback(
            Output("barplotAlgo", "figure"),
            [Input("load_results_button", "n_clicks")],
            State("design_dropdown_summary", "value"),
        )
        @log_exceptions(self._logger)
        def show_barplot_compare_accuracy_algo(n_clicks, design_name):
            """
            retrieve balanced accuracy values now
            """
            if n_clicks >= 1:
                algos = list(self.r[design_name].keys())

                train_acc = []
                train_std = []
                test_acc = []
                test_std = []
                for a in algos:
                    df = self.r[design_name][a].results["metrics_table"]
                    train_m, train_s = df["train"][1].split("(")
                    train_acc.append(float(train_m))
                    train_std.append(float(train_s.split(")")[0]))

                    test_m, test_s = df["test"][1].split("(")
                    test_acc.append(float(test_m))
                    test_std.append(float(test_s.split(")")[0]))

                fig = self._plots.show_barplot_comparaison_algo(algos, train_acc, train_std, test_acc, test_std)
                return fig
            else:
                return dash.no_update

