import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, callback, Input, Output, State, dash_table, ctx
from dash_iconify import DashIconify
#import plotly.express as px
import pandas as pd
import numpy as np
#from functools import reduce
import plotly.graph_objects as go
from datetime import datetime
from openpyxl import Workbook
#from app import df

dash.register_page(__name__, name=[DashIconify(icon="ri:pin-distance-fill", style={"marginRight": 8}), "Parcourir les données par section"], order=2)

###################### Pré-traitement des données #########################
df_section_init = pd.read_csv("https://raw.githubusercontent.com/Grenouil/FFN-web-app/main/Base_parties_nagees.csv", dtype = {'id_analyse':int, 'nom_analyse':str, 'nom_prenom':str, 'nageur_sexe':str, 'competition_nom':str, 'mois_annee':str, 'distance_course':int, 'style_nage':str, 'round':str, 'temps_final':float,  'temps_reaction':float, 'temps_vol':float, 'temps_depart':float, 'TEMPS_SECTION':str, 'VITESSE':str, 'NB_CYCLE': str, 'FREQUENCE': str, 'TEMPO': str, 'AMPLITUDE': str})
df_section_init = df_section_init.rename(columns={'round': 'round_name'})

reset_section_icon = DashIconify(icon="grommet-icons:power-reset", style={"marginRight": 5})
csv_section_icon = DashIconify(icon="fa6-solid:file-csv", style={"marginRight": 5})
excel_section_icon = DashIconify(icon="file-icons:microsoft-excel", style={"marginRight": 5})
graph_section_icon = DashIconify(icon="mdi:graph-line", style={"marginRight": 5})
selectall_section_icon = DashIconify(icon="fluent:select-all-on-24-filled", style={"marginRight": 5})
deselectall_section_icon = DashIconify(icon="charm:square-cross", style={"marginRight": 5})

color_first_section = "darkturquoise"
color_second_section = "teal"
color_third_section = "#005364"

thicker_hr_style_first_section = {
    'border-top': '5px solid darkturquoise',
}

thicker_hr_style_second_section = {
    'border-top': '5px solid teal',
}


