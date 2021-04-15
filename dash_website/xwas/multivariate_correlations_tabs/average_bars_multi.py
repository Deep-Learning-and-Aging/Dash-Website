from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import pandas as pd

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import (
    get_main_category_radio_items,
    get_dimension_drop_down,
    get_item_radio_items,
    get_correlation_type_radio_items,
    get_options,
)
from dash_website import DIMENSIONS, MAIN_CATEGORIES_TO_CATEGORIES, ALGORITHMS_RENDERING


def get_average_bars():
    return dbc.Container(
        [
            dcc.Loading(
                [dcc.Store(id="memory_average_multi", data=get_data_multi()), dcc.Store(id="memory_correlations_multi")]
            ),
            html.H1("Multivariate XWAS - Correlations between accelerated aging"),
            html.Br(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            get_controls_tab_average_multi(),
                            html.Br(),
                            html.Br(),
                        ],
                        md=3,
                    ),
                    dbc.Col(
                        [
                            dcc.Loading(
                                [
                                    html.H2(id="title_average_multi"),
                                    dcc.Graph(id="graph_average_multi"),
                                ]
                            )
                        ],
                        style={"overflowY": "scroll", "height": 1000, "overflowX": "scroll", "width": 0},
                        md=9,
                    ),
                ]
            ),
        ],
        fluid=True,
    )


def get_data_multi():
    return load_feather(f"xwas/multivariate_correlations/averages_correlations.feather").to_dict()


@APP.callback(
    Output("memory_correlations_multi", "data"),
    [Input("dimension_1_average_multi", "value"), Input("dimension_2_average_multi", "value")],
)
def _modify_store_correlations(dimension_1, dimension_2):
    if dimension_2 == "average":
        raise PreventUpdate
    else:
        return load_feather(
            f"xwas/multivariate_correlations/correlations/dimensions/correlations_{dimension_1}.feather"
        ).to_dict()


def get_controls_tab_average_multi():
    return dbc.Card(
        [
            get_main_category_radio_items("main_category_average_multi", list(MAIN_CATEGORIES_TO_CATEGORIES.keys())),
            get_dimension_drop_down(
                "dimension_1_average_multi", ["MainDimensions", "SubDimensions"] + DIMENSIONS, idx_dimension=1
            ),
            html.Div(
                [get_dimension_drop_down("dimension_2_average_multi", ["average"] + DIMENSIONS, idx_dimension=2)],
                id="hiden_dimension_2_average_multi",
                style={"display": "none"},
            ),
            get_item_radio_items(
                "display_mode_average_multi",
                {"view_all": "Decreasing correlation", "view_per_main_category": "X main category"},
                "Rank by : ",
            ),
            get_item_radio_items(
                "algorithm_average",
                {
                    "elastic_net": ALGORITHMS_RENDERING["elastic_net"],
                    "light_gbm": ALGORITHMS_RENDERING["light_gbm"],
                    "neural_network": ALGORITHMS_RENDERING["neural_network"],
                },
                "Select an Algorithm :",
            ),
            get_correlation_type_radio_items("correlation_type_average_multi"),
        ]
    )


@APP.callback(
    [
        Output("hiden_dimension_2_average_multi", component_property="style"),
        Output("dimension_2_average_multi", "options"),
        Output("dimension_2_average_multi", "value"),
    ],
    Input("dimension_1_average_multi", "value"),
)
def _change_controls_average(dimension_1):
    if dimension_1 in ["MainDimensions", "SubDimensions"]:
        return {"display": "none"}, get_options(["average"]), "average"
    else:
        return (
            {"display": "block"},
            get_options(["average"] + pd.Index(DIMENSIONS).drop(dimension_1).tolist()),
            "average",
        )


