import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, callback, Input, Output, State, dash_table, ctx
from dash_iconify import DashIconify
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel

dash.register_page(__name__, name=[DashIconify(icon="wpf:statistics", style={"marginRight": 8}), "Modélisation des profils de course"], order=4)

###################### Pré-traitement des données #########################
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

reset_icon = DashIconify(icon="grommet-icons:power-reset", style={"marginRight": 5})

def comparer_noms(nom):
    return nom.split()[-1]

def clean_data(data,value_freq_min=35):
    new_data = data.copy()
    # Suppression des lignes avec des valeurs manquantes dans une ou plusieurs colonnes
    new_data.dropna(subset=['frequence_instantanee', 'amplitude_instantanee'], inplace=True)
    new_data = new_data.drop(['id_analyse','nom_prenom','nageur_sexe','competition_nom','date', 'distance_course','round_name','style_nage','id_cycle'],axis=1)
    new_data =new_data[new_data['frequence_instantanee'] >= value_freq_min]
    return(new_data)

# Définition du noyau RBF (Radial Basis Function) et du noyau White pour le bruit
kernel = RBF(length_scale=40, length_scale_bounds=(40, 50)) + WhiteKernel(noise_level=9.0, noise_level_bounds=(1e-5, 1e+1))

# Fonction compute_points_GP et application aux données
def compute_points_GP(data, variable, distance, kernel=kernel):
    sub_dataframes = {}
    df_points_pentes = pd.DataFrame()
    X_new = np.array([])  # Initialisation de X_new avec une valeur par défaut

    for name in set(data['nom_analyse']):
        sub_dataframes[name] = data[data['nom_analyse'] == name]

    for name, sub_df in sub_dataframes.items():
        X = np.array(sub_df.loc[:, 'distance'])
        y = np.array(sub_df.loc[:, variable])

        # Création du modèle de processus gaussien
        gp = GaussianProcessRegressor(kernel=kernel, alpha=0.0, normalize_y=True)

        # Apprentissage du modèle sur les données
        gp.fit(X.reshape(-1, 1), y)

        # Prédiction sur un nouvel ensemble de données
        X_new = np.linspace(14, distance, 100)
        y_pred, y_std = gp.predict(X_new.reshape(-1, 1), return_std=True)

        new_row = pd.Series(y_pred)
        df_points_pentes = pd.concat([df_points_pentes,new_row], axis=1,ignore_index=True)
    df_points_pentes = df_points_pentes.transpose()
    return df_points_pentes, X_new


# Fonction df_pentes_coefficientees
def df_pentes_coefficientees(df_points_gp,X_echantillon,moy_pts_df):
    # Création d'un dataframe vide avec des noms de colonnes
    columns = ['pente_' + str(i) for i in range(0,df_points_gp.shape[1]-1)]
    df_pentes = pd.DataFrame(columns=columns)

    # Boucle pour ajouter des lignes
    for i in range(0, df_points_gp.shape[0]):
        diff_ligne = []
        for j in range(0, df_points_gp.shape[1]-1):
            new = (df_points_gp.loc[i,j+1] - df_points_gp.loc[i,j]) / (X_echantillon[j+1] - X_echantillon[j])
            diff_ligne.append(new)
        # Ajout de la nouvelle ligne avec les valeurs calculées
        df_pentes.loc[i] = diff_ligne

    # Calcul des valeurs absolues de chaque coefficient du df_pentes
    abs_df = df_pentes.abs()

    # Calcul de la moyenne des valeurs absolues
    mean_abs = abs_df.mean().mean()
    moyenne_points_df = moy_pts_df

    def apply_normalisation(x,moy_pts_df=moyenne_points_df,moyenne_dataframe_pentes=mean_abs):
        return((x/moyenne_dataframe_pentes)*moy_pts_df)

    df_pentes = df_pentes.applymap(apply_normalisation)
    return(df_pentes)


