import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


def get_dataset_options(list_):
    list_label_value = []
    for elem in list_:
        d = {"value": elem, "label": elem}
        list_label_value.append(d)
    return list_label_value


def get_correlation_type_radio_items(id):
    return dbc.FormGroup(
        [
            dbc.Label("Select correlation type :"),
            dcc.RadioItems(
                id=id,
                options=get_dataset_options(["Pearson", "Spearman"]),
                value="Pearson",
                labelStyle={"display": "inline-block", "margin": "5px"},
            ),
        ]
    )


def get_subset_method_radio_items(id):
    return dbc.FormGroup(
        [
            dbc.Label("Select subset method :"),
            dcc.RadioItems(
                id=id,
                options=get_dataset_options(["All", "Union", "Intersection"]),
                value="Union",
                labelStyle={"display": "inline-block", "margin": "5px"},
            ),
        ]
    )


def get_category_radio_items(id, categories):
    return dbc.FormGroup(
        [
            html.P("Select category: "),
            dcc.RadioItems(
                id=id,
                options=get_dataset_options(categories),
                value=categories[0],
                labelStyle={"display": "inline-block", "margin": "5px"},
            ),
            html.Br(),
        ]
    )


def get_dataset_drop_down(id):
    return dbc.FormGroup(
        [
            html.P("Select X Dataset: "),
            dcc.Dropdown(id=id, options=[{"value": "", "label": ""}], placeholder="Select a dataset..."),
            html.Br(),
        ]
    )


def get_organ_drop_down(id, organs, idx_organ=""):
    return dbc.FormGroup(
        [
            html.P(f"Select an Organ {idx_organ}: "),
            dcc.Dropdown(id=id, options=get_dataset_options(organs), value=organs[0]),
            html.Br(),
        ],
    )