import json
import pickle
import pprint
from datetime import datetime
from io import StringIO
from time import time
from typing import Any, Dict, Union

import h5py
import numpy as np
import pandas as pd
import plotly
import plotly.express as px
from dash import Dash, Input, Output, callback, callback_context, dcc, html, no_update
from dash_bootstrap_components import Popover
from loguru import logger
from plotly.subplots import make_subplots
from skactiveml.classifier import SklearnClassifier
from skactiveml.pool import UncertaintySampling
from sklearn.decomposition import PCA
from sklearn.svm import SVC

embeddings_file = None
arrays_file = None
filecolumn = None
classcolumn = None
emb_dim_prefix = None
ENCODING = "utf-16-le"


def _no_matchin_data_message() -> dict:
    """Display a message when there is no matching data.

    Returns:
        dictionary with options to display the message
    """
    return {
        "layout": {
            "xaxis": {"visible": False},
            "yaxis": {"visible": False},
            "annotations": [
                {
                    "text": "No matching data",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {"size": 28},
                },
            ],
        },
    }


def _no_trajectory_selected_message() -> dict:
    """Show a 'no trajectory selected' message.

    Returns:
        dictionary with options to display the message
    """
    return {
        "layout": {
            "xaxis": {"visible": False},
            "yaxis": {"visible": False},
            "annotations": [
                {
                    "text": "No point selected",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {"size": 28},
                },
            ],
        },
    }


def _renorm_array(image: np.ndarray) -> np.ndarray:
    """Transform array values to [0, 1] interval

    Args:
        image: input array

    Returns:
        array of identical shape, with values between 0 and 1
    """
    if image.max() != image.min():
        return (image - image.min()) / (image.max() - image.min())
    else:
        return image


def show_hdf5_image(filename: str) -> plotly.graph_objs.Figure:
    """Create a plotly express image rendering.

    Args:
        filename: HDF5 dataset to be displayed

    Returns:
        the rendered Figure
    """
    with h5py.File(arrays_file) as file:
        farray = file[filename][()]
    farray = np.transpose(farray, (1, 2, 0))

    for channel_idx in range(farray.shape[-1]):
        farray[:, :, channel_idx] = _renorm_array(farray[:, :, channel_idx])

    while farray.shape[-1] < 3:
        farray = np.append(farray, np.zeros_like(farray)[:, :, 0:1], axis=-1)
    return px.imshow(farray)


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    title="LatentViewer",
)

gamma_description = [
    html.H6("Gamma", id="svm-gamma-param-title"),
    dcc.Input(
        id="svm-gamma-param",
        type="number",
        value=0.03,
        min=0,
    ),
    Popover(
        [
            "Gamma defines the reach of a single training example. "
            "High gamma --> far reaching influence. (see ",
            html.A(
                "the SKLearn docs",
                href=(
                    "https://scikit-learn.org/stable/auto_examples/svm"
                    "/plot_rbf_parameters.html"
                ),
                target="_blank",
            ),
            ")",
        ],
        target="svm-gamma-param-title",
        id="gamma-popover",
        trigger="click",
        hide_arrow=False,
        placement="top",
    ),
]

c_regularization_description = [
    html.H6("C", id="svm-C-param-title"),
    dcc.Input(
        id="svm-C-param",
        type="number",
        value=1.0,
        min=0,
    ),
    Popover(
        [
            "C regularizes SVM decision function. Higher C --> more complex decision "
            "function. (see ",
            html.A(
                "the SKLearn docs",
                href=(
                    "https://scikit-learn.org/stable/auto_examples/svm/"
                    "plot_rbf_parameters.html"
                ),
                target="_blank",
            ),
            ")",
        ],
        target="svm-C-param-title",
        id="C-popover",
        trigger="click",
        hide_arrow=False,
        placement="top",
    ),
]