# Fonction df_par_section complète
def df_par_sections(df, distance):
    dff = df.copy()
    dff['temps_final'] = dff['temps_final'].apply(lambda x: '{:02d}:{:05.2f}'.format(int(float(x) // 60), float(x) % 60))
    if distance in [50, 100, 200]:
        col_temps = ['Temps 15m', 'Temps 25m', 'Temps 45m', 'Temps 50m',
               'Temps 55m', 'Temps 65m', 'Temps 75m', 'Temps 95m', 'Temps 100m',
               'Temps 105m', 'Temps 115m', 'Temps 125m', 'Temps 145m', 'Temps 150m',
               'Temps 155m', 'Temps 165m', 'Temps 175m', 'Temps 195m', 'Temps 200m']

        col_vitesse = ['Vitesse 0-15m', 'Vitesse 15-25m', 'Vitesse 25-45m', 'Vitesse 45-50m',
               'Vitesse 50-55m', 'Vitesse 55-65m', 'Vitesse 65-75m', 'Vitesse 75-95m', 'Vitesse 95-100m',
               'Vitesse 100-105m', 'Vitesse 105-115m', 'Vitesse 115-125m', 'Vitesse 125-145m', 'Vitesse 145-150m',
               'Vitesse 150-155m', 'Vitesse 155-165m', 'Vitesse 165-175m', 'Vitesse 175-195m', 'Vitesse 195-200m']

        col_nb_cycles = ['Nb cycles 0-15m', 'Nb cycles 15-25m', 'Nb cycles 25-45m', 'Nb cycles 45-50m',
               'Nb cycles 50-55m', 'Nb cycles 55-65m', 'Nb cycles 65-75m', 'Nb cycles 75-95m', 'Nb cycles 95-100m',
               'Nb cycles 100-105m', 'Nb cycles 105-115m', 'Nb cycles 115-125m', 'Nb cycles 125-145m', 'Nb cycles 145-150m',
               'Nb cycles 150-155m', 'Nb cycles 155-165m', 'Nb cycles 165-175m', 'Nb cycles 175-195m', 'Nb cycles 195-200m']

        dff = dff.loc[dff.distance_course.isin([50,100,200])].reset_index(drop=True)
        series_temps = dff['TEMPS_SECTION'].str.split(';', expand=True)
        series_vitesse = dff['VITESSE'].str.split(';', expand=True)
        series_cycles = dff['NB_CYCLE'].str.split(';', expand=True)
        df_sep_temps = pd.DataFrame({col_temps[i]: series_temps[i] for i in range(len(col_temps))})
        df_sep_vitesse = pd.DataFrame({col_vitesse[i]: series_vitesse[i] for i in range(len(col_vitesse))})
        df_sep_cycles = pd.DataFrame({col_nb_cycles[i]: series_cycles[i] for i in range(len(col_nb_cycles))})
        dff = pd.concat([dff, df_sep_temps, df_sep_vitesse, df_sep_cycles], axis=1)
        dff = dff.loc[dff.distance_course == distance]
        dff = dff.dropna(axis=1, how='all')

        for colonne in dff.columns:
            if colonne.startswith('Temps'):
                dff[str(colonne)] = dff[str(colonne)].apply(lambda x: '{:02d}:{:05.2f}'.format(int(float(x) // 60), float(x) % 60))

    if distance in [400, 800, 1500]:
        col_temps = ['Temps 15m', 'Temps 25m', 'Temps 45m', 'Temps 50m',
               'Temps 55m', 'Temps 75m', 'Temps 95m', 'Temps 100m',
               'Temps 105m', 'Temps 125m', 'Temps 145m', 'Temps 150m',
               'Temps 155m', 'Temps 175m', 'Temps 195m', 'Temps 200m',
               'Temps 205m', 'Temps 225m', 'Temps 245m', 'Temps 250m',
               'Temps 255m', 'Temps 275m', 'Temps 295m', 'Temps 300m',
               'Temps 305m', 'Temps 325m', 'Temps 345m', 'Temps 350m',
               'Temps 355m', 'Temps 375m', 'Temps 395m', 'Temps 400m',
               'Temps 405m', 'Temps 425m', 'Temps 445m', 'Temps 450m',
               'Temps 455m', 'Temps 475m', 'Temps 495m', 'Temps 500m',
               'Temps 505m', 'Temps 525m', 'Temps 545m', 'Temps 550m',
               'Temps 555m', 'Temps 575m', 'Temps 595m', 'Temps 600m',
               'Temps 605m', 'Temps 625m', 'Temps 645m', 'Temps 650m',
               'Temps 655m', 'Temps 675m', 'Temps 695m', 'Temps 700m',
               'Temps 705m', 'Temps 725m', 'Temps 745m', 'Temps 750m',
               'Temps 755m', 'Temps 775m', 'Temps 795m', 'Temps 800m',
               'Temps 805m', 'Temps 825m', 'Temps 845m', 'Temps 850m',
               'Temps 855m', 'Temps 875m', 'Temps 895m', 'Temps 900m',
               'Temps 905m', 'Temps 925m', 'Temps 945m', 'Temps 950m',
               'Temps 955m', 'Temps 975m', 'Temps 995m', 'Temps 1000m',
               'Temps 1005m', 'Temps 1025m', 'Temps 1045m', 'Temps 1050m',
               'Temps 1055m', 'Temps 1075m', 'Temps 1095m', 'Temps 1100m',
               'Temps 1105m', 'Temps 1125m', 'Temps 1145m', 'Temps 1150m',
               'Temps 1155m', 'Temps 1175m', 'Temps 1195m', 'Temps 1200m',
               'Temps 1205m', 'Temps 1225m', 'Temps 1245m', 'Temps 1250m',
               'Temps 1255m', 'Temps 1275m', 'Temps 1295m', 'Temps 1300m',
               'Temps 1305m', 'Temps 1325m', 'Temps 1345m', 'Temps 1350m',
               'Temps 1355m', 'Temps 1375m', 'Temps 1395m', 'Temps 1400m',
               'Temps 1405m', 'Temps 1425m', 'Temps 1445m', 'Temps 1450m',
               'Temps 1455m', 'Temps 1475m', 'Temps 1495m', 'Temps 1500m']

        col_vitesse = ['Vitesse 0-15m', 'Vitesse 15-25m', 'Vitesse 25-45m', 'Vitesse 45-50m',
               'Vitesse 50-55m', 'Vitesse 55-75m', 'Vitesse 75-95m', 'Vitesse 95-100m',
               'Vitesse 100-105m', 'Vitesse 105-125m', 'Vitesse 125-145m', 'Vitesse 145-150m',
               'Vitesse 150-155m', 'Vitesse 155-175m', 'Vitesse 175-195m', 'Vitesse 195-200m',
               'Vitesse 200-205m', 'Vitesse 205-225m', 'Vitesse 225-245m', 'Vitesse 245-250m',
               'Vitesse 250-255m', 'Vitesse 255-275m', 'Vitesse 275-295m', 'Vitesse 295-300m',
               'Vitesse 300-305m', 'Vitesse 305-325m', 'Vitesse 325-345m', 'Vitesse 345-350m',
               'Vitesse 350-355m', 'Vitesse 355-375m', 'Vitesse 375-395m', 'Vitesse 395-400m',
               'Vitesse 400-405m', 'Vitesse 405-425m', 'Vitesse 425-445m', 'Vitesse 445-450m',
               'Vitesse 450-455m', 'Vitesse 455-475m', 'Vitesse 475-495m', 'Vitesse 495-500m',
               'Vitesse 500-505m', 'Vitesse 505-525m', 'Vitesse 525-545m', 'Vitesse 545-550m',
               'Vitesse 550-555m', 'Vitesse 555-575m', 'Vitesse 575-595m', 'Vitesse 595-600m',
               'Vitesse 600-605m', 'Vitesse 605-625m', 'Vitesse 625-645m', 'Vitesse 645-650m',
               'Vitesse 650-655m', 'Vitesse 655-675m', 'Vitesse 675-695m', 'Vitesse 695-700m',
               'Vitesse 700-705m', 'Vitesse 705-725m', 'Vitesse 725-745m', 'Vitesse 745-750m',
               'Vitesse 750-755m', 'Vitesse 755-775m', 'Vitesse 775-795m', 'Vitesse 795-800m',
               'Vitesse 800-805m', 'Vitesse 805-825m', 'Vitesse 825-845m', 'Vitesse 845-850m',
               'Vitesse 850-855m', 'Vitesse 855-875m', 'Vitesse 875-895m', 'Vitesse 895-900m',
               'Vitesse 900-905m', 'Vitesse 905-925m', 'Vitesse 925-945m', 'Vitesse 945-950m',
               'Vitesse 950-955m', 'Vitesse 955-975m', 'Vitesse 975-995m', 'Vitesse 995-1000m',
               'Vitesse 1000-1005m', 'Vitesse 1005-1025m', 'Vitesse 1025-1045m', 'Vitesse 1045-1050m',
               'Vitesse 1050-1055m', 'Vitesse 1055-1075m', 'Vitesse 1075-1095m', 'Vitesse 1095-1100m',
               'Vitesse 1100-1105m', 'Vitesse 1105-1125m', 'Vitesse 1125-1145m', 'Vitesse 1145-1150m',
               'Vitesse 1150-1155m', 'Vitesse 1155-1175m', 'Vitesse 1175-1195m', 'Vitesse 1195-1200m',
               'Vitesse 1200-1205m', 'Vitesse 1205-1225m', 'Vitesse 1225-1245m', 'Vitesse 1245-1250m',
               'Vitesse 1250-1255m', 'Vitesse 1255-1275m', 'Vitesse 1275-1295m', 'Vitesse 1295-1300m',
               'Vitesse 1300-1305m', 'Vitesse 1305-1325m', 'Vitesse 1325-1345m', 'Vitesse 1345-1350m',
               'Vitesse 1350-1355m', 'Vitesse 1355-1375m', 'Vitesse 1375-1395m', 'Vitesse 1395-1400m',
               'Vitesse 1400-1405m', 'Vitesse 1405-1425m', 'Vitesse 1425-1445m', 'Vitesse 1445-1450m',
               'Vitesse 1450-1455m', 'Vitesse 1455-1475m', 'Vitesse 1475-1495m', 'Vitesse 1495-1500m'
            ]

        col_nb_cycles = ['Nb cycles 0-15m', 'Nb cycles 15-25m', 'Nb cycles 25-45m', 'Nb cycles 45-50m',
               'Nb cycles 50-55m', 'Nb cycles 55-75m', 'Nb cycles 75-95m', 'Nb cycles 95-100m',
               'Nb cycles 100-105m', 'Nb cycles 105-125m', 'Nb cycles 125-145m', 'Nb cycles 145-150m',
               'Nb cycles 150-155m', 'Nb cycles 155-175m', 'Nb cycles 175-195m', 'Nb cycles 195-200m',
               'Nb cycles 200-205m', 'Nb cycles 205-225m', 'Nb cycles 225-245m', 'Nb cycles 245-250m',
               'Nb cycles 250-255m', 'Nb cycles 255-275m', 'Nb cycles 275-295m', 'Nb cycles 295-300m',
               'Nb cycles 300-305m', 'Nb cycles 305-325m', 'Nb cycles 325-345m', 'Nb cycles 345-350m',
               'Nb cycles 350-355m', 'Nb cycles 355-375m', 'Nb cycles 375-395m', 'Nb cycles 395-400m',
               'Nb cycles 400-405m', 'Nb cycles 405-425m', 'Nb cycles 425-445m', 'Nb cycles 445-450m',
               'Nb cycles 450-455m', 'Nb cycles 455-475m', 'Nb cycles 475-495m', 'Nb cycles 495-500m',
               'Nb cycles 500-505m', 'Nb cycles 505-525m', 'Nb cycles 525-545m', 'Nb cycles 545-550m',
               'Nb cycles 550-555m', 'Nb cycles 555-575m', 'Nb cycles 575-595m', 'Nb cycles 595-600m',
               'Nb cycles 600-605m', 'Nb cycles 605-625m', 'Nb cycles 625-645m', 'Nb cycles 645-650m',
               'Nb cycles 650-655m', 'Nb cycles 655-675m', 'Nb cycles 675-695m', 'Nb cycles 695-700m',
               'Nb cycles 700-705m', 'Nb cycles 705-725m', 'Nb cycles 725-745m', 'Nb cycles 745-750m',
               'Nb cycles 750-755m', 'Nb cycles 755-775m', 'Nb cycles 775-795m', 'Nb cycles 795-800m',
               'Nb cycles 800-805m', 'Nb cycles 805-825m', 'Nb cycles 825-845m', 'Nb cycles 845-850m',
               'Nb cycles 850-855m', 'Nb cycles 855-875m', 'Nb cycles 875-895m', 'Nb cycles 895-900m',
               'Nb cycles 900-905m', 'Nb cycles 905-925m', 'Nb cycles 925-945m', 'Nb cycles 945-950m',
               'Nb cycles 950-955m', 'Nb cycles 955-975m', 'Nb cycles 975-995m', 'Nb cycles 995-1000m',
               'Nb cycles 1000-1005m', 'Nb cycles 1005-1025m', 'Nb cycles 1025-1045m', 'Nb cycles 1045-1050m',
               'Nb cycles 1050-1055m', 'Nb cycles 1055-1075m', 'Nb cycles 1075-1095m', 'Nb cycles 1095-1100m',
               'Nb cycles 1100-1105m', 'Nb cycles 1105-1125m', 'Nb cycles 1125-1145m', 'Nb cycles 1145-1150m',
               'Nb cycles 1150-1155m', 'Nb cycles 1155-1175m', 'Nb cycles 1175-1195m', 'Nb cycles 1195-1200m',
               'Nb cycles 1200-1205m', 'Nb cycles 1205-1225m', 'Nb cycles 1225-1245m', 'Nb cycles 1245-1250m',
               'Nb cycles 1250-1255m', 'Nb cycles 1255-1275m', 'Nb cycles 1275-1295m', 'Nb cycles 1295-1300m',
               'Nb cycles 1300-1305m', 'Nb cycles 1305-1325m', 'Nb cycles 1325-1345m', 'Nb cycles 1345-1350m',
               'Nb cycles 1350-1355m', 'Nb cycles 1355-1375m', 'Nb cycles 1375-1395m', 'Nb cycles 1395-1400m',
               'Nb cycles 1400-1405m', 'Nb cycles 1405-1425m', 'Nb cycles 1425-1445m', 'Nb cycles 1445-1450m',
               'Nb cycles 1450-1455m', 'Nb cycles 1455-1475m', 'Nb cycles 1475-1495m', 'Nb cycles 1495-1500m']
        dff = dff.loc[dff.distance_course.isin([400,800,1500])].reset_index(drop=True)
        series_temps = dff['TEMPS_SECTION'].str.split(';', expand=True)
        series_vitesse = dff['VITESSE'].str.split(';', expand=True)
        series_cycles = dff['NB_CYCLE'].str.split(';', expand=True)
        df_sep_temps = pd.DataFrame({col_temps[i]: series_temps[i] for i in range(len(col_temps))})
        df_sep_vitesse = pd.DataFrame({col_vitesse[i]: series_vitesse[i] for i in range(len(col_vitesse))})
        df_sep_cycles = pd.DataFrame({col_nb_cycles[i]: series_cycles[i] for i in range(len(col_nb_cycles))})
        dff = pd.concat([dff, df_sep_temps, df_sep_vitesse, df_sep_cycles], axis=1)
        dff = dff.loc[dff.distance_course == distance]
        dff = dff.dropna(axis=1, how='all')

        for colonne in dff.columns:
            if colonne.startswith('Temps'):
                dff[str(colonne)] = dff[str(colonne)].apply(lambda x: '{:02d}:{:05.2f}'.format(int(float(x) // 60), float(x) % 60))

    return dff

# Fonction df_freq_ampl
def df_freq_ampl(df, distance):
    dff = df.copy()
    dff['temps_final'] = dff['temps_final'].apply(lambda x: '{:02d}:{:05.2f}'.format(int(float(x) // 60), float(x) % 60))
    freq = ['Freq 25m', 'Freq 50m', 'Freq 75m', 'Freq 100m',
            'Freq 125m', 'Freq 150m', 'Freq 175m', 'Freq 200m',
            'Freq 225m', 'Freq 250m', 'Freq 275m', 'Freq 300m',
            'Freq 325m', 'Freq 350m', 'Freq 375m', 'Freq 400m',
            'Freq 425m', 'Freq 450m', 'Freq 475m', 'Freq 500m',
            'Freq 525m', 'Freq 550m', 'Freq 575m', 'Freq 600m',
            'Freq 625m', 'Freq 650m', 'Freq 675m', 'Freq 700m',
            'Freq 725m', 'Freq 750m', 'Freq 775m', 'Freq 800m',
            'Freq 825m', 'Freq 850m', 'Freq 875m', 'Freq 900m',
            'Freq 925m', 'Freq 950m', 'Freq 975m', 'Freq 1000m',
            'Freq 1025m', 'Freq 1050m', 'Freq 1075m', 'Freq 1100m',
            'Freq 1125m', 'Freq 1150m', 'Freq 1175m', 'Freq 1200m',
            'Freq 1225m', 'Freq 1250m', 'Freq 1275m', 'Freq 1300m',
            'Freq 1325m', 'Freq 1350m', 'Freq 1375m', 'Freq 1400m',
            'Freq 1425m', 'Freq 1450m', 'Freq 1475m', 'Freq 1500m']

    ampl = ['Ampl 25m', 'Ampl 50m', 'Ampl 75m', 'Ampl 100m',
            'Ampl 125m', 'Ampl 150m', 'Ampl 175m', 'Ampl 200m',
            'Ampl 225m', 'Ampl 250m', 'Ampl 275m', 'Ampl 300m',
            'Ampl 325m', 'Ampl 350m', 'Ampl 375m', 'Ampl 400m',
            'Ampl 425m', 'Ampl 450m', 'Ampl 475m', 'Ampl 500m',
            'Ampl 525m', 'Ampl 550m', 'Ampl 575m', 'Ampl 600m',
            'Ampl 625m', 'Ampl 650m', 'Ampl 675m', 'Ampl 700m',
            'Ampl 725m', 'Ampl 750m', 'Ampl 775m', 'Ampl 800m',
            'Ampl 825m', 'Ampl 850m', 'Ampl 875m', 'Ampl 900m',
            'Ampl 925m', 'Ampl 950m', 'Ampl 975m', 'Ampl 1000m',
            'Ampl 1025m', 'Ampl 1050m', 'Ampl 1075m', 'Ampl 1100m',
            'Ampl 1125m', 'Ampl 1150m', 'Ampl 1175m', 'Ampl 1200m',
            'Ampl 1225m', 'Ampl 1250m', 'Ampl 1275m', 'Ampl 1300m',
            'Ampl 1325m', 'Ampl 1350m', 'Ampl 1375m', 'Ampl 1400m',
            'Ampl 1425m', 'Ampl 1450m', 'Ampl 1475m', 'Ampl 1500m']

    tempo = ['Tempo 25m', 'Tempo 50m', 'Tempo 75m', 'Tempo 100m',
            'Tempo 125m', 'Tempo 150m', 'Tempo 175m', 'Tempo 200m',
            'Tempo 225m', 'Tempo 250m', 'Tempo 275m', 'Tempo 300m',
            'Tempo 325m', 'Tempo 350m', 'Tempo 375m', 'Tempo 400m',
            'Tempo 425m', 'Tempo 450m', 'Tempo 475m', 'Tempo 500m',
            'Tempo 525m', 'Tempo 550m', 'Tempo 575m', 'Tempo 600m',
            'Tempo 625m', 'Tempo 650m', 'Tempo 675m', 'Tempo 700m',
            'Tempo 725m', 'Tempo 750m', 'Tempo 775m', 'Tempo 800m',
            'Tempo 825m', 'Tempo 850m', 'Tempo 875m', 'Tempo 900m',
            'Tempo 925m', 'Tempo 950m', 'Tempo 975m', 'Tempo 1000m',
            'Tempo 1025m', 'Tempo 1050m', 'Tempo 1075m', 'Tempo 1100m',
            'Tempo 1125m', 'Tempo 1150m', 'Tempo 1175m', 'Tempo 1200m',
            'Tempo 1225m', 'Tempo 1250m', 'Tempo 1275m', 'Tempo 1300m',
            'Tempo 1325m', 'Tempo 1350m', 'Tempo 1375m', 'Tempo 1400m',
            'Tempo 1425m', 'Tempo 1450m', 'Tempo 1475m', 'Tempo 1500m']

    series_freq = dff['FREQUENCE'].str.split(';', expand=True)
    series_ampl = dff['AMPLITUDE'].str.split(';', expand=True)
    series_tempo = dff['TEMPO'].str.split(';', expand=True)
    df_sep_freq = pd.DataFrame({freq[i]: series_freq[i] for i in range(len(freq))})
    df_sep_ampl = pd.DataFrame({ampl[i]: series_ampl[i] for i in range(len(ampl))})
    df_sep_tempo = pd.DataFrame({tempo[i]: series_tempo[i] for i in range(len(tempo))})
    dff = pd.concat([dff, df_sep_freq, df_sep_ampl, df_sep_tempo], axis=1)
    dff = dff.loc[dff.distance_course == distance]
    dff = dff.dropna(axis=1, how='all')

    return dff


def lien_frequence_amplitude_vitesse(id_analyse, distance):
    df_vitesse = df_section_init.copy()
    df_vitesse = df_par_sections(df_vitesse, distance)
    df_vitesse = df_vitesse.loc[df_vitesse.id_analyse.isin([id_analyse])]
    df_frequence_amplitude = df_section_init.copy()
    df_frequence_amplitude = df_freq_ampl(df_frequence_amplitude, distance)
    df_frequence_amplitude = df_frequence_amplitude.loc[df_frequence_amplitude.id_analyse.isin([id_analyse])]
    if distance == 50 :
        df_frequence_amplitude = df_frequence_amplitude.rename(columns={'Freq 25m': 'Freq 15-25m', 'Freq 50m': 'Freq 25-45m',
                                                                        'Ampl 25m' : 'Ampl 15-25m', 'Ampl 50m':'Ampl 25-45m'})
    if distance == 100 :
        df_frequence_amplitude = df_frequence_amplitude.rename(columns={'Freq 25m': 'Freq 15-25m', 'Freq 50m': 'Freq 25-45m', 'Freq 75m': 'Freq 65-75m', 'Freq 100m': 'Freq 75-95m',
                                                                    'Ampl 25m' : 'Ampl 15-25m', 'Ampl 50m':'Ampl 25-45m', 'Ampl 75m': 'Ampl 65-75m', 'Ampl 100m': 'Ampl 75-95m'})
    if distance == 200 :
        df_frequence_amplitude = df_frequence_amplitude.rename(columns={'Freq 25m': 'Freq 15-25m', 'Freq 50m': 'Freq 25-45m', 'Freq 75m': 'Freq 65-75m', 'Freq 100m': 'Freq 75-95m', 'Freq 125m': 'Freq 115-125m', 'Freq 150m': 'Freq 125-145m', 'Freq 175m': 'Freq 165-175m', 'Freq 200m': 'Freq 175-195m',
                                                                    'Ampl 25m' : 'Ampl 15-25m', 'Ampl 50m':'Ampl 25-45m', 'Ampl 75m': 'Ampl 65-75m', 'Ampl 100m': 'Ampl 75-95m', 'Ampl 125m': 'Ampl 115-125m', 'Ampl 150m': 'Ampl 125-145m', 'Ampl 175m': 'Ampl 165-175m', 'Ampl 200m': 'Ampl 175-195m'})
    if distance == 400 :
        df_frequence_amplitude = df_frequence_amplitude.rename(columns={'Freq 25m': 'Freq 15-25m', 'Freq 50m': 'Freq 25-45m', 'Freq 75m': 'Freq 55-75m', 'Freq 100m': 'Freq 75-95m', 'Freq 125m': 'Freq 105-125m', 'Freq 150m': 'Freq 125-145m', 'Freq 175m': 'Freq 155-175m', 'Freq 200m': 'Freq 175-195m', 'Freq 225m': 'Freq 205-225m', 'Freq 250m': 'Freq 225-245m', 'Freq 275m': 'Freq 255-275m', 'Freq 300m': 'Freq 275-295m', 'Freq 325m': 'Freq 305-325m', 'Freq 350m': 'Freq 325-345m', 'Freq 375m': 'Freq 355-375m', 'Freq 400m': 'Freq 375-395m',
                                                                    'Ampl 25m' : 'Ampl 15-25m', 'Ampl 50m':'Ampl 25-45m', 'Ampl 75m': 'Ampl 55-75m', 'Ampl 100m': 'Ampl 75-95m', 'Ampl 125m': 'Ampl 105-125m', 'Ampl 150m': 'Ampl 125-145m', 'Ampl 175m': 'Ampl 155-175m', 'Ampl 200m': 'Ampl 175-195m', 'Ampl 225m': 'Ampl 205-225m', 'Ampl 250m': 'Ampl 225-245m', 'Ampl 275m': 'Ampl 255-275m', 'Ampl 300m': 'Ampl 275-295m', 'Ampl 325m': 'Ampl 305-325m', 'Ampl 350m': 'Ampl 325-345m', 'Ampl 375m': 'Ampl 355-375m', 'Ampl 400m': 'Ampl 375-395m',})
    if distance == 800 :
        df_frequence_amplitude = df_frequence_amplitude.rename(columns={'Freq 25m': 'Freq 15-25m', 'Freq 50m': 'Freq 25-45m', 'Freq 75m': 'Freq 55-75m', 'Freq 100m': 'Freq 75-95m', 'Freq 125m': 'Freq 105-125m', 'Freq 150m': 'Freq 125-145m', 'Freq 175m': 'Freq 155-175m', 'Freq 200m': 'Freq 175-195m', 'Freq 225m': 'Freq 205-225m', 'Freq 250m': 'Freq 225-245m', 'Freq 275m': 'Freq 255-275m', 'Freq 300m': 'Freq 275-295m', 'Freq 325m': 'Freq 305-325m', 'Freq 350m': 'Freq 325-345m', 'Freq 375m': 'Freq 355-375m', 'Freq 400m': 'Freq 375-395m', 'Freq 425m': 'Freq 405-425m', 'Freq 450m': 'Freq 425-445m', 'Freq 475m': 'Freq 455-475m', 'Freq 500m': 'Freq 475-495m', 'Freq 525m': 'Freq 505-525m', 'Freq 550m': 'Freq 525-545m', 'Freq 575m': 'Freq 555-575m', 'Freq 600m': 'Freq 575-595m', 'Freq 625m': 'Freq 605-625m', 'Freq 650m': 'Freq 625-645m', 'Freq 675m': 'Freq 655-675m', 'Freq 700m': 'Freq 675-695m', 'Freq 725m': 'Freq 705-725m', 'Freq 750m': 'Freq 725-745m', 'Freq 775m': 'Freq 755-775m', 'Freq 800m': 'Freq 775-795m',
                                                                    'Ampl 25m' : 'Ampl 15-25m', 'Ampl 50m':'Ampl 25-45m', 'Ampl 75m': 'Ampl 55-75m', 'Ampl 100m': 'Ampl 75-95m', 'Ampl 125m': 'Ampl 105-125m', 'Ampl 150m': 'Ampl 125-145m', 'Ampl 175m': 'Ampl 155-175m', 'Ampl 200m': 'Ampl 175-195m', 'Ampl 225m': 'Ampl 205-225m', 'Ampl 250m': 'Ampl 225-245m', 'Ampl 275m': 'Ampl 255-275m', 'Ampl 300m': 'Ampl 275-295m', 'Ampl 325m': 'Ampl 305-325m', 'Ampl 350m': 'Ampl 325-345m', 'Ampl 375m': 'Ampl 355-375m', 'Ampl 400m': 'Ampl 375-395m', 'Ampl 425m': 'Ampl 405-425m', 'Ampl 450m': 'Ampl 425-445m', 'Ampl 475m': 'Ampl 455-475m', 'Ampl 500m': 'Ampl 475-495m', 'Ampl 525m': 'Ampl 505-525m', 'Ampl 550m': 'Ampl 525-545m', 'Ampl 575m': 'Ampl 555-575m', 'Ampl 600m': 'Ampl 575-595m', 'Ampl 625m': 'Ampl 605-625m', 'Ampl 650m': 'Ampl 625-645m', 'Ampl 675m': 'Ampl 655-675m', 'Ampl 700m': 'Ampl 675-695m', 'Ampl 725m': 'Ampl 705-725m', 'Ampl 750m': 'Ampl 725-745m', 'Ampl 775m': 'Ampl 755-775m', 'Ampl 800m': 'Ampl 775-795m',})

    if distance == 1500 :
        df_frequence_amplitude = df_frequence_amplitude.rename(columns={'Freq 25m': 'Freq 15-25m', 'Freq 50m': 'Freq 25-45m', 'Freq 75m': 'Freq 55-75m', 'Freq 100m': 'Freq 75-95m', 'Freq 125m': 'Freq 105-125m', 'Freq 150m': 'Freq 125-145m', 'Freq 175m': 'Freq 155-175m', 'Freq 200m': 'Freq 175-195m', 'Freq 225m': 'Freq 205-225m', 'Freq 250m': 'Freq 225-245m', 'Freq 275m': 'Freq 255-275m', 'Freq 300m': 'Freq 275-295m', 'Freq 325m': 'Freq 305-325m', 'Freq 350m': 'Freq 325-345m', 'Freq 375m': 'Freq 355-375m', 'Freq 400m': 'Freq 375-395m', 'Freq 425m': 'Freq 405-425m', 'Freq 450m': 'Freq 425-445m', 'Freq 475m': 'Freq 455-475m', 'Freq 500m': 'Freq 475-495m', 'Freq 525m': 'Freq 505-525m', 'Freq 550m': 'Freq 525-545m', 'Freq 575m': 'Freq 555-575m', 'Freq 600m': 'Freq 575-595m', 'Freq 625m': 'Freq 605-625m', 'Freq 650m': 'Freq 625-645m', 'Freq 675m': 'Freq 655-675m', 'Freq 700m': 'Freq 675-695m', 'Freq 725m': 'Freq 705-725m', 'Freq 750m': 'Freq 725-745m', 'Freq 775m': 'Freq 755-775m', 'Freq 800m': 'Freq 775-795m',
                                                                        'Freq 825m': 'Freq 805-825m', 'Freq 850m': 'Freq 825-845m', 'Freq 875m': 'Freq 855-875m', 'Freq 900m': 'Freq 875-895m', 'Freq 925m': 'Freq 905-925m', 'Freq 950m': 'Freq 925-945m', 'Freq 975m': 'Freq 955-975m', 'Freq 1000m': 'Freq 975-995m', 'Freq 1025m': 'Freq 1005-1025m', 'Freq 1050m': 'Freq 1025-1045m', 'Freq 1075m': 'Freq 1055-1075m', 'Freq 1100m': 'Freq 1075-1095m', 'Freq 1125m': 'Freq 1105-1125m', 'Freq 1150m': 'Freq 1125-1145m', 'Freq 1175m': 'Freq 1155-1175m', 'Freq 1200m': 'Freq 1175-1195m', 'Freq 1225m': 'Freq 1205-1225m', 'Freq 1250m': 'Freq 1225-1245m', 'Freq 1275m': 'Freq 1255-1275m', 'Freq 1300m': 'Freq 1275-1295m', 'Freq 1325m': 'Freq 1305-1325m', 'Freq 1350m': 'Freq 1325-1345m', 'Freq 1375m': 'Freq 1355-1375m', 'Freq 1400m': 'Freq 1375-1395m', 'Freq 1425m': 'Freq 1405-1425m', 'Freq 1450m': 'Freq 1425-1445m', 'Freq 1475m': 'Freq 1455-1475m', 'Freq 1500m': 'Freq 1475-1495m',
                                                                        'Ampl 25m' : 'Ampl 15-25m', 'Ampl 50m':'Ampl 25-45m', 'Ampl 75m': 'Ampl 55-75m', 'Ampl 100m': 'Ampl 75-95m', 'Ampl 125m': 'Ampl 105-125m', 'Ampl 150m': 'Ampl 125-145m', 'Ampl 175m': 'Ampl 155-175m', 'Ampl 200m': 'Ampl 175-195m', 'Ampl 225m': 'Ampl 205-225m', 'Ampl 250m': 'Ampl 225-245m', 'Ampl 275m': 'Ampl 255-275m', 'Ampl 300m': 'Ampl 275-295m', 'Ampl 325m': 'Ampl 305-325m', 'Ampl 350m': 'Ampl 325-345m', 'Ampl 375m': 'Ampl 355-375m', 'Ampl 400m': 'Ampl 375-395m', 'Ampl 425m': 'Ampl 405-425m', 'Ampl 450m': 'Ampl 425-445m', 'Ampl 475m': 'Ampl 455-475m', 'Ampl 500m': 'Ampl 475-495m', 'Ampl 525m': 'Ampl 505-525m', 'Ampl 550m': 'Ampl 525-545m', 'Ampl 575m': 'Ampl 555-575m', 'Ampl 600m': 'Ampl 575-595m', 'Ampl 625m': 'Ampl 605-625m', 'Ampl 650m': 'Ampl 625-645m', 'Ampl 675m': 'Ampl 655-675m', 'Ampl 700m': 'Ampl 675-695m', 'Ampl 725m': 'Ampl 705-725m', 'Ampl 750m': 'Ampl 725-745m', 'Ampl 775m': 'Ampl 755-775m', 'Ampl 800m': 'Ampl 775-795m',
                                                                        'Ampl 825m': 'Ampl 805-825m', 'Ampl 850m': 'Ampl 825-845m', 'Ampl 875m': 'Ampl 855-875m', 'Ampl 900m': 'Ampl 875-895m', 'Ampl 925m': 'Ampl 905-925m', 'Ampl 950m': 'Ampl 925-945m', 'Ampl 975m': 'Ampl 955-975m', 'Ampl 1000m': 'Ampl 975-995m', 'Ampl 1025m': 'Ampl 1005-1025m', 'Ampl 1050m': 'Ampl 1025-1045m', 'Ampl 1075m': 'Ampl 1055-1075m', 'Ampl 1100m': 'Ampl 1075-1095m', 'Ampl 1125m': 'Ampl 1105-1125m', 'Ampl 1150m': 'Ampl 1125-1145m', 'Ampl 1175m': 'Ampl 1155-1175m', 'Ampl 1200m': 'Ampl 1175-1195m', 'Ampl 1225m': 'Ampl 1205-1225m', 'Ampl 1250m': 'Ampl 1225-1245m', 'Ampl 1275m': 'Ampl 1255-1275m', 'Ampl 1300m': 'Ampl 1275-1295m', 'Ampl 1325m': 'Ampl 1305-1325m', 'Ampl 1350m': 'Ampl 1325-1345m', 'Ampl 1375m': 'Ampl 1355-1375m', 'Ampl 1400m': 'Ampl 1375-1395m', 'Ampl 1425m': 'Ampl 1405-1425m', 'Ampl 1450m': 'Ampl 1425-1445m', 'Ampl 1475m': 'Ampl 1455-1475m', 'Ampl 1500m': 'Ampl 1475-1495m'})
    # Définir le nom des colonnes et leur type
    colonnes = ['ID analyse', 'Nom Analyse', 'Nom et prénom', 'Sexe', 'Nom compétition', 'Date', 'Distance de la course', 'Epreuve', 'Style', 'Temps final', 'Section', 'Vitesse moyenne', 'Fréquence moyenne', 'Amplitude moyenne']
    types = [str, str, str, str, str, str, int, str, str, str, str, float, float, float]

    # Colonnes du DataFrame existant qui commencent par 'Vitesse'
    colonnes_vitesse = [colonne for colonne in df_vitesse.columns if colonne.startswith('Vitesse')]
    print(colonnes_vitesse)
    # Créer un dictionnaire vide avec des listes vides pour chaque colonne
    donnees_vides = {colonne: [] for colonne in colonnes}

    # Créer le DataFrame vide en spécifiant le nom des colonnes
    df_2 = pd.DataFrame(donnees_vides)

    # Ajouter les lignes au DataFrame vide
    df_2 = pd.concat([df_2] * len(colonnes_vitesse), ignore_index=True)

    # Remplir la colonne 'Section' avec les chaînes de caractères après 'Vitesse' dans le DataFrame existant
    df_2['Section'] = [colonne.split(' ')[1:] for colonne in colonnes_vitesse]
    df_2['Section'] = df_2['Section'].apply(lambda x: x[0] if x else '')
    # Listes de colonnes à répéter
    colonnes_a_repeter = ['ID analyse', 'Nom Analyse', 'Nom et prénom', 'Sexe', 'Nom compétition', 'Date', 'Distance de la course', 'Epreuve', 'Style', 'Temps final']
    colonnes_source = ['id_analyse', 'nom_analyse', 'nom_prenom', 'nageur_sexe', 'competition_nom', 'mois_annee', 'distance_course', 'style_nage','round_name', 'temps_final']

    # Répéter les valeurs pour les colonnes spécifiées
    for col_df_2, col_source in zip(colonnes_a_repeter, colonnes_source):
        df_2[col_df_2] = df_vitesse[col_source].tolist() * len(df_2)

    sections_a_enlever_before_400 = ['0-15m'] + [f'{i}-{i+5}m' for i in range(50, distance, 50)] + [f'{i+5}-{i+15}m' for i in range(50, distance, 50)] + [f'{i-5}-{i}m' for i in range(50, distance + 50, 50)]
    sections_a_enlever_from_400 = ['0-15m'] +[f'{i}-{i+5}m' for i in range(50, distance, 50)] + [f'{i-5}-{i}m' for i in range(50, distance + 50, 50)]
    print('sections',sections_a_enlever_from_400)
    for i in range(0, df_2.shape[0]):
        section = df_2.loc[i, 'Section']
        if distance == 50 or distance == 100 or distance == 200:
            if section in sections_a_enlever_before_400:
                df_2.drop(i, inplace=True)
        if distance == 400 or distance == 800 or distance == 1500:
            if section in sections_a_enlever_from_400:
                df_2.drop(i, inplace=True)
    df_2.reset_index(drop=True, inplace=True)

    df_vitesse = df_vitesse.set_index('id_analyse')
    # Boucle pour remplir la colonne 'Vitesse moyenne' de df_2
    for index, row in df_2.iterrows():
        id_analyse = row['ID analyse']
        section = row['Section']
        vitesse_col = 'Vitesse ' + section  # construire le nom de la colonne dans df_section
        vitesse_moyenne = df_vitesse.at[id_analyse, vitesse_col]  # récupérer la valeur de df_section
        df_2.at[index, 'Vitesse moyenne'] = vitesse_moyenne


    df_frequence_amplitude = df_frequence_amplitude.set_index('id_analyse')

    # Boucle pour remplir la colonne 'Fréquence moyenne' de df_2
    for index, row in df_2.iterrows():
        id_analyse = row['ID analyse']
        section = row['Section']
        frequence_col = 'Freq ' + section  # construire le nom de la colonne dans df_section
        frequence_moyenne = df_frequence_amplitude.at[id_analyse, frequence_col]  # récupérer la valeur de df_section
        df_2.at[index, 'Fréquence moyenne'] = frequence_moyenne


    # Boucle pour remplir la colonne 'Amplitude moyenne' de df_2
    for index, row in df_2.iterrows():
        id_analyse = row['ID analyse']
        section = row['Section']
        amplitude_col = 'Ampl ' + section  # construire le nom de la colonne dans df_section
        amplitude_moyenne = df_frequence_amplitude.at[id_analyse, amplitude_col]  # récupérer la valeur de df_section
        df_2.at[index, 'Amplitude moyenne'] = amplitude_moyenne
    return(df_2)


def comparer_noms(nom):
    return nom.split()

card_carac_event_section = dbc.Card(
    dbc.CardBody(
        [
            html.H4([DashIconify(icon="pajamas:timer", style={"marginRight": 10}), "Sélection de l'épreuve"], className="text-nowrap"),
            html.Div("Choisissez l'épreuve que vous souhaitez parcourir. Si un menu déroulant est laissé vide, la base de données ne sera pas filtrée en fonction de la valeur de ce menu."),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(id='distance-course-section-dropdown',
                    options=[{'label': k, 'value': k} for k in sorted(df_section_init.distance_course.unique())],
                    multi=False,
                    placeholder='Distance'),
                ], width=5),
                dbc.Col([
                    dcc.Dropdown(id='style-nage-section-dropdown',
                    options=[{'label': k, 'value': k} for k in sorted(df_section_init.style_nage.unique())],
                    multi=True,
                    placeholder='Style de nage'),
                ], width=7),
            ], justify='center'),

            html.Br(),

            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(id='competition-nom-section-dropdown',
                    options=[{'label': k, 'value': k} for k in sorted(df_section_init.competition_nom.unique())],
                    multi=True,
                    placeholder='Compétition'),
                ], width=8),


                dbc.Col([
                    dcc.Dropdown(id='round-name-section-dropdown',
                    options=[{'label': k, 'value': k} for k in sorted(df_section_init.round_name.unique())],
                    multi=True,
                    placeholder='Epreuve'),
                ], width=4),
            ], justify='center')
        ], className="border-start border-dark border-5"
    ), style={"width": "50rem","background":"paleturquoise"},
    className="text-center m-4 ml-3"
)

card_carac_swimmer_section = dbc.Card(
    dbc.CardBody(
        [
            html.H4([DashIconify(icon="fa-solid:swimmer", style={"marginRight": 10}), "Sélection du nageur"], className="text-nowrap"),
            html.Div("Choisissez le sexe et / ou le patronyme que vous souhaitez parcourir. La sélection multiple est possible. Si un menu déroulant est laissé vide, la base de données ne sera pas filtrée en fonction de la valeur de ce menu."),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(id='sexe-section-dropdown',
                    options=[{'label': k, 'value': k} for k in sorted(df_section_init.nageur_sexe.unique())],
                    multi=True,
                    placeholder='Sexe'),
                ], width=4),
                dbc.Col([
                    dcc.Dropdown(id='nom-prenom-section-dropdown',
                    options=[{'label': k, 'value': k} for k in pd.Series(sorted((df_section_init['nom_prenom']), key=comparer_noms)).unique()],
                    multi=True,
                    placeholder='Nom et prénom',
                    className="mb-3"),
                ], width=8)
            ]),
        ], className="border-start border-dark border-5"
    ), style={"width": "40rem","background": "turquoise"},
    className="text-center m-4 ml-3"
)

