import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, callback, Input, Output, State, dash_table, ctx
from dash_iconify import DashIconify
#import plotly.express as px
import pandas as pd
#import numpy as np
#from functools import reduce
#from app import df
from openpyxl import Workbook

dash.register_page(__name__, name=[DashIconify(icon="mdi:database-search", style={"marginRight": 8}), "Parcourir les données brutes"], order=5)

###################### Pré-traitement des données #########################
csv_icon = DashIconify(icon="fa6-solid:file-csv", style={"marginRight": 5})
excel_icon = DashIconify(icon="file-icons:microsoft-excel", style={"marginRight": 5})
database_icon = DashIconify(icon="mdi:database-search", style={"marginRight": 5})
reset_brutes_icon = DashIconify(icon="grommet-icons:power-reset", style={"marginRight": 5})

df = pd.read_csv("https://media.githubusercontent.com/media/Grenouil/FFN-web-app/main/Freq_amp_base_entiere_date.csv", dtype = {'id_analyse':int, 'nom_analyse':str, 'nom_prenom':str, 'nageur_sexe':str, 'competition_nom':str, 'mois_annee':str, 'date':str, 'distance_course':str, 'round':str, 'style_nage':str, 'temps_final':float, 'id_cycle':float, 'temps':float, 'distance':float, 'frequence_instantanee':float, 'amplitude_instantanee':float})
liste_columns = df.columns
df = df[~df['distance_course'].astype(str).str.contains('x')].reset_index(drop=True)
df.distance_course = df.distance_course.astype(int)
df = df.dropna(subset=['nom_prenom']).reset_index(drop=True)

mini_df = df.loc[df.temps_final>0,['id_analyse', 'temps_final']].reset_index(drop=True)
df = df.drop(columns=['temps_final'],axis=1)
df = df.merge(mini_df, on = 'id_analyse')
df = df[liste_columns]
df = df.rename(columns={'round': 'round_name'})
df = df.drop('mois_annee',axis=1)
df['temps_final'] = df['temps_final'].apply(lambda x: '{:02d}:{:05.2f}'.format(int(float(x) // 60), float(x) % 60))
df['distance'] = df['distance'].round(1)
df['frequence_instantanee'] = df['frequence_instantanee'].round(1)
df['amplitude_instantanee'] = df['amplitude_instantanee'].round(1)


def comparer_noms(nom):
    return nom.split()[-1]



###################### Définition des cards #########################

card_carac_swimmer = dbc.Card(
    dbc.CardBody(
        [
            html.H4([DashIconify(icon="fa-solid:swimmer", style={"marginRight": 10}), "Sélection du nageur"], className="text-nowrap"),
            html.Div("Choisissez le sexe et / ou le patronyme."),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(id='sexe-dropdown',
                    options=[{'label': k, 'value': k} for k in sorted(df.nageur_sexe.unique())],
                    multi=True,
                    placeholder='Sexe'),
                ], width=4),
                dbc.Col([
                    dcc.Dropdown(id='nom-prenom-dropdown',
                    options=[{'label': k, 'value': k} for k in pd.Series(sorted((df['nom_prenom']), key=comparer_noms)).unique()],
                    multi=True,
                    placeholder='Nom et prénom',
                    className="mb-3"),
                ], width=8)
            ]),
            html.Br()
        ], className="border-start border-dark border-5"
    ), style={"width": "23rem","background":'#fdd7d4'},
    className="text-center m-4 ml-3"
)

card_carac_compet = dbc.Card(
    dbc.CardBody(
        [
            html.H4([DashIconify(icon="ph:calendar-fill", style={"marginRight": 10}), "Sélection de la compétition"], className="text-nowrap"),
            html.Div("Choisissez la date et / ou le nom de la compétition."),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(id='date-dropdown',
                    options=[{'label': k, 'value': k} for k in sorted(df.date.unique())],
                    multi=True,
                    placeholder='Date'),
                ], width=4),
                dbc.Col([
                    dcc.Dropdown(id='nom-competition-dropdown',
                    options=[{'label': k, 'value': k} for k in sorted(df.competition_nom.unique())],
                    multi=True,
                    placeholder='Nom de la compétition',
                    className="mb-5"),
                ], width=8),
            ])
        ], className="border-start border-dark border-5"
    ), style={"width": "32rem","background":'#fbacb9',},
    className="text-center m-4 ml-3"
)

