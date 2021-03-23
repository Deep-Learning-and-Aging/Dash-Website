import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from .tools import get_dataset_options, ETHNICITY_COLS, get_colorscale, load_csv
from pandas import Index
from plotly.graph_objs import Scattergl, Scatter, Histogram, Figure, Bar, Heatmap
from scipy.cluster import hierarchy
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import base64
from dash_website.app import app, MODE
import glob
import os
import numpy as np
from scipy.stats import pearsonr
import dash_table
import copy
from scipy.spatial.distance import squareform

order = [
    "Brain",
    "Eyes",
    "Hearing",
    "Lungs",
    "Arterial",
    "Heart",
    "Abdomen",
    "Musculoskeletal",
    "PhysicalActivity",
    "Biochemistry",
    "ImmuneSystem",
]
value_step = "Test"
# path_performance = './' + app.get_asset_url('page2_predictions/Performances/')
# path_residualscorr = './' + app.get_asset_url('page4_correlations/ResidualsCorrelations/')
# path_clustering = './' + app.get_asset_url('page4_correlations/HC_final.png')

path_performance = "page2_predictions/Performances/"
path_residualscorr = "page4_correlations/ResidualsCorrelations/"
path_clustering = "page4_correlations/HC_final.png"

if MODE == "All":
    controls = dbc.Card(
        [
            dbc.FormGroup(
                [
                    html.P("Select eid vs instances : "),
                    dcc.RadioItems(
                        id="select_eid_or_instances_res",
                        options=get_dataset_options(["*", "instances", "eids"]),
                        value="eids",
                        labelStyle={"display": "inline-block", "margin": "5px"},
                    ),
                    html.Br(),
                ]
            ),
            dbc.FormGroup(
                [
                    html.P("Select aggregate type : "),
                    dcc.RadioItems(
                        id="select_aggregate_type_res",
                        options=[
                            {"value": "bestmodels", "label": "Best models"},
                            {"value": "All", "label": "All models"},
                        ],
                        value="bestmodels",
                        labelStyle={"display": "inline-block", "margin": "5px"},
                    ),
                    html.Br(),
                ]
            ),
            dbc.FormGroup(
                [
                    html.P("Select an Organ : "),
                    dcc.Dropdown(
                        id="Select_organ_res",
                        options=get_dataset_options(order + ["All"]),
                        placeholder="All",
                        value="All",
                    ),
                    html.Br(),
                ],
                id="select_organ_res_full",
            ),
            # dbc.FormGroup([
            #     html.P("Select step : "),
            #     dcc.Dropdown(
            #         id='Select_step_res',
            #         options = get_dataset_options(['Test', 'Validation', 'Train']),
            #         value = 'Test'
            #         ),
            #     html.Br()
            # ]),
            dbc.FormGroup(
                [
                    html.P("Order by: "),
                    dcc.Dropdown(
                        id="Select_ordering",
                        options=get_dataset_options(["Score", "Custom", "Clustering"]),
                        value="Clustering",
                    ),
                    html.Br(),
                ],
                id="Select_ordering_full",
            ),
        ]
    )

    controls2 = dbc.Card(
        [
            dbc.FormGroup(
                [
                    html.P("Select eid vs instances : "),
                    dcc.RadioItems(
                        id="select_eid_or_instances_res_2",
                        options=get_dataset_options(["*", "instances", "eids"]),
                        value="*",
                        labelStyle={"display": "inline-block", "margin": "5px"},
                    ),
                    html.Br(),
                ]
            ),
            dbc.FormGroup(
                [
                    html.P("Select aggregate type : "),
                    dcc.RadioItems(
                        id="select_aggregate_type_res_2",
                        options=[
                            {"value": "bestmodels", "label": "Best models"},
                            {"value": "All", "label": "All models"},
                        ],
                        value="bestmodels",
                        labelStyle={"display": "inline-block", "margin": "5px"},
                    ),
                    html.Br(),
                ]
            ),
            dbc.FormGroup(
                [
                    html.P("Select an Organ : "),
                    dcc.Dropdown(
                        id="Select_organ_res_2",
                        options=get_dataset_options(order + ["All"]),
                        placeholder="All",
                        value="All",
                    ),
                    html.Br(),
                ],
                id="select_organ_res_full_2",
            ),
            # dbc.FormGroup([
            #     html.P("Select step : "),
            #     dcc.Dropdown(
            #         id='Select_step_res_2',
            #         options = get_dataset_options(['Test', 'Validation', 'Train']),
            #         value = 'Test'
            #         ),
            #     html.Br()
            # ])
        ]
    )