app.layout = html.Div(
    [
        html.Div(
            [
                dcc.Graph(
                    id="trajectories-scatter",
                    style={
                        "width": "100vh",
                        "height": "100vh",
                    },
                ),
            ],
            style={
                "width": "60%",
                "display": "inline-block",
                "padding": "0 20",
            },
            id="scatter-plot-container",
        ),
        html.Div(
            [
                dcc.Graph(
                    id="show-trajectory",
                    style={
                        "height": "40%",
                    },
                ),
                html.Div(
                    [
                        dcc.RadioItems(
                            id="label-selector",
                            options=[
                                {"label": "None", "value": -1},
                                {"label": "Regular", "value": 0},
                                {"label": "Outlier", "value": 1},
                            ],
                            inline=True,
                        ),
                        html.Button(
                            "Least certain trajectory?",
                            id="query-model",
                        ),
                        html.Div(
                            gamma_description,
                            style={
                                "display": "inline-block",
                                "text-align": "center",
                                "padding": "5pt",
                            },
                        ),
                        html.Div(
                            c_regularization_description,
                            style={
                                "display": "inline-block",
                                "text-align": "center",
                            },
                        ),
                    ],
                    id="label-prediction-container",
                    style={"inline": "true"},
                ),
                dcc.Graph(
                    id="show-related-images",
                    style={
                        "height": "60%",
                    },
                ),
                html.Button("Download Excel", id="btn-download-excel"),
                html.Button("Download CSV", id="btn-download-csv"),
                html.Button("Download Model", id="btn-download-model"),
                dcc.Download(id="download-data"),
            ],
            style={
                "display": "inline-block",
                "vertical-align": "top",
                "width": "40%",
            },
        ),
        html.Div(
            [
                html.Button("Like!", id="like-button"),
                dcc.Store(
                    id="stored-data",
                    data={"last-clicked-time": time()},
                ),
                dcc.Store(id="raw-pca-data"),
                dcc.Store(id="fitted-data"),
                dcc.Store(id="x-values"),
                dcc.Store(id="y-labeled"),
                dcc.Store(id="y-predicted"),
                dcc.Store(id="selected-data-point"),
                dcc.Store(id="queried-data-point"),
                dcc.Store(id="svc-model"),
                dcc.Store(id="metadata-column-names"),
                dcc.Download(id="download-model"),
            ],
        ),
    ],
)


@callback(
    Output("trajectories-scatter", "clickData"),
    Output("stored-data", "data"),
    Input("stored-data", "data"),
    Input("scatter-plot-container", "n_clicks"),
    prevent_initial_call=True,
)
def update_stored_data(stored_data: dict, _) -> tuple:
    """Reset clicked data point to None after a double-click.

    Args:
        stored_data: has time of previous click inside scatter-plot-container
        _: we only need to know whether the scatter-plot-container was clicked

    Returns:
        ([None | no_update], [{'last-clicked-time': now} | no_update])
    """
    changed_inputs = [x["prop_id"] for x in callback_context.triggered]
    # Only change something if there was a click inside scatter-plot-container
    if "scatter-plot-container.n_clicks" in changed_inputs:
        # If there is less than 0.3 sec between clicks, reset selected data point
        now = time()
        if now - stored_data["last-clicked-time"] < 0.3:
            logger.debug("Reset clicked data point")
            return None, {"last-clicked-time": now}
        else:
            return no_update, {"last-clicked-time": now}
    else:
        return no_update, no_update


@callback(
    Output("show-trajectory", "figure"),
    Input("trajectories-scatter", "hoverData"),
    Input("selected-data-point", "data"),
    Input("metadata-column-names", "data"),
    prevent_initial_call=True,
)
def render_trajectory_image(
    hoverData: Union[dict, None],
    clickData: Union[Dict, None],
    metadata_columns_json: str,
) -> Union[plotly.graph_objs.Figure, dict]:
    """Render the main image.

    Args:
        hoverData: the datapoint on which the cursor hovered last
        clickData: a datapoint selected by being clicked
        metadata_columns: column names to be displayed next to the image

    Returns:
        a figure to be shown in the top right of the interface
    """
    # If there is no selected data point, show a message about this
    if clickData is not None:
        filename = clickData["points"][0]["customdata"][0]
        metadata_dict = clickData["points"][0]["customdata"]
    elif hoverData is not None:
        filename = hoverData["points"][0]["customdata"][0]
        metadata_dict = hoverData["points"][0]["customdata"]
    else:
        return _no_trajectory_selected_message()

    metadata_columns: list[str] = json.loads(metadata_columns_json)
    # Add classification probabilities to metadata
    metadata_columns += ["P_regular", "P_outlier"]
    fig = show_hdf5_image(filename)
    fig.update_layout(
        title=filename.split(
            "/",
        )[-1],
        margin={"l": 0, "b": 0, "r": 150},
    )

    # Show metatdata values
    annotation_string = ""
    for idx, m_col_name in enumerate(metadata_columns):
        # Class probabilities are only present after querying the model,
        # deal with this through a try-except
        try:
            value = metadata_dict[idx + 1]
            annotation_string += f"{m_col_name}: {value}<br>"
        except IndexError:
            pass

    fig.add_annotation(
        dict(
            text=annotation_string,
            x=0.85,
            y=1,
            showarrow=False,
            textangle=0,
            xref="paper",
            yref="paper",
            align="left",
            xanchor="left",
        ),
    )

    return fig