#  Kmeans sur les pentes + les points d'inflexion (pics et creux)
def kmeans_pentes_points_inflexion(df_points_gp,df_pentes,n_clust,X_echantillon,temps,course,title='fréquence'):
    df_inflex = pd.DataFrame()
    df_points_gp['Temps'] = np.array(temps).astype(float)
    df_inflex['Peak 1'] = np.zeros(df_pentes.shape[0])
    df_inflex['Valley 1'] = np.zeros(df_pentes.shape[0])

    for i in range(0,df_inflex.shape[0]):
        dy = np.diff(df_pentes.iloc[i,:])
        peaks_idx = (np.where((dy[:-1] > 0) & (dy[1:] < 0))[0] + 1).tolist()  # Indices des pics
        valleys_idx = (np.where((dy[:-1] < 0) & (dy[1:] > 0))[0] + 1).tolist()  # Indices des creux
        n_peaks = len(peaks_idx)
        n_valleys = len(valleys_idx)
        for j in range(0,n_peaks):
            if j == 0 :
                df_inflex.loc[i,'Peak 1'] = peaks_idx[j]
            else :
                if ('Peak ' + str(j+1)) in df_inflex.columns:
                    df_inflex.loc[i,'Peak ' + str(j+1)] = peaks_idx[j]
                else :
                    df_inflex['Peak ' + str(j+1)] = np.zeros(df_pentes.shape[0])
                    df_inflex.loc[i,'Peak ' + str(j+1)] = peaks_idx[j]

        for j in range(0,n_valleys):
            if j == 0 :
                df_inflex.loc[i,'Valley 1'] = valleys_idx[j]
            else :
                if ('Valley ' + str(j+1)) in df_inflex.columns:
                    df_inflex.loc[i,'Valley ' + str(j+1)] = valleys_idx[j]
                else :
                    df_inflex['Valley ' + str(j+1)] = np.zeros(df_pentes.shape[0])
                    df_inflex.loc[i,'Valley ' + str(j+1)] = valleys_idx[j]

    df_pentes_inflex = pd.concat([df_pentes,df_inflex],axis=1)
    kmeans = KMeans(n_clusters=n_clust, random_state=0, n_init=n_clust)
    kmeans.fit(np.array(df_pentes_inflex))

    df_points_gp['Clusters'] = kmeans.labels_
    df_points_gp_inflex = df_points_gp.copy()
    df_points_gp_inflex['Clusters'] = kmeans.labels_
    df_points_gp_inflex['Course'] = [c.replace('100 Papillon', '') for c in course]
    df_points_gp_inflex['Temps'] = temps
    df_points_gp_inflex=df_points_gp_inflex.sort_values(by='Temps')

    centroid_clusters, cluster = [], []
    for clust in df_points_gp_inflex.Clusters.unique():
        df_clust = df_points_gp_inflex.loc[df_points_gp_inflex.Clusters == clust].copy().reset_index(drop=True)
        centroid_clusters.append(np.mean(df_clust.iloc[:,:100], axis=0))
        cluster.append(clust)
    return(df_points_gp)

###################### Définition des cards #########################
card_swimmer = dbc.Card(
    dbc.CardBody(
        [
            html.H4([DashIconify(icon="carbon:user-avatar-filled", style={"marginRight": 10}), "Nom et prénom du nageur"], className="text-nowrap"),
            html.Div("Choisissez le nageur pour lequel vous souhaitez réaliser l'analyse."),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(id='nageur-dropdown',
                    options=[{'label': k, 'value': k} for k in pd.Series(sorted((df['nom_prenom']), key=comparer_noms)).unique()],
                    multi=False,
                    placeholder='Sélectionnez ...',
                    className="mb-3"),
                ], width=8)
            ],justify="center"),
            html.Br(),
            html.Br(),
        ], className="border-start border-dark border-5"
    ),
    style={"background": "#ECFED6 "},
    className="text-center m-4"
)

card_nage = dbc.Card(
    dbc.CardBody(
        [
            html.H4([DashIconify(icon="fa-solid:swimmer", style={"marginRight": 10}), "Style de nage"], className="text-nowrap"),
            html.Div("Choisissez le style de nage pour lequel vous souhaitez réaliser l'analyse. On affiche uniquement les styles qui sont associés au nageur sélectionné."),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(id='nage-dropdown',
                    options=[{'label': k, 'value': k} for k in sorted(df.style_nage.unique())],
                    multi=False,
                    placeholder='Sélectionnez ...',
                    className="mb-3"),
                ], width=8)
            ],justify="center")
        ], className="border-start border-dark border-5"
    ),
    style={"background":"#E1FEBC"},
    className="text-center m-4"
)