card_carac_event = dbc.Card(
    dbc.CardBody(
        [
            html.H4([DashIconify(icon="pajamas:timer", style={"marginRight": 10}), "Sélection de l'épreuve"], className="text-nowrap"),
            html.Div("Choisissez la distance, l'épreuve et / ou le style de nage."),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(id='distance-course-dropdown',
                    options=[{'label': k, 'value': k} for k in sorted(df.distance_course.unique())],
                    multi=True,
                    placeholder='Distance'),
                ], width=5),
                dbc.Col([
                    dcc.Dropdown(id='style-nage-dropdown',
                    options=[{'label': k, 'value': k} for k in sorted(df.style_nage.unique())],
                    multi=True,
                    placeholder='Style de nage'),
                ], width=7),
            ], justify='center'),

            html.Br(),

            dbc.Row([
                 dbc.Col([
                    dcc.Dropdown(id='round-name-dropdown',
                    options=[{'label': k, 'value': k} for k in sorted(df.round_name.unique())],
                    multi=True,
                    placeholder='Epreuve'),
                ], width=8),
            ], justify='center')
        ], className="border-start border-dark border-5"
    ), style={"width": "32rem","background":'#f767a1'},
    className="text-center m-4 ml-3"
)


####################### Layout ######################
layout = dbc.Container([
    dbc.Row([
        dbc.Col(
                html.H1([DashIconify(icon = "mdi:database-search", style={"marginRight": 30}),'Parcourir les données brutes']),
                width={"size": 'auto', "offset": 1}, style={"fontSize": 30, "textAlign": 'center'}
            ),
    ]),

    dbc.Row(
        [dbc.Col(card_carac_swimmer),dbc.Col(card_carac_compet)]
    ),

    dbc.Row(
        [dbc.Col(card_carac_event, width={"offset": 2}),
    ]),

    html.Br(),

    dbc.Row([
        dbc.Col([
            dbc.Button(
            [reset_brutes_icon, "Actualiser la base de données "], id="reset-brutes-button", className="me-2", n_clicks=0, style={'background-color': 'black'}
            ),
    ],  width={"size": 'auto', "offset": 4})
    ]),

    html.Br(),

    dcc.Store(id = 'df-stored-table'),

    dbc.Row(
        html.Div(dash_table.DataTable(
            columns=[],
            id='bdd-table',
            page_size=10,
            editable=True,
            style_cell={'textAlign': 'center'},
            style_header={
                'backgroundColor': '#f767a1',
                'color': 'white',
                'fontWeight': 'bold'
            },
            style_data={
                'width': '100px', 'minWidth': '100px', 'maxWidth': '100px',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
            }
        )),
    ),

    html.Br(),

    dbc.Row([
        dbc.Col([
            dbc.Button([csv_icon, "Télécharger la base de données sous format .csv"], id="btn_csv", style={'background-color':'#cd238f'}),
            dcc.Download(id="download-dataframe-csv"),
        ], width={"size": 'auto'}),
        dbc.Col([
            dbc.Button([excel_icon, "Télécharger la base de données sous format .xlsx"], id="btn_excel", style={'background-color':'#cd238f'}),
            dcc.Download(id="download-dataframe-xlsx"),
        ],  width={"size": 'auto', "offset": 0})
    ])

])


####################### Callbacks ######################
@callback(
    Output('nom-competition-dropdown', "options"),
    Input('nom-prenom-dropdown',"value"),
    Input('date-dropdown', "value"),
)
def update_nom_compet(nom_prenom, date):
    dff = df.copy()
    if nom_prenom:
        dff = dff.loc[dff.nom_prenom.isin(nom_prenom)]
    if date:
        dff = dff.loc[dff.date.isin(date)]
    return [{'label': i, 'value': i} for i in sorted(dff.competition_nom.unique())]