@callback(
    Output("trajectories-scatter", "figure"),
    Input("raw-pca-data", "data"),
    Input("y-predicted", "data"),
    Input("metadata-column-names", "data"),
)
def plot_trajectory_points(
    plot_json: str,
    predicted_labels: str,
    metadata_columns_json: str,
) -> plotly.graph_objs.Figure:
    """Plot the 3D embeddings of the images.

    Args:
        plot_json: json-string with embedding data after PCA
        predicted_labels: predicted classification of images
        metadata_columns: columns containing metadata to be displayed next to the image

    Returns:
        3D scatterplot of image embeddings
    """
    plot_df = pd.read_json(StringIO(plot_json))
    metadata_columns = json.loads(metadata_columns_json)

    if predicted_labels is not None:
        plabels = pd.read_json(StringIO(predicted_labels))
        plot_df = plot_df.drop(columns=classcolumn)

        plot_df = pd.merge(plot_df, plabels, on=filecolumn)

    plot_df[filecolumn] = plot_df[filecolumn].apply(lambda x: x[5:])

    fig = px.scatter_3d(
        data_frame=plot_df,
        x="xcol",
        y="ycol",
        z="zcol",
        custom_data=[filecolumn] + metadata_columns,
        size="ms",
        opacity=0.5,
        color=classcolumn,
    )
    fig.update_layout(
        margin={
            "l": 0,
            "b": 0,
            "t": 0,
            "r": 0,
        },
        hovermode="closest",
    )
    return fig


@callback(
    Output("show-related-images", "figure"),
    Input("trajectories-scatter", "clickData"),
    Input("raw-pca-data", "data"),
)
def update_related_images(
    clickData: Union[dict, None], plot_json: str
) -> Union[plotly.graph_objs.Figure, dict]:
    """Show the nine images whose embeddings are closest to the selected one.

    Args:
        clickData: the clicked data point
        plot_json: PCA data of the embeddings

    Returns:
        3x3 grid of related images, or a message saying there are none
    """
    # due to rendering speed, we only show related images on a clicked data point,
    # not on a hovered point
    if clickData is None:
        return _no_matchin_data_message()

    plot_df = pd.read_json(StringIO(plot_json))

    # in the dataframe we prepend the filename with "file_" to prevent
    # converting to float here we remove those first 5 characters again
    plot_df[filecolumn] = plot_df[filecolumn].apply(lambda x: x[5:])

    click_dict = clickData["points"][0]

    distances = np.zeros_like(plot_df["xcol"].values)
    for axis in ["x", "y", "z"]:
        distances += (plot_df[f"{axis}col"].values - click_dict[axis]) ** 2

    rown_nr_sorted_by_distance = np.argsort(distances)

    rows, cols = 3, 3
    fig = make_subplots(
        rows=rows,
        cols=cols,
        horizontal_spacing=0.1,
        vertical_spacing=0.01,
    )
    for i in range(min(rows * cols, len(rown_nr_sorted_by_distance) - 1)):
        plot_row = i // cols + 1
        plot_col = i % cols + 1
        df_index = rown_nr_sorted_by_distance[i + 1]
        filename = plot_df.iloc[df_index].loc[filecolumn]

        fig.add_trace(
            show_hdf5_image(
                filename,
            ).data[0],
            row=plot_row,
            col=plot_col,
        )

    fig.update_layout(
        {
            ax: {"visible": False, "matches": None}
            for ax in fig.to_dict()["layout"]
            if "axis" in ax
        },
    )
    fig.update_layout(margin={"l": 0, "b": 0, "t": 50, "r": 0})
    return fig


