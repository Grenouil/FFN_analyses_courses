import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, callback, Input, Output, State, dash_table, ctx
import pandas as pd
from dash_iconify import DashIconify


app = dash.Dash(__name__, use_pages=True,suppress_callback_exceptions=True,external_stylesheets=[dbc.themes.LUX, '/assets/styles.css'])

app.css.append_css({
    'external_url': (
        '.hr-thicker {'
        '   border-top: 5px solid black;'  # Augmenter l'épaisseur à 5px (ou la valeur souhaitée)
        '}'
    )
})

###################### Pré-traitement des données #########################

thicker_hr_style = {
    'border-top': '5px solid black',
}

sidebar = dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Div(page["name"], className="ms-2"),
                    ],
                    href=page["path"],
                    active="exact",
                )
                for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True,
            className="bg-light",
)


app.layout = dbc.Container(
    [
        # main app framework
        dbc.Row([
            dbc.Col(
                html.Img(src='assets/Essai_logo_Hugo_blanc.png', alt='Mon Image', style={'width': '160px'}),
                width={"size": 2, "offset": 1}
            ),
            dbc.Col([
                html.Br(),
                html.Div("Analyses de courses", style={'fontSize': 90, 'textAlign': 'center'}, className="titlefamily")
            ], width={"size": 7, "offset": 0})
        ]),

        #html.Div("FFN - Analyses de courses", style={'fontSize':50, 'textAlign':'center', 'fontFamily': 'Raleway'}),

        html.Hr(style = thicker_hr_style),

        # content of each page
        dbc.Row(
        [
            dbc.Col(
                [
                    sidebar
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),

            dbc.Col(
                [
                    dash.page_container
                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10)
        ]
    )
], fluid=True)


if __name__ == "__main__":
    app.run(debug=True)