####################### Layout ######################
layout = dbc.Container([
    dbc.Row([
        # dbc.Col([
        #     html.H2(children='')
        # ], width={"size": 1, "offset": 0}, style={"fontSize": 30, "backgroundColor": "black"}),

        dbc.Col(
                html.H1([DashIconify(icon="ri:pin-distance-fill",style={"marginRight": 30}),'Parcourir les données par section']),
                width={"size": 'auto', "offset": 1}, style={"fontSize": 30, "textAlign": 'center'}
            ),

        # dbc.Col([
        #     html.H2(children='')
        # ], width={"size": 1, "offset": 0}, style={"fontSize": 30, "backgroundColor": "black"}),
    ]),

    dbc.Row([
        dbc.Col([card_carac_event_section], width={'size': 9, 'offset': 1}),
    ]),

    dbc.Row([
        dbc.Col([card_carac_swimmer_section], width={'size': 9, 'offset': 2})
    ]),

    html.Hr(style=thicker_hr_style_first_section),

    dbc.Row([
        dbc.Col(
            html.Div([DashIconify(icon="material-symbols:highlight-mouse-cursor", style={"marginRight": 10}), "Sélectionnez le paramètre d'étude par section (variable selon la distance)"], style={"fontSize": 25}),
            width={"size": 12, "offset": 0}, style={"fontSize": 15, "textAlign": 'center'}
        )
    ]),

    dbc.Row([
        dbc.Col([
            dcc.RadioItems(['  Temps', '  Vitesse', '  Nombre de cycles'], '  Temps', inline=True, labelStyle={'margin-right': '100px'}, id = 'variable-section-item')
        ], width={"size": 'auto', "offset": 3})

    ]),

    html.Br(),

    dbc.Row([
        dbc.Col([
            dbc.Button(
            [reset_section_icon, "Actualiser "], id="reset-section-button", className="me-2", n_clicks=0, style={'background-color': "black"}
            ),
        ],  width={"size": 'auto', "offset": 5})
    ]),

    html.Br(),

    dbc.Row([
        dbc.Col(html.Div(id='warning-message-section', style={'color': 'teal', 'fontWeight': 'bold', 'textAlign' : 'center'}), width={"offset": 0})
    ]),

    dcc.Store(id = 'df-stored-section'),

    html.Br(),

    dbc.Row([
        html.Div(dash_table.DataTable(
                columns=[],
                #data=[],
                id='bdd-section',
                page_size=20,
                editable=True,
                row_selectable='multi',
                selected_rows=[],
                style_cell={'textAlign': 'center'},
                style_header={
                    'backgroundColor': 'darkturquoise',
                    'color': 'white',
                    'fontWeight': 'bold'
                },
                style_data={
                    'width': '100px', 'minWidth': '100px', 'maxWidth': '100px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                }
                )),

        # html.Div(id='selected-rows', style={'textAlign': "center"})
        ]
    ),


    html.Br(),

    dbc.Row([
         dbc.Col([
            dbc.Button(
            [selectall_section_icon, "Tout sélectionner "], id="selectall-section-button", className="me-2", n_clicks=0, style={'background-color': 'black'}
            ),
        ],  width={"size": '2', "offset": 0}),
        dbc.Col([
            dbc.Button(
            [deselectall_section_icon, "Tout désélectionner"], id="deselectall-section-button", className="me-2", n_clicks=0, style={'background-color': 'black'}
            ),
        ],  width={"size": '2', "offset": 0}),
        dbc.Col([
            dbc.Button([csv_section_icon, "Télécharger sous format .csv"], id="btn_csv_section", style={'background-color': color_first_section}),
            dcc.Download(id="download-dataframe-section-csv"),
        ], width={"size": '3', "offset": 1}),
        dbc.Col([
            dbc.Button([excel_section_icon, "Télécharger sous format .xlsx"], id="btn_excel_section", style={'background-color': color_first_section}),
            dcc.Download(id="download-dataframe-section-csv"),
        ],  width={"size": '3', "offset": 0}),
    ]),

    html.Br(),

    dbc.Row([
        dbc.Col([
            dbc.Button(
            [graph_section_icon, "Mettre à jour le graphique"], id="reset-graph-section-button", className="me-2", n_clicks=0, style={'background-color': "black"}
            ),
        ],  width={"size": 'auto', "offset": 4})
    ]),

    html.Br(),

    dbc.Row([
        dbc.Col([
            dcc.Graph(figure={}, id='graph-par-section')
        ])
    ]),

    html.Br(),

    html.Hr(style=thicker_hr_style_second_section),

    dbc.Row([
        dbc.Col(
            html.Div([DashIconify(icon="material-symbols:highlight-mouse-cursor", style={"marginRight": 10}), "Sélectionnez le paramètre d'étude par 25m"], style={"fontSize": 25}),
            width={"size": 12, "offset": 0}, style={"fontSize": 15, "textAlign": 'center'}
        )
    ]),

    dbc.Row([
        dbc.Col([
            dcc.RadioItems(['  Fréquence', '  Tempo', '  Amplitude'], '  Fréquence', inline=True, labelStyle={'margin-right': '100px'}, id = 'variable-25m-item')
        ], width={"size": 'auto', "offset": 3})

    ]),

    html.Br(),

    dbc.Row([
        dbc.Col([
            dbc.Button(
            [reset_section_icon, "Actualiser "], id="reset-25m-button", className="me-2", n_clicks=0, style={'background-color': "black"}
            ),
        ],  width={"size": 'auto', "offset": 5})
    ]),

    html.Br(),

    dbc.Row([
        dbc.Col(html.Div(id='warning-message-25m', style={'color': 'darkslategray', 'fontWeight': 'bold', 'textAlign' : 'center'}), width={"offset": 0})
    ]),

    html.Br(),

    dcc.Store(id = 'df-stored-25m'),

    dbc.Row([
        html.Div(dash_table.DataTable(
                columns=[],
                #data=[],
                id='bdd-var-par-25m',
                page_size=20,
                editable=True,
                row_selectable='multi',
                selected_rows=[],
                style_cell={'textAlign': 'center'},
                style_header={
                    'backgroundColor': color_second_section,
                    'color': 'white',
                    'fontWeight': 'bold'
                },
                style_data={
                    'width': '100px', 'minWidth': '100px', 'maxWidth': '100px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                }
                )),

        # html.Div(id='selected-rows', style={'textAlign': "center"})
        ]
    ),

    html.Br(),

    dbc.Row([
        dbc.Col([
            dbc.Button(
            [selectall_section_icon, "Tout sélectionner "], id="selectall-25m-button", className="me-2", n_clicks=0, style={'background-color': 'black'}
            ),
        ],  width={"size": '2', "offset": 0}),
        dbc.Col([
            dbc.Button(
            [deselectall_section_icon, "Tout désélectionner"], id="deselectall-25m-button", className="me-2", n_clicks=0, style={'background-color': 'black'}
            ),
        ],  width={"size": '2', "offset": 0}),
        dbc.Col([
            dbc.Button([csv_section_icon, "Télécharger sous format .csv"], id="btn_csv_25m", style={'background-color': color_second_section}),
            dcc.Download(id="download-dataframe-25m-csv"),
        ], width={"size": '3', "offset": 1}),
        dbc.Col([
            dbc.Button([excel_section_icon, "Télécharger sous format .xlsx"], id="btn_excel_25m", style={'background-color': color_second_section}),
            dcc.Download(id="download-dataframe-25m-csv"),
        ],  width={"size": '3', "offset": 0})
    ]),

    html.Br(),

    dbc.Row([
        dbc.Col([
            dbc.Button(
            [graph_section_icon, "Mettre à jour le graphique"], id="reset-graph-25m-button", className="me-2", n_clicks=0, style={'background-color': "black"}
            ),
        ],  width={"size": 'auto', "offset": 4})
    ]),

    html.Br(),

    dbc.Row([
        dbc.Col([
            dcc.Graph(figure={}, id='graph-par-25m')
        ])
    ]),

    html.Br(),

    html.Hr(style=thicker_hr_style_second_section),

    dbc.Row([
        dbc.Col(
            html.Div([DashIconify(icon="bi:table", style={"marginRight": 10}), "Tableau récapitulatif des vitesses, fréquences et amplitudes par section"], style={"fontSize": 25}),
            #html.Div(children=["Tableau récapitulatif des vitesses, fréquences et amplitudes par section"], style={"fontSize": 25}),
            width={"size": 12, "offset": 0}, style={"fontSize": 15, "textAlign": 'center'}
        )
    ]),

    html.Br(),

    dbc.Row([
        dbc.Col(html.Div(id='warning-message-VFA', style={'color': '#005364', 'fontWeight': 'bold', 'textAlign' : 'center'}), width={"offset": 0})
    ]),

    html.Br(),

    dbc.Row([
        dbc.Col([
            dbc.Button(
            [reset_section_icon, "Actualiser "], id="reset-VFA-button", className="me-2", n_clicks=0, style={'background-color': "black"}
            ),
        ],  width={"size": 'auto', "offset": 5})
    ]),

    html.Br(),
    dcc.Store(id = 'df-stored-vitesse-freq-ampl'),

    dbc.Row(
        html.Div(
            id='bdd-vitesse-freq-ampl'
        ),
    ),

    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Button([csv_section_icon, "Télécharger sous format .csv"], id="btn_csv_VFA", style={'background-color': color_third_section}),
            dcc.Download(id="download-dataframe-VFA-csv"),
        ], width={"size": '3', "offset": 3}),
        dbc.Col([
            dbc.Button([excel_section_icon, "Télécharger sous format .xlsx"], id="btn_excel_VFA", style={'background-color': color_third_section}),
            dcc.Download(id="download-dataframe-VFA-csv"),
        ],  width={"size": '3', "offset": 0})

    ])
])