@callback(
    Output("raw-pca-data", "data"),
    Output("fitted-data", "data"),
    Output("metadata-column-names", "data"),
    Input("like-button", "n_clicks"),
)
def update_raw_pca_data(_: Any) -> tuple:
    """Perform initial embedding data parsing.

    Args:
        _: Any type of input on start-up, for now solved with a like-button

    Returns:
        PCA(3) of embedding vectors, embeddings dataframe, and metadata column names

    Raises:
        ValueError: if no embedding file has been provided
    """
    if embeddings_file is None:
        raise ValueError("No embeddings file provided")
    edf = pd.read_csv(embeddings_file, sep=";", index_col=0)
    df = edf.copy()

    embeddings_columns = [col for col in df.columns if col.startswith(emb_dim_prefix)]
    if len(embeddings_columns) == 0:
        logger.error(
            f"No embedding columns found with prefix {emb_dim_prefix}",
        )
    logger.debug(f"Embedding file columns: {pprint.pformat(list(df.columns))}")
    logger.info(f"Label column: '{classcolumn}'")
    if classcolumn not in df.columns:
        logger.warning(
            f"Label column '{classcolumn}' not found, adding it instead",
        )
        df[classcolumn] = "regular"

    known_columns = embeddings_columns + [filecolumn, classcolumn]
    metadata_columns = [col for col in df.columns if col not in known_columns]

    pca_decomposer = PCA()
    pca_vectors = pca_decomposer.fit_transform(
        df.loc[:, embeddings_columns].values,
    )

    xvalues = df.loc[:, embeddings_columns]
    xvalues = pca_vectors[:, :3]

    # Force to dataframe to make the linter happy
    plot_df = pd.DataFrame(df[[filecolumn, classcolumn] + metadata_columns].copy())

    plot_df[filecolumn] = plot_df[filecolumn].apply(lambda x: f"file_{x}")
    plot_df["xcol"] = xvalues[:, 0]
    plot_df["ycol"] = xvalues[:, 1]
    plot_df["zcol"] = xvalues[:, 2]
    plot_df["ms"] = 10

    df[filecolumn] = df[filecolumn].apply(lambda x: f"file_{x}")

    return plot_df.to_json(), df.to_json(), json.dumps(metadata_columns)


@callback(
    Output("x-values", "data"),
    Output("y-labeled", "data", allow_duplicate=True),
    Output("y-predicted", "data", allow_duplicate=True),
    Input("fitted-data", "data"),
    prevent_initial_call="initial_duplicate",
)
def set_initial_xy_values(dataf: str) -> tuple:
    """Set the initial values for model input and output.

    Fitted-data gets only one update, on start-up, so this function will run only once
    during the execution lifetime.

    Args:
        dataf: json string for original dataframe

    Returns:
        dataframe with filename and embeddings, label indicator, predicted class
    """
    df = pd.DataFrame(pd.read_json(StringIO(dataf)))

    embeddings_columns = [col for col in df.columns if col.startswith(emb_dim_prefix)]
    if len(embeddings_columns) == 0:
        logger.error(
            f"No embedding columns found with prefix {emb_dim_prefix}",
        )

    # x_values is just filename and embeddings
    x_values = df.loc[
        :,
        [
            filecolumn,
        ]
        + embeddings_columns,
    ]

    # Use -1 to set every data point to unlabeled
    y_labeled = df.loc[:, [filecolumn]].copy()
    y_labeled["label"] = -1

    # Initial class prediction is "Regular" for every data point
    y_prediction = df.loc[:, [filecolumn]].copy()
    y_prediction[classcolumn] = "Regular"

    return x_values.to_json(), y_labeled.to_json(), y_prediction.to_json()


