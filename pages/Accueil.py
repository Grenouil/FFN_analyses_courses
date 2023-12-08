import dash
from dash import dcc, html, callback, Input, Output, ctx
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify

dash.register_page(__name__,path="/",name="Menu principal", order=1)

####################### Définition des cards ######################

card_carac_donnees_brutes = dbc.Card(
    dbc.CardBody(
        [
            html.H5([DashIconify(icon = "mdi:database-search", style={"marginRight": 10}), "Parcourir les données brutes"], className="text-nowrap"),
            html.Ul([
                html.Br(),
                html.Li("affichage de la base de données détaillée des analyses de courses, avec la fréquence et l'amplitude estimées en instantanné."),
                html.Br(),
                html.Li("possibilité de trier la base de données selon les paramètres saisis par l'utilisateur (nageur(s), compétition(s) & épreuve(s))."),
                html.Br(),
                html.Li(["exportation de la base de données affichée aux formats .csv", DashIconify(icon="fa6-solid:file-csv", style={"marginLeft":5, "marginRight": 5}), " et .xlsx", DashIconify(icon="file-icons:microsoft-excel", style={"marginLeft": 5, "marginRight": 5})]),
            ], style={"textAlign": "justify"}),
        ], className="border-start border-dark border-5"
    ), style={"width": "27rem","background": '#fbacb9'},
    className="text-center m-4 ml-3"
)


card_carac_analyse_courses = dbc.Card(
    dbc.CardBody(
        [
            html.H5([DashIconify(icon = "wpf:statistics", style={"marginRight": 10}), "Analyse des parties nagées"], className="text-nowrap"),
            html.Ul([
                html.Br(),
                html.Li("clustering sur les courbes de fréquence OU d'amplitude afin d'établir un modèle de 'profil de course'."),
                html.Br(),
                html.Li("boxplot de la performance chronométrique en fonction du cluster : identification des profils de course intéressants."),
                html.Br(),
                html.Li("possibilité d'appliquer l'étude au nageur et à la course choisis par l'utilisateur.")
            ], style={"textAlign": "justify"}),
        ], className="border-start border-dark border-5"
    ), style={"width": "26rem","background": "#E1FEBC"},
    className="text-center m-4 ml-3"
)


card_carac_donnees_section = dbc.Card(
    dbc.CardBody(
        [
            html.H5([DashIconify(icon = "ri:pin-distance-fill", style={"marginRight": 10}), "Parcourir les données/section"], className="text-nowrap"),
            html.Ul([
                html.Br(),
                html.Li("affichage de la base de données des analyses de courses en fonction du temps OU de la vitesse OU du nombre de cycles par section."),
                html.Br(),
                html.Li("affichage de la base de données des analyses de courses en fonction de la fréquence OU du tempo OU de l'amplitude par section."),
                html.Br(),
                html.Li("tableau retraçant l'évolution de la vitesse, fréquence et amplitude en fonction de la section de course."),
                html.Br(),
                html.Li(["exportation de la base de données affichée aux formats .csv", DashIconify(icon="fa6-solid:file-csv", style={"marginLeft":5, "marginRight": 5}), " et .xlsx", DashIconify(icon="file-icons:microsoft-excel", style={"marginLeft": 5, "marginRight": 5})]),
                html.Br(),
                html.Li("graphique représentant la variable d'étude en fonction de la distance parcourue, en sélectionnant autant de nageurs que souhaité."),
                html.Br(),
                html.Li("possibilité de trier la base de données affichée selon les paramètres saisis par l'utilisateur (épreuve & nageur(s)).")
            ], style={"textAlign": "justify"}),
        ], className="border-start border-dark border-5"
    ), style={"width": "27rem","background": "turquoise"},
    className="text-center m-4 ml-3"
)



card_carac_parties_NN = dbc.Card(
    dbc.CardBody(
        [
            html.H5([DashIconify(icon = 'map:diving', style={"marginRight": 10}), "Parcourir les parties"], className="text-nowrap"),
            html.H5("non nagées", className="text-nowrap"),
            html.Ul([
                html.Br(),
                html.Li("affichage de la base de données des parties non nagées en fonction de l'épreuve ET / OU du (des) nageur(s) sélectionné(s)."),
                html.Br(),
                html.Li(["exportation de la base de données affichée aux formats .csv", DashIconify(icon="fa6-solid:file-csv", style={"marginLeft":5, "marginRight": 5}), " et .xlsx", DashIconify(icon="file-icons:microsoft-excel", style={"marginLeft": 5, "marginRight": 5})]),
                html.Br(),
                html.Li("graphiques représentant la variable d'étude en fonction de la coulée et des nageurs sélectionnés."),
                html.Br(),
                html.Li("possibilité d'afficher 2 types de modélisation : l'une en une dimension (pour une coulée donnée, on annote le temps OU la distance parcourue en fonction du nageur), l'autre en 2 dimensions (pour une coulée donnée, on annote le temps ET la distance parcourue en fonction du nageur).")
            ], style={"textAlign": "justify"}),
        ], className="border-start border-dark border-5"
    ), style={"width": "26rem","background": '#fdc692'},
    className="text-center m-4 ml-3"
)