####################### Callbacks ######################
@callback(
    Output('style-nage-section-dropdown', "options"),
    Input('distance-course-section-dropdown', "value"),
    Input('round-name-section-dropdown', "value"),
    Input('nom-prenom-section-dropdown', "value")
)
def update_style_section(distance, round_number, nageur):
    dff = df_section_init.copy()
    if distance:
        dff = dff.loc[dff.distance_course == distance]
    if round_number:
        dff = dff.loc[dff.round_name.isin(round_number)]
    if nageur:
        dff = dff.loc[dff.nom_prenom.isin(nageur)]
    return [{'label': i, 'value': i} for i in sorted(dff.style_nage.unique())]


@callback(
    Output('distance-course-section-dropdown', "options"),
    Input('style-nage-section-dropdown', "value"),
    Input('round-name-section-dropdown', "value"),
    Input('competition-nom-section-dropdown', "value"),
    Input('nom-prenom-section-dropdown', "value")
)
def update_distance_section(style, round_number, compet, nageur):
    dff = df_section_init.copy()
    if style:
        dff = dff.loc[dff.style_nage.isin(style)]
    if round_number:
        dff = dff.loc[dff.round_name.isin(round_number)]
    if compet:
        dff = dff.loc[dff.competition_nom.isin(compet)]
    if nageur:
        dff = dff.loc[dff.nom_prenom.isin(nageur)]
    return [{'label': i, 'value': i} for i in sorted(dff.distance_course.unique())]