@callback(
    Output('nom-prenom-dropdown', "options"),
    Input('nom-competition-dropdown',"value"),
    Input('date-dropdown',"value"),
    Input('sexe-dropdown', "value"),
    Input('style-nage-dropdown', "value"),
    Input('distance-course-dropdown', "value"),
    Input('round-name-dropdown',"value")
)
def update_nom_prenom(nom_compet,date,sexe,style,distance,round_name):
    dff = df.copy()
    if nom_compet:
        dff = dff.loc[dff.competition_nom.isin(nom_compet)]
    if date:
        dff = dff.loc[dff.date.isin(date)]
    if sexe:
        dff = dff.loc[dff.nageur_sexe.isin(sexe)]
    if style:
        dff = dff.loc[dff.style_nage.isin(style)]
    if distance:
        dff = dff.loc[dff.distance_course.isin(distance)]
    if round_name:
        dff = dff.loc[dff.round_name.isin(round_name)]
    return [{'label': i, 'value': i} for i in pd.Series(sorted((dff['nom_prenom']), key=comparer_noms)).unique()]


@callback(
    Output('date-dropdown', "options"),
    Input('nom-prenom-dropdown',"value"),
    Input('nom-competition-dropdown', "value"),
)
def update_date(nom_prenom, nom_compet):
    dff = df.copy()
    if nom_prenom:
        dff = dff.loc[dff.nom_prenom.isin(nom_prenom)]
    if nom_compet:
        dff = dff.loc[dff.competition_nom.isin(nom_compet)]
    return [{'label': i, 'value': i} for i in sorted(dff.date.unique())]


@callback(
    Output('distance-course-dropdown', "options"),
    Input('nom-prenom-dropdown',"value"),
    Input('style-nage-dropdown', "value"),
    Input('round-name-dropdown', "value"),
)
def update_distance(nom_prenom,style,round):
    dff = df.copy()
    if nom_prenom:
        dff = dff.loc[dff.nom_prenom.isin(nom_prenom)]
    if style:
        dff = dff.loc[dff.style_nage.isin(style)]
    if round:
        dff = dff.loc[dff.round_name.isin(round)]
    return [{'label': i, 'value': i} for i in sorted(dff.distance_course.unique())]


@callback(
    Output('style-nage-dropdown', "options"),
    Input('nom-prenom-dropdown',"value"),
    Input('distance-course-dropdown', "value"),
    Input('round-name-dropdown', "value")
)
def update_style(nom_prenom, distance,round):
    dff = df.copy()
    if nom_prenom:
        dff = dff.loc[dff.nom_prenom.isin(nom_prenom)]
    if distance:
        dff = dff.loc[dff.distance_course.isin(distance)]
    if round:
        dff = dff.loc[dff.round_name.isin(round)]
    return [{'label': i, 'value': i} for i in sorted(dff.style_nage.unique())]

@callback(
    Output('round-name-dropdown', "options"),
    Input('nom-prenom-dropdown',"value"),
    Input('distance-course-dropdown',"value"),
    Input('style-nage-dropdown',"value")
)
def update_round(nom_prenom,distance,style):
    dff = df.copy()
    if nom_prenom:
        dff = dff.loc[dff.nom_prenom.isin(nom_prenom)]
    if distance:
        dff = dff.loc[dff.distance_course.isin(distance)]
    if style:
        dff = dff.loc[dff.style_nage.isin(style)]
    return [{'label': i, 'value': i} for i in sorted(dff.round_name.unique())]



