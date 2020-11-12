import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from .tools import get_dataset_options, ETHNICITY_COLS, hierarchy_biomarkers, empty_graph
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from app import app, MODE
import glob
import os
import numpy as np
from scipy.stats import pearsonr
import dash_table
path_feat_imps = './' + app.get_asset_url('page18_MultivariateXWASFeatures/')
targets = sorted([ "*", "*instances01", "*instances1.5x", "*instances23", "Abdomen", "AbdomenLiver", "AbdomenPancreas", "Arterial", "ArterialPulseWaveAnalysis", "ArterialCarotids", "Biochemistry", "BiochemistryUrine", "BiochemistryBlood", "Brain", "BrainCognitive", "BrainMRI", "Eyes", "EyesAll" ,"EyesFundus", "EyesOCT", "Hearing", "HeartMRI", "Heart", "HeartECG", "ImmuneSystem", "Lungs", "Musculoskeletal", "MusculoskeletalSpine", "MusculoskeletalHips", "MusculoskeletalKnees", "MusculoskeletalFullBody", "MusculoskeletalScalars", "PhysicalActivity" ])
list_models = ['Correlation', 'ElasticNet', 'LightGBM', 'NeuralNetwork']
path_score = './' + app.get_asset_url('page7_MultivariateXWASResults/Scores/Scores_')

scores_nn = pd.read_csv(path_score + 'NeuralNetwork_test.csv')
scores_elastic = pd.read_csv(path_score + 'ElasticNet_test.csv')
scores_lightgbm = pd.read_csv(path_score + 'LightGbm_test.csv')

#list_organs = [os.path.basename(elem).replace('.csv', '').split('_')[2] for elem in glob.glob(path_feat_imps + '*.csv')]
#list_organs = sorted(list(set(list_organs)))

#if MODE != 'All':
#    list_organs = [elem for elem in list_organs if MODE in elem]



Environmental = sorted(['Alcohol', 'Diet', 'Education', 'ElectronicDevices',
                 'Employment', 'FamilyHistory', 'Eyesight', 'Mouth',
                 'GeneralHealth', 'Breathing', 'Claudification', 'GeneralPain',
                 'ChestPain', 'CancerScreening', 'Medication', 'Hearing',
                 'Household', 'MentalHealth', 'OtherSociodemographics',
                 'PhysicalActivity', 'SexualFactors', 'Sleep', 'SocialSupport',
                 'SunExposure', 'EarlyLifeFactors'])
Biomarkers = sorted(['HandGripStrength', 'BrainGreyMatterVolumes', 'BrainSubcorticalVolumes',
              'HeartSize', 'HeartPWA', 'ECGAtRest', 'AnthropometryImpedance',
              'UrineBiochemestry', 'BloodBiochemestry', 'BloodCount',
              'EyeAutorefraction', 'EyeAcuity', 'EyeIntraoculaPressure',
              'BraindMRIWeightedMeans', 'Spirometry', 'BloodPressure',
              'AnthropometryBodySize', 'ArterialStiffness', 'CarotidUltrasound',
              'BoneDensitometryOfHeel', 'HearingTest'])
Pathologies = sorted(['medical_diagnoses_%s' % letter for letter in ['A', 'B', 'C', 'D', 'E',
                                                    'F', 'G', 'H', 'I', 'J',
                                                    'K', 'L', 'M', 'N', 'O',
                                                    'P', 'Q', 'R', 'S', 'T',
                                                    'U', 'V', 'W', 'X', 'Y', 'Z']])
All = sorted(list(set(Environmental + Biomarkers + Pathologies)))

if MODE == 'All' :
    organ_select = dbc.FormGroup([
        html.P("Select X dataset : "),
        dcc.Dropdown(
            id='Select_organ_feat_imps_xwas_1',
            options = get_dataset_options(All)
            ),
        html.Br()
    ])