card_distance = dbc.Card(
    dbc.CardBody(
        [
            html.H4([DashIconify(icon="game-icons:path-distance", style={"marginRight": 10}), "Distance"], className="text-nowrap"),
            html.Div("Choisissez la distance sur laquelle vous souhaitez réaliser l'analyse. On affiche uniquement les distances qui sont associées au nageur et au style sélectionnés."),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(id='distance-dropdown',
                    options=[{'label': k, 'value': k} for k in sorted(df.distance_course.unique())],
                    multi=False,
                    placeholder='Sélectionnez ...',
                    className="mb-3"),
                ], width=8)
            ],justify="center")
        ], className="border-start border-dark border-5"
    ),
    style={"background":"#C2EB8F"},
    className="text-center m-4"
)

card_saison = dbc.Card(
    dbc.CardBody(
        [
            html.H4([DashIconify(icon="el:calendar", style={"marginRight": 10}), "Date"], className="text-nowrap"),
            html.Div("Choisissez la date (mois, année) à partir de laquelle vous souhaitez réaliser l'analyse. On affiche uniquement les dates disponibles pour le nageur sélectionné."),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(id='mois-annee-dropdown',
                    options=[{'label': k, 'value': k} for k in sorted(df.date.unique())],
                    multi=False,
                    placeholder='Sélectionnez ... ',
                    className="text-center"),
                ], width=8)
            ],justify="center"),
            html.Br(),
        ], className="border-start border-dark border-5"
    ),
    style={"background":"#A0C76E"},
    className="text-center m-4"
)

card_legend = dbc.Card(
    dbc.CardBody(
        [
            html.H5([DashIconify(icon="material-symbols:help", style={"marginRight": 10}), "Aide légende"], className="text-nowrap"),
            html.Div("Lorsque vous survolez une boîte avec la souris, différents arguments apparaissent. Voici leur signification :"),
            html.Br(),
            html.Div("0, 1, 2 ... : numéro du cluster"),
            html.Div("min : temps minimal"),
            html.Div("lower fence : borne inférieure"),
            html.Div("q1 : 1er quartile"),
            html.Div("median : médiane"),
            html.Div("q3 : 3ème quartile"),
            html.Div("upper fence : borne supérieure"),
            html.Div("max : temps maximal"),
            html.Br(),
        ]
    ),
    style={"width": "20rem","background":"#70DB93"},
    className="text-center m-4"
)

card_warning = dbc.Card(
    dbc.CardBody(
        [
            html.H5([DashIconify(icon="ph:warning-fill", style={"marginRight": 10}), "Remarque"], className="text-nowrap"),
            html.Div('Il peut arriver que le "min" (respectivement "max") soit un outlier (i.e. une valeur extrême). Dans ce cas, on distingue le "lower fence" (resp. "upper fence") du "min" (resp. "max"). Il peut être interprété comme le "min"/"max" le plus cohérent par rapport aux données du cluster.'),
        ]
    ),
    style={"width": "40rem","background":"LightCoral"},
    className="text-center m-4"
)


####################### Layout ######################