else:
    controls = dbc.Card(
        [
            dbc.FormGroup(
                [
                    html.P("Select eid vs instances : "),
                    dcc.RadioItems(
                        id="select_eid_or_instances_res",
                        options=get_dataset_options(["*", "instances", "eids"]),
                        value="*",
                        labelStyle={"display": "inline-block", "margin": "5px"},
                    ),
                    html.Br(),
                ]
            ),
            dbc.FormGroup(
                [
                    html.P("Select aggregate type : "),
                    dcc.RadioItems(
                        id="select_aggregate_type_res",
                        options=get_dataset_options(["All"]),
                        value="ALL",
                        labelStyle={"display": "inline-block", "margin": "5px"},
                    ),
                    html.Br(),
                ],
                style={"display": "none"},
            ),
            dbc.FormGroup(
                [
                    html.P("Select an Organ : "),
                    dcc.Dropdown(id="Select_organ_res", options=get_dataset_options([MODE]), value=MODE),
                    html.Br(),
                ],
                id="select_organ_res_full",
                style={"display": "none"},
            ),
            # dbc.FormGroup([
            #     html.P("Select step : "),
            #     dcc.Dropdown(
            #         id='Select_step_res',
            #         options = get_dataset_options(['Test', 'Validation', 'Train']),
            #         value = 'Test'
            #         ),
            #     html.Br()
            # ]),
            dbc.FormGroup(
                [
                    html.P("Order by: "),
                    dcc.Dropdown(
                        id="Select_ordering",
                        options=get_dataset_options(["Score", "Custom", "Clustering"]),
                        value="Score",
                    ),
                    html.Br(),
                ],
                id="Select_ordering_full",
            ),
        ]
    )

    controls2 = dbc.Card(
        [
            dbc.FormGroup(
                [
                    html.P("Select eid vs instances : "),
                    dcc.RadioItems(
                        id="select_eid_or_instances_res_2",
                        options=get_dataset_options(["*", "instances", "eids"]),
                        value="*",
                        labelStyle={"display": "inline-block", "margin": "5px"},
                    ),
                    html.Br(),
                ]
            ),
            dbc.FormGroup(
                [
                    html.P("Select aggregate type : "),
                    dcc.RadioItems(
                        id="select_aggregate_type_res_2",
                        options=get_dataset_options([MODE]),
                        value=MODE,
                        labelStyle={"display": "inline-block", "margin": "5px"},
                    ),
                    html.Br(),
                ],
                style={"display": "none"},
            ),
            dbc.FormGroup(
                [
                    html.P("Select an Organ : "),
                    dcc.Dropdown(id="Select_organ_res_2", options=get_dataset_options([MODE]), value=MODE),
                    html.Br(),
                ],
                id="select_organ_res_full_2",
                style={"display": "none"},
            ),
            # dbc.FormGroup([
            #     html.P("Select step : "),
            #     dcc.Dropdown(
            #         id='Select_step_res_2',
            #         options = get_dataset_options(['Test', 'Validation', 'Train']),
            #         value = 'Test'
            #         ),
            #     html.Br()
            # ])
        ]
    )


layout = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Correlations between accelerated aging - Heatmap", tab_id="tab_corr"),
                dbc.Tab(label="Correlations between accelerated aging - Clustering", tab_id="tab_HC"),
            ],
            id="tab_manager_corr",
            active_tab="tab_corr",
        ),
        html.Div(id="tab_content_corr"),
    ]
)


@app.callback(Output("tab_content_corr", "children"), [Input("tab_manager_corr", "active_tab")])
def _plot(ac_tab):
    if ac_tab == "tab_corr":
        return dbc.Container(
            [
                html.H1("Correlation between accelerated aging dimensions"),
                html.Br(),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col([controls, html.Br(), html.Br()], md=3),
                        dbc.Col(
                            [dcc.Loading([html.H2(id="title_corr_scores"), dcc.Graph(id="Plot Corr Heatmap")])],
                            style={"overflowX": "scroll", "width": 1000},
                            md=9,
                        ),
                    ]
                ),
            ],
            fluid=True,
        )
    elif ac_tab == "tab_HC":
        return dbc.Container(
            [
                html.H1("Correlations between accelerated aging dimensions"),
                html.Br(),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col([controls2, html.Br(), html.Br()], md=3),
                        dbc.Col(
                            [dcc.Loading([], id="loading_plot_hc")], style={"overflowX": "scroll", "width": 1000}, md=9
                        ),
                    ]
                ),
            ],
            fluid=True,
        )


