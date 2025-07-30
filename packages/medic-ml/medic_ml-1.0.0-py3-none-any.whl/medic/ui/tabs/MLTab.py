import json
import re

import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, State, Input, Output, dash, dcc, callback_context, ALL
from os.path import basename

from .MetaTab import MetaTab
from ...service import Utils, init_logger, log_exceptions
from ...domain import MetaboController


class MLTab(MetaTab):
    def __init__(self, app: dash.Dash, metabo_controller: MetaboController):
        super().__init__(app, metabo_controller)
        self._logger = init_logger()

    def getLayout(self) -> dbc.Tab:       
        __splitConfigFile = html.Div(
            [
                dbc.Label("Select CV search type", className="form_labels"),
                dbc.RadioItems(
                    options=Utils.format_list_for_checklist(
                        self.metabo_controller.get_cv_types()
                    ),
                    value=self.metabo_controller.get_selected_cv_type(),
                    id="radio_cv_types",
                ),
                html.Br(),
                html.Div(id="cv_params"),
            ],
            className="form_field",
        )

        __ThreadingConfig = html.Div(
            [
                dbc.Label("Multi-threading activation", className="form_labels"),
                dbc.Checklist(
                    options=[
                        {"label": "Multi-threading is off", "value": 1},
                    ],
                    id="switches-input",
                    value=[1],
                    switch=True,
                ),
                html.Div(id="output_cv_folds_ml", style={"color": "red"}),
            ],
            className="form_field",
        )

        _definitionLearningConfig = html.Div(
            className="title_and_form",
            children=[
                html.H4(id="Learn_conf_title", children="Define Learning configs"),
                dbc.Form(
                    children=[
                        dbc.Col(
                            children=[
                                __splitConfigFile,
                                __ThreadingConfig,
                            ],
                        )
                    ]
                ),
            ],
        )

        __availableAlgorithms = html.Div(
            [
                dbc.Label("Available Algorithms", className="form_labels"),
                dbc.Checklist(
                    id="in_algo_ML",
                    # inline=True
                ),
                html.Div(id="output_checklist_ml", children="", style={"color": "red"}),
            ],
            className="form_field",
        )

        __addCustomAlgorithm = html.Div(
            [
                dbc.Label("Add Sklearn Algorithms", className="form_labels"),
                dbc.Label("from sklearn.A import B"),
                dbc.Input(
                    id="import_new_algo",
                    placeholder="Complete import (A)",
                    className="form_input_text",
                ),
                dbc.Input(
                    id="name_new_algo",
                    placeholder="Enter Name (B)",
                    className="form_input_text",
                ),
                dbc.Button(
                    "Get attributes",
                    color="success",
                    id="get_attribute_button",
                    className="custom_buttons",
                    n_clicks=0,
                ),
                dbc.Button(
                    "Manual configuration",
                    color="success",
                    id="manual_config_button",
                    className="custom_buttons",
                    n_clicks=0,
                ),
                html.Div(id="output_import_algo"),
                html.Div("WARNING: Incorrect configuration may lead to errors", style={"color": "orange"}),
                html.Br(),
                dbc.Label("Specify parameters to explore by gridsearch"),
                html.Div(id="table_param"),
                html.Div(id="output_error_import_algo"),
                dbc.Label("Specify importance attribute"),
                dbc.Select(
                    id="importance_attributes_dropdown_menu",
                ),
                dbc.Button(
                    "Add",
                    color="success",
                    id="add_n_refresh_sklearn_algo_button",
                    className="custom_buttons",
                    n_clicks=0,
                ),
            ],
            className="form_field",

        )

        __validationButton = html.Div(
            id="Learning_button_box",
            className="button_box",
            children=[
                dcc.Loading(
                    id="learn_loading",
                    children=[
                        html.Div(
                            id="learn_loading_output",
                            style={"color": "green"},
                        )
                    ],
                    style={"width": "100%"},
                    type="dot",
                    color="#13BD00",
                ),
                dbc.Button(
                    "Learn",
                    color="primary",
                    id="start_learning_button",
                    className="custom_buttons",
                    n_clicks=0,
                ),
                html.Div(id="output_button_ml", children="", style={"display": "none"}),
            ], )

        _definitionLearningAlgorithm = html.Div(
            className="title_and_form",
            children=[
                html.H4(id="learn_algo_title", children="Define Learning Algorithms"),
                dbc.Form(
                    children=[
                        dbc.Col(
                            children=[
                                __availableAlgorithms,
                                # TODO: change button style
                                dbc.Button(
                                    "Add custom sklearn algorithm (for experts)",
                                    id="collapse-button",
                                    className="mb-3",
                                    color="outline-primary",
                                    n_clicks=0,
                                ),
                                dbc.Collapse(
                                    dbc.Card(dbc.CardBody(__addCustomAlgorithm)),
                                    id="collapse",
                                    is_open=False,
                                ),
                                __validationButton,
                            ],
                        )
                    ]
                ),
            ],
        )

        _learn_completed_modal = dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Learning completed")),
                dbc.ModalBody(id="learn_completed_body", children="The learning is completed."),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-learn_completed_modal", className="ml-auto")
                ),
            ],
            id="learn_completed_modal",
            is_open=False,
            centered=True
        )

        return dbc.Tab(
            className="global_tab",
            label="Machine Learning",
            children=[
                dcc.Store(id='learn-button-state', data=False),
                dcc.Store(id='classification_design_filename-store', data=""),
                html.Div(
                    className="fig_group",
                    children=[_definitionLearningConfig, _definitionLearningAlgorithm, _learn_completed_modal],
                ),
            ],
        )

    def _registerCallbacks(self) -> None:
        @self.app.callback(
            Output("in_nbr_CV_folds", "value"), [Input("custom_big_tabs", "active_tab")]
        )
        @log_exceptions(self._logger)
        def update_nbr_CV_folds(active_tab):
            if active_tab == "tab-2":
                return self.metabo_controller.get_cv_folds()
            return dash.no_update

        @self.app.callback(
            Output("switches-input", "options"), [Input("switches-input", "value")]
        )
        def update_switch(value):
            if value == [1]:
                self.metabo_controller.set_multithreading(True)
                return [
                    {"label": "Multi-threading is on", "value": 1},
                ]
            elif not value:
                self.metabo_controller.set_multithreading(False)
                return [
                    {"label": "Multi-threading is off", "value": 1},
                ]
            return dash.no_update

        @self.app.callback(
            [
                Output("in_algo_ML", "options"),
                Output("in_algo_ML", "value"),
                Output("output_checklist_ml", "children"),
                Output("output_error_import_algo", "children"),
            ],
            [
                Input("add_n_refresh_sklearn_algo_button", "n_clicks"),
                Input("in_algo_ML", "value"),
                Input("custom_big_tabs", "active_tab"),
            ],
            [
                State("import_new_algo", "value"),
                State("name_new_algo", "value"),
                State("table_param", "children"),
                State("importance_attributes_dropdown_menu", "value")
            ]
        )
        @log_exceptions(self._logger)
        def add_refresh_available_sklearn_algorithms(
                n, value, active_tab, import_algo, name_algo, table_param, importance_attribute
        ):
            triggered_by = callback_context.triggered[0]["prop_id"].split(".")[0]
            if triggered_by == "custom_big_tabs":
                self._logger.info("Triggered by tab")
                if active_tab == "tab-2":
                    self.metabo_controller.update_classification_designs_with_selected_models()

            if triggered_by == "add_n_refresh_sklearn_algo_button":
                grid_search_params = {}
                model = Utils.get_model_from_import([import_algo], name_algo)
                param_types = {param: type for param, type in Utils.get_model_parameters(model)}
                error_children = []
                if "{'props': {'children': 'Name', 'colSpan': 1}, 'type': 'Th', 'namespace': 'dash_html_components'}" in str(
                        table_param[-1]["props"]):
                    params_and_values = re.findall(r"{'id': '(\w+)'[\w,' :]*'value': '([\[\],. \w]+)',[\w,': ]*}",
                                                   str(table_param))
                    try:
                        grid_search_params = Utils.transform_params_to_cross_validation_dict(params_and_values,
                                                                                             param_types)
                    except ValueError as e:
                        for error in e.args[0]:
                            error_children.append(html.P(error, style={"color": "red"}))
                else:
                    json_params_and_values = table_param[-1]["props"]["value"]
                    try:
                        params_and_values = json.loads(json_params_and_values)
                    except json.decoder.JSONDecodeError as e:
                        return dash.no_update, dash.no_update, dash.no_update, html.P("Error in parameters:" + e.msg,
                                                                                      style={"color": "red"})

                if importance_attribute is None:
                    error_children.append(html.P("Please select an importance attribute", style={"color": "red"}))

                if error_children:
                    return dash.no_update, dash.no_update, dash.no_update, error_children

                self.metabo_controller.add_custom_model(
                    name_algo, import_algo, grid_search_params, importance_attribute
                )
            if triggered_by == "in_algo_ML":
                self._logger.info("Triggered by dropdown")
                try:
                    self.metabo_controller.set_selected_models(value)
                except ValueError as ve:
                    self._logger.error(f"{ve}")
                    return (
                        Utils.format_list_for_checklist(
                            self.metabo_controller.get_all_algos_names()
                        ),
                        [],
                        str(ve),
                        "",
                    )

            return (
                Utils.format_list_for_checklist(
                    self.metabo_controller.get_all_algos_names()
                ),
                self.metabo_controller.get_selected_models(),
                "",
                "",
            )

        @self.app.callback(
            [
                Output("output_button_ml", "children"),
                Output("learn_loading_output", "children"),
                Output("learn-button-state", "data"),
                Output('classification_design_filename-store', 'data'),
            ],
            [Input("start_learning_button", "n_clicks")],
        )
        @log_exceptions(self._logger)
        def start_machine_learning(n):
            if n >= 1:
                self._logger.info(f"in\n{self.metabo_controller.get_selected_models()}")
                self.metabo_controller.learn()

                # Dump file to dump folder and to save folder (backup)
                metabo_expe_filename = Utils.get_metabo_experiment_path("medic_ml")
                metabo_expe_obj = self.metabo_controller.generate_save()
                Utils.dump_metabo_expe(metabo_expe_obj) # Dump the classification design to the dump folder
                Utils.dump_metabo_expe(metabo_expe_obj, metabo_expe_filename) # Save classification design.
                del metabo_expe_obj
                self._logger.info(f'The classification design file "{metabo_expe_filename}" has been saved.')
                self._logger.info(f"bip bip 3 : {self.metabo_controller._metabo_experiment.classification_designs}")
                return "Done!", "", True, basename(metabo_expe_filename)
            else:
                return dash.no_update

        @self.app.callback(
            Output("learn_completed_modal", "is_open"),
            [Input("close-learn_completed_modal", "n_clicks"),
            Input('learn-button-state', 'data')],
            [State("learn_completed_modal", "is_open")]
        )
        def toggle_learn_completed_modal(close_clicks, learn_state, is_open):
            if close_clicks or learn_state:
                return not is_open
            return is_open

        @self.app.callback(
        Output("learn_completed_body", "children"),
        [Input('classification_design_filename-store', 'data')]
        )
        @log_exceptions(self._logger)
        def update_modal_message(filename):
            if filename:
                return [
                    html.P(f'The classification design file "{filename}" has been saved.', style={'color': 'green'}),
                    html.P('You can go to the "Results" tabs.'),
                ]
            return "Error!"

        @self.app.callback(
            [Output("radio_cv_types", "value"),
             Output("cv_params", "children")],
            [Input("radio_cv_types", "value"),
             Input("custom_big_tabs", "active_tab"),
             Input({"type": "cv_params", "index": ALL}, "value")],
        )
        @log_exceptions(self._logger)
        def set_cv_type(cv_value, tab, input_params):
            if callback_context.triggered[0]["prop_id"] == "radio_cv_types.value":
                params_form = []
                self.metabo_controller.set_cv_type(cv_value)
                params = self.metabo_controller.get_cv_algorithm_configuration()
                if params:
                    for param in params:
                        if not param["constant"]:
                            name = param["name"]
                            value = param["value"]
                            type = param["type"]
                            if type == "int":
                                html_type = "number"
                            elif type == "float":
                                html_type = "number"
                            elif type == "bool":
                                html_type = "checkbox"
                            else:
                                html_type = "text"
                            params_form.append(
                                html.Tr(
                                    [
                                        html.Td(name),
                                        html.Td(
                                            dcc.Input(
                                                id={"type": "cv_params", "index": name},
                                                type=html_type,
                                                value=value,
                                            )
                                        ),
                                    ]
                                )
                            )
                return cv_value, params_form
            else:
                if input_params is not None and input_params != []:
                    self.metabo_controller.set_cv_algorithm_configuration(input_params)

            return self.metabo_controller.get_selected_cv_type(), dash.no_update

        @self.app.callback(
            [Output("output_import_algo", "children"),
             Output("output_import_algo", "style"),
             Output("table_param", "children"),
             Output("importance_attributes_dropdown_menu", "options")],
            [Input("get_attribute_button", "n_clicks"),
             Input("manual_config_button", "n_clicks")],
            [State("import_new_algo", "value"),
             State("name_new_algo", "value")],
        )
        @log_exceptions(self._logger)
        def get_attribute_algo(n_attribute, n_manual, import_new, new_algo_name):
            triggered_by = callback_context.triggered[0]["prop_id"].split(".")[0]
            self._logger.info(f"triggered by: [{triggered_by}]")
            if n_manual > 0 or n_attribute > 0:
                try:
                    model = Utils.get_model_from_import([import_new], new_algo_name)
                except Exception as e:
                    self._logger.error(f"{e}")
                    return "Import failed: " + str(e), {"color": "red"}, "", ""
                importance_attributes = [param_name for param_name, _ in
                                         Utils.get_model_parameters_after_training(model)]
                if not importance_attributes:
                    return "Import failed: No importance attribute found.", {"color": "red"}, "", ""
                if triggered_by == "get_attribute_button":
                    try:
                        attributes = Utils.get_model_parameters(model)
                        attributes_table = pd.DataFrame(attributes, columns=["Name", "Type"])
                        attributes_table["Type"].replace(
                            {"str": "String", "int": "Integer", "float": "Float", "NoneType": "Unspecified"},
                            inplace=True)
                        inputs = []
                        for attribute, _ in attributes:
                            inputs.append(dbc.Input(id=attribute, type="text", placeholder="Value"))
                        attributes_table["Value"] = inputs

                        default_text = [
                            html.Br(),
                            html.P("You can set the grid search parameters as followed:"),
                            html.P(
                                "Values: 'val1A, val1B, val1C'"
                            ),
                            dbc.Table.from_dataframe(attributes_table)
                        ]

                        return f"{model.__name__} found", {
                            "color": "green"}, default_text, Utils.format_list_for_checklist(importance_attributes)
                    except Exception as e:
                        self._logger.info(f"{e}")
                        return "Import failed: " + str(e), {"color": "red"}, "", ""
                elif triggered_by == "manual_config_button":
                    return "", None, [html.P("The following configuration must be in JSON format",
                                             style={"color": "orange"}), html.Br(),
                                      dcc.Textarea()], Utils.format_list_for_checklist(importance_attributes)
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update

        @self.app.callback(
            Output("collapse", "is_open"),
            [Input("collapse-button", "n_clicks")],
            [State("collapse", "is_open")],
        )
        def toggle_collapse(n, is_open):
            if n:
                return not is_open
            return is_open