layout = dbc.Container([
    dbc.Row([
        dbc.Col(
                html.H1([DashIconify(icon='wpf:statistics', style={"marginRight": 30}),'Modélisation des profils de course']),
                width={"size": 'auto', "offset": 2}, style={"fontSize": 30, "textAlign": 'center', "fontWeight": "bold"},
            ),
    ]),

    html.Br(),
    html.Br(),

    dbc.Row([
        dbc.Col(
            html.Div(children=[DashIconify(icon="ph:number-circle-one-fill", style={"marginRight": 5}),"Sélectionnez la variable sur laquelle vous souhaitez réaliser l'analyse"], style={"fontSize": 25}),
            width={"size": 12, "offset": 0}, style={"fontSize": 15, "textAlign": 'center'}
        )
    ]),

    html.Br(),

    dbc.Row([
        dbc.Col([
            dcc.RadioItems(['  Fréquence', '  Amplitude'], '  Fréquence', inline=True, labelStyle={'margin-right': '100px'}, id = 'variable-item')
        ], width={"size": 'auto', "offset": 4})

    ]),

    html.Br(),
    html.Br(),

    dbc.Row([
        dbc.Col(
            html.Div(children=[DashIconify(icon="ph:number-circle-two-fill", style={"marginRight": 5}),"Sélectionnez les paramètres de l'analyse"], style={"fontSize": 25}),
            width={"size": 12, "offset": 0}, style={"fontSize": 15, "textAlign": 'center'}
        )
    ]),

    dbc.Row(
        [dbc.Col(card_swimmer), dbc.Col(card_nage), dbc.Col(card_distance), dbc.Col(card_saison)],
    ),

    dbc.Row([
        dbc.Col([
            dbc.Button(
            [reset_icon, "Actualiser l'analyse"], id="reset-button", className="me-2", n_clicks=0
        ),
            dcc.Download(id="download-dataframe-csv"),
        ], width={"size": 'auto', "offset": 4})
    ]),

    dcc.Store(id = 'clustering-df'),
    dcc.Store(id = 'X-echantillon'),

    html.Br(),
    html.Br(),

    dbc.Row([
        dbc.Col(
            html.Div(children=[DashIconify(icon="ph:number-circle-three-fill", style={"marginRight": 5}),"Consultez les résultats de l'analyse"], style={"fontSize": 25}),
            width={"size": 12, "offset": 0}, style={"fontSize": 15, "textAlign": 'center'}
        )
    ]),

    dbc.Row([
        dbc.Col(html.Div(id='warning-message'), width={"offset": 1})
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(figure={}, id='cluster-fig0')
        ])
    ]),

    dbc.Row([

        dbc.Col([
            dcc.Graph(figure={}, id='cluster-fig1')
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(figure={}, id='cluster-fig2')
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(figure={}, id='cluster-fig3')
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(figure={}, id='cluster-fig4')
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(figure={}, id='cluster-fig5')
        ])
    ]),

    dbc.Row([
        dbc.Col([card_legend], width={"size": 4, "offset": 0}),
        dbc.Col([
            dcc.Graph(figure={}, id='boxplot-perf')
        ], width={"size": 8, "offset": 0}),
    ]),

    dbc.Row([
        dbc.Col([card_warning], width={"size": 10, "offset": 2})
    ])
])


############################# Callbacks ###########################

@callback(
    Output('nage-dropdown', "options"),
    Input('nageur-dropdown',"value"),
)
def update_nage(nom_prenom):
    dff = df.copy()
    if nom_prenom:
        dff = dff.loc[dff.nom_prenom == nom_prenom]
    return [{'label': i, 'value': i} for i in sorted(dff.style_nage.unique())]


@callback(
    Output('distance-dropdown', "options"),
    Input('nageur-dropdown',"value"),
    Input('nage-dropdown',"value")
)
def update_distance(nom_prenom, nage):
    dff = df.copy()
    if nom_prenom:
        dff = dff.loc[dff.nom_prenom == nom_prenom]
    if nage:
        dff = dff.loc[dff.style_nage == nage]
    return [{'label': i, 'value': i} for i in sorted(dff.distance_course.unique())]


@callback(
    Output('mois-annee-dropdown', "options"),
    Input('nageur-dropdown',"value"),
    Input('nage-dropdown',"value"),
    Input('distance-dropdown',"value")
)
def update_date(nom_prenom, nage, distance):
    dff = df.copy()
    if nom_prenom:
        dff = dff.loc[dff.nom_prenom == nom_prenom]
    if nage:
        dff = dff.loc[dff.style_nage == nage]
    if distance:
        dff = dff.loc[dff.distance_course == distance]
    return [{'label': i, 'value': i} for i in sorted(dff.date.unique())]



