import os
import time

import dash_bootstrap_components as dbc
import dash_interactive_graphviz as dg
import pandas as pd
from dash import html, dcc, Output, Input, State, dash, Dash
import dash_cytoscape as cyto
from matplotlib import pyplot as plt
from sklearn import tree

from ...conf import parameters as cfg
from . import utils
from .MetaTab import MetaTab
from ...domain import MetaboController
from ...service import Plots, Utils, init_logger, log_exceptions

PATH_TO_BIGRESULTS = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "big_results.p")
)

CONFIG = {
    "toImageButtonOptions": {
        "format": "svg",  # one of png, svg, jpeg, webp
        "height": None,
        "width": None,
        "scale": 1,  # Multiply title/legend/axis/canvas sizes by this factor
    }
}


class ResultsTab(MetaTab):
    def __init__(self, app: Dash, metabo_controller: MetaboController):
        super().__init__(app, metabo_controller)
        self._logger = init_logger()
        # self.r = pkl.load(open(PATH_TO_BIGRESULTS, "rb"))
        self.r = self.metabo_controller.get_all_results()
        self._plots = Plots("blues")

    def getLayout(self) -> dbc.Tab:
        __resultsMenuDropdowns = dbc.Card(
            className="results_menu_dropdowns",
            children=[
                dbc.CardBody(
                    [
                        html.Div(
                            className="dropdowns",
                            children=[
                                html.H6("Classification Design : "),
                                dbc.Select(
                                    id="design_dropdown",
                                    className="form_select",
                                    options=[{"label": "None", "value": "None"}],
                                    value="None",
                                ),
                            ],
                        ),
                        html.Div(
                            className="dropdowns",
                            children=[
                                html.H6("ML Algorithm : "),
                                dbc.Select(
                                    id="ml_dropdown",
                                    className="form_select",
                                    options=[{"label": "None", "value": "None"}],
                                    value="None",
                                ),
                            ],
                        ),
                        dbc.Button(
                            "Load",
                            color="primary",
                            id="load_ML_results_button",
                            className="custom_buttons",
                            n_clicks=0,
                        ),
                        html.Div(id="output_button_load_ML_results"),
                    ],
                    id="menu_results",
                )
            ],
        )

        __currentExperimentInfo = dbc.Card(
            children=[
                dbc.CardBody(
                    children=[
                        html.H6(
                            "Current experiment info"
                        ),  # , style={"marginTop": 25},
                        # html.Div(id="view_info", children=[
                        dcc.Loading(
                            id="loading_expe_table",
                            children=html.Div(id="expe_table", children=""),
                            type="circle",
                        ),
                        # dcc.Loading(id="loading-1", children=[html.Div(id="loading-output-1")],
                        #             type="dot", color="#13BD00")
                    ]
                )
            ],
            className="w-25",
        )

        _resultsInfo = html.Div(
            className="Results_info",
            children=[
                __resultsMenuDropdowns,
                __currentExperimentInfo,
            ],
        )

        ___pcaPlot = html.Div(
            className="pca_plot_and_title",
            children=[
                html.Div(
                    className="title_and_help",
                    children=[
                        html.H6("PCA", id="PCA_title"),
                        dcc.RadioItems(
                            id='pca_dimensions',
                            options=[
                                {'label': ' 2D', 'value': '2d'},
                                {'label': ' 3D', 'value': '3d'},
                            ],
                            value='2d',
                            labelStyle={'margin': 'auto', 'padding': '5px'},
                            inline=True
                        ),
                    ],
                    style={"display": "flex", "justify-content": "space-between"},
                ),
                # Should we put the title on the plot?
                dcc.Loading(
                    dcc.Graph(id="PCA", config=CONFIG), type="dot", color="#13BD00"
                ),
                dcc.Slider(
                    step=None,
                    value=1,
                    marks={**cfg.default_marks, **cfg.all_mark},
                    id="pca_slider",
                ),
            ],
        )

        ___umap = html.Div(
            className="umap_plot_and_title",
            children=[
                html.Div(
                    className="title_and_help",
                    children=[
                        html.H6("Umap"),
                        dcc.RadioItems(
                            id='umap_dimensions',
                            options=[
                                {'label': ' 2D', 'value': '2d'},
                                {'label': ' 3D', 'value': '3d'},
                            ],
                            value='2d',
                            # add space between radio and label
                            labelStyle={'margin': 'auto', 'padding': '5px'},
                            inline=True

                        ),
                    ],
                    style={"display": "flex", "justify-content": "space-between"},
                ),
                dcc.Loading(
                    dcc.Graph(id="umap_overview", config=CONFIG),
                    type="dot",
                    color="#13BD00",
                ),
                dcc.Slider(
                    step=None,
                    value=1,
                    marks={**cfg.default_marks, **cfg.all_mark},
                    id="umap_slider",
                )
            ],
        )

        ___2dPlot = html.Div(
            className="umap_plot_and_title",
            children=[
                html.Div(
                    className="title_and_help",
                    children=[
                        html.H6("2D"),
                        dbc.Button(
                            "[?]",
                            className="text-muted btn-secondary popover_btn",
                            id="help_2dPlot",
                        ),
                        dbc.Popover(
                            children=[dbc.PopoverBody("Blablabla wout wout")],
                            id="pop_help_2dPlot",
                            is_open=False,
                            target="help_2dPlot",
                        ),
                    ],
                ),
                dcc.Loading(
                    dcc.Graph(id="2d_overview", config=CONFIG),
                    type="dot",
                    color="#13BD00",
                ),
            ],
        )

        ___3dPlot = html.Div(
            className="umap_plot_and_title",
            children=[
                html.Div(
                    className="title_and_help",
                    children=[
                        html.H6("3D"),
                        dbc.Button(
                            "[?]",
                            className="text-muted btn-secondary popover_btn",
                            id="help_3dPlot",
                        ),
                        dbc.Popover(
                            children=[dbc.PopoverBody("Blablabla wout wout")],
                            id="pop_help_3dPlot",
                            is_open=False,
                            target="help_3dPlot",
                        ),
                    ],
                ),
                dcc.Loading(
                    dcc.Graph(id="3d_overview", config=CONFIG),
                    type="dot",
                    color="#13BD00",
                ),
            ],
        )

        __dataResultTab = dbc.Tab(
            className="sub_tab",
            label="Data",
            children=[
                html.Div(className="fig_group", children=[___pcaPlot, ___umap]),
                html.Div(className="fig_group", children=[___2dPlot, ___3dPlot]),
            ],
        )

        ___accuracyPlot = html.Div(
            className="acc_plot_and_title",
            children=[
                html.Div(
                    className="title_and_help",
                    children=[
                        html.H6("Balanced accuracy plot"),
                        dbc.Button(
                            "[?]",
                            className="text-muted btn-secondary popover_btn",
                            id="help_accPlot",
                        ),
                        dbc.Popover(
                            children=[
                                dbc.PopoverBody(
                                    "Accuracies for each split on train and test set. Here you would want to check"
                                    "the difference between each set, because a really good train performance and a mediocre"
                                    "or bad test performance is a sign of over-fitting."
                                )
                            ],
                            id="pop_help_accPlot",
                            is_open=False,
                            target="help_accPlot",
                        ),
                    ],
                ),
                dcc.Loading(
                    dcc.Graph(id="accuracy_overview", config=CONFIG),
                    type="dot",
                    color="#13BD00",
                ),
            ],
        )

        ___globalMetric = html.Div(
            className="w-25",
            children=[
                html.H6("Global confusion matrix"),
                dcc.Loading(
                    dcc.Graph(id="conf_matrix", config=CONFIG),
                    type="dot",
                    color="#13BD00",
                ),
            ],
        )
        ___specificFilters = html.Div(
            className="fig_group_col",
            children=[
                html.Div(
                    className="",
                    children=[
                        html.H6("Splits number"),
                        dbc.Select(
                            id="splits_dropdown",
                            className="form_select_large",
                            options=[{"label": "None", "value": "None"}],
                            value="None",
                        ),
                        dbc.Button(
                            "Update",
                            color="primary",
                            id="update_specific_results_button",
                            className="custom_buttons",
                            n_clicks=0,
                        ),
                        html.Div(id="output_button_update_specific_results"),
                    ],
                ),
                html.Div(
                    className="",
                    style={"display": "flex", "width": "100%"},
                    children=[
                        html.Div(
                            children=[
                                html.H6("Confusion matrix"),
                                dcc.Loading(
                                    dcc.Graph(id="split_conf_matrix", config=CONFIG),
                                    type="dot",
                                    color="#13BD00",
                                ),
                            ],
                        ),
                        html.Div(
                            children=[
                                html.H6("Table of used hyperparameter"),
                                dcc.Loading(
                                    html.Div(id="hyperparam_table", children="", style={"margin-top": "2em"}),
                                ),
                            ],
                        )
                    ],
                ),
            ],
        )
        ___metricsTable = html.Div(
            className="table_features",
            children=[
                html.H6("Metrics table : mean(std)"),
                dcc.Loading(
                    id="loading_metrics_table",
                    children=html.Div(id="metrics_score_table", children=""),
                    type="circle",
                ),
            ],
        )

        __algoResultsTab = dbc.Tab(
            className="sub_tab",
            label="Algorithm",
            children=[
                html.Div(
                    className="fig_group",
                    children=[
                        ___accuracyPlot,
                        # ___globalMetric,
                        ___metricsTable,
                    ],
                ),
                html.Div(className="fig_group", children=[___specificFilters]),
            ],
        )

        __DTTreeTab = dbc.Tab(
            id="DTTT", className="sub_tab", label="DT Tree", disabled=True,
            children=[
                html.Div(dg.DashInteractiveGraphviz(
                    id="DTTT_graph"
                ),
                    style={"letter-spacing": "0"}),
            ]
        )

        ___featuresTable = html.Div(
            className="table_features",
            children=[
                html.H6("Top 10 features sorted by importance"),
                dbc.Button(
                    "Export",
                    color="primary",
                    id="export_features",
                    className="custom_buttons",
                    n_clicks=0,
                ),
                dcc.Download(id="download_dataframe_csv"),
                dcc.Loading(
                    id="loading_features_table",
                    children=html.Div(id="features_table", children=""),
                    type="circle",
                ),
            ],
        )
        ___stripChart = html.Div(
            className="umap_plot_and_title",
            children=[
                html.Div(
                    className="title_and_help",
                    children=[
                        html.H6("StripChart of features"),
                        dbc.Button(
                            "[?]",
                            className="text-muted btn-secondary popover_btn",
                            id="help_stripChart",
                        ),
                        dbc.Popover(
                            children=[dbc.PopoverBody("Blablabla wout wout")],
                            id="pop_help_stripChart",
                            is_open=False,
                            target="help_stripChart",
                        ),
                    ],
                ),
                # dbc.Select(
                #     id="features_dropdown",
                #     className="form_select",
                #     options=[{"label": "None", "value": "None"}],
                #     value="None",
                #     style={"width": "35%"},
                # ),
                dcc.Loading(
                    dcc.Graph(id="features_stripChart", config=CONFIG),
                    type="dot",
                    color="#13BD00",
                ),
                dcc.Slider(
                    step=None,
                    value=1,
                    marks=cfg.default_marks,
                    id="strip_chart_slider",
                )
            ],
        )

        ___coocMatrix = html.Div(
            id="cooc_matrix",
            style={"width": "50%", "height": "5em"},
            children=[
                html.H6("Co-occurence graph of features"),
                dcc.Loading(
                    children=[
                        cyto.Cytoscape(
                            id="cooc_matrix_graph",
                            layout={"name": "cose"},
                            style={"width": "100%", "height": "100%", "border": "1px solid black"},
                            stylesheet=self._plots.get_default_stylesheet_for_cooc_graph(),
                            elements=[],

                        ),
                        html.Div(
                            id="cooc_matrix_graph_error",
                            children="",
                            style={"color": "red", "height": "100%", "background-color": "lightgrey",
                                   "text-align": "center", "vertical-align": "middle"},
                        ),
                    ],
                    type="dot",
                    color="#13BD00",
                ),
            ],
        )

        __featuresResultsTab = dbc.Tab(
            className="sub_tab",
            label="Features",
            children=[
                html.Div(
                    className="fig_group", children=[___featuresTable,
                                                     ___stripChart
                                                     ]
                ),
                ___coocMatrix
            ],
        )

        _mainPlotContent = html.Div(
            id="main_plots-content",
            children=[  # className="six columns",
                dbc.Tabs(
                    className="custom_sub_tabs",
                    id="sub_tabs",
                    children=[
                        __dataResultTab,
                        __algoResultsTab,
                        __featuresResultsTab,
                        __DTTreeTab,
                    ],
                )
            ],
        )

        return dbc.Tab(
            className="global_tab",
            id="results_tab",
            label="Results",
            children=[
                dcc.Store(id='design_dropdown_store', storage_type='session'),
                dcc.Store(id='ml_dropdown_store', storage_type='session'),
                dcc.Store(id='splits_dropdown_store', storage_type='session'),
                _resultsInfo,
                _mainPlotContent
            ],
        )

    def _registerCallbacks(self) -> None:
        @self.app.callback(
            Output("pop_help_accPlot", "is_open"),
            [Input("help_accPlot", "n_clicks")],
            [State("pop_help_accPlot", "is_open")],
        )
        def toggle_popover(n, is_open):
            if n:
                return not is_open
            return is_open

        @self.app.callback(
            [Output("design_dropdown", "options"), Output("design_dropdown", "value")],
            [Input("custom_big_tabs", "active_tab")],
            State('design_dropdown_store', 'data'),
        )
        @log_exceptions(self._logger)
        def update_results_dropdown_design(active, stored_value):
            if active == "tab-3":
                self.r = self.metabo_controller.get_all_results()
                experiment_designs = list(self.r.keys())
                if len(experiment_designs) == 0:
                    return dash.no_update, dash.no_update
                if stored_value is not None and stored_value in experiment_designs:
                    return Utils.format_list_for_checklist(experiment_designs), stored_value
                return (
                    Utils.format_list_for_checklist(experiment_designs),
                    experiment_designs[0],
                )
            else:
                return dash.no_update, dash.no_update

        @self.app.callback(
            [Output("ml_dropdown", "options"), Output("ml_dropdown", "value")],
            [Input("design_dropdown", "value")],
            [State("custom_big_tabs", "active_tab"), State('ml_dropdown_store', 'data')],
        )
        @log_exceptions(self._logger)
        def update_results_dropdown_algo(design, active, stored_value):
            if active == "tab-3":
                a = list(self.r[design].keys())
                if stored_value is not None and stored_value in a:
                    return [{"label": i, "value": i} for i in a], stored_value
                else:
                    return [{"label": i, "value": i} for i in a], a[0]
            else:
                return dash.no_update

        @self.app.callback(
            [Output("splits_dropdown", "options"), Output("splits_dropdown", "value")],
            [Input("sub_tabs", "active_tab")],
            [State("ml_dropdown", "value"), State("design_dropdown", "value"), State('splits_dropdown_store', 'data')],
        )
        @log_exceptions(self._logger)
        def update_nbr_splits_dropdown(active, algo, design, stored_value):
            if active == "tab-1":
                a = list(self.r[design][algo].splits_number)
                if stored_value is not None and stored_value in a:
                    return [{"label": i, "value": i} for i in a], stored_value
                else:
                    return [{"label": i, "value": i} for i in a], a[0]
            else:
                return dash.no_update

        @self.app.callback(
            [Output("loading-output-1", "children")],
            [Input("custom_big_tabs", "active_tab")],
        )
        def input_triggers_spinner(value):
            time.sleep(1)
            return

        # --- Callbacks to Save Values (persist dropdown selection) ---
        @self.app.callback(
            Output('design_dropdown_store', 'data'),
            Input('load_ML_results_button', 'n_clicks'),
            State('design_dropdown', 'value'),
        )
        def save_design_dropdown_value(_, value):
            return value

        @self.app.callback(
            Output('ml_dropdown_store', 'data'),
            Input('load_ML_results_button', 'n_clicks'),
            State('ml_dropdown', 'value'),
        )
        def save_ml_dropdown_value(_, value):
            return value

        @self.app.callback(
            Output('splits_dropdown_store', 'data'),
            Input('update_specific_results_button', 'n_clicks'),
            State('splits_dropdown', 'value'),
        )
        def save_splits_dropdown_value(_, value):
            return value

        # @self.app.callback(
        #     Output("2features", "figure"),
        #     [Input("load_ML_results_button", "n_clicks"), Input("pca_slider", "value")],
        #     [State("ml_dropdown", "value"), State("design_dropdown", "value")],
        # )
        # def show_pca(n_clicks, features, algo, design_name):
        #     if n_clicks >= 1:
        #         df = self.r[design_name][algo].results["features_table"]
        #         classes = self.r[design_name][algo].results["classes"]
        #         return self._plots.show_two_most_important_feature(df[pca_value], classes, pca_value, algo)
        #     else:
        #         return dash.no_update

        @self.app.callback(
            [
                Output("cooc_matrix_graph", "elements"),
                Output("cooc_matrix_graph", "style"),
                Output("cooc_matrix_graph_error", "children")
            ],
            [
                Input("load_ML_results_button", "n_clicks")
            ],
            [
                State("ml_dropdown", "value"), 
                State("design_dropdown", "value")
            ]
        )
        @log_exceptions(self._logger)
        def show_cooc_matrix(_, algo, design_name):
            if algo == "None" or design_name == "None":
                return [dash.no_update] * 3
            
            (
                counter, 
                mean_importance, 
                number_of_split, 
                cardinality
            ) = self.r[design_name][algo].results["coocurence_matrix"]

            if counter is None:
                msg = "Due to the high cardinality of the features, " \
                "the co-occurrence graph cannot be displayed. " \
                "The estimated cardinality is " + str(int(cardinality)) + \
                " and exceed the 1000 links limit."
                return dash.no_update, {'display': 'none'}, msg
                   
            parameters = self._plots.create_coocurence_graph(counter, mean_importance, number_of_split)
            return parameters, {'display': 'block', "width": "100%", "height": "800px"}, ""

        @self.app.callback(Output('cooc_matrix_graph', 'stylesheet'),
                           [Input('cooc_matrix_graph', 'selectedNodeData')])
        @log_exceptions(self._logger)
        def update_stylesheet(nodes):
            default_stylesheet = self._plots.get_default_stylesheet_for_cooc_graph()
            if nodes is None:
                return default_stylesheet
            else:
                updated_stylesheet = default_stylesheet.copy()
                self._logger.info(f"nodes:\n{nodes}")
                for node in nodes:
                    updated_stylesheet.append(self._plots.format_style_for_selected_node(node))
                return updated_stylesheet

        @self.app.callback(
            [
                Output("pca_slider", "marks"),
                Output("umap_slider", "marks"),
                Output("strip_chart_slider", "marks"),
                Output("pca_slider", "value"),
                Output("umap_slider", "value"),
                Output("strip_chart_slider", "value"),
            ],
            [
                Input("load_ML_results_button", "n_clicks")
            ],
            [
                State("ml_dropdown", "value"), State("design_dropdown", "value")
            ]
        )
        @log_exceptions(self._logger)
        def update_sliders_with_used(_, algo, design_name):
            """Update PCA, UMAP and Strip chart sliders marks and triggers each plots by updating there values"""
            if algo == "None" or design_name == "None":
                return [dash.no_update] * 6
            
            feature_df = self.r[design_name][algo].results["features_table"]
            number_of_used_feature = len(feature_df[feature_df["times_used"] > 0])

            marks_container = []
            locations_container = []

            marks, used_location = utils.update_marks(
                custom_value=number_of_used_feature, 
                add_all_value=True
            )
            pca_marks, umap_marks = marks, marks
            pca_location, umap_location = used_location, used_location
            marks_container.extend([pca_marks, umap_marks])
            locations_container.extend([pca_location, umap_location])

            strip_chart_marks, strip_location = utils.update_marks(
                custom_value=number_of_used_feature, 
                add_all_value=False
            )
            marks_container.append(strip_chart_marks)
            locations_container.append(strip_location)

            return (*marks_container, *locations_container)
                    

        @self.app.callback(
            [
                Output("PCA", "figure")
            ],
            [
                Input("pca_slider", "value"),
                Input("pca_dimensions", "value")
            ],
            [
                State("ml_dropdown", "value"),
                State("design_dropdown", "value"),
                State("pca_slider", "marks")
            ],
            prevent_initial_call=True
        )
        @log_exceptions(self._logger)
        def show_pca(pca_value, dimensions, algo, design_name, marks):
            """
            pca_value : represent the number of feature selected by the slider, but is given as indexes
            """
            if algo == "None" or design_name == "None":
                return dash.no_update

            classes = self.r[design_name][algo].results["classes"]

            index = utils.get_index_from_marks(pca_value, marks)

            if dimensions == "2d":
                data_list, labels_list = self.r[design_name][algo].results["pca_data"]
                fig = self._plots.show_PCA(
                    data_list[index], labels_list[index], classes, index, algo,
                    self.r[design_name][algo].results["samples_id"]
                )
            elif dimensions == "3d":
                data_list, labels_list = self.r[design_name][algo].results["3d_pca_data"]
                fig = self._plots.show_3D_PCA(
                    data_list[index], labels_list[index], classes, index, algo,
                    self.r[design_name][algo].results["samples_id"]
                )
            
            return [fig]

        @self.app.callback(
            [
                Output("umap_overview", "figure")
            ],
            [
                Input("load_ML_results_button", "n_clicks"),
                Input("umap_slider", "value"),
                Input("umap_dimensions", "value"),
            ],
            [
                State("ml_dropdown", "value"), 
                State("design_dropdown", "value"), 
                State("umap_slider", "marks")
            ],
        )
        @log_exceptions(self._logger)
        def show_umap(_, slider_value, dimensions, algo, design_name, marks):
            if algo == "None" or design_name == "None":
                return dash.no_update
            
            classes = self.r[design_name][algo].results["classes"]

            index = utils.get_index_from_marks(slider_value, marks)

            if dimensions == "2d":
                df = self.r[design_name][algo].results["umap_data"]
                fig = self._plots.show_umap(
                    df[index], classes, algo, index, 
                    self.r[design_name][algo].results["samples_id"]
                )
            elif dimensions == "3d":
                df = self.r[design_name][algo].results["3d_umap_data"]
                fig = self._plots.show_3D_umap(
                    df[index], classes, algo, index, 
                    self.r[design_name][algo].results["samples_id"]
                )
            
            return [fig]
    

        @self.app.callback(
            [
                Output("2d_overview", "figure")
            ],
            [
                Input("load_ML_results_button", "n_clicks")
            ],
            [
                State("ml_dropdown", "value"), 
                State("design_dropdown", "value")
            ],
        )
        @log_exceptions(self._logger)
        def show_2d(_, algo, design_name):
            if algo == "None" or design_name == "None":
                return dash.no_update
            
            df = (
                self.r[design_name][algo].results["features_2d_and_3d"].iloc[:, :-1]
            )
            classes = self.r[design_name][algo].results["classes"]
            fig = self._plots.show_2d(
                df, classes, 
                self.r[design_name][algo].results["samples_id"]
            )
            return [fig]
            

        @self.app.callback(
            [
                Output("3d_overview", "figure")
            ],
            [
                Input("load_ML_results_button", "n_clicks")
            ],
            [
                State("ml_dropdown", "value"), 
                State("design_dropdown", "value")
            ],
        )
        @log_exceptions(self._logger)
        def show_3d(_, algo, design_name):
            if algo == "None" or design_name == "None":
                return dash.no_update
            
            df = self.r[design_name][algo].results["features_2d_and_3d"]
            classes = self.r[design_name][algo].results["classes"]
            fig = self._plots.show_3d(
                df, classes, 
                self.r[design_name][algo].results["samples_id"]
            )
            return [fig]

        @self.app.callback(
            [
                Output("expe_table", "children")
            ],
            [
                Input("load_ML_results_button", "n_clicks")
            ],
            [
                State("ml_dropdown", "value"), 
                State("design_dropdown", "value")
            ],
        )
        @log_exceptions(self._logger)
        def get_experiment_statistics(_, algo, design_name):
            if algo == "None" or design_name == "None":
                return dash.no_update
            
            df = self.r[design_name][algo].results["info_expe"]
            table_body = self._plots.show_exp_info_all(df)
            table = dbc.Table(
                table_body, id="table_exp_info", borderless=True, hover=True
            ) # dbc.Table.from_dataframe(df, borderless=True)
            return [table]


        @self.app.callback(
            [
                Output("accuracy_overview", "figure")
            ],
            [
                Input("load_ML_results_button", "n_clicks")
            ],
            [
                State("ml_dropdown", "value"), 
                State("design_dropdown", "value")
            ],
        )
        @log_exceptions(self._logger)
        def generates_accuracyPlot_global(_, algo, design_name):
            if algo == "None" or design_name == "None":
                return dash.no_update
            
            df = self.r[design_name][algo].results["accuracies_table"]
            fig = self._plots.show_accuracy_all(df, algo)
            return [fig]

        @self.app.callback(
            [
                Output("metrics_score_table", "children")
            ],
            [
                Input("load_ML_results_button", "n_clicks")
            ],
            [
                State("ml_dropdown", "value"), 
                State("design_dropdown", "value")
            ],
        )
        @log_exceptions(self._logger)
        def show_metrics(_, algo, design_name):
            if algo == "None" or design_name == "None":
                return dash.no_update
            
            df = self.r[design_name][algo].results["metrics_table"]
            table = dbc.Table.from_dataframe(df, borderless=True)
            return [table]


        @self.app.callback(
            [
                Output("split_conf_matrix", "figure"),
                Output("hyperparam_table", "children")
            ],
            [
                Input("update_specific_results_button", "n_clicks")],
            [
                State("ml_dropdown", "value"),
                State("design_dropdown", "value"),
                State("splits_dropdown", "value"),
            ],
        )
        @log_exceptions(self._logger)
        def compute_split_conf_matrix(_, algo, design_name, split):
            if algo == "None" or design_name == "None":
                return dash.no_update, dash.no_update
            
            cm = self.r[design_name][algo].results[split]["Confusion_matrix"][1]
            labels = self.r[design_name][algo].results[split]["Confusion_matrix"][0]

            text_mat = []
            for i, line in enumerate(cm):
                text_mat.append([])
                for j, col in enumerate(line):
                    text_mat[i].append(str(col))

            hps = self.r[design_name][algo].results[split]["hyperparameters"]

            hps_df = pd.DataFrame.from_dict({"Hyperparameters": hps.keys(), "Values": hps.values()})

            dash_table_element = dbc.Table.from_dataframe(hps_df, borderless=True)
            fig = self._plots.show_general_confusion_matrix(
                cm, labels, text_mat, algo, split
            )

            return  fig, dash_table_element


        @self.app.callback(
            Output("features_table", "children"),
            Input("load_ML_results_button", "n_clicks"),
            [
                State("ml_dropdown", "value"), 
                State("design_dropdown", "value")
            ],
        )
        @log_exceptions(self._logger)
        def show_features(_, algo, design_name):
            if algo == "None" or design_name == "None":
                return dash.no_update
            
            df = self.r[design_name][algo].results["features_table"].copy()
            df = df.sort_values(by="importance_usage", ascending=False)
            df = df.round(4)

            return dbc.Table.from_dataframe(df.iloc[:10, :], borderless=True)


        @self.app.callback(
            Output("download_dataframe_csv", "data"),
            [Input("export_features", "n_clicks")],
            [State("ml_dropdown", "value"), State("design_dropdown", "value")],
            prevent_initial_call=True,
        )
        @log_exceptions(self._logger)
        def export_download_features_table(n_click, algo, design_name):
            if n_click >= 1:
                df = self.r[design_name][algo].results["features_table"]
                return dcc.send_data_frame(
                    df.to_csv, "featuresImportancesTable" + algo + ".csv"
                )
            else:
                return dash.no_update


        @self.app.callback(
            [
                Output("features_stripChart", "figure")
            ],
            [
                Input("strip_chart_slider", "value")
            ],
            [
                State("ml_dropdown", "value"), 
                State("design_dropdown", "value"), 
                State("strip_chart_slider", "marks")
            ],
        )
        @log_exceptions(self._logger)
        def show_stripChart_features(slider_value, algo, design_name, marks):
            if algo == "None" or design_name == "None":
                return dash.no_update

            try:
                real_value = utils.get_index_from_marks(slider_value, marks)
                strip_chart_data = self.r[design_name][algo].results["features_stripchart"][real_value]
                fig = self._plots.show_metabolite_levels(
                    strip_chart_data, algo, 
                    self.r[design_name][algo].results["samples_id"]
                )
                return [fig]
            except IndexError:
                return dash.no_update

        @self.app.callback(
            [
                Output("DTTT", "disabled"), 
                Output("DTTT_graph", "dot_source")
            ],
            [
                Input("load_ML_results_button", "n_clicks")
            ],
            [
                State("ml_dropdown", "value"), 
                State("design_dropdown", "value")
            ],
        )
        @log_exceptions(self._logger)
        def disable_DTTT(_, algo, design_name):
            if algo == "None" or design_name == "None":
                return dash.no_update, dash.no_update
            
            if algo == "DecisionTree":
                model = self.r[design_name][algo].results["best_model"]
                classes = list(set(self.r[design_name][algo].results["classes"]))
                plt.margins(0.05)
                df = self.r[design_name][algo].results["features_table"]
                df.sort_index(inplace=True)
                features_name = list(df["features"])
                dot_data = tree.export_graphviz(
                    model,
                    out_file=None,
                    class_names=classes,
                    feature_names=features_name,
                    proportion=True,
                    filled=True,
                    rounded=True,
                    special_characters=True,
                )

                return False, dot_data
            
            return True, ""
