# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import webbrowser
import pandas as pd
import numpy as np

class DashComplement(object):

    def LaunchWebBrowser(self,url):
        webbrowser.open_new(url)
        self.app.run_server(debug=False)

    def generate_table(self,dataframe, max_rows=36):
        return html.Table(
            # Header
            [html.Tr([html.Th("Carater #1"),html.Th("Carater #2"),html.Th("Carater #3"),html.Th("Carater #4"),html.Th("Carater #5"),html.Th("Carater #6")])] +

            # Body
            [html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))]
        )

    def DashMethod(self,Placa):

        df=pd.read_csv('Predicciones.csv',header=None,dtype=str)
        self.app = dash.Dash()

        colors = {
            'background': '#111111',
            'text': '#7FDBFF'
        }

        self.app.layout = html.Div(children=[
            html.H1(children='ESTIMADOR DE MATRICULAS VEHICULARES',
            style={
            'textAlign': 'center','font':'verdana'}),

            html.Div(children='''
                Valores de la prediccion
            ''',style={
            'textAlign': 'center','font':'verdana'}),

            dcc.Graph(
                id='Gráfica de entrenamiento del modelo para la predicción',
                figure={
                    'data': [
                        {'x': [1, 2, 3,5,6,6,7,8,9,], 'y': [4, 1, 2,4,5,6,7,9,9], 'type': 'line', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'line', 'name': u'Montréal'},
                    ],
                    'layout': {
                        'title': 'Visualizacion del entrenamiento'
                    }
                }
            )
        ,html.H1(children='Porcentaje de prediccion de cada caracter de la matricula vehicular {}'.format(Placa)),
        self.generate_table(df)])
        self.LaunchWebBrowser('http://127.0.0.1:8050/')