@callback(
    Output('competition-nom-section-dropdown', "options"),
    Input('style-nage-section-dropdown', "value"),
    Input('distance-course-section-dropdown', "value"),
    Input('round-name-section-dropdown', "value"),
    Input('nom-prenom-section-dropdown', "value")
)
def update_competition_nom_section(style, distance, round_number, nageur):
    dff = df_section_init.copy()
    if style:
        dff = dff.loc[dff.style_nage.isin(style)]
    if distance:
        dff = dff.loc[dff.distance_course == distance]
    if round_number:
        dff = dff.loc[dff.round_name.isin(round_number)]
    if nageur:
        dff = dff.loc[dff.nom_prenom.isin(nageur)]
    return [{'label': i, 'value': i} for i in sorted(dff.competition_nom.unique())]


@callback(
    Output('round-name-section-dropdown', "options"),
    Input('competition-nom-section-dropdown', "value"),
    Input('distance-course-section-dropdown', "value"),
    Input('style-nage-section-dropdown', "value"),
    Input('nom-prenom-section-dropdown', "value")
)
def update_round_section(competition, distance, style, nageur):
    dff = df_section_init.copy()
    if competition:
        dff = dff.loc[dff.competition_nom.isin(competition)]
    if distance:
        dff = dff.loc[dff.distance_course == distance]
    if style:
        dff = dff.loc[dff.style_nage.isin(style)]
    if nageur:
        dff = dff.loc[dff.nom_prenom.isin(nageur)]
    return [{'label': i, 'value': i} for i in sorted(dff.round_name.unique())]


