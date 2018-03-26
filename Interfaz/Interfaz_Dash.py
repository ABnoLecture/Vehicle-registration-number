#!/usr/bin/python3
# -*- coding: utf-8 -*-

#Interfaz con PyQt5
import base64
import sys
import numpy as np
import random
import Model_plate_car
import cv2
import pandas as pd
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import plotly.graph_objs as go
from dash.dependencies import *
import webbrowser
import tempfile

class VentanaPrincipal(object):
    def __init__ (self):
        super(VentanaPrincipal,self).__init__()#Se define como super clase
        # self.DashMethod()

    def Registro(self,Datos):    #Registro de datos en excel
        self.Datos=list(map(list, zip(*Datos)))
        df=pd.DataFrame(self.Datos)# Create a una tiras de datos en formato de pandas.
        df.to_csv('Predicciones.csv', encoding='utf-8', index=False,header=False)


    def data_uri_to_cv2_img(self,uri):
        encoded_data = uri.split(',')[1]
        nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        directory_name = tempfile.mkdtemp()
        cv2.imwrite((directory_name+str('/DashPrueba.jpg')), img)

        self.Test_plate=Model_plate_car.IdentificadorCaracter()
        self.Resultado,self.PorcentPrediction,NewImgPlate=self.Test_plate.Modelo((directory_name+str('/DashPrueba.jpg')))
        self.Registro(self.PorcentPrediction)
        matricula=str("{} - {} - {} - {} - {} - {}".format(self.Resultado[0],self.Resultado[1],self.Resultado[2],self.Resultado[3],self.Resultado[4],self.Resultado[5]))
        cv2.imwrite(str('image.jpg'), NewImgPlate)
        os.remove((directory_name+str('/DashPrueba.jpg')))
        os.removedirs(directory_name)

        return NewImgPlate,matricula#"data:image/jpeg;base64,"+str(base64.b64encode(img))

    def DashMethod(self):
        classLabels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'
        , 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        dft = pd.read_csv('Entrenamiento.csv', header=None, dtype=float)
        dft = np.array(dft)
        x = np.arange(0,100,1)
        app = dash.Dash(__name__)
        style={'textAlign': 'center',"font-family":"arial"}
        ListaB=[{}]
        app.scripts.config.serve_locally = True
        app.config['suppress_callback_exceptions']=True
        app.layout = html.Div(
        [
        html.H1('ESTIMADOR DE MATRICULAS VEHICULARES'),
        dcc.Graph(
                id='Gráfica de entrenamiento del modelo para la predicción',
                figure={
                    'data': [
                        {'x': x, 'y': dft[::][0], 'type': 'line', 'name': 'Train_Loss'},
                        {'x': x, 'y': dft[::][1], 'type': 'line', 'name': u'Val_Loss'},
                        {'x': x, 'y': dft[::][2], 'type': 'line', 'name': u'Train_Acc'},
                        {'x': x, 'y': dft[::][3], 'type': 'line', 'name': u'Val_Acc'}
                    ],
                    'layout':  go.Layout(title='Visualizacion del entrenamiento del modelo para la predición de caracteres' ,
                        xaxis=dict(
                            title='# Epocas',
                            titlefont=dict(
                                family='Courier New, monospace',
                                size=18,
                                color='#7f7f7f'
                            )
                        ),
                        yaxis=dict(
                            title='Perdida[%]',
                            titlefont=dict(
                                family='Courier New, monospace',
                                size=18,
                                color='#7f7f7f'
                            )
                        )
                    )
                }
            ),
        dcc.Upload(
            id='upload-image',
            children=html.Div([
                html.A('Seleccionar Archivo')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            # Allow multiple files to be uploaded
            multiple=True
        ),
        html.Div(id='output-image-upload'),
        html.H1('Porcentaje de prediccion de cada caracter de la matricula vehicular'),
        html.Div(id='output-mat'),
        dt.DataTable(id='datatable-not-working', rows=ListaB),
        dcc.Interval(id='interval-component',interval=1*1000, n_intervals="1000")

        ]
        ,style=style)

        @app.callback(Output('datatable-not-working','rows'),[Input('interval-component', 'n_intervals')])
        def update_info_table(n):
            df=pd.read_csv('Predicciones.csv',header=None,dtype=str)
            df.insert(loc=0,column=6,value=classLabels)
            ListaB=[([(df[col][Fila]) for col in range (0,7)]) for Fila in range (0,36)]
            return ListaB

        @app.callback(Output('output-image-upload', 'children'),[Input('upload-image', 'contents'),])
        def update_output(list_of_contents):
            if list_of_contents is not None:
                img,_=self.data_uri_to_cv2_img(list_of_contents[0])
                image_filename = 'image.jpg' # replace with your own image
                encoded_image = base64.b64encode(open(image_filename, 'rb').read())
                return html.Div([html.Img(src=list_of_contents,height='160', width='315')])
                # html.Div([html.Img(src="data:image/jpeg;base64,{}".format(encoded_string),height='160', width='315')])

        @app.callback(Output('output-mat', 'children'),[Input('upload-image', 'contents'),Input('upload-image', 'contents')])
        def update_mat(n,list_of_contents):
            if list_of_contents is not None:
                _,matri=self.data_uri_to_cv2_img(list_of_contents[0])
                return [html.Span(matri,style={'fontSize': '35px'})]


        app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
        webbrowser.open_new( "http://127.0.0.1:8050/")
        app.run_server(debug=False)


if __name__ =='__main__':
    ex=VentanaPrincipal()


Prueba=VentanaPrincipal()
Muestra=Prueba.DashMethod()