@callback(
    Output('bdd-table', 'data'),
    Output('df-stored-table', "data"),
    [
        Input('nom-prenom-dropdown', 'value'),
        Input('nom-competition-dropdown', 'value'),
        Input('distance-course-dropdown', 'value'),
        Input('round-name-dropdown', 'value'),
        Input('style-nage-dropdown', 'value'),
        Input('sexe-dropdown', 'value'),
        Input('date-dropdown', 'value'),
        Input('reset-brutes-button', "n_clicks")
    ]
)
def display_table(nom_prenom_v, competition_nom_v, distance_course_v, epreuve_v, nage_v, sexe_v, date_v, reset_btn):
    dff = pd.DataFrame()
    dff_stored = pd.DataFrame()

    if "reset-brutes-button" in ctx.triggered[0]['prop_id']:
        dff = df.copy()
        if nom_prenom_v:
            dff = dff.loc[dff.nom_prenom.isin(nom_prenom_v)]

        if competition_nom_v:
            dff = dff.loc[dff.competition_nom.isin(competition_nom_v)]

        if distance_course_v:
            dff = dff.loc[dff.distance_course.isin(distance_course_v)]

        if epreuve_v:
            dff = dff.loc[dff.round_name.isin(epreuve_v)]

        if nage_v:
            dff = dff.loc[dff.style_nage.isin(nage_v)]

        if sexe_v:
            dff = dff.loc[dff.nageur_sexe.isin(sexe_v)]

        if date_v:
            dff = dff.loc[dff.date.isin(date_v)]


        dff = dff.drop(columns = 'competition_nom', axis=1)
        dff = dff.rename(columns={'id_analyse': 'ID', 'nom_analyse': 'ID complet (distance, nage, épreuve, compétition)',
                                'nom_prenom' : 'Nom & prénom du nageur', 'nageur_sexe': 'Sexe', 'distance_course': 'Distance',
                                'round_name': 'Epreuve', 'style_nage': 'Nage', 'temps_final': 'Temps final', 'id_cycle': 'ID cycle',
                                'frequence_instantanee': 'Fréquence instantanée', 'amplitude_instantanee': 'Amplitude instantanée'}
                        )

        if dff.shape[0] > 10000:
            dff = dff.iloc[:10000,:]

        dff = dff.sort_values(by='Temps final', ascending=True)

        dff_stored = dff.copy()
        dff_stored = dff_stored.to_dict('records')
        return dff_stored, dff.to_dict('records')

    return dff_stored.to_dict('records'), dff_stored.to_dict('records')



@callback(
    Output('bdd-table', 'columns'),
    [Input('df-stored-table', 'data')],
)

def update_columns(data):
    if data is not None:
        # Récupérez les colonnes du DataFrame
        df_columns = pd.DataFrame(data).columns
        # Créez une liste de colonnes au format attendu par dash_table.DataTable
        columns = [{'name': str(column), 'id': str(column)} for column in df_columns]
        return columns
    # Si aucune donnée n'est disponible, utilisez une liste vide pour les colonnes
    return []


@callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv","n_clicks"),
    Input("btn_excel","n_clicks"),
    Input('nom-prenom-dropdown', 'value'),
    Input('nom-competition-dropdown', 'value'),
    Input('distance-course-dropdown', 'value'),
    Input('round-name-dropdown', 'value'),
    Input('style-nage-dropdown', 'value'),
    Input('sexe-dropdown', 'value'),
    prevent_initial_call=True,
)
def func(btn_csv_clicks, btn_excel_clicks, nom_prenom_v, competition_nom_v, distance_course_v, epreuve_v, nage_v, sexe_v):
    dff = df.copy()
    if nom_prenom_v:
        dff = dff.loc[dff.nom_prenom.isin(nom_prenom_v)]

    if competition_nom_v:
        dff = dff.loc[dff.competition_nom.isin(competition_nom_v)]

    if distance_course_v:
        dff = dff.loc[dff.distance_course.isin(distance_course_v)]

    if epreuve_v:
        dff = dff.loc[dff.round_name.isin(epreuve_v)]

    if nage_v:
        dff = dff.loc[dff.style_nage.isin(nage_v)]

    if sexe_v:
        dff = dff.loc[dff.nageur_sexe.isin(sexe_v)]

    if "btn_csv" == ctx.triggered_id:
        return dcc.send_data_frame(dff.to_csv, "FFN_app_bdd.csv")

    if "btn_excel" == ctx.triggered_id:
        return dcc.send_data_frame(dff.to_excel, "FFN_app_bdd.xlsx", sheet_name="Feuille_1")