def LoadData(value_eid_vs_instances, value_aggregate, value_organ, value_step):
    dict_value_step_value = dict(zip(["Validation", "Train", "Test"], ["val", "train", "test"]))
    if value_aggregate == "bestmodels":
        df = load_csv(
            path_residualscorr
            + "ResidualsCorrelations_bestmodels_%s_Age_%s.csv"
            % (value_eid_vs_instances, dict_value_step_value[value_step])
        )
        std = load_csv(
            path_residualscorr
            + "ResidualsCorrelations_bestmodels_sd_%s_Age_%s.csv"
            % (value_eid_vs_instances, dict_value_step_value[value_step])
        )
        if value_eid_vs_instances == "*":
            df_instances = load_csv(
                path_residualscorr
                + "ResidualsCorrelations_bestmodels_%s_Age_%s.csv" % ("*", dict_value_step_value[value_step])
            )
    else:
        df = load_csv(
            path_residualscorr
            + "ResidualsCorrelations_%s_Age_%s.csv" % (value_eid_vs_instances, dict_value_step_value[value_step])
        )
        std = load_csv(
            path_residualscorr
            + "ResidualsCorrelations_sd_%s_Age_%s.csv" % (value_eid_vs_instances, dict_value_step_value[value_step])
        )
        if value_eid_vs_instances == "*":
            df_instances = load_csv(
                path_residualscorr + "ResidualsCorrelations_%s_Age_%s.csv" % ("*", dict_value_step_value[value_step])
            )

    index_std = std.columns[0]
    index = df.columns[0]
    std = std.set_index(index_std)
    df = df.set_index(index)
    std.index.name = "Models"
    df.index.name = "Models"

    df.index = ["-".join(elem.split("_")[:4]) for elem in df.index.values]
    df.columns = ["-".join(elem.split("_")[:4]) for elem in df.index.values]

    std.index = ["-".join(elem.split("_")[:4]) for elem in std.index.values]
    std.columns = ["-".join(elem.split("_")[:4]) for elem in std.index.values]

    if value_eid_vs_instances != "*":
        if value_aggregate == "bestmodels":
            scores = load_csv(
                path_performance
                + "PERFORMANCES_bestmodels_alphabetical_%s_Age_%s.csv"
                % (value_eid_vs_instances, dict_value_step_value[value_step])
            )[["version", "R-Squared_all"]].set_index("version")
            scores_organs = [elem.split("_")[1] for elem in scores.index.values]
            scores_view = [
                (elem.split("_")[2]).replace("*", "").replace("HearingTest", "").replace("BloodCount", "")
                for elem in scores.index.values
            ]
            scores.index = [organ + view for organ, view in zip(scores_organs, scores_view)]

            intersect = scores.index.intersection(df.index)
            customdata_score = scores.loc[intersect]
            df = df.loc[intersect, intersect]
            std = std.loc[intersect, intersect]
        else:
            scores = load_csv(
                path_performance
                + "PERFORMANCES_withEnsembles_alphabetical_%s_Age_%s.csv"
                % (value_eid_vs_instances, dict_value_step_value[value_step])
            )[["version", "R-Squared_all"]].set_index("version")
            scores.index = ["-".join(elem.split("_")[1:5]) for elem in scores.index.values]
            customdata_score = scores.loc[df.index]

        customdata_score = customdata_score["R-Squared_all"]
        customdata_score_x = copy.deepcopy(df)
        customdata_score_y = copy.deepcopy(df)
        customdata_score_x.values[:] = np.tile(customdata_score, (len(customdata_score), 1))
        customdata_score_y.values[:] = customdata_score_x.T

    else:
        if value_aggregate == "bestmodels":
            scores_instances = load_csv(
                path_performance
                + "PERFORMANCES_bestmodels_alphabetical_instances_Age_%s.csv" % (dict_value_step_value[value_step])
            )[["version", "R-Squared_all"]].set_index("version")
            scores_eids = load_csv(
                path_performance
                + "PERFORMANCES_bestmodels_alphabetical_eids_Age_%s.csv" % (dict_value_step_value[value_step])
            )[["version", "R-Squared_all"]].set_index("version")
        else:
            scores_instances = load_csv(
                path_performance
                + "PERFORMANCES_withEnsembles_alphabetical_instances_Age_%s.csv" % (dict_value_step_value[value_step])
            )[["version", "R-Squared_all"]].set_index("version")
            scores_eids = load_csv(
                path_performance
                + "PERFORMANCES_withEnsembles_alphabetical_eids_Age_%s.csv" % (dict_value_step_value[value_step])
            )[["version", "R-Squared_all"]].set_index("version")

        index = df_instances.columns[0]
        df_instances = df_instances.set_index(index)
        df_instances.index.name = "Models"
        df_instances.index = ["-".join(elem.split("_")[:4]) for elem in df_instances.index.values]
        df_instances.columns = ["-".join(elem.split("_")[:4]) for elem in df_instances.index.values]
        if value_aggregate == "bestmodels":
            scores_instances_organs = [elem.split("_")[1] for elem in scores_instances.index.values]
            scores_instances_views = [
                (elem.split("_")[2]).replace("*", "").replace("HearingTest", "").replace("BloodCount", "")
                for elem in scores_instances.index.values
            ]
            scores_instances.index = [
                organ + view for organ, view in zip(scores_instances_organs, scores_instances_views)
            ]

            scores_eids_organs = [elem.split("_")[1] for elem in scores_eids.index.values]
            scores_eids_view = [
                elem.split("_")[2].replace("*", "").replace("HearingTest", "").replace("BloodCount", "")
                for elem in scores_eids.index.values
            ]
            scores_eids.index = [organ + view for organ, view in zip(scores_eids_organs, scores_eids_view)]

            intersect = scores_instances.index.intersection(df.index)
            customdata_score_eids = scores_eids.loc[intersect]
            customdata_score_instances = scores_instances.loc[intersect]

            df = df.loc[intersect, intersect]
            std = std.loc[intersect, intersect]
            df_instances = df_instances.loc[intersect, intersect]
        else:
            scores_instances.index = ["-".join(elem.split("_")[1:5]) for elem in scores_instances.index.values]
            scores_eids.index = ["-".join(elem.split("_")[1:5]) for elem in scores_eids.index.values]
            customdata_score_eids = scores_eids.loc[df.index.values]
            customdata_score_instances = scores_instances.loc[df.index.values]

        customdata_score_eids = customdata_score_eids["R-Squared_all"].values
        customdata_score_eids_x = np.tile(customdata_score_eids, (len(customdata_score_eids), 1))
        customdata_score_eids_y = customdata_score_eids_x.T

        customdata_score_instances = customdata_score_instances["R-Squared_all"].values
        customdata_score_instances_x = np.tile(customdata_score_instances, (len(customdata_score_instances), 1))
        customdata_score_instances_y = customdata_score_instances_x.T

        na_instances = df_instances.isna().values

        customdata_score_x = copy.deepcopy(df)
        customdata_score_y = copy.deepcopy(df)
        customdata_score_x.values[na_instances] = customdata_score_instances_x[na_instances]
        customdata_score_y.values[na_instances] = customdata_score_instances_y[na_instances]
        customdata_score_x.values[np.invert(na_instances)] = customdata_score_eids_x[np.invert(na_instances)]
        customdata_score_y.values[np.invert(na_instances)] = customdata_score_eids_y[np.invert(na_instances)]

    custom_order = []
    for organ_ in order:
        custom_order = custom_order + list(df.index[df.index.str.contains(organ_)])
    difference = df.index.difference(Index(custom_order))
    custom_order = list(difference) + custom_order

    return customdata_score_x, customdata_score_y, df, std, custom_order