@callback(
    Output('nom-prenom-section-dropdown', "options"),
    Input('sexe-section-dropdown', "value"),
    Input('distance-course-section-dropdown', "value"),
    Input('style-nage-section-dropdown', "value"),
    Input('competition-nom-section-dropdown', "value"),
    Input('round-name-section-dropdown', "value")
)
def update_nom_prenom_section(sexe, distance, style, competition, round):
    dff = df_section_init.copy()
    if sexe:
        dff = dff.loc[dff.nageur_sexe.isin(sexe)]
    if distance:
        dff = dff.loc[dff.distance_course == distance]
    if style:
        dff = dff.loc[dff.style_nage.isin(style)]
    if competition:
        dff = dff.loc[dff.competition_nom.isin(competition)]
    if round:
        dff = dff.loc[dff.round_name.isin(round)]
    return [{'label': i, 'value': i} for i in sorted(dff.nom_prenom.unique())]


@callback(
    Output('warning-message-section',"children"),
    #Output('bdd-var-par-section', "children"),
    Output('bdd-section', "data"),
    Output('df-stored-section', "data"),
    Input('distance-course-section-dropdown', "value"),
    Input('style-nage-section-dropdown', "value"),
    Input('competition-nom-section-dropdown', "value"),
    Input('round-name-section-dropdown', "value"),
    Input('sexe-section-dropdown', "value"),
    Input('nom-prenom-section-dropdown', "value"),
    Input('variable-section-item', "value"),
    Input('reset-section-button', "n_clicks"),
)

def display_bdd_var_par_section(distance_c, style, competition, round, sexe, nom, variable, btn_reset_clicks):
    warning = "ATTENTION : soit vous n'avez pas sélectionné d'épreuve pour le moment, soit vous n'avez pas actualisé après avoir changé le paramètre d'étude. N'oubliez pas d'actualiser pour tenir compte des changements opérés."
    dff = pd.DataFrame()
    dff_store = pd.DataFrame().to_dict('records')
    if "reset-section-button" in ctx.triggered[0]['prop_id']:
        if distance_c:
            warning = ''
            dff = df_section_init.copy()
            dff = df_par_sections(dff, int(distance_c))
            dff = dff.loc[dff.distance_course == distance_c]
            if style:
                dff = dff.loc[dff.style_nage.isin(style)]

            if competition:
                dff = dff.loc[dff.competition_nom.isin(competition)]

            if round:
                dff = dff.loc[dff.round_name.isin(round)]

            if sexe:
                dff = dff.loc[dff.nageur_sexe.isin(sexe)]

            if nom:
                dff = dff.loc[dff.nom_prenom.isin(nom)]

            if variable == '  Temps':
                for colonne in dff.columns:
                    if colonne.startswith('Vitesse') | colonne.startswith('Nb cycles'):
                        dff = dff.drop(colonne, axis=1)

            if variable == '  Vitesse':
                for colonne in dff.columns:
                    if colonne.startswith('Temps') | colonne.startswith('Nb cycles'):
                        dff = dff.drop(colonne, axis=1)

            if variable == '  Nombre de cycles':
                for colonne in dff.columns:
                    if colonne.startswith('Temps') | colonne.startswith('Vitesse'):
                        dff = dff.drop(colonne, axis=1)


            liste_col = ['id_analyse', 'competition_nom', 'distance_course', 'style_nage', 'round_name', 'TEMPS_SECTION', 'VITESSE', 'NB_CYCLE',
                            'FREQUENCE', 'TEMPO', 'AMPLITUDE']
            dff = dff.drop(columns = liste_col, axis=1)

            dff = dff.rename(columns={'nom_analyse': 'ID complet (distance, nage, épreuve, compétition)',
                                    'nom_prenom' : 'Nom & prénom du nageur', 'nageur_sexe': 'Sexe', 'mois_annee': 'Date',
                                    'temps_final': 'Temps final', 'temps_reaction': 'Temps réaction',
                                    'temps_depart': 'Temps départ', 'temps_vol': 'Temps vol'})

            liste_round = ['Temps vol', 'Temps réaction', 'Temps départ']
            for col in liste_round:
                dff[col] = dff[col].astype(float).round(2)

            dff = dff.sort_values(by='Temps final', ascending=True)

            dff_store = dff.copy()
            dff_store['index'] = dff_store.index
            dff_store = dff_store.to_dict('records')

            return (warning, dff_store, dff_store)
        else:
            warning = 'ATTENTION : Veuillez au moins sélectionner une distance.'
            dff_store = df_section_init.to_dict('records')

    return(warning, dff_store, dff_store)


@callback(
    Output('bdd-section', 'columns'),
    [Input('df-stored-section', 'data')],
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
    Output('selected-rows', 'children'),
    [Input('bdd-section', 'selected_rows'),
     Input('reset-graph-section-button', "n_clicks"),
     Input('selectall-section-button', "n_clicks")],
     Input('deselectall-section-button', "n_clicks"),
    [State('bdd-section', 'data')],
)
def display_selected_rows(selected_rows, btn_reset, btn_selectall, data):
    if "reset-graph-section-button" in ctx.triggered[0]['prop_id']:
        if selected_rows:
            indices = [row['index'] for i, row in enumerate(data) if i in selected_rows]
            return f"Lignes sélectionnées : {indices}"

        if "selectall-section-button" in ctx.triggered[0]['prop_id']:
            all_rows = list(range(len(data)))
            if "deselectall-section-button" in ctx.triggered[0]['prop_id']:
                all_rows = []
            return all_rows
    else :
        return {}


@callback(
    Output('bdd-section', "selected_rows"),
    Input('selectall-section-button', "n_clicks"),
    Input('deselectall-section-button', "n_clicks"),
    State('bdd-section', 'data')
)
def select_all_rows(n_clicks_select, n_clicks_deselect, data):
    all_rows = []
    if n_clicks_select is not None and n_clicks_select > 0 and n_clicks_select > n_clicks_deselect:
        # Sélectionnez toutes les lignes en utilisant les indices de ligne
        all_rows = list(range(len(data)))

    if n_clicks_deselect is not None and n_clicks_deselect > 0 and n_clicks_deselect >= n_clicks_select:
        all_rows = []
    return all_rows
    # # Si le bouton n'est pas encore cliqué, renvoyez une liste vide
    # return []


@callback(
    Output('graph-par-section', "figure"),
    Input('variable-section-item', "value"),
    Input('bdd-section', "data"),
    Input('bdd-section', "selected_rows"),
    Input('reset-graph-section-button', "n_clicks"),
)