else:
    organ_select = dbc.FormGroup([
        html.P("Select X dataset : "),
        dcc.Dropdown(
            id='Select_organ_feat_imps_xwas_1',
            options = get_dataset_options([MODE]),
            value= MODE
            ),
        html.Br()
    ], style = {'display' : 'None'})

controls = dbc.Card([
    dbc.FormGroup([
        html.P("Select a target organ : "),
        dcc.Dropdown(
            id = 'Select_target_feat_imps',
            options = get_dataset_options(targets),
            value = 'Heart'
            ),
        html.Br()
    ]),
    organ_select
])




table_df = pd.DataFrame(data = {'Corr' : ['Correlation', 'ElasticNet', 'LightGBM', 'NeuralNetwork'],
                                'Correlation' : [1, 0, 0, 0],
                                'ElasticNet' : [0, 1, 0, 0],
                                'LightGBM': [0, 0, 1, 0],
                                'NeuralNetwork' : [0, 0, 0, 1]})

table = dbc.Card([
    dbc.FormGroup([
        html.P("Select correlation type"),
        dcc.RadioItems(
            id = 'select correlation type feat imps xwas',
            options = get_dataset_options(['Pearson', 'Spearman']),
            value = 'Pearson',
            labelStyle = {'display': 'inline-block', 'margin': '5px'}
        ),
        html.Br()
    ]),
    dbc.FormGroup([
        html.P("Correlation between feature importances/correlation : "),
        dash_table.DataTable(
            id = 'table_corr_xwas_feat_imps',
            columns =[{"name": i, "id": i} for i in table_df.columns],
            data = table_df.to_dict('records')
        ),
        html.Br()
    ])
])

layout =  html.Div([
    dcc.Store(id='memory_xwas_feat_imps'),
    dcc.Store(id = 'memory_no_str_xwas_feat_imps'),
    dcc.Loading([
        dbc.Container([
            html.H1('Multivariate XWAS - Features importances'),
            html.Br(),
            html.H2(id = 'scores_xwas'),
            html.Br(),
            dbc.Row([
                dbc.Col([controls,
                         html.Br(),
                         html.Br(),
                         table
                         ], md=3),
                dbc.Col([
                    html.H2('Feature Importances - Bar plot'),
                    dcc.Graph(
                         id='Plot Feature Imps XWAS',
                         )
                ],
                md=9,
                style={'overflowY': 'scroll', 'height' : 1000}),

                ],
                className="h-5"),
            html.Br(),
            html.Br(),
            html.H2('Feature Importances - Table'),
            html.Br(),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dash_table.DataTable(
                        id = 'table_feature_imps_xwas',
                        sort_action="native",
                        )
                     ],
                    style={'overflowY': 'scroll', 'height': 800},
                    width={"size": 10, "offset": 1})
                ], className="h-75")
            ],
            style={"height": "100vh"},
            fluid = True)
        ],
        id = 'Loading Data'
    )])



@app.callback([Output("memory_xwas_feat_imps", "data"), Output("memory_no_str_xwas_feat_imps", "data"), Output("table_feature_imps_xwas", 'columns'), Output("Plot Feature Imps XWAS", "figure"), Output("scores_xwas", "children")],
              [Input('Select_target_feat_imps', 'value'), Input('Select_organ_feat_imps_xwas_1', 'value')])
