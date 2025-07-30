import math

import dash_bootstrap_components as dbc
import pandas
from dash import html, Output, Input, dash, State, dcc, callback_context, MATCH, ALL
from dash.dcc import send_file
from os.path import basename

from .MetaTab import MetaTab
from ...domain import MetaboController
from ...service import Utils, Plots, init_logger, log_exceptions

EXP_NAME = []
SPLIT_NUMBER_VALUES = {i: str(i) for i in range(0, 101, 10)}
SPLIT_NUMBER_VALUES.update({1: "1"})

NUMBER_OF_STEP_IN_CLASS_BALANCE = 5

CONFIG = {
    "toImageButtonOptions": {
        "format": "svg",  # one of png, svg, jpeg, webp
        "height": None,
        "width": None,
        "scale": 1,  # Multiply title/legend/axis/canvas sizes by this factor
    }
}


class SplitsTab(MetaTab):
    def __init__(self, app: dash.Dash, metabo_controller: MetaboController):
        super().__init__(app, metabo_controller)
        self._logger = init_logger()

    def getLayout(self) -> dbc.Tab:
        _introductionNotice = html.Div(
            className="fig_group_all_width",
            children=[
                dbc.Card(
                    children=[
                        dbc.CardBody(
                            [
                                html.Div(
                                    "In this tab, you will create a setting file with all info necessary "
                                    "to run a machine learning experiment. The recommended order to proceed is : Files, Classification design, "
                                    "Define Splits, Sample Pairing, Class Balancing, Generate file."
                                ),
                            ]
                        ),
                    ]
                ),
            ],
        )

        __dataFile = html.Div(
            [
                dbc.Label("Data file(s) *", className="form_labels"),
                html.Div(
                    [
                        dcc.Upload(
                            id="upload_datatable",
                            children=[
                                dbc.Button(
                                    "Upload File",
                                    id="upload_datatable_button",
                                    # className="custom_buttons",
                                    color="outline-primary",
                                )
                            ],
                        ),
                        dcc.Loading(
                            id="upload_datatable_loading",
                            children=[
                                html.Div(
                                    id="upload_datatable_output",
                                    style={"color": "green"},
                                )
                            ],
                            style={"width": "100%"},
                            type="dot",
                            color="#13BD00",
                        ),
                    ],
                    style={"display": "flex", "align-items": "center"},
                ),
                dbc.FormText(
                    "You can give a Progenesis abundance file, or a matrix with samples as lines and features as "
                    "columns.",
                ),
                html.Div(id="error_upload_datatable", style={"color": "red"}),
            ],
            className="form_field",
            id="datatable-section",
            style={"display": "none"},
        )

        __metaDataFile = html.Div(
            [
                dbc.Label(
                    className="form_labels",
                    children=[
                        html.Span("Metadata file  "),
                        html.Span(
                            "(optionnal if Progenesis matrix given)",
                            style={"font-size": "0.9em", "text-transform": "none"},
                        ),
                    ],
                ),
                html.Div(
                    [
                        dcc.Upload(
                            id="upload_metadata",
                            children=[
                                dbc.Button(
                                    "Upload File",
                                    id="upload_metadata_button",
                                    # className="custom_buttons",
                                    color="outline-primary",
                                )
                            ],
                        ),
                        dcc.Loading(
                            id="upload_metadata_loading",
                            children=[
                                html.Div(
                                    id="upload_metadata_output",
                                    style={"color": "green"},
                                )
                            ],
                            style={"width": "100%"},
                            type="dot",
                            color="#13BD00",
                        ),
                    ],
                    style={"display": "flex", "align-items": "center"},
                ),
                dbc.FormText(
                    "The metadata file should at least contain : one column with samples name corresponding to names in the"
                    "data file, and one column of target/class/condition.",
                ),
                html.Div(id="error_upload_metadata", style={"color": "red"}),
            ],
            className="form_field",
            id="metadata-section",
            style={"display": "none"},
        )

        __useRawData = html.Div(
            [
                dbc.Label("DATA NORMALIZATION FOR PROGENESIS", className="form_labels"),
                dbc.FormText(
                    "If there is normalized and raw data in your file, you can choose which one to use. ",
                ),
                dbc.RadioItems(
                    id="in_use_raw",
                    options=[
                        {"label": "Raw", "value": "raw"},
                        {"label": "Normalized", "value": "normalized"},
                        {"label": "Not Progenesis", "value": "nap"},
                    ],
                    # if self.metabo_controller.is_data_raw() is None
                    # else (
                    #    "raw"
                    #    if not self.metabo_controller.is_data_raw()
                    #    else "normalized"
                    # ),
                    labelCheckedStyle={"color": "#13BD00"},
                ),
                html.Div(id="error_data_normalization", style={"color": "red"}),
            ],
            className="form_field",
        )

        __removeRTlessThan1min = html.Div(
            [
                dbc.Label(
                    "Remove features with RT lower than 1 min (progenesis only)", className="form_labels"
                ),
                dbc.FormText(
                    "We highly recommend to keep this as true, choose false at your own risks (see in documentation).",
                ),
                dbc.RadioItems(
                    id="in_remove_rt",
                    options=[
                        {"label": "True", "value": True, "disabled": True},
                        {"label": "False", "value": False, "disabled": True},
                    ],
                    labelCheckedStyle={"color": "#13BD00"},
                ),
                html.Div(id="warning_select_false", style={"color": "red"}),
            ],
            className="form_field",
            id="remove-rt-section",
            style={"display": "none"},
        )

        _file = html.Div(
            className="title_and_form",
            children=[
                html.H4(id="CreateSplits_paths_title", children="Files"),
                dbc.Form(
                    children=[
                        dbc.Col(
                            children=[
                                __useRawData,
                                __removeRTlessThan1min,
                                __dataFile,
                                __metaDataFile,
                            ]
                        ),
                    ]
                ),
            ],
        )

        __typeGroupLink = dbc.Card(
            [
                html.Div(
                    [
                        dbc.Label("Name of the targets column"),
                        dbc.Checklist(
                            id="in_target_col_name",
                            value=[],
                            # options=Utils.format_list_for_checklist(
                            #    self.metabo_controller.get_metadata_columns()
                            # ),
                            # value=[], #if self.metabo_controller.get_target_column() is None else [self.metabo_controller.get_target_column()],
                            inline=True,
                        ),
                    ],
                    className="form_field",
                ),
                html.Div(
                    [
                        dbc.Label("Name of the unique id column"),
                        dbc.RadioItems(
                            id="in_ID_col_name",
                            options=Utils.format_list_for_checklist(
                                self.metabo_controller.get_metadata_columns()
                            ),
                            value=self.metabo_controller.get_id_column(),
                            inline=True,
                        ),
                    ],
                    className="form_field",
                ),
                html.Div(
                    id="info_progenesis_loaded",
                    style={
                        "color": "grey",
                        "padding-left": "2em",
                        "font-style": "italic",
                    },
                ),
            ],
            body=True,
        )

        __labelDefinition = dbc.Card(
            id="",
            children=[
                html.Div(
                    [
                        dbc.Label("Type of classification"),
                        dbc.RadioItems(
                            id="in_classification_type",
                            value=0,
                            inline=True,
                            options=[
                                {"label": "Binary", "value": 0},
                                {"label": "Multiclass", "value": 1, "disabled": True},
                            ],
                        ),
                    ],
                    className="form_field",
                ),
                html.Div(
                    [
                        dbc.Label("Labels"),
                        dbc.FormText("It is good practice to define the control group as target 0 and the 'condition' group as target 1. "),
                        dbc.FormText("To do so, add a 0 or a 1 at the beginning of corresponding labels (ex: 0GroupA or 0_GroupA). "),
                        dbc.FormText("See more details in the documentation."),
                        html.Div(
                            className="fig_group_mini",
                            id="define_classes_desgn_exp",
                            children=[
                                dbc.Input(
                                    id="class1_name",
                                    type="text",
                                ),
                                dbc.Checklist(
                                    id="possible_groups_for_class1",
                                ),
                                dbc.Input(
                                    id="class2_name",
                                ),
                                dbc.Checklist(
                                    id="possible_groups_for_class2",
                                ),
                            ],
                        ),
                    ],
                    className="form_field",
                ),
                html.Div(id="error_classification_type", style={"color": "red"}),
                dbc.Button(
                    "Add",
                    id="btn_add_design_exp",
                    color="primary",
                    className="custom_buttons",
                    n_clicks=0,
                ),
                html.Div(id="output_btn_add_desgn_exp"),
            ],
            body=True,
        )

        _classificationDesigns = html.Div(
            className="title_and_form",
            children=[
                html.H4(id="Exp_desg_title", children="Define Classification designs"),
                dbc.Form(
                    children=[
                        dbc.Col(
                            children=[
                                dbc.FormText("Link each sample to its target/class."),
                                __typeGroupLink,
                                html.Div(id="error_link_each_sample_to_target", style={"color": "red"}),
                                html.Br(),
                                dbc.FormText("Classification Designs."),
                                dbc.Card(
                                    id="setted_classes_container",
                                    children=self._get_wrapped_classification_designs(),
                                    style={"display": "block", "padding": "1em"},
                                ),
                                html.Div(id="error_classification_designs", style={"color": "red"}),
                                dbc.FormText("Define labels and filter out samples."),
                                __labelDefinition,
                            ]
                        ),
                    ]
                ),
            ],
        )

        __samplePairing = html.Div(
            children=[
                dbc.FormText("Select the column you want to group."),
                dbc.Label("Column(s)"),
                html.Div(
                    id="pairing_columns",
                    children=[
                        dcc.Dropdown(
                            self.metabo_controller.get_metadata_columns(),
                            id="pairing_group_column",
                        )
                    ],
                ),
            ]
        )

        __classBalancing = html.Div(
            children=[
                html.H4(id="class_balancing_title", children="Class balancing"),
                html.Div(id="class_balancing_options", children=[]),
                html.Div(id="class_balancing_values_nutshell", children=[]),
            ]
        )

        _dataFusion = html.Div(
            className="title_and_form",
            children=[
                html.H4(id="sep_samples_title", children="Sample pairing"),
                dbc.Form(
                    children=[
                        dbc.Col(
                            [
                                __samplePairing,
                                __classBalancing
                            ]
                        )
                    ]
                ),
            ],
        )

        __sampleProportion = html.Div(
            [
                dbc.Label("Proportion of samples in test"),
                dbc.Input(
                    id="in_percent_samples_in_test",
                    value=self.metabo_controller.get_train_test_proportion(),
                    type="number",
                    min=0.01,
                    max=1,
                    step=0.01,
                    size="5",
                ),
                html.Div(id="error_percent_samples_in_test", style={"color": "red", "margin-top": "0.5em"}),
            ],
            className="form_field",
        )

        __trainTestSplitGraph = html.Div(
            [
                dbc.Label("Train/Test split graph"),
                dcc.Loading(
                    dcc.Graph(id="train_test_split_graph", config=CONFIG),
                    type="dot",
                    color="#13BD00",
                ),                
                dcc.Slider(
                    id='in_nbr_splits',
                    min=1,
                    max=100,
                    step=1,
                    value=self.metabo_controller.get_number_of_splits(),
                    marks=SPLIT_NUMBER_VALUES,
                ),
                html.Div(
                    children=[
                        html.P('a) Probability that all the samples are seen at least once in a test set'),
                        html.P(
                            'b) With a confidence level of 99.99%, proportion of the samples that are seen at least '
                            'once in a test set'),
                    ])
            ],
            className="form_field",
        )

        _splitDefinition = html.Div(
            className="title_and_form",
            children=[
                html.H4(id="Define_split_title", children="Define splits"),
                dbc.Form(
                    children=[
                        dbc.Col(children=[__sampleProportion, __trainTestSplitGraph]),
                    ]
                ),
            ],
        )
        __LDTDDataType = html.Div(
            [
                dbc.Label("Processing according to data type"),
                dbc.FormText(
                    "LDTD1 means the preprocessing will be done on all samples in one time. "
                    "LDTD2 means the preprocessing will be done seperatly for each split."
                ),
                dbc.RadioItems(
                    id="in_type_of_data",
                    value="none",
                    inline=True,
                    options=[
                        {"label": "None", "value": "none"},
                        {"label": "LDTD 1", "value": "LDTD1"},
                        {"label": "LDTD 2", "value": "LDTD2"},
                    ],
                ),
            ],
            className="form_field",
        )

        __LDTDPeakPicking = html.Div(
            [
                dbc.Label("Perform peak picking"),
                dbc.RadioItems(
                    id="in_peak_picking",
                    value=0,
                    inline=True,
                    options=[
                        {"label": "No", "value": 0, "disabled": True},
                        {"label": "Yes", "value": 1, "disabled": True},
                    ],
                ),
            ],
            className="form_field",
        )

        __LDTDAlignment = html.Div(
            [
                dbc.Label("Perform alignment"),
                dbc.RadioItems(
                    id="in_alignment",
                    value=0,
                    inline=True,
                    options=[
                        {"label": "No", "value": 0, "disabled": True},
                        {"label": "Yes", "value": 1, "disabled": True},
                    ],
                ),
            ],
            className="form_field",
        )

        __LDTDNormalization = html.Div(
            [
                dbc.Label("Perform normalization"),
                dbc.RadioItems(
                    id="in_normalization",
                    value=0,
                    inline=True,
                    options=[
                        {"label": "No", "value": 0, "disabled": True},
                        {"label": "Yes", "value": 1, "disabled": True},
                    ],
                ),
            ],
            className="form_field",
        )

        __peakThreshold = html.Div(
            [
                dbc.Label("Peak Threshold"),
                dbc.Input(
                    id="in_peak_threshold_value",
                    value="500",
                    type="number",
                    min=1,
                    size="5",
                ),
            ],
            className="form_field",
        )

        __autoOptimizeNumber = html.Div(
            [
                dbc.Label("AutoOptimize number"),
                dbc.Input(
                    id="in_autoOptimize_value",
                    value="20",
                    type="number",
                    min=1,
                    size="5",
                ),
            ],
            className="form_field",
        )

        # TODO: Not displayed
        _otherProcessing = html.Div(
            className="title_and_form",
            children=[
                html.H4(id="preprocess_title", children="Other Preprocessing"),
                dbc.Form(
                    children=[
                        dbc.Col(
                            children=[
                                dbc.FormText(
                                    "Options in case of LDTD data that needs to be preprocess"
                                ),
                                dbc.Collapse(
                                    dbc.Card(
                                        dbc.CardBody(
                                            children=[
                                                __LDTDDataType,
                                                __LDTDPeakPicking,
                                                __LDTDAlignment,
                                                __LDTDNormalization,
                                                __peakThreshold,
                                                __autoOptimizeNumber,
                                            ]
                                        )
                                    ),
                                    id="collapse_preprocessing",
                                ),
                                dbc.Button(
                                    "Open",
                                    id="collapse_preprocessing_button",
                                    className="custom_buttons",
                                    color="primary",
                                    n_clicks=0,
                                ),
                            ]
                        )
                    ]
                ),
            ],
            style={"visibility": "hidden"},
        )

        _generateFile = html.Div(
            className="title_and_form",
            children=[
                html.H4(id="create_split_title", children="E) Generate file"),
                dbc.Form(
                    children=[
                        dbc.Col(
                            children=[
                                html.Div(id="output_button_split_file"),
                                html.Div(
                                    className="button_box",
                                    children=[
                                        html.Div(
                                            "Before clicking on the Create button, make shure all field with an * are correctly filled."
                                        ),
                                        dbc.Button(
                                            "Create",
                                            color="primary",
                                            id="split_dataset_button",
                                            className="custom_buttons",
                                            n_clicks=0,
                                        ),
                                        html.Div(
                                            id="output_button_split",
                                            children="",
                                            style={"display": "none"},
                                        ),
                                    ],
                                ),
                            ]
                        )
                    ]
                ),
            ],
        )

        return dbc.Tab(
            className="global_tab",
            label="Splits",
            children=[
                _introductionNotice,
                html.Div(
                    className="fig_group",
                    children=[
                        _file,
                        _classificationDesigns,
                    ],
                ),
                html.Div(
                    className="fig_group", children=[_splitDefinition, _dataFusion]
                ),
                html.Div(
                    className="fig_group", children=[_otherProcessing, _generateFile]
                ),
            ],
        )

    def _registerCallbacks(self) -> None:
        @self.app.callback(
            Output("train_test_split_graph", "figure"),
            [
                Input("in_nbr_splits", "value"),
                Input("in_percent_samples_in_test", "value"),
                Input("upload_datatable_output", "children"),
            ],
        )
        @log_exceptions(self._logger)
        def update_train_test_split_graph(slider_value, percent_test, uploaded_data):
            """
            uploaded_data : not used in the function, but its presence is needed to triger the callback
                            when the data file is uploaded/changed
            """
            if percent_test is None:
                return dash.no_update
            nbr_of_samples = len(self.metabo_controller.get_samples_id())
            if nbr_of_samples == 0:
                return dash.no_update
            percent_test = float(percent_test)
            slider_value = int(slider_value)

            return Plots.get_train_test_split_graph(
                nbr_of_samples, slider_value, percent_test
            )

        @self.app.callback(
            Output("in_use_raw", "value"), [Input("custom_big_tabs", "active_tab")]
        )
        @log_exceptions(self._logger)
        def update_use_raw(active_tab):
            if active_tab == "tab-1":
                use_raw = self.metabo_controller.is_data_raw()
                if use_raw is None:
                    return None
                if use_raw:
                    return "raw"
                progenesis_usage = self.metabo_controller.is_progenesis_data()
                if progenesis_usage:
                    return "normalized"
                return "nap"
            else:
                return dash.no_update

        @self.app.callback(
            [Output("datatable-section", "style"),
             Output("remove-rt-section", "style"),
             Output("in_remove_rt", "options"),
             Output("in_remove_rt", "value")],
            [Input("in_use_raw", "value"), Input("custom_big_tabs", "active_tab")],
        )
        @log_exceptions(self._logger)
        def normalization_selection(value, active_tab):
            options = [
                {"label": "True", "value": True},
                {"label": "False", "value": False},
            ]
            disabled_options = []
            for option in options:
                copied_option = option.copy()
                copied_option["disabled"] = True
                disabled_options.append(copied_option)

            if value is not None:
                if value == "nap":  # Not a Progenesis file
                    self.metabo_controller.set_raw_use_for_data(False)
                    self.metabo_controller.set_data_matrix_remove_rt(False)
                    return {"display": "block"}, {"display": "block"}, disabled_options, None

                self.metabo_controller.set_raw_use_for_data(
                    True if value == "raw" else False
                )
                return {"display": "block"}, {"display": "block"}, options, True
            return dash.no_update

        @self.app.callback(
            Output("metadata-section", "style"),
            [Input("upload_datatable_output", "style")],
        )
        def display_metadata_after_data_upload(style):
            if style == {"color": "green"}:
                return {"display": "block"}
            return {"display": "none"}

        @self.app.callback(
            [
                Output("info_progenesis_loaded", "children"),
                Output("upload_datatable_output", "children"),
                Output("upload_datatable_output", "style"),
            ],
            [Input("upload_datatable", "contents"),
             Input("upload_metadata", "contents")],
            [State("upload_datatable", "filename")],
        )
        @log_exceptions(self._logger)
        def upload_data(list_of_contents, _, list_of_names):
            if callback_context.triggered[0]["prop_id"] == "upload_metadata.contents":
                return "", dash.no_update, dash.no_update
            if list_of_contents is not None:
                try:
                    self.metabo_controller.set_data_matrix_from_path(
                        list_of_names, data=list_of_contents
                    )
                except TypeError as err:
                    return dash.no_update, [html.P(str(err))], {"color": "red"}
                except pandas.errors.ParserError as err:
                    return (
                        dash.no_update,
                        [html.P("Rows must have an equal number of columns")],
                        {"color": "red"},
                    )
                self.metabo_controller.reset_classification_designs()

                if self.metabo_controller.is_progenesis_data():
                    # trigger the update of possible targets
                    return (
                        "Info: Selection not needed, handled by Progenesis.",
                        [html.P(f'"{list_of_names}" has successfully been uploaded !')],
                        {"color": "green"},
                    )
                return (
                    "",
                    [html.P(f'"{list_of_names}" has successfully been uploaded !')],
                    {"color": "green"},
                )
            else:
                return dash.no_update, dash.no_update, dash.no_update

        @self.app.callback(
            [
                Output("in_target_col_name", "options"),
                Output("in_ID_col_name", "options"),
                Output("pairing_group_column", "options"),
                Output("upload_metadata_output", "children"),
                Output("upload_metadata_output", "style"),
            ],
            [
                Input("upload_metadata", "contents"),
                Input("custom_big_tabs", "active_tab")
            ],
            [State("upload_metadata", "filename")],
        )
        @log_exceptions(self._logger)
        def get_metadata_cols_names_to_choose_from(list_of_contents, active_tab, list_of_names):
            triggered_item = callback_context.triggered[0]["prop_id"].split(".")[0]
            self._logger.info(f"triggered_item: [{triggered_item}]")
            if active_tab == "tab-1":
                if triggered_item == "upload_metadata":
                    try:
                        self.metabo_controller.set_metadata(list_of_names, data=list_of_contents)
                    except TypeError as err:
                        return [], [], [], html.P(str(err)), {"color": "red"}
                    except Exception as e:
                        return [], [], [], html.P(str(e)), {"color": "red"}
                    self.metabo_controller.reset_classification_designs()

                    formatted_columns = Utils.format_list_for_checklist(self.metabo_controller.get_metadata_columns())
                    return (formatted_columns, formatted_columns, formatted_columns,
                            html.P(f'"{list_of_names}" has successfully been uploaded !'), {"color": "green"})
                else:
                    formatted_columns = Utils.format_list_for_checklist(self.metabo_controller.get_metadata_columns())
                    return formatted_columns, formatted_columns, formatted_columns, dash.no_update, dash.no_update

            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

        @self.app.callback(
            Output("warning_select_false", "children"),
            [Input("in_remove_rt", "value")],
        )
        @log_exceptions(self._logger)
        def remove_features_from_datamatrix(value):
            if value is not None:
                self.metabo_controller.set_data_matrix_remove_rt(bool(value))
                if value:
                    return ""
                else:
                    return (
                        "Warning : features detected before 1 minute in the experiment are extremely likely to be "
                        "noise and to be biologically irrelevant."
                    )

        @self.app.callback(
            Output("define_classes_desgn_exp", "children"),
            [Input("in_classification_type", "value")],
        )
        @log_exceptions(self._logger)
        def define_classes_for_experiment_design(t):
            """
            if the classification type is binary (0), certain options will be available
            if it is multiclass (1), other options wil be shown
            :param t:
            :return:
            """
            if t == 0:
                return [
                    html.Div(
                        className="title_and_form_mini",
                        children=[
                            dbc.Form(
                                children=[
                                    dbc.Col(
                                        children=[
                                            html.Div(
                                                [
                                                    dbc.Label("Label 1"),
                                                    dbc.Input(
                                                        id="class1_name",
                                                        placeholder="Enter name",
                                                        debounce=True,
                                                        className="form_input_text",
                                                    ),
                                                ],
                                                className="form_field",
                                            ),
                                            html.Div(
                                                [
                                                    dbc.Label("Class(es)"),
                                                    dbc.Checklist(
                                                        id="possible_groups_for_class1"
                                                    ),
                                                ]
                                            ),
                                        ]
                                    )
                                ]
                            )
                        ],
                    ),
                    html.Div(
                        className="title_and_form_mini",
                        children=[
                            dbc.Form(
                                children=[
                                    dbc.Col(
                                        children=[
                                            html.Div(
                                                [
                                                    dbc.Label("Label 2"),
                                                    dbc.Input(
                                                        id="class2_name",
                                                        placeholder="Enter name",
                                                        debounce=True,
                                                        className="form_input_text",
                                                    ),
                                                ],
                                                className="form_field",
                                            ),
                                            html.Div(
                                                [
                                                    dbc.Label("Class(es)"),
                                                    dbc.Checklist(
                                                        id="possible_groups_for_class2"
                                                    ),
                                                ]
                                            ),
                                        ]
                                    )
                                ]
                            )
                        ],
                    ),
                ]

        @self.app.callback(
            [
                Output("possible_groups_for_class1", "options"),
                Output("possible_groups_for_class2", "options"),
                Output("output_btn_add_desgn_exp", "children"),
            ],
            [
                Input("in_target_col_name", "value"),
                Input("info_progenesis_loaded", "children"),
                Input("custom_big_tabs", "active_tab"),
            ],
        )
        @log_exceptions(self._logger)
        def update_possible_classes_exp_design(target_col, children, active_tab):
            triggered_id = callback_context.triggered[0]["prop_id"].split(".")[0]
            if active_tab == "tab-1":
                if triggered_id == "info_progenesis_loaded" or \
                        (triggered_id == "in_target_col_name" and target_col not in [None, "", []]):
                    # Give the MetaData attribute the values of either one or multiple column to create the targets
                    # for the experiment
                    if triggered_id == "in_target_col_name":
                        self.metabo_controller.set_target_columns(target_col)
                    # Format the targets list to get only the (maybe new) classes names to display
                    formatted_possible_targets = Utils.format_list_for_checklist(
                        self.metabo_controller.get_unique_targets()
                    )
                    return (
                        formatted_possible_targets,
                        formatted_possible_targets,
                        "",
                    )
                else:
                    return dash.no_update, dash.no_update, dash.no_update
            else:
                return dash.no_update, dash.no_update, dash.no_update

        @self.app.callback(
            [Output("class1_name", "value"),
             Output("possible_groups_for_class1", "value"),
             Output("class2_name", "value"),
             Output("possible_groups_for_class2", "value"),
             Output("setted_classes_container", "children"),
             Output("setted_classes_container", "style"),
             Output("error_classification_type", "children")],
            [Input("btn_add_design_exp", "n_clicks"),
             Input("remove_classification_design_button", "n_clicks"),
             Input("in_target_col_name", "value"),
             Input("info_progenesis_loaded", "children"),
             Input("custom_big_tabs", "active_tab")],
            [State("class1_name", "value"),
             State("possible_groups_for_class1", "value"),
             State("class2_name", "value"),
             State("possible_groups_for_class2", "value")],
        )
        @log_exceptions(self._logger)
        def add_n_reset_classes_exp_design(n_add, n_remove, target_col, children, active_tab, c1, g1, c2, g2):
            triggered_id = callback_context.triggered[0]["prop_id"].split(".")[0]

            if (triggered_id == "remove_classification_design_button" or triggered_id == "in_target_col_name"
                    or triggered_id == "info_progenesis_loaded"):
                self.metabo_controller.reset_classification_designs()
            elif triggered_id == "btn_add_design_exp":
                try:
                    self.metabo_controller.add_classification_design({c1: g1, c2: g2})
                    self._logger.info(f"Classification designs : {self.metabo_controller._metabo_experiment.classification_designs}")
                except ValueError as ve:
                    return (dash.no_update, dash.no_update, dash.no_update, dash.no_update,
                            dash.no_update, dash.no_update, str(ve))

            return ("", 0, "", 0, self._get_wrapped_classification_designs(), {"display": "block", "padding": "1em"}, "")

        @self.app.callback(
            Output("collapse_preprocessing", "is_open"),
            [Input("collapse_preprocessing_button", "n_clicks")],
            [State("collapse_preprocessing", "is_open")],
        )
        def toggle_collapse_preprocessing(n, is_open):
            if n:
                return not is_open
            return is_open

        @self.app.callback(
            Output("in_ID_col_name", "value"),
            [Input("in_ID_col_name", "value"), Input("custom_big_tabs", "active_tab")],
        )
        @log_exceptions(self._logger)
        def update_ID_col_name(new_value, active_tab):
            if active_tab == "tab-1":
                if new_value not in [None, ""]:
                    self.metabo_controller.set_id_column(new_value)
                return self.metabo_controller.get_id_column()
            return dash.no_update

        @self.app.callback(
            Output("pairing_group_column", "value"),
            [
                Input("pairing_group_column", "value"),
                Input("custom_big_tabs", "active_tab"),
            ],
        )
        @log_exceptions(self._logger)
        def update_pairing_group_column(new_value, active_tab):
            if active_tab == "tab-1":
                if new_value not in [None, ""]:
                    self.metabo_controller.set_pairing_group_column(new_value)
                return self.metabo_controller.get_pairing_group_column()
            return dash.no_update

        @self.app.callback(
            [
                Output("output_button_split_file", "children"),
                Output("error_percent_samples_in_test", "children"),
                Output("error_upload_datatable", "children"),
                Output("error_data_normalization", "children"),
                Output("error_upload_metadata", "children"),
                Output("error_classification_designs", "children"),
            ],
            [Input("split_dataset_button", "n_clicks")],
            [State("in_percent_samples_in_test", "value"),
             State("in_nbr_splits", "value")],
        )
        @log_exceptions(self._logger)
        def saving_params_of_splits_batch(n, train_test_proportion, nbr_splits):
            """
            Create the file (json) which will contains all info about the split creation / data experiment.
            """
            if n >= 1:
                train_test_proportion_error = ""
                try:
                    casted_train_test_proportion = float(train_test_proportion)
                    if casted_train_test_proportion >= 1 or casted_train_test_proportion <= 0:
                        train_test_proportion_error = "The proportion must be between 0 and 1 (excluded)."
                    self.metabo_controller.set_train_test_proportion(casted_train_test_proportion)
                except (ValueError, TypeError):
                    train_test_proportion_error = "The train/test proportion must be a decimal number between 0 and 1 " \
                                                  "excluded."

                normalization_error = ""
                datatable_error = ""
                metadata_error = ""
                invalid_id_error = ""
                classification_design_error = ""
                if self.metabo_controller.is_data_raw() is None:
                    normalization_error = "Please select a normalization method."
                elif not self.metabo_controller.data_is_set():
                    datatable_error = "You must upload a file before splitting it."
                elif not self.metabo_controller.metadata_is_set():
                    metadata_error = "You must upload a metadata file before splitting it."
                elif not self.metabo_controller.validate_id_column():
                    invalid_id_error = html.P(f'You must provide a valid name of unique id column', style={"color": "red"})
                elif not self.metabo_controller.get_all_classification_designs_names():
                    classification_design_error = "You must add at least one classification design before " \
                                                "splitting the data."

                if train_test_proportion_error != "" or datatable_error != "" or normalization_error != "" or metadata_error != "" \
                    or classification_design_error != "" or invalid_id_error != "":
                    return invalid_id_error, train_test_proportion_error, datatable_error, normalization_error, metadata_error, classification_design_error
                self.metabo_controller.set_number_of_splits(nbr_splits)
                self.metabo_controller.create_splits()
                
                # Dump file to dump folder and to save folder (backup)
                metabo_expe_filename = Utils.get_metabo_experiment_path("medic_splits") # Get save file path
                metabo_expe_obj = self.metabo_controller.generate_save()
                Utils.dump_metabo_expe(metabo_expe_obj) # Dump the classification design to the dump folder
                Utils.dump_metabo_expe(metabo_expe_obj, metabo_expe_filename) # Save the classification design
                del metabo_expe_obj

                self._logger.info(f"{self.metabo_controller._metabo_experiment.classification_designs}")
                self._logger.info(f"Classification design splits file '{metabo_expe_filename}' saved.")
                send_file(Utils.get_dumped_metabo_experiment_path())
                
                return (
                    [html.P(f'The parameters file "{basename(metabo_expe_filename)}" and the splits have been created.', style={"color": "green"}),
                     html.P('Please select the "Machine Learning" tab to continue.')],
                    "", "", "", "", "",
                )
            else:
                return (dash.no_update,) * 6

        @self.app.callback(
            Output("class_balancing_options", "children"),
            [Input("btn_add_design_exp", "n_clicks"),
             Input("remove_classification_design_button", "n_clicks")],
        )
        @log_exceptions(self._logger)
        def add_class_balancing_options(n_clicks_add, n_clicks_remove):
            """
            Add a class balancing option to the list of class balancing options.
            """
            global_classes_repartition = None
            if n_clicks_add >= 1:
                global_classes_repartition = self.metabo_controller.get_classes_repartition_for_all_experiment()

            if global_classes_repartition is None:
                return dash.no_update

            sliders = []
            for classes_name, classes_repartition in global_classes_repartition.items():
                if len(classes_repartition) > 2:
                    raise NotImplementedError("Only two classes are supported for now.")

                keys = list(classes_repartition.keys())
                total = sum(classes_repartition.values())
                class_a_repartition = math.floor(classes_repartition[keys[0]] / total * 100)
                class_b_repartition = math.ceil(classes_repartition[keys[1]] / total * 100)

                if class_a_repartition == class_b_repartition:
                    sliders.append(
                        html.Div(
                            [
                                html.H5(f"{keys[0]} versus {keys[1]}"),
                                html.P("The classes are already balanced."),
                            ]
                        )
                    )
                    continue

                if class_a_repartition < class_b_repartition:
                    class_a_repartition, class_b_repartition = class_b_repartition, class_a_repartition
                    keys[0], keys[1] = keys[1], keys[0]

                difference_to_balance = class_a_repartition - 50

                steps = Utils.get_closest_integer_steps(difference_to_balance)

                marks = {}
                for step in steps:
                    marks[step] = f"{class_a_repartition - step}:{class_b_repartition + step}"

                sliders.append(
                    html.Div(
                        [
                            html.H5(f"{keys[0]} versus {keys[1]}"),
                            html.P(f"The classes are not balanced, you can use the slider to balance them."),

                            dcc.Slider(
                                id={
                                    "type": "class_balancing_slider",
                                    "index": classes_name,
                                },
                                min=0,
                                max=difference_to_balance,
                                step=1,
                                value=0,
                                marks=marks
                            ),
                        ]
                    )
                )

            return sliders

        @self.app.callback(
            Output({"type": "class_balancing_slider", "index": MATCH}, "value"),
            Input({"type": "class_balancing_slider", "index": MATCH}, "value"),
            [State({"type": "class_balancing_slider", "index": MATCH}, "id")],
        )
        @log_exceptions(self._logger)
        def update_class_balancing_slider(value, id):
            """
            Update the class balancing slider.
            """
            if value is None:
                return dash.no_update

            self.metabo_controller.set_balance_correction_for_experiment(id["index"], value)
            return value

        @self.app.callback(
            Output("error_link_each_sample_to_target", "children"),
            [Input("in_ID_col_name", "value"),
             Input("custom_big_tabs", "active_tab"),
             Input("split_dataset_button", "n_clicks")],
        )
        @log_exceptions(self._logger)
        def validate_id_column(value, active_tab, n_clicks) -> dash._callback.NoUpdate | str:
            if active_tab != "tab-1":
                return dash.no_update

            if self.metabo_controller.validate_id_column():
                return ""
            
            id_column = self.metabo_controller.get_id_column()
            if id_column is None:
                error_msg = dash.no_update if n_clicks < 1 else "You must provide a valid name of unique id column"
            else:                            
                error_msg = f"'{id_column}' is not a valid name of unique id column"
            return error_msg

    def _get_wrapped_classification_designs(self):
        children_container = [html.Div("Classification design")]
        all_classification_designs = (
            self.metabo_controller.get_all_classification_designs_names()
        )

        if len(all_classification_designs) == 0:
            button = html.Div(
                dbc.Button(
                    "Reset",
                    className="custom_buttons",
                    id="remove_classification_design_button",
                ),
                style={"display": "none"},
            )
            return html.Div([html.P("No classification design setted yet."), button])

        for _, full_name in all_classification_designs:
            children_container.append(
                html.Div(
                    children=["- " + full_name],
                    style={
                        "display": "flex",
                        "justify-content": "space-between",
                        "align-items": "center",
                    },
                )
            )
        button = html.Div(
            dbc.Button(
                "Reset",
                className="custom_buttons",
                id="remove_classification_design_button",
            ),
            style={"textAlign": "right"},
        )
        children_container.append(button)
        return children_container