@APP.callback(
    [Output("graph_average_multi", "figure"), Output("title_average_multi", "children")],
    [
        Input("algorithm_average", "value"),
        Input("correlation_type_average_multi", "value"),
        Input("main_category_average_multi", "value"),
        Input("dimension_1_average_multi", "value"),
        Input("dimension_2_average_multi", "value"),
        Input("display_mode_average_multi", "value"),
        Input("memory_correlations_multi", "data"),
        Input("memory_average_multi", "data"),
    ],
)
def _fill_graph_tab_average(
    algorithm,
    correlation_type,
    main_category,
    dimension_1,
    dimension_2,
    display_mode,
    data_correlations,
    data_averages,
):
    import plotly.graph_objs as go

    if dimension_2 == "average":
        averages = pd.DataFrame(data_averages).set_index(["dimension", "category"])
        averages.columns = pd.MultiIndex.from_tuples(
            list(map(eval, averages.columns.tolist())), names=["algorithm", "correlation_type", "observation"]
        )

        sorted_averages = averages.loc[
            (dimension_1, MAIN_CATEGORIES_TO_CATEGORIES[main_category] + [f"All_{main_category}"]),
            (algorithm, correlation_type),
        ].sort_values(by=["mean"], ascending=False)

        if sorted_averages.shape[0] == 0:
            return go.Figure(), "The data for this X main category is not provided :("

        if display_mode == "view_all":
            bars = go.Bar(
                x=sorted_averages.index.get_level_values("category"),
                y=sorted_averages["mean"],
                error_y={"array": sorted_averages["std"], "type": "data"},
                name="Average correlations",
                marker_color="indianred",
            )
        else:  # display_mode == view_per_main_category then main_category = All
            list_main_category = []
            list_categories = []
            # Get the ranking of subcategories per main category
            for main_category_group in MAIN_CATEGORIES_TO_CATEGORIES.keys():
                if main_category_group == "All":
                    continue
                sorted_categories = (
                    sorted_averages.swaplevel()
                    .loc[
                        sorted_averages.index.get_level_values("category").isin(
                            MAIN_CATEGORIES_TO_CATEGORIES[main_category_group]
                        )
                    ]
                    .sort_values(by=["mean"], ascending=False)
                )
                sorted_index_categories = sorted_categories.index.get_level_values("category")

                list_categories.extend(sorted_index_categories)
                list_main_category.extend([main_category_group] * len(sorted_index_categories))

            bars = go.Bar(
                x=[list_main_category + [""], list_categories + ["FamilyHistory"]],
                y=sorted_averages["mean"].swaplevel()[list_categories + ["FamilyHistory"]],
                error_y={
                    "array": sorted_averages["std"].swaplevel()[list_categories + ["FamilyHistory"]],
                    "type": "data",
                },
                name="Correlations",
                marker_color="indianred",
            )

        title = f"Average average correlation across aging dimensions and X categories = {sorted_averages['mean'].mean().round(3)} +- {sorted_averages['mean'].std().round(3)}"
        y_label = "Average correlation"
    else:
        correlations_raw = pd.DataFrame(data_correlations).set_index(["dimension", "category"])
        correlations_raw.columns = pd.MultiIndex.from_tuples(
            list(map(eval, correlations_raw.columns.tolist())), names=["algorithm", "correlation_type"]
        )

        sorted_correlations = correlations_raw.loc[
            (dimension_2, MAIN_CATEGORIES_TO_CATEGORIES[main_category] + [f"All_{main_category}"]),
            (algorithm, correlation_type),
        ].sort_values(ascending=False)

        if sorted_correlations.shape[0] == 0:
            return go.Figure(), "The data for this X main category is not provided :("

        if display_mode == "view_all":
            bars = go.Bar(
                x=sorted_correlations.index.get_level_values("category"),
                y=sorted_correlations,
                name="Correlations",
                marker_color="indianred",
            )
        else:  # display_mode == view_per_main_category then main_category = All
            list_main_category = []
            list_categories = []
            # Get the ranking of subcategories per main category
            for main_category_group in MAIN_CATEGORIES_TO_CATEGORIES.keys():
                if main_category_group == "All":
                    continue
                sorted_categories = (
                    sorted_correlations.swaplevel()
                    .loc[
                        sorted_correlations.index.get_level_values("category").isin(
                            MAIN_CATEGORIES_TO_CATEGORIES[main_category_group]
                        )
                    ]
                    .sort_values(ascending=False)
                )
                sorted_index_categories = sorted_categories.index.get_level_values("category")

                list_categories.extend(sorted_index_categories)
                list_main_category.extend([main_category_group] * len(sorted_index_categories))

            bars = go.Bar(
                x=[list_main_category + [""], list_categories + ["FamilyHistory"]],
                y=sorted_correlations.swaplevel()[list_categories + ["FamilyHistory"]],
                name="Correlations",
                marker_color="indianred",
            )

        title = f"Average correlation on feature importances = {sorted_correlations.mean().round(3)} +- {sorted_correlations.std().round(3)}"
        y_label = "Correlation"

    fig = go.Figure(bars)

    fig.update_layout(
        {
            "width": 2000,
            "height": 800,
            "xaxis": {"title": "X subcategory", "tickangle": 90, "showgrid": False},
            "yaxis": {"title": y_label},
        }
    )

    return fig, title