@callback(
    Output("label-selector", "value"),
    Output("label-selector", "style"),
    Input("selected-data-point", "data"),
    Input("y-labeled", "data"),
)
def display_label_container(
    click_data: Union[dict, None], labels_str: str
) -> tuple[int, dict]:
    """Render labeling interface

    Args:
        click_data: the selected data point
        labels_str: dataframe json with human-assigned labels

    Returns:
        the human-assigned label, and the rendering style
    """
    # Only render on click, not on hover
    if click_data is None:
        return -1, {"visibility": "hidden"}

    trajectory_id = f"file_{click_data['points'][0]['customdata'][0]}"
    logger.debug({f"Selected trajectory {trajectory_id}"})

    labels = pd.read_json(StringIO(labels_str))
    label: int = labels[labels[filecolumn] == trajectory_id]["label"].iloc[0]

    logger.debug(f"Current label: {label}")
    return label, {"visibility": "visible"}


@callback(
    Output("y-labeled", "data", allow_duplicate=True),
    Input("y-labeled", "data"),
    # Input("trajectories-scatter", "clickData"),
    Input("selected-data-point", "data"),
    Input("label-selector", "value"),
    prevent_initial_call="initial_duplicate",
)
def update_label(all_labels, click_data, label):
    if click_data is None:
        return no_update

    trajectory_id = f"file_{click_data['points'][0]['customdata'][0]}"
    labels = pd.read_json(StringIO(all_labels))
    labels.loc[labels[filecolumn] == trajectory_id, "label"] = label

    return labels.to_json()


@callback(Input("y-labeled", "data"))
def print_labels(labels):
    ldf: pd.arrays.ArrayLike = pd.DataFrame(pd.read_json(StringIO(labels)))[
        "label"
    ].values
    logger.debug(f"Currently labeled values: {ldf[ldf >= 0]}")


@callback(
    Output("queried-data-point", "data", allow_duplicate=True),
    Output("svc-model", "data"),
    Output("y-predicted", "data", allow_duplicate=True),
    Input("query-model", "n_clicks"),
    Input("x-values", "data"),
    Input("y-labeled", "data"),
    Input("raw-pca-data", "data"),
    Input("svc-model", "data"),
    Input("svm-C-param", "value"),
    Input("svm-gamma-param", "value"),
    Input("metadata-column-names", "data"),
    prevent_initial_call="initial_duplicate",
)
def query_model(
    button_click: Any,
    x_values_str: str,
    y_labels_str: str,
    pca_data: str,
    model: Union[str, None],
    svm_C: float,
    svm_gamma: float,
    metadata_columns: str,
) -> tuple:
    """Query the model for the least confident data point.

    Args:
        button_click: trigger for function call
        x_values_str: json string for embedding dataframe
        y_labels_str: json string for label dataframe
        pca_data: json string for PCA(3) of the embeddings
        model: hexstring containing SVC model
        svm_C: SVC C hyperparameter
        svm_gamma: SVC gamma hyperparameter
        metadata_columns: json string containing list of metadata columns

    Returns:
        clickdata for queried data point, retrained SVC model, y_pred from new model
    """
    # Only run when the query-model button has been clicked
    if callback_context.triggered_id != "query-model":
        return no_update, no_update, no_update

    if model is not None:
        clf: SklearnClassifier = pickle.loads(bytes.fromhex(model))
    else:
        clf = SklearnClassifier(
            SVC(probability=True, kernel="rbf"),
            classes=[0, 1],
            missing_label=-1,
        )
    logger.debug(f"Using model of type {type(clf)}")

    clf.estimator.set_params(C=svm_C, gamma=svm_gamma)

    x_values = pd.read_json(StringIO(x_values_str))
    files = x_values[[filecolumn]].copy()

    x_values = x_values.drop(columns=filecolumn)
    y_values = pd.read_json(StringIO(y_labels_str))["label"].values
    clf.fit(x_values, y_values)

    qs = UncertaintySampling(
        method="least_confident",
        random_state=42,
        missing_label=-1,
    )
    query_idx = qs.query(x_values, y_values, clf)[0]
    file_id = files.loc[query_idx, filecolumn][5:]

    probabilities = clf.predict_proba(
        x_values.iloc[query_idx : query_idx + 1, :],
    )

    logger.debug(f"Probabilities for queried item: {probabilities}")

    # Locate the queried data point in PCA(3) space
    pca_loc = pd.read_json(StringIO(pca_data)).loc[query_idx, :]
    pcas = pca_loc.loc[["xcol", "ycol", "zcol"]]
    metadata_columns = json.loads(metadata_columns)
    pca_metadata = list(pca_loc.loc[metadata_columns])

    pca_dict = {}
    for col_index, axis in enumerate(["x", "y", "z"]):
        pca_dict.update({axis: pcas.values[col_index]})
    pca_dict.update(
        {
            "customdata": [
                file_id,
            ]
            + pca_metadata
            + list(probabilities[0]),
        },
    )

    logger.debug(f"{pca_dict}")

    clickdata = {"points": [pca_dict]}

    files[classcolumn] = clf.predict(x_values)
    files[classcolumn] = files[classcolumn].apply(
        lambda x: ["Regular", "Outlier"][x],
    )
    out_clf = pickle.dumps(clf).hex()
    return clickdata, out_clf, files.to_json()