def update_graph(variable, data_stored, selected_rows, btn_reset_clicks):
    data_stored = pd.DataFrame(data_stored)
    if "reset-graph-section-button" in ctx.triggered[0]['prop_id']:
        if variable == '  Vitesse' or variable == '  Nombre de cycles':
            if selected_rows is not None and len(selected_rows) > 0:
                # Obtenez l'indice de la ligne sélectionnée
                # Vous pouvez maintenant utiliser l'indice pour effectuer des opérations spécifiques
                # Par exemple, mettez à jour le graphique avec les données de la ligne sélectionnée
                figure = go.Figure()
                listes_colonnes = {}
                for j, colonne in enumerate((data_stored.iloc[:,7:]).columns):
                    listes_colonnes[j] = []
                for i in range(len(selected_rows)):
                    selected_index = selected_rows[i]
                    row_variable = data_stored.iloc[selected_index,7:]
                    temps_final = data_stored.loc[selected_index, 'Temps final']
                    row_variable = row_variable.drop('index', axis=0)
                    row_variable = pd.DataFrame(row_variable)
                    for j in range(0,(row_variable.shape[1])-1):
                        listes_colonnes[j].append(row_variable.iloc[i,j])
                    vecteur_float = row_variable.astype(float)
                    Y = np.array(vecteur_float).ravel()
                    index = pd.Index(row_variable.T.columns)
                    distances_float = index.str.split('-', expand=True).get_level_values(1).str.replace('m', '').astype(float)
                    df_indiv = pd.DataFrame({'Distance': distances_float,
                                            variable: Y})
                    figure.add_trace(go.Scatter(
                        x = df_indiv['Distance'],
                        y = df_indiv[variable],
                        mode='lines',
                        name=str(temps_final) + ', ' + data_stored.loc[selected_rows[i], 'Nom & prénom du nageur'] + ', ' + data_stored.loc[selected_rows[i], 'ID complet (distance, nage, épreuve, compétition)'],
                        hovertemplate='Distance : %{x}<br>' + variable + ': %{y}'
                    ))

                    figure.update_layout(
                    yaxis_title=variable,
                    xaxis_title='Distance (en mètres)',
                    title=variable + ' en fonction de la distance parcourue',
                    #hovermode="x",
                    legend={'itemsizing': 'constant', 'title_font': {'size': 12}, 'font': {'size': 10}},
                    legend_itemclick="toggleothers",
                )

                return figure
            else :
                return {}

        if variable == '  Temps':
            if selected_rows is not None and len(selected_rows) > 0:
                # Obtenez l'indice de la ligne sélectionnée
                # Vous pouvez maintenant utiliser l'indice pour effectuer des opérations spécifiques
                # Par exemple, mettez à jour le graphique avec les données de la ligne sélectionnée
                figure = go.Figure()
                row_variable = data_stored.iloc[:,8:]
                row_variable = row_variable.drop('index', axis=1)
                for col in row_variable.columns:
                    row_variable[col] = pd.to_datetime(row_variable[col].str.replace('.', ':') + '0', format='%M:%S:%f')
                    # Extraire les parties de temps souhaitées (minutes, secondes, centièmes) en utilisant dt.time
                    durees_time = row_variable[col].dt.time
                    # Convertir à nouveau les durées en format datetime en spécifiant une date fictive
                    date_fictive = datetime.strptime('00:21.00', '%M:%S.%f')
                    row_variable[col] = durees_time.apply(lambda x: datetime.combine(date_fictive, x))

                temp = row_variable.diff(axis=1).iloc[:, 1:]
                temp = temp.applymap(lambda x: x.total_seconds()).astype('float64')
                temp.insert(0, 'Temps 15m', row_variable.iloc[:,0])
                reference_date = pd.Timestamp('1900-01-01')
                temp['Temps 15m'] = (temp['Temps 15m'] - reference_date) / pd.Timedelta(seconds=1)

                for i in range(len(selected_rows)):
                    selected_index = selected_rows[i]
                    row_variable = temp.iloc[selected_index,:]
                    temps_final = data_stored.loc[selected_index, 'Temps final']
                    row_variable = pd.DataFrame(row_variable)
                    vecteur_float = row_variable.astype(float)
                    Y = np.array(vecteur_float).ravel()
                    index = pd.Index(row_variable.T.columns)
                    distances_float = index.str.extract(r'(\d+\.?\d*)').astype(float)
                    distances_float = np.array(distances_float).ravel()
                    df_indiv = pd.DataFrame({'Distance': distances_float,
                                            variable: Y})
                    figure.add_trace(go.Scatter(
                        x = df_indiv['Distance'],
                        y = df_indiv[variable],
                        mode='lines',
                        name=str(temps_final) + ', ' + data_stored.loc[selected_rows[i], 'Nom & prénom du nageur'] + ', ' + data_stored.loc[selected_rows[i], 'ID complet (distance, nage, épreuve, compétition)'],
                        hovertemplate='Distance : %{x}<br>' + variable + ': %{y}'
                    ))

                    figure.update_layout(
                        yaxis_title=variable,
                        xaxis_title='Distance (en mètres)',
                        title=variable + ' en fonction de la distance parcourue',
                        #hovermode="x",
                        legend={'itemsizing': 'constant', 'title_font': {'size': 12}, 'font': {'size': 10}},
                        legend_itemclick="toggleothers",
                )

                return figure
        else:
            return {}
    else:
        return {}



@callback(
    Output("download-dataframe-section-csv", "data"),
    Input("btn_csv_section","n_clicks"),
    Input("btn_excel_section","n_clicks"),
    Input('df-stored-section', "data"),
    prevent_initial_call = True
)

def download_df_section_csv(btn_csv_clicks, btn_excel_clicks, df_stored):
    dff = df_stored.copy()
    dff = pd.DataFrame(dff)
    if "btn_csv_section" == ctx.triggered_id:
        return dcc.send_data_frame(dff.to_csv, "FFN_app_bdd_section.csv")

    if "btn_excel_section" == ctx.triggered_id:
        return dcc.send_data_frame(dff.to_excel, "FFN_app_bdd_section.xlsx", sheet_name="Feuille_1")

@callback(
    Output('warning-message-25m',"children"),
    Output('bdd-var-par-25m', "data"),
    Output('df-stored-25m', "data"),
    Input('distance-course-section-dropdown', "value"),
    Input('style-nage-section-dropdown', "value"),
    Input('competition-nom-section-dropdown', "value"),
    Input('round-name-section-dropdown', "value"),
    Input('sexe-section-dropdown', "value"),
    Input('nom-prenom-section-dropdown', "value"),
    Input('variable-25m-item', "value"),
    Input('reset-25m-button', "n_clicks")
)

def display_bdd_var_par_25(distance_c, style, competition, round, sexe, nom, variable, btn_reset_clicks):
    warning = "ATTENTION : soit vous n'avez pas sélectionné d'épreuve pour le moment, soit vous n'avez pas actualisé après avoir changé le paramètre d'étude. N'oubliez pas d'actualiser pour tenir compte des changements opérés."
    dff = pd.DataFrame()
    dff_store = pd.DataFrame().to_dict('records')
    if "reset-25m-button" in ctx.triggered[0]['prop_id']:
        if distance_c:
            warning = ''
            dff = df_section_init.copy()
            dff = df_freq_ampl(dff, int(distance_c))
            dff = dff.loc[dff.distance_course == distance_c]
            if style:
                dff = dff.loc[dff.style_nage.isin(style)]

            if competition:
                dff = dff.loc[dff.competition_nom.isin(competition)]

            if round:
                dff = dff.loc[dff.round_name.isin(round)]

            if sexe:
                dff = dff.loc[dff.nageur_sexe.isin(sexe)]

            if nom:
                dff = dff.loc[dff.nom_prenom.isin(nom)]

            if variable == '  Fréquence':
                for colonne in dff.columns:
                    if colonne.startswith('Ampl') | colonne.startswith('Tempo'):
                        dff = dff.drop(colonne, axis=1)

            if variable == '  Amplitude':
                for colonne in dff.columns:
                    if colonne.startswith('Freq') | colonne.startswith('Tempo'):
                        dff = dff.drop(colonne, axis=1)

            if variable == '  Tempo':
                for colonne in dff.columns:
                    if colonne.startswith('Freq') | colonne.startswith('Ampl'):
                        dff = dff.drop(colonne, axis=1)


            liste_col = ['id_analyse', 'competition_nom', 'distance_course', 'style_nage', 'round_name', 'TEMPS_SECTION', 'VITESSE', 'NB_CYCLE',
                            'FREQUENCE', 'TEMPO', 'AMPLITUDE']
            dff = dff.drop(columns = liste_col, axis=1)

            dff = dff.rename(columns={'nom_analyse': 'ID complet (distance, nage, épreuve, compétition)',
                                    'nom_prenom' : 'Nom & prénom du nageur', 'nageur_sexe': 'Sexe',
                                    'mois_annee': 'Date', 'temps_final': 'Temps final', 'temps_reaction': 'Temps réaction',
                                    'temps_vol': 'Temps vol', 'temps_depart': 'Temps départ'})

            liste_round = ['Temps départ', 'Temps réaction', 'Temps vol']
            for col in liste_round:
                dff[col] = dff[col].round(2)

            dff = dff.sort_values(by='Temps final', ascending=True)
            dff_store = dff.copy()
            dff_store = dff_store.to_dict('records')

            return (warning, dff_store, dff_store)
        else:
            warning = 'ATTENTION : Veuillez au moins sélectionner une distance.'
            dff_store = df_section_init.to_dict('records')

    return(warning, dff_store, dff_store)


@callback(
    Output('bdd-var-par-25m', 'columns'),
    [Input('df-stored-25m', 'data')],
)

def update_columns_25m(data):
    if data is not None:
        # Récupérez les colonnes du DataFrame
        df_columns = pd.DataFrame(data).columns
        # Créez une liste de colonnes au format attendu par dash_table.DataTable
        columns = [{'name': str(column), 'id': str(column)} for column in df_columns]
        return columns
    # Si aucune donnée n'est disponible, utilisez une liste vide pour les colonnes
    return []


@callback(
    Output("download-dataframe-25m-csv", "data"),
    Input("btn_csv_25m","n_clicks"),
    Input("btn_excel_25m","n_clicks"),
    Input('df-stored-25m', "data"),
    prevent_initial_call = True
)

def download_df_section_csv_25m(btn_csv_clicks, btn_excel_clicks, df_stored):
    dff = df_stored.copy()
    dff = pd.DataFrame(dff)
    if "btn_csv_25m" == ctx.triggered_id:
        return dcc.send_data_frame(dff.to_csv, "FFN_app_bdd_25m.csv")

    if "btn_excel_25m" == ctx.triggered_id:
        return dcc.send_data_frame(dff.to_excel, "FFN_app_bdd_25m.xlsx", sheet_name="Feuille_1")


@callback(
    Output('selected-rows-25m', 'children'),
    [Input('bdd-var-par-25m', 'selected_rows'),
     Input('reset-graph-25m-button', "n_clicks"),
     Input('selectall-25m-button', "n_clicks")],
     Input('deselectall-25m-button', "n_clicks"),
    [State('bdd-var-par-25m', 'data')],
)
def display_selected_rows_25m(selected_rows, btn_reset, btn_selectall, data):
    if "reset-graph-25m-button" in ctx.triggered[0]['prop_id']:
        if selected_rows:
            indices = [row['index'] for i, row in enumerate(data) if i in selected_rows]
            return f"Lignes sélectionnées : {indices}"

        if "selectall-25m-button" in ctx.triggered[0]['prop_id']:
            all_rows = list(range(len(data)))
            if "deselectall-25m-button" in ctx.triggered[0]['prop_id']:
                all_rows = []
            return all_rows
    else :
        return {}