## Hide if value_aggreate not All :
@app.callback(Output("select_organ_res_full", "style"), [Input("select_aggregate_type_res", "value")])
def _hide_organ_dropdown(value_aggregate):
    if value_aggregate is not None and value_aggregate != "All":
        return {"display": "none"}
    else:
        return {}


@app.callback(Output("select_organ_res_full_2", "style"), [Input("select_aggregate_type_res_2", "value")])
def _hide_organ_dropdown(value_aggregate):
    if value_aggregate is not None and value_aggregate != "All":
        return {"display": "none"}
    else:
        return {}


@app.callback(Output("Select_ordering", "value"), [Input("select_aggregate_type_res", "value")])
def _hide_organ_dropdown(value_aggregate):
    if value_aggregate == "All":
        return "Custom"
    elif value_aggregate == "bestmodels":
        return "Clustering"


@app.callback(
    Output("loading_plot_hc", "children"),
    [
        Input("select_eid_or_instances_res_2", "value"),
        Input("select_aggregate_type_res_2", "value"),
        Input("Select_organ_res_2", "value"),
        # Input('Select_step_res_2', 'value')
    ],
)
def _plot_r2_scores(value_eid_vs_instances, value_aggregate, value_organ):
    if value_aggregate is not None and value_organ is not None and value_step is not None:
        ## Load Data :
        customdata_score_x, customdata_score_y, df, std, custom_order = LoadData(
            value_eid_vs_instances, value_aggregate, value_organ, value_step
        )

        if value_organ != "All":
            mask = df.columns.str.contains(value_organ)
            df = df[df.columns[mask]]
            df = df.loc[mask]

        n_cols = len(df.columns)
        df = df.fillna(0)
        df[df > 1] = 1
        d2 = ff.create_dendrogram(df, labels=df.index, distfun=lambda x: squareform(1 - x))
        d2.update_layout(width=np.max([1000, n_cols * 15]), margin=dict(b=250), height=500)
        return dcc.Graph(id="plot HC", figure=d2)