############################ Layout #############################
layout = dbc.Container(
    [
        html.Br(),
        html.H1([DashIconify(icon="emojione-monotone:1st-place-medal", style={"marginRight": 15, "size": "60px"}),'Bienvenue !'], className="text-nowrap", style={'textAlign': "center"}),
        html.Br(),
        html.Br(),
        html.H4([DashIconify(icon="wpf:ask-question", style={"marginRight": 15, "size": "60px"}), "FFN Web App, quésaco ?"], className="text-nowrap", style={'textAlign': "left"}),
        html.Div([
            html.Span("FFN application web ",style={'font-weight': 'bold'}),
            "a été conçue dans le but de :"
        ]),
        html.Ul([
            html.Li("faciliter l'accès aux bases de données relatives aux analyses de courses mises à disposition par la FFN & Seenovate ;"),
            html.Li("visualiser dynamiquement les données en laissant l'utilisateur libre de paramétrer les graphiques ; "),
            html.Li("proposer un modèle de profils de courses en fonction des données de fréquence ou d'amplitude et faire le lien avec la performance.")
        ], style={"textAlign": "justify"}),
        html.Br(),

        html.H4([DashIconify(icon="mdi:head-question-outline", style={"marginRight": 15, "size": "70px"}), "Et comment ça marche ?"], className="text-nowrap", style={'textAlign': "left"}),
        html.Div("Afin de répondre à ces besoins, l'application a été divisée en 4 onglets distincts. Vous trouverez ci-dessous une description du contenu de chaque onglet. Pour naviguer entre les différentes sections, veuillez cliquer sur l'onglet de votre choix dans la barre latérale gauche."),
        html.Br(),

        dbc.Row([
            dbc.Col(card_carac_donnees_brutes), dbc.Col(card_carac_analyse_courses)
        ]),

        dbc.Row([
            dbc.Col(card_carac_donnees_section), dbc.Col(card_carac_parties_NN)
        ]),

        html.Br(),
        html.H4([DashIconify(icon="emojione-monotone:light-bulb", style={"marginRight": 15, "size": "90px"}), "Pour aller plus loin : astuces et autres conseils"], className="text-nowrap", style={'textAlign': "left"}),
        html.Div("Tous les graphiques affichés par l'application peuvent être ajustés selon les préférences de l'utilisateur. Un émoticône spécifique à chaque fonctionnalité apparaît en haut à droite dudit graphique :"),
        html.Br(),
        html.Div([DashIconify(icon="subway:camera", style={"marginRight": 10, "size": "50px"}), html.Span("Download plot as png", style={'font-weight': 'bold'}),
                  " : télécharge le graphique affiché au format .png", DashIconify(icon="bi:filetype-png", style={"marginLeft": 10, "size": "70px"}), "."]),
        html.Div([DashIconify(icon="carbon:zoom-fit",  style={"marginRight": 10, "size": "90px"}), html.Span("Zoom", style={'font-weight': 'bold'}),
                 " : zoome sur la zone contenue dans le rectangle défini manuellement par l'utilisateur."]),
        html.Div([DashIconify(icon="grommet-icons:pan", style={"marginRight": 10, "size": "50px"}), html.Span("Pan", style={'font-weight': 'bold'}),
                  " : décale le graphique vers le haut, le bas, la gauche, la droite selon le déplacement du curseur", DashIconify(icon="clarity:cursor-arrow-solid", style={"marginLeft": 5,"marginRight": 5, "size": "50px"}),
                  " de l'utilisateur."]),
        html.Div([DashIconify(icon="mdi:plus-box", style={"marginRight": 10, "size": "50px"}), html.Span("Zoom in", style={'font-weight': 'bold'}),
                  " : zoom automatique sur le graphique."]),
        html.Div([DashIconify(icon="mdi:minus-box", style={"marginRight": 10, "size": "50px"}), html.Span("Zoom out", style={'font-weight': 'bold'}),
                  " : dézoom automatique sur le graphique."]),
        html.Div([DashIconify(icon="material-symbols:zoom-out-map", style={"marginRight": 10, "size": "50px"}), html.Span("Autoscale", style={'font-weight': 'bold'}),
                  " : réinitialise l'affichage du graphique automatiquement."]),
        html.Div([DashIconify(icon="ion:home", style={"marginRight": 10, "size": "50px"}), html.Span("Reset axes",  style={'font-weight': 'bold'}),
                  " : réinitialise les axes (abscisses et ordonnées) automatiquement."]),
        html.Br(),
        html.Br(),

        html.Div("Sur chaque graphique, il est également possible d'isoler une courbe / un point associé à un nageur ou à une course donné(e). Pour ce faire, il faut cliquer dans la légende sur le label que l'utilisateur souhaite isoler. Pour revenir au graphique initial, il suffit de cliquer à nouveau sur le label isolé."),
        html.Br(),
        html.Div("Les courbes ou les points de tous les graphiques affichent des informations précises : lorsque l'utilisateur survole une courbe ou un point donné(e) avec son curseur, les données relatives à cette courbe ou à ce point s'affichent à l'écran."),
        html.Br(),
        html.Br(),

        html.H4([DashIconify(icon="emojione-monotone:skull-and-crossbones", style={"marginRight": 15, "size": "80px"}), "En cas d'erreur ..."], className="text-nowrap", style={'textAlign': "left"}),
        html.Div(["Si un message d'erreur apparaît à l'écran ou que la page web semble plantée, rafraîchissez-la avec l'icône",
                  DashIconify(icon="material-symbols:refresh", style={"marginLeft": 5,"marginRight": 5, "size": "50px"}), "de votre navigateur ou cliquez sur la barre de recherche et pressez la touche Entrée",
                  DashIconify(icon="icon-park-solid:enter-key-one", style={"marginLeft": 5,"marginRight": 5, "size": "50px"}), "du clavier."]),
        html.Br(),
        html.Br()
    ])