@callback(Input("selected-data-point", "data"))
def show_click_data(clickData: dict):
    """Log properties of selected data point for debugging purposes.

    Args:
        clickData: data of selected data point
    """
    logger.debug(f"Updating selected data point to: {clickData}")


@callback(
    Output("selected-data-point", "data"),
    Input("trajectories-scatter", "clickData"),
    Input("queried-data-point", "data"),
)
def update_selection(clickData: dict, queryData: dict) -> dict:
    """Update selected data point to queried data point after model querying.

    This is necessary to show the image selected by the SVM querying.

    Args:
        clickData: a clicked data point
        queryData: data point selected by SVM querying

    Returns:
        data point dictionary
    """
    if "trajectories-scatter.clickData" in callback_context.triggered_prop_ids.keys():
        return clickData
    else:
        return queryData


@callback(
    Output("download-data", "data"),
    Input("btn-download-excel", "n_clicks"),
    Input("btn-download-csv", "n_clicks"),
    Input("x-values", "data"),
    Input("y-labeled", "data"),
    Input("y-predicted", "data"),
    prevent_initial_call=True,
)
def download_excel(
    _n_clicks_excel: int,
    _n_clicks_csv: int,
    x_values_str: str,
    y_labeled_str: str,
    y_predicted_str: str,
):
    """Download data and class predictions.

    Args:
        _n_clicks_excel: trigger to download as Excel file
        _n_clicks_csv: trigger to download as CSV file
        x_values_str: json string containing embedding dataframe
        y_labeled_str: json string containing human-assigned labels
        y_predicted_str: json string containing model predictions

    Returns:
        downloadable XLSX/CSV file
    """
    if callback_context.triggered_id not in ["btn-download-excel", "btn-download-csv"]:
        return no_update
    x_values = pd.read_json(StringIO(x_values_str))
    y_labeled = pd.read_json(StringIO(y_labeled_str))
    y_predicted = pd.read_json(StringIO(y_predicted_str))
    out_df = pd.merge(x_values, y_labeled, on=filecolumn)
    out_df = pd.merge(out_df, y_predicted, on=filecolumn)

    if callback_context.triggered_id == "btn-download-excel":
        return dcc.send_data_frame(out_df.to_excel, "predictions.xlsx")
    else:
        return dcc.send_data_frame(out_df.to_csv, "predictions.csv")


@callback(
    Output("download-model", "data"),
    Input("btn-download-model", "n_clicks"),
    Input("svc-model", "data"),
    prevent_initial_call=True,
)
def download_model(_n_clicks_button: int, svc_model: str):
    """Download the bytestring version of the SVC model.

    Args:
        _n_clicks_button: trigger for download
        svc_model: hex bytestring of SVC model

    Returns:
        model download
    """
    if callback_context.triggered_id != "btn-download-model":
        return no_update

    dt_stamp = datetime.now().strftime("%Y%m%d_%H%M")

    active_learning_classifier = pickle.loads(bytes.fromhex(svc_model))
    svm = active_learning_classifier.estimator

    return dcc.send_bytes(pickle.dumps(svm), filename=f"model_{dt_stamp}.pkl")