@callback(
    Output('clustering-df', "data"),
    Output('X-echantillon', "data"),
    Output('boxplot-perf',"figure"),
    Output('warning-message',"children"),
    Input('nageur-dropdown',"value"),
    Input('nage-dropdown', "value"),
    Input('distance-dropdown', "value"),
    Input('mois-annee-dropdown', "value"),
    Input('variable-item', "value"),
    Input('reset-button', "n_clicks")
)
def plot_boxplot(nageur,nage,distance,date,variable, btn_reset_clicks):
    df_test = pd.DataFrame({'Clusters':[],
                                'Temps':[]})
    clustering = []
    X_echantillon = []
    dff_points_gp = []
    warning = ""
    fig = go.Figure()
    if "reset-button" in ctx.triggered[0]['prop_id']:
        dff = df.copy()
        if nageur:
            dff = dff.loc[dff.nom_prenom == nageur]
        if nage:
            dff = dff.loc[dff.style_nage == nage]
        if distance:
            dff = dff.loc[dff.distance_course == distance]
        if date:
            dff = dff.loc[dff.mois_annee > date]
        dff = clean_data(dff).reset_index(drop=True)

        if len(dff.nom_analyse.unique()) < 30:
            warning = "ATTENTION : le nombre de courses résultant (" + str(len(dff.nom_analyse.unique())) + ") est insuffisant pour avoir une analyse de qualité."

        if len(dff.nom_analyse.unique()) > 6:
            if variable == '  Fréquence':
                dff_points_gp, X_echantillon = compute_points_GP(dff,variable='frequence_instantanee',distance=distance)
            if variable == '  Amplitude':
                dff_points_gp, X_echantillon = compute_points_GP(dff,variable='amplitude_instantanee',distance=distance)

            moyenne_dataframe_points = dff_points_gp.mean().mean()
            dff_pentes = df_pentes_coefficientees(dff_points_gp,X_echantillon,moyenne_dataframe_points)

            # Concaténation des dataframes df_points_gp et df_pentes
            df_global = pd.concat([dff_points_gp, dff_pentes], axis=1)

            # Récupération des noms des courses et des temps associés à chaque course
            sub_dataframes = {}
            courses = []
            temps = []
            for name in set(dff['nom_analyse']):
                sub_dataframes[name] = dff[dff['nom_analyse'] == name]

            for name, sub_df in sub_dataframes.items():
                # Obtenir l'indice de la dernière ligne
                last_index = sub_df.index[-1]
                courses.append(name)
                temps.append(sub_df.loc[last_index,'temps_final'])
            n_clust = 6
            clustering = kmeans_pentes_points_inflexion(dff_points_gp,dff_pentes,n_clust,X_echantillon,temps,courses,title='fréquence')
            clustering['Course'] = courses

            df_test = clustering[['Clusters','Temps']]
            clustering = clustering.to_dict('records')
            fig = px.box(df_test, x='Clusters',y='Temps', color='Clusters',
                         labels = {'Temps': 'Temps (en secondes)'},
                        category_orders={'Clusters': sorted(df_test['Clusters'].unique())},
                        color_discrete_sequence=px.colors.qualitative.Dark2
                        )


    return clustering, X_echantillon, fig, warning


@callback(
    Output('cluster-fig0', "figure"),
    Input('clustering-df', "data"),
    Input('X-echantillon', "data"),
    Input('variable-item', "value"),
)