@app.callback(
    [Output("Plot Corr Heatmap", "figure"), Output("title_corr_scores", "children")],
    [
        Input("select_eid_or_instances_res", "value"),
        Input("select_aggregate_type_res", "value"),
        Input("Select_organ_res", "value"),
        # Input('Select_step_res', 'value'),
        Input("Select_ordering", "value"),
    ],
)
def _plot_r2_scores(value_eid_vs_instances, value_aggregate, value_organ, value_ordering):
    if value_aggregate is not None and value_organ is not None and value_step is not None:
        ## Load Data :
        customdata_score_x, customdata_score_y, df, std, custom_order = LoadData(
            value_eid_vs_instances, value_aggregate, value_organ, value_step
        )
        organ_sorted_by_score = customdata_score_x.iloc[0].sort_values(ascending=True).index
        d = {}
        d["layout"] = dict(
            height=1000,
            width=1000,
            margin={"l": 0, "b": 0, "t": 0, "r": 0},
            xaxis=dict(titlefont=dict(size=8)),
            yaxis=dict(titlefont=dict(size=8)),
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(size=8),
        )

        if value_organ == "All":
            # Color Scale
            colorscale = get_colorscale(df)
            df_miror = 1 * df.isna()
            df_miror = df_miror.replace(0, np.nan).values
            np.fill_diagonal(df_miror, 1)
            cols = df.columns
            df_den = df.fillna(0).copy()
            df_den[df_den > 1] = 1
            d2 = ff.create_dendrogram(df_den, labels=df.index, distfun=lambda x: squareform(1 - x))
            dendro_leaves = d2["layout"]["xaxis"]["ticktext"]
            n_cols = len(cols)

            dict_value_ordering_to_index = {
                "Score": (organ_sorted_by_score, organ_sorted_by_score),
                "Clustering": (dendro_leaves, dendro_leaves),
                "Custom": (custom_order, custom_order),
            }
            df = df.loc[dict_value_ordering_to_index[value_ordering]]
            std = std.loc[dict_value_ordering_to_index[value_ordering]]
            customdata_score_x = customdata_score_x.loc[dict_value_ordering_to_index[value_ordering]]
            customdata_score_y = customdata_score_y.loc[dict_value_ordering_to_index[value_ordering]]

            if value_aggregate == "All":
                ## Remove ticks labels :
                d["layout"]["yaxis"] = dict(showticklabels=False)
                d["layout"]["xaxis"] = dict(showticklabels=False)

                distincts_organs = list(set([elem.split("-")[0] for elem in df.index.values]))
                distincts_views = list(set([elem.split("-")[1] for elem in df.index.values]))
                list_elem_0 = np.char.array([elem.split("-") for elem in df.index])[:, 0]
                list_elem_1 = np.char.array([elem.split("-") for elem in df.index])[:, 1]
                list_elem_2 = np.char.array([elem.split("-") for elem in df.index])[:, 2]
                list_elem_3 = np.char.array([elem.split("-") for elem in df.index])[:, 3]

                x, y = df.index, df.index

                ## Custom data & hovertemplate
                # 4 different values
                customdata_x = np.tile(list_elem_0, (len(list_elem_0), 1))
                customdata_y = customdata_x.T
                customdata_1_x = np.tile(list_elem_1, (len(list_elem_1), 1))
                customdata_1_y = customdata_1_x.T
                customdata_2_x = np.tile(list_elem_2, (len(list_elem_2), 1))
                customdata_2_y = customdata_2_x.T
                custom_data_3_x = np.tile(list_elem_3, (len(list_elem_3), 1))
                custom_data_3_y = custom_data_3_x.T
                # Std
                custom_data_std = std.values
                # Score
                customdata = np.dstack(
                    (
                        customdata_x,
                        customdata_y,
                        customdata_1_x,
                        customdata_1_y,
                        customdata_2_x,
                        customdata_2_y,
                        custom_data_3_x,
                        custom_data_3_y,
                        custom_data_std,
                        customdata_score_x,
                        customdata_score_y,
                    )
                )
                hovertemplate = "Organ_x : %{customdata[0]}\
                                 <br>View x: %{customdata[2]}\
                                 <br>Transformation x : %{customdata[4]}\
                                 <br>Architecture x : %{customdata[6]}\
                                 <br>Score x : %{customdata[9]:.3f}\
                                 <br>\
                                 <br>Organ_y : %{customdata[1]}\
                                 <br>View y : %{customdata[3]}\
                                 <br>Transformation y : %{customdata[5]}\
                                 <br>Architecture y : %{customdata[7]}\
                                 <br>Score y : %{customdata[10]:.3f}\
                                 <br>\
                                 <br>Correlation : %{z:.3f} ± %{customdata[8]:.3f}"

                shapes = []
                annotations = []
                line = dict(color="Black", width=0.5)
                for organ in distincts_organs:
                    x0 = -40
                    x1 = -80
                    where_organ = np.where(x.str.startswith(organ))[0]
                    min_organ = where_organ.min()
                    max_organ = where_organ.max()

                    shapes.append(
                        dict(
                            type="line",
                            xref="x",
                            yref="y",
                            x0=x0,
                            y0=min_organ - 0.5,
                            x1=x1,
                            y1=min_organ - 0.5,
                            line=line,
                        )
                    )
                    shapes.append(
                        dict(
                            type="line",
                            xref="x",
                            yref="y",
                            x0=min_organ - 0.5,
                            y0=x0,
                            x1=min_organ - 0.5,
                            y1=x1,
                            line=line,
                        )
                    )
                    annotations.append(
                        dict(
                            text=organ,
                            xref="x",
                            yref="y",
                            x=(x0 + x1) / 2,
                            y=(max_organ + min_organ) / 2,
                            showarrow=False,
                            font=dict(size=7),
                        )
                    )
                    if organ in [",", "*", "?"]:
                        textangle = 0
                    else:
                        textangle = -90
                    annotations.append(
                        dict(
                            text=organ,
                            xref="x",
                            yref="y",
                            x=(max_organ + min_organ) / 2,
                            y=(x0 + x1) / 2,
                            showarrow=False,
                            textangle=textangle,
                            font=dict(size=7),
                        )
                    )

                    distincts_views = x[x.str.startswith(organ)]
                    distincts_views = [elem.split("-")[1] for elem in distincts_views]
                    distincts_views = list(set(distincts_views))
                    x0 = -40
                    x1 = -0
                    for view in distincts_views:
                        where_organ_view = np.where(x.str.contains(organ + "-" + view, regex=False))[0]
                        min_view = where_organ_view.min()
                        max_view = where_organ_view.max()
                        ## Add bottom bar
                        shapes.append(
                            dict(
                                type="line",
                                xref="x",
                                yref="y",
                                x0=x0,
                                y0=min_view - 0.5,
                                x1=x1,
                                y1=min_view - 0.5,
                                line=line,
                            )
                        )
                        shapes.append(
                            dict(
                                type="line",
                                xref="x",
                                yref="y",
                                x0=min_view - 0.5,
                                y0=x0,
                                x1=min_view - 0.5,
                                y1=x1,
                                line=line,
                            )
                        )
                        ## Add annotation :
                        annotations.append(
                            dict(
                                text=view,
                                xref="x",
                                yref="y",
                                x=(x0 + x1) / 2,
                                y=(max_view + min_view) / 2,
                                showarrow=False,
                                font=dict(size=7),
                            )
                        )
                        if view in [",", "*", "?"]:
                            textangle = 0
                        else:
                            textangle = -90
                        annotations.append(
                            dict(
                                text=view,
                                xref="x",
                                yref="y",
                                x=(max_view + min_view) / 2,
                                y=(x0 + x1) / 2,
                                showarrow=False,
                                textangle=textangle,
                                font=dict(size=7),
                            )
                        )
                ## Add final Bar
                shapes.append(dict(type="line", xref="x", yref="y", x0=-0.5, y0=len(x), x1=-40.5, y1=len(x), line=line))
                shapes.append(dict(type="line", xref="x", yref="y", x0=len(x), y0=-0.5, x1=len(x), y1=-40.5, line=line))
                colorbar = dict(len=1000 - 250, lenmode="pixels", y=0.58)
                if value_ordering not in ["Score", "Clustering"]:
                    d["layout"]["shapes"] = shapes
                    d["layout"]["annotations"] = annotations
                df = df.values
                np.fill_diagonal(df, np.nan)
            else:
                x = df.index
                y = df.index

                hovertemplate = "Organ_x : %{x}\
                                 <br>Score x : %{customdata[1]:.3f}\
                                 <br>\
                                 <br>Organ_y : %{y}\
                                 <br>Score y : %{customdata[2]:.3f}\
                                 <br>\
                                 <br>Correlation : %{z:.3f} ± %{customdata[0]:.3f}"

                customdata = np.dstack([std.values, customdata_score_x, customdata_score_y])
                df = df.values
                np.fill_diagonal(df, np.nan)

            d["data"] = [
                ## Actual plot
                Heatmap(
                    z=df,
                    x=x,
                    y=y,
                    zsmooth=False,
                    hoverongaps=False,
                    colorscale=colorscale,
                    customdata=customdata,
                    hovertemplate=hovertemplate,
                ),
                ## Miror to fill na
                Heatmap(
                    z=df_miror,
                    x=x,
                    y=y,
                    showlegend=False,
                    showscale=False,
                    hoverinfo="skip",
                    colorscale=[[0, "rgba(128,128,128, 0.7)"], [1, "rgba(128,128,128, 0.7)"]],
                ),
            ]
            title = "Average correlation = %.3f ± %.3f" % (np.nanmean(df), np.nanstd(df))
            # pdist = hierarchy.distance.pdist(df)

        else:
            mask = df.columns.str.contains(value_organ)
            customdata_score_x = customdata_score_x.iloc[mask, mask]
            customdata_score_y = customdata_score_y.iloc[mask, mask]
            organ_ordered_by_score = customdata_score_x.index
            df = df[df.columns[df.columns.str.contains(value_organ)]]
            df = df.loc[df.index.str.contains(value_organ)]
            std = std[std.columns[std.columns.str.contains(value_organ)]]
            std = std.loc[std.index.str.contains(value_organ)]

            organ_sorted_by_score = customdata_score_x.iloc[0].sort_values(ascending=True).index
            df_den = df.fillna(0).copy()
            df_den[df_den > 1] = 1
            d2 = ff.create_dendrogram(df_den, labels=df.index, distfun=lambda x: squareform(1 - x))
            dendro_leaves = d2["layout"]["xaxis"]["ticktext"]

            if value_ordering == "Score":
                df = df.loc[organ_sorted_by_score, organ_sorted_by_score]
                std = std.loc[organ_sorted_by_score, organ_sorted_by_score]
                customdata_score_x = customdata_score_x.loc[organ_sorted_by_score, organ_sorted_by_score]
                customdata_score_y = customdata_score_y.loc[organ_sorted_by_score, organ_sorted_by_score]
            elif value_ordering == "Clustering":
                df = df.loc[dendro_leaves, dendro_leaves]
                customdata_score_x = customdata_score_x.loc[dendro_leaves, dendro_leaves]
                customdata_score_y = customdata_score_y.loc[dendro_leaves, dendro_leaves]
                std = std.loc[dendro_leaves, dendro_leaves]

            if value_aggregate == "All" and value_ordering != "Clustering" and value_ordering != "Score":
                list_elem_0 = np.char.array([elem.split("-") for elem in df.index])[:, 1]
                list_elem_1 = (
                    np.char.array([elem.split("-") for elem in df.index])[:, 2]
                    + "_"
                    + np.char.array([elem.split("-") for elem in df.index])[:, 3]
                )
                x = [list_elem_0, list_elem_1]
                y = [list_elem_0, list_elem_1]
            else:
                x = df.index
                y = df.index

            list_elem_1 = np.char.array([elem.split("-") for elem in df.index])[:, 1]
            list_elem_2 = np.char.array([elem.split("-") for elem in df.index])[:, 2]
            list_elem_3 = np.char.array([elem.split("-") for elem in df.index])[:, 3]

            ## 3 Values
            customdata_1_x = np.tile(list_elem_1, (len(list_elem_1), 1))
            customdata_1_y = customdata_1_x.T
            customdata_2_x = np.tile(list_elem_2, (len(list_elem_2), 1))
            customdata_2_y = customdata_2_x.T
            custom_data_3_x = np.tile(list_elem_3, (len(list_elem_3), 1))
            custom_data_3_y = custom_data_3_x.T
            # Std
            custom_data_std = std.values
            # Score
            customdata = np.dstack(
                (
                    customdata_1_x,
                    customdata_1_y,
                    customdata_2_x,
                    customdata_2_y,
                    custom_data_3_x,
                    custom_data_3_y,
                    custom_data_std,
                    customdata_score_x,
                    customdata_score_y,
                )
            )
            hovertemplate = "View x: %{customdata[0]}\
                             <br>Transformation x : %{customdata[2]}\
                             <br>Architecture x : %{customdata[4]}\
                             <br>Score x : %{customdata[7]:.3f}\
                             <br>\
                             <br>View y : %{customdata[1]}\
                             <br>Transformation y : %{customdata[3]}\
                             <br>Architecture y : %{customdata[5]}\
                             <br>Score x : %{customdata[8]:.3f}\
                             <br>\
                             <br>Correlation : %{z:.3f} ± %{customdata[6]:.3f}"
            colorscale = get_colorscale(df)

            df_miror = 1 * df.isna()
            df_miror = df_miror.replace(0, np.nan).values
            np.fill_diagonal(df_miror, 1)
            cols = df.columns
            df_den = df.fillna(0).copy()
            df_den[df_den > 1] = 1
            d2 = ff.create_dendrogram(df_den, labels=df.index, distfun=lambda x: squareform(1 - x))
            df = df.values

            np.fill_diagonal(df, np.nan)

            d["data"] = [
                Heatmap(z=df, x=x, y=y, colorscale=colorscale, customdata=customdata, hovertemplate=hovertemplate),
                Heatmap(
                    z=df_miror,
                    x=x,
                    y=y,
                    showlegend=False,
                    showscale=False,
                    hoverinfo="skip",
                    colorscale=[[0, "rgba(128,128,128, 0.7)"], [1, "rgba(128,128,128, 0.7)"]],
                ),
            ]
            title = "Average correlation = %.3f ± %.3f" % (np.nanmean(df), np.nanstd(df))
            d["layout"]["width"] = 900
            d["layout"]["height"] = 800

            n_cols = len(cols)

        if value_ordering == "Clustering":
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02)
            for elem in d["data"]:
                fig.add_trace(elem, row=2, col=1)
            for elem in d2["data"]:
                elem["showlegend"] = False
                fig.add_trace(elem, row=1, col=1)

            fig["layout"]["xaxis"]["range"] = [0, 100]
            fig["layout"]["xaxis"]["showgrid"] = False
            fig["layout"]["yaxis"]["domain"] = [0.7, 1.0]
            fig["layout"]["yaxis"]["showticklabels"] = False
            fig["layout"]["yaxis"]["showgrid"] = False
            fig["layout"]["yaxis2"]["domain"] = [0, 0.7]
            fig["layout"]["yaxis2"]["showgrid"] = False
            fig["layout"]["width"] = 1100
            fig["layout"]["height"] = 1100
            fig["layout"]["xaxis"]["autorange"] = True
            if value_aggregate == "All":
                fig["layout"]["xaxis2"]["showticklabels"] = False
                fig["layout"]["yaxis2"]["showticklabels"] = False
        else:
            fig = Figure(d)
        print(title)
        return fig, title
    else:
        return Figure(), ""