def _plot_r2_scores(value_target, value_organ):
    if None not in [value_organ, value_target] :

        list_models = []
        list_df = glob.glob(path_feat_imps + 'FeatureImp_%s_%s_*.csv' % (value_organ, value_target))
        if len(list_df) > 0 :
            for idx, elem in enumerate(list_df):

                df_new = pd.read_csv(elem, na_filter = False).set_index('features')
                _, _, _, model = os.path.basename(elem).split('_')
                model = model.replace('.csv', '').replace('LightGbm', 'LightGBM')
                list_models.append(model)
                df_new.columns = [model]
                if idx == 0:
                    df = df_new
                else :
                    df = df.join(df_new)
            df = np.abs(df)/np.abs(df).sum()
            score_lightgbm = scores_lightgbm[(scores_lightgbm.env_dataset == value_organ) & (scores_lightgbm.organ == value_target)].iloc[0]['r2']
            score_nn = scores_nn[(scores_nn.env_dataset == value_organ) & (scores_nn.organ == value_target)].iloc[0]['r2']
            score_elastic = scores_elastic[(scores_elastic.env_dataset == value_organ) & (scores_elastic.organ == value_target)].iloc[0]['r2']

            ## Sort by best model :
            if score_lightgbm > score_nn and score_lightgbm > score_elastic:
                df = df.sort_values('LightGBM')
            elif score_nn > score_lightgbm and score_nn > score_elastic:
                df = df.sort_values('NeuralNetwork')
            else :
                df = df.sort_values('ElasticNet')

            title = 'R-Squared : ElasticNet %.3f, LightGBM %.3f, NeuralNetwork %.3f' % (score_elastic, score_lightgbm, score_nn)

            features = df.index

            df_str = df.round(4).astype(str)
            df.index = df.index.str.replace('.0$', '', regex = True)
            df_str.index = df_str.index.str.replace('.0$', '', regex = True)


            ## Plot
            d = {'data' : [go.Bar(name = model, x = df[model], y = df.index, orientation='h') for model in sorted(df.columns)],
                 'layout' : dict(height = len(df.index) * 20,
                                 margin={'l': 40, 'b': 30, 't': 10, 'r': 0})}
            matrix = df[sorted(list_models)].corr()
            matrix.index.name = 'Corr'
            matrix = matrix.reset_index().round(3)

            table = dbc.Card([
                dbc.FormGroup([
                    html.P("Select correlation type"),
                    dcc.RadioItems(
                        id = 'select correlation type',
                        options = get_dataset_options(['pearson', 'spearman']),
                        value = 'pearson',
                        labelStyle = {'display': 'inline-block', 'margin': '5px'}
                    ),
                    html.Br()
                ]),
                dbc.FormGroup([
                    html.P("Correlation between feature importances/correlation : "),
                    dash_table.DataTable(
                        id = 'table_corr_xwas_feat_imps',
                        columns =[{"name": i, "id": i} for i in table_df.columns],
                        style_cell={'textAlign': 'left'},
                        data = matrix.to_dict('records')
                    ),
                    html.Br()
                ])
            ])


            return df_str.iloc[::-1].to_dict(), df.iloc[::-1].to_dict(), [{"name": i, "id": i} for i in ['Features'] + sorted(df.columns)], go.Figure(d), title
    else :
        return None, None, None, go.Figure(empty_graph), ""



@app.callback(Output('table_feature_imps_xwas', 'data'),
              [Input('table_feature_imps_xwas', 'sort_by'), Input('memory_xwas_feat_imps', 'data')])

def _sort_table(sort_by_col, data):
    df = pd.DataFrame(data = data)
    df = df[sorted(df.columns)]
    df.index.name = 'Features'
    df = df.reset_index()
    if sort_by_col is not None and len(sort_by_col):
        sorting = sort_by_col[0]
        ascending = (sorting['direction'] == 'asc')
        df = df.sort_values(sorting['column_id'], ascending = ascending)
    df = df.round(5)
    return df.to_dict('records')


@app.callback(Output('table_corr_xwas_feat_imps', 'data'),
              [Input('select correlation type feat imps xwas', 'value'), Input('memory_no_str_xwas_feat_imps', 'data')])
def _change_corr_method(value, data):
    print(data)
    df = pd.DataFrame(data = data)
    df = df[sorted(df.columns)]
    corr_matrix = df.corr(method=value.lower())
    corr_matrix.index.name = 'Corr'
    corr_matrix = corr_matrix.reset_index().round(3)
    return corr_matrix.to_dict('record')