@callback(
    Output('bdd-var-par-25m', "selected_rows"),
    Input('selectall-25m-button', "n_clicks"),
    Input('deselectall-25m-button', "n_clicks"),
    State('bdd-var-par-25m', 'data')
)
def select_all_rows_25m(n_clicks_select, n_clicks_deselect, data):
    all_rows = []
    if n_clicks_select is not None and n_clicks_select > 0 and n_clicks_select > n_clicks_deselect:
        # Sélectionnez toutes les lignes en utilisant les indices de ligne
        all_rows = list(range(len(data)))

    if n_clicks_deselect is not None and n_clicks_deselect > 0 and n_clicks_deselect >= n_clicks_select:
        all_rows = []
    return all_rows
    # # Si le bouton n'est pas encore cliqué, renvoyez une liste vide
    # return []


@callback(
    Output('graph-par-25m', "figure"),
    Input('variable-25m-item', "value"),
    Input('bdd-var-par-25m', "data"),
    Input('bdd-var-par-25m', "selected_rows"),
    Input('reset-graph-25m-button', "n_clicks"),
)

def update_graph_25m(variable, data_stored, selected_rows, btn_reset_clicks):
    data_stored = pd.DataFrame(data_stored)
    if "reset-graph-25m-button" in ctx.triggered[0]['prop_id']:
        if variable == '  Fréquence' or variable == '  Tempo' or variable == '  Amplitude':
            if selected_rows is not None and len(selected_rows) > 0:
                # Obtenez l'indice de la ligne sélectionnée
                # Vous pouvez maintenant utiliser l'indice pour effectuer des opérations spécifiques
                # Par exemple, mettez à jour le graphique avec les données de la ligne sélectionnée
                figure = go.Figure()
                for i in range(len(selected_rows)):
                    selected_index = selected_rows[i]
                    row_variable = data_stored.iloc[selected_index,8:]
                    temps_final = data_stored.loc[selected_index, 'Temps final']
                    row_variable = pd.DataFrame(row_variable)
                    vecteur_float = row_variable.astype(float)
                    Y = np.array(vecteur_float).ravel()
                    index = pd.Index(row_variable.T.columns)
                    distances_float = [float(''.join(filter(str.isdigit, item))) for item in index]
                    df_indiv = pd.DataFrame({'Distance': distances_float,
                                            variable: Y})
                    figure.add_trace(go.Scatter(
                        x = df_indiv['Distance'],
                        y = df_indiv[variable],
                        mode='lines',
                        name=str(temps_final) + ', ' + data_stored.loc[selected_rows[i], 'Nom & prénom du nageur'] + ', ' + data_stored.loc[selected_rows[i], 'ID complet (distance, nage, épreuve, compétition)'],
                        hovertemplate='Distance : %{x}<br>' + variable + ': %{y}'
                    ))

                    figure.update_layout(
                        yaxis_title=variable,
                        xaxis_title='Distance (en mètres)',
                        title=variable + ' en fonction de la distance parcourue',
                        #hovermode="x",
                        legend={'itemsizing': 'constant', 'title_font': {'size': 12}, 'font': {'size': 10}},
                        legend_itemclick="toggleothers",
                    )

                return figure
            else :
                return {}
        else:
            return {}
    else:
        return {}


@callback(
    Output('warning-message-VFA',"children"),
    Output('bdd-vitesse-freq-ampl', "children"),
    Output('df-stored-vitesse-freq-ampl', "data"),
    Input('distance-course-section-dropdown', "value"),
    Input('style-nage-section-dropdown', "value"),
    Input('competition-nom-section-dropdown', "value"),
    Input('round-name-section-dropdown', "value"),
    Input('nom-prenom-section-dropdown', "value"),
    Input('reset-VFA-button', "n_clicks"),
)
def bdd_vitesse_freq_ampl(distance, style, competition, epreuve, nom, btn_reset_clicks):
    warning = "ATTENTION : le tableau des vitesses, fréquences et amplitudes par section est uniquement disponible si vous choisissez un nageur et une course particulière (distance, style de nage, nom de la compétition et épreuve)."
    dff = pd.DataFrame()
    dff_store = pd.DataFrame()
    if "reset-VFA-button" in ctx.triggered[0]['prop_id']:
            dff = df_section_init.copy()
            if distance:
                dff = dff.loc[dff.distance_course == distance]

            if style:
                dff = dff.loc[dff.style_nage.isin(style)]

            if competition:
                dff = dff.loc[dff.competition_nom.isin(competition)]

            if epreuve:
                dff = dff.loc[dff.round_name.isin(epreuve)]

            if nom:
                dff = dff.loc[dff.nom_prenom.isin(nom)]

            unique_count = dff['id_analyse'].nunique()
            if unique_count == 1:
                warning = 'Veuillez trouver ci-dessous le tableau des vitesses, fréquences et amplitudes par section. Chaque ligne est associée à une section existante pour la course sélectionnée.'
                identifiant = dff['id_analyse'].unique()
                dff = lien_frequence_amplitude_vitesse(identifiant[0],distance)
                dff = dff.drop(['ID analyse', 'Nom Analyse'], axis=1)
                dff = dff.rename(columns={'Nom et prénom' : 'Nom & prénom du nageur', 'Nom compétition': 'Nom de la compétition',
                                            'Distance de la course': 'Distance', 'Epreuve': 'Style de nage', 'Style': 'Epreuve'})

                dff['Vitesse moyenne'] = pd.to_numeric(dff['Vitesse moyenne'], errors='coerce')
                dff['Fréquence moyenne'] = pd.to_numeric(dff['Fréquence moyenne'], errors='coerce')
                dff['Amplitude moyenne'] = pd.to_numeric(dff['Amplitude moyenne'], errors='coerce')
                # Configuration de la DataTable
                # Calcul de la différence entre les valeurs consécutives de 'Vitesse moyenne'
                dff['Evolution vitesse'] = (dff['Vitesse moyenne'].diff()).round(2)
                dff['Evolution fréquence'] = (dff['Fréquence moyenne'].diff()).round(2)
                dff['Evolution amplitude'] = (dff['Amplitude moyenne'].diff()).round(2)
                dff['Evolution vitesse'] = dff['Evolution vitesse'].fillna(0)
                dff['Evolution fréquence'] = dff['Evolution fréquence'].fillna(0)
                dff['Evolution amplitude'] = dff['Evolution amplitude'].fillna(0)
                # Créez la liste de styles
                styles = [
                    {
                        'if': {'filter_query': '{{Evolution vitesse}} > {}'.format(0), 'column_id': 'Evolution vitesse'},
                        'backgroundColor': '#c5f6af',
                        'color': 'black'
                    },
                    {
                        'if': {'filter_query': '{{Evolution vitesse}} < {}'.format(0), 'column_id': 'Evolution vitesse'},
                        'backgroundColor': '#fa6979',
                        'color': 'black'
                    },
                    {
                        'if': {'filter_query': '{{Evolution vitesse}} = {}'.format(0), 'column_id': 'Evolution vitesse'},
                        'backgroundColor': 'white',
                        'color': 'black'
                    },
                    {
                        'if': {'filter_query': '{{Evolution fréquence}} > {}'.format(0), 'column_id': 'Evolution fréquence'},
                        'backgroundColor': '#c5f6af',
                        'color': 'black'
                    },
                    {
                        'if': {'filter_query': '{{Evolution fréquence}} < {}'.format(0), 'column_id': 'Evolution fréquence'},
                        'backgroundColor': '#fa6979',
                        'color': 'black'
                    },
                    {
                        'if': {'filter_query': '{{Evolution fréquence}} = {}'.format(0), 'column_id': 'Evolution fréquence'},
                        'backgroundColor': 'white',
                        'color': 'black'
                    },
                    {
                        'if': {'filter_query': '{{Evolution amplitude}} > {}'.format(0), 'column_id': 'Evolution amplitude'},
                        'backgroundColor': '#c5f6af',
                        'color': 'black'
                    },
                    {
                        'if': {'filter_query': '{{Evolution amplitude}} < {}'.format(0), 'column_id': 'Evolution amplitude'},
                        'backgroundColor': '#fa6979',
                        'color': 'black'
                    },
                    {
                        'if': {'filter_query': '{{Evolution amplitude}} = {}'.format(0), 'column_id': 'Evolution amplitude'},
                        'backgroundColor': 'white',
                        'color': 'black'
                    },
                ]

                # Étendre la liste pour chaque ligne
                styles *= len(dff['Evolution vitesse'])
                dff_store = dff.copy()

                datatable = dash_table.DataTable(
                    id='bdd-vitesse-freq-ampl',
                    data=dff.to_dict('records'),
                    columns=[{'name': col, 'id': col} for col in dff.columns],
                    editable=True,
                    style_cell={'textAlign': 'center'},
                    style_header={
                        'backgroundColor': color_third_section,
                        'color': 'white',
                        'fontWeight': 'bold'
                    },
                    style_data={
                        'width': '100px', 'minWidth': '100px', 'maxWidth': '100px',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                    },
                    style_data_conditional=styles

                )
                #dff = dff.to_dict('records')
                dff_store = dff_store.to_dict('records')
                return (warning, datatable, dff_store)
            else:
                warning = "Vous n'avez pas sélectionné une seule et unique course."
                dff = pd.DataFrame()  # Assurez-vous de renvoyer un DataFrame vide
                dff_store = pd.DataFrame().to_dict('records')
                dff = dff.to_dict('records')
                return (warning, dff, dff_store)

    dff = dff.to_dict('records')
    dff_store = dff_store.to_dict('records')
    return(warning, dff, dff_store)



@callback(
    Output("download-dataframe-VFA-csv", "data"),
    Input("btn_csv_VFA","n_clicks"),
    Input("btn_excel_VFA","n_clicks"),
    Input('df-stored-vitesse-freq-ampl', "data"),
    prevent_initial_call = True
)

def download_df_VFA_csv(btn_csv_clicks, btn_excel_clicks, df_stored):
    dff = df_stored.copy()
    dff = pd.DataFrame(dff)
    if "btn_csv_VFA" == ctx.triggered_id:
        return dcc.send_data_frame(dff.to_csv, "FFN_app_bdd_section_VFA.csv")

    if "btn_excel_VFA" == ctx.triggered_id:
        return dcc.send_data_frame(dff.to_excel, "FFN_app_bdd_section_VFA.xlsx", sheet_name="Feuille_1")