def plot_fig0(clustering_df, X_echantillon, variable):
    df = clustering_df.copy()
    df = pd.DataFrame(df)
    fig_clust = go.Figure()
    if not df.empty:
        df_clust = df.loc[df.Clusters == 0].copy().reset_index(drop=True)
        df_clust = df_clust.sort_values(by = 'Temps', ascending=True)
        df_clust['Temps'] = df_clust['Temps'].apply(lambda x: '{:02d}:{:05.2f}'.format(int(float(x) // 60), float(x) % 60))
        hover_templates = []
        for i in range(df_clust.shape[0]):
            liste_points_GP = df_clust.iloc[i,:100]
            df_race = pd.DataFrame({'X_echantillon':X_echantillon,
                                    'Points_GP':liste_points_GP.to_numpy().flatten()})
            hover_templates.append(df_clust.loc[i, 'Temps'])
            fig_clust.add_trace(go.Scatter(
                x=df_race['X_echantillon'],
                y=df_race['Points_GP'],
                mode='lines',
                name=str(df_clust.loc[i,'Temps']) + ' - ' + df_clust.loc[i, 'Course'],
                hovertemplate=hover_templates[i]
            ))

        fig_clust.update_layout(
            yaxis_title=variable,
            xaxis_title='Distance',
            title='Cluster 0',
            legend_traceorder="normal",
            legend_itemclick="toggleothers"
        )

    return fig_clust



@callback(
    Output('cluster-fig1', "figure"),
    Input('clustering-df', "data"),
    Input('X-echantillon', "data"),
    Input('variable-item', "value"),
)

def plot_fig1(clustering_df, X_echantillon, variable):
    df = clustering_df.copy()
    df = pd.DataFrame(df)
    fig_clust = go.Figure()
    if not df.empty:
        df_clust = df.loc[df.Clusters == 1].copy().reset_index(drop=True)
        df_clust = df_clust.sort_values(by = 'Temps', ascending=True)
        df_clust['Temps'] = df_clust['Temps'].apply(lambda x: '{:02d}:{:05.2f}'.format(int(float(x) // 60), float(x) % 60))
        hover_templates = []
        for i in range(df_clust.shape[0]):
            liste_points_GP = df_clust.iloc[i,:100]
            df_race = pd.DataFrame({'X_echantillon':X_echantillon,
                                    'Points_GP':liste_points_GP.to_numpy().flatten()})
            hover_templates.append(df_clust.loc[i, 'Temps'])
            fig_clust.add_trace(go.Scatter(
                x=df_race['X_echantillon'],
                y=df_race['Points_GP'],
                mode='lines',
                name=str(df_clust.loc[i,'Temps']) + ' - ' + df_clust.loc[i, 'Course'],
                hovertemplate=hover_templates[i]
            ))

        fig_clust.update_layout(
            yaxis_title=variable,
            xaxis_title='Distance',
            title='Cluster 1',
            legend_traceorder="normal",
            legend_itemclick="toggleothers"
        )

    return fig_clust


@callback(
    Output('cluster-fig2', "figure"),
    Input('clustering-df', "data"),
    Input('X-echantillon', "data"),
    Input('variable-item', "value"),
)

def plot_fig2(clustering_df, X_echantillon,variable):
    df = clustering_df.copy()
    df = pd.DataFrame(df)
    fig_clust = go.Figure()
    if not df.empty:
        df_clust = df.loc[df.Clusters == 2].copy().reset_index(drop=True)
        df_clust = df_clust.sort_values(by = 'Temps', ascending=True)
        df_clust['Temps'] = df_clust['Temps'].apply(lambda x: '{:02d}:{:05.2f}'.format(int(float(x) // 60), float(x) % 60))
        hover_templates=[]
        for i in range(df_clust.shape[0]):
            liste_points_GP = df_clust.iloc[i,:100]
            df_race = pd.DataFrame({'X_echantillon':X_echantillon,
                                    'Points_GP':liste_points_GP.to_numpy().flatten()})
            hover_templates.append(df_clust.loc[i, 'Temps'])
            fig_clust.add_trace(go.Scatter(
                x=df_race['X_echantillon'],
                y=df_race['Points_GP'],
                mode='lines',
                name=str(df_clust.loc[i,'Temps']) + ' - ' + df_clust.loc[i, 'Course'],
                hovertemplate=hover_templates[i]
            ))

        fig_clust.update_layout(
            yaxis_title=variable,
            xaxis_title='Distance',
            title='Cluster 2',
            legend_traceorder="normal",
            legend_itemclick="toggleothers"
        )

    return fig_clust


@callback(
    Output('cluster-fig3', "figure"),
    Input('clustering-df', "data"),
    Input('X-echantillon', "data"),
    Input('variable-item', "value"),
)

def plot_fig3(clustering_df, X_echantillon, variable):
    df = clustering_df.copy()
    df = pd.DataFrame(df)
    fig_clust = go.Figure()
    if not df.empty:
        df_clust = df.loc[df.Clusters == 3].copy().reset_index(drop=True)
        df_clust = df_clust.sort_values(by = 'Temps', ascending=True)
        df_clust['Temps'] = df_clust['Temps'].apply(lambda x: '{:02d}:{:05.2f}'.format(int(float(x) // 60), float(x) % 60))
        hover_templates = []
        for i in range(df_clust.shape[0]):
            liste_points_GP = df_clust.iloc[i,:100]
            df_race = pd.DataFrame({'X_echantillon':X_echantillon,
                                    'Points_GP':liste_points_GP.to_numpy().flatten()})
            hover_templates.append(df_clust.loc[i, 'Temps'])
            fig_clust.add_trace(go.Scatter(
                x=df_race['X_echantillon'],
                y=df_race['Points_GP'],
                mode='lines',
                name=str(df_clust.loc[i,'Temps']) + ' - ' + df_clust.loc[i, 'Course'],
                hovertemplate=hover_templates[i]
            ))

        fig_clust.update_layout(
            yaxis_title=variable,
            xaxis_title='Distance',
            title='Cluster 3',
            legend_traceorder="normal",
            legend_itemclick="toggleothers"
        )

    return fig_clust



@callback(
    Output('cluster-fig4', "figure"),
    Input('clustering-df', "data"),
    Input('X-echantillon', "data"),
    Input('variable-item', "value"),
)

def plot_fig4(clustering_df, X_echantillon, variable):
    df = clustering_df.copy()
    df = pd.DataFrame(df)
    fig_clust = go.Figure()
    if not df.empty:
        df_clust = df.loc[df.Clusters == 4].copy().reset_index(drop=True)
        df_clust = df_clust.sort_values(by = 'Temps', ascending=True)
        df_clust['Temps'] = df_clust['Temps'].apply(lambda x: '{:02d}:{:05.2f}'.format(int(float(x) // 60), float(x) % 60))
        hover_templates = []
        for i in range(df_clust.shape[0]):
            liste_points_GP = df_clust.iloc[i,:100]
            df_race = pd.DataFrame({'X_echantillon':X_echantillon,
                                    'Points_GP':liste_points_GP.to_numpy().flatten()})
            hover_templates.append(df_clust.loc[i, 'Temps'])
            fig_clust.add_trace(go.Scatter(
                x=df_race['X_echantillon'],
                y=df_race['Points_GP'],
                mode='lines',
                name=str(df_clust.loc[i,'Temps']) + ' - ' + df_clust.loc[i, 'Course'],
                hovertemplate=hover_templates[i]
            ))

        fig_clust.update_layout(
            yaxis_title=variable,
            xaxis_title='Distance',
            title='Cluster 4',
            legend_traceorder="normal",
            legend_itemclick="toggleothers"
        )

    return fig_clust



@callback(
    Output('cluster-fig5', "figure"),
    Input('clustering-df', "data"),
    Input('X-echantillon', "data"),
    Input('variable-item', "value"),
)

def plot_fig5(clustering_df, X_echantillon, variable):
    df = clustering_df.copy()
    df = pd.DataFrame(df)
    fig_clust = go.Figure()
    if not df.empty:
        df_clust = df.loc[df.Clusters == 5].copy().reset_index(drop=True)
        df_clust = df_clust.sort_values(by = 'Temps', ascending=True)
        df_clust['Temps'] = df_clust['Temps'].apply(lambda x: '{:02d}:{:05.2f}'.format(int(float(x) // 60), float(x) % 60))
        hover_templates = []
        for i in range(df_clust.shape[0]):
            liste_points_GP = df_clust.iloc[i,:100]
            df_race = pd.DataFrame({'X_echantillon':X_echantillon,
                                    'Points_GP':liste_points_GP.to_numpy().flatten()})
            hover_templates.append(df_clust.loc[i, 'Temps'])
            fig_clust.add_trace(go.Scatter(
                x=df_race['X_echantillon'],
                y=df_race['Points_GP'],
                mode='lines',
                name=str(df_clust.loc[i,'Temps']) + ' - ' + df_clust.loc[i, 'Course'],
                hovertemplate=hover_templates[i]
            ))

        fig_clust.update_layout(
            yaxis_title=variable,
            xaxis_title='Distance',
            title='Cluster 5',
            legend_traceorder="normal",
            legend_itemclick="toggleothers"
        )

    return fig_clust