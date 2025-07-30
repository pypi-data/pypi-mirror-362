import matplotlib
matplotlib.use('agg')

from dash import html, dcc
from dash.dependencies import Input, Output
import dash
import dash_bootstrap_components as dbc
from flask import request, jsonify
import os
import signal

from .tabs import *
from ..domain import MetaboController

from medic.service import set_log_filename, init_logger
import threading

# Code for the logging
if threading.current_thread() is threading.main_thread():
    logger = set_log_filename()
    logger.info(f"Starting MeDIC")
else:
    logger = init_logger()
    logger.debug(f"New thread '{threading.current_thread().name}')")

# Launch dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.LUX],
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)
app.title = "MeDIC"
server = app.server
# app.scripts.config.serve_locally = False
app.css.config.serve_locally = False
app.config.suppress_callback_exceptions = True
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

metabo_controller = MetaboController()
infoTab = InfoTab(app, metabo_controller)
splitsTab = SplitsTab(app, metabo_controller)
mLTab = MLTab(app, metabo_controller)
resultsTab = ResultsTab(app, metabo_controller)
resultsAggregatedTab = ResultsAggregatedTab(app, metabo_controller)
interpretTab = InterpretTab(app, metabo_controller)

app.layout = html.Div(
    id="page",
    children=[
        html.Div(id="dataCache", children=[], style={"display": "none"}),
        html.Div(
            id="title_container",
            className="row",
            style={"display": "flex", "justify-content": "space-between", "align-items": "center"},
            children=[
                html.Div(
                    children=[
                        html.H1(id="title", children="MeDIC"),
                        html.Div(
                            children=[
                                html.P(
                                    "Metabolomics Dashboard", style={"color": "white", 'text-transform': 'uppercase', "margin-bottom": "0"}
                                ),
                                html.P(
                                    "for Interpretable Classification",
                                    style={"color": "white", 'text-transform': 'uppercase', "margin-bottom": "0"},
                                ),
                            ],
                            id="acronym",
                            style={"display": "flex", "justify-content": "center"},
                        ),
                    ],
                    id="title_bg",
                ),
                html.Div(  # Conteneur parent du bouton
                    children=[
                        html.Button("X", id="close-button", style={
                            "color": "white", "background-color": "darkred",
                            "border": "none", "border-radius": "50%", "width": "30px", "height": "30px",
                            "font-size": "20px", "line-height": "20px", "text-align": "center", "padding": "0",
                            "cursor": "pointer", "margin": "20px", "margin-top": "0px", "flex-shrink": "0"})
                    ],
                    style={"display": "flex", "justify-content": "flex-end", "align-items": "center", "flex": "1"}
                ),
                html.Div(id="message_close", style={"color": "white", "background-color": "darkred", "font-size": "24px", "display": "none"}),
            ],
        ),
        dcc.Location(id='url', refresh=True),
        html.Div(id='clientside-container', style={"display": "none"}),
        html.Div(
            id="main-content",
            children=[
                dbc.Tabs(
                    id="custom_big_tabs",
                    active_tab="tab-0",
                    className="global_tabs_container",
                    children=[
                        infoTab.getLayout(),
                        splitsTab.getLayout(),
                        mLTab.getLayout(),
                        #dbc.Tab(label="Splits", disabled=True),
                        #dbc.Tab(label="Machine Learning", disabled=True),
                        resultsTab.getLayout(),
                        resultsAggregatedTab.getLayout()
                        # interpretTab.getLayout()
                    ],
                )
            ],
        ),
    ],
)


app.clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks > 0) {
            if (confirm("Do you want to close MeDIC application server?")) {
                window.close();
                fetch('/shutdown', {method: 'POST'})
                    .then(response => response.json())
                    .then(data => console.log(data));
                document.getElementById('message_close').innerHTML = 'Server stopped. Please close this web page.';
                document.getElementById('message_close').style.display = 'block';
            }
        }
    }
    """,
    Output('clientside-container', 'children'),
    Input('close-button', 'n_clicks')
)

@server.route('/shutdown', methods=['POST'])
def shutdown():
    try:
        logger.info("Shutting down MeDIC server...")
        shutdown_func = request.environ.get('werkzeug.server.shutdown')
        if shutdown_func:
            shutdown_func()
        else:
            os.kill(os.getpid(), signal.SIGINT)
        return jsonify({'message': 'MeDIC server is shutting down...'})
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")
        return jsonify({'error': str(e)}), 500
