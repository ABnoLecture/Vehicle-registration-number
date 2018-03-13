#!/usr/bin/python3
# -*- coding: utf-8 -*-

#Interfaz con PyQt5
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import numpy as np
import random
import Model_plate_car
import cv2
import pandas as pd
import multiprocessing as mp
# import OwnDash
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import webbrowser
class VentanaPrincipal(QMainWindow):
    def __init__ (self):
        super(VentanaPrincipal,self).__init__()#Se define como super clase
        self.initUI()# Se Crea un metodo encargado de lanzar GUI
        self.checkEvents()
    '''Definicion y ubicacion de elementos en la ventana principal del programa'''
    def initUI(self):

        '''Diseno de la ventana Principal'''

        '''BOTONES'''
        self.Boton0=QPushButton("Cargar",self)
        self.Boton0.setToolTip("Sirve para <b>Cargar</b> la imagen en la interfaz") # El <b> ### </b> Sirve para poner en negrita
        self.Boton0.setStatusTip("Sirve para Cargar la imagen en la interfaz")
        self.Boton0.resize(self.Boton0.sizeHint()) #Ajusta el tamano del boton al texto que tiene en el interior
        self.Boton0.move(25,410)

        self.Boton1=QPushButton('Identificar',self)
        self.Boton1.setToolTip("<b>Identifica</b> los caracteres de la matricula vehicular") # El <b> ### </b> Sirve para poner en negrita
        self.Boton1.setStatusTip("Identifica los caracteres de la matricula vehicular")
        self.Boton1.resize(self.Boton1.sizeHint()) #Ajusta el tamano del boton al texto que tiene en el interior
        self.Boton1.move(120,410)

        self.Boton2=QPushButton(' Estadisticas',self)
        self.Boton2.setToolTip("<b>Lanza el navegador </b>para mostrar las estadisticas de la prediccion") # El <b> ### </b> Sirve para poner en negrita
        self.Boton2.setStatusTip("Lanza el navegador para mostrar las estadisticas de la prediccion")
        self.Boton2.resize(self.Boton2.sizeHint()) #Ajusta el tamano del boton al texto que tiene en el interior
        self.Boton2.move(230,410)

        self.Boton3=QPushButton('Cerrar',self)
        self.Boton3.setToolTip("<b>Cierra la interfaz</b> ") # El <b> ### </b> Sirve para poner en negrita
        self.Boton3.setStatusTip("Cierra la interfaz")
        self.Boton3.resize(self.Boton3.sizeHint()) #Ajusta el tamano del boton al texto que tiene en el interior
        self.Boton3.move(350,410)

        '''POSICION DE LA IMAGEN EN LA PANTALLA'''
        self.square = QFrame(self)
        self.square.setGeometry(25, 55, 845, 325)
        self.square.setStyleSheet("background-color: rgb(255, 255, 255);""border:1px solid rgb(0,0,0);")
        self.Texto1=QLabel('NO HAY IMAGEN',self)
        self.Texto1.move(400,162)

        self.Prediccion = QFrame(self)
        self.Prediccion.setGeometry(460, 390, 410, 60)
        self.Prediccion.setStyleSheet("background-color: rgb(255, 255, 255);""border:1px solid rgb(0,0,0);")
        self.Texto3=QLabel(self)
        self.Texto3.move(550,390)

        '''ICONOS BARRA DE TAREAS'''
        self.IconosAccionCargar=QAction(QIcon("Cargar.png"),'Cargar',self)
        self.IconosAccionCargar.setShortcut("Ctrl+C")
        self.IconosAccionCargar.setStatusTip("Cargar Imagen")
        self.IconosAccionCargar.setToolTip("Cargar Imagen")

        self.IconosAccionEstadistica=QAction(QIcon("Estaditica.png"),'Estadistica',self)
        self.IconosAccionEstadistica.setShortcut("Ctrl+E")
        self.IconosAccionEstadistica.setStatusTip("Mostrar estadisticas de la Matricula")
        self.IconosAccionEstadistica.setToolTip("Mostrar estadisticas de la Matricula")

        self.IconosAccionSalir=QAction(QIcon("logout.png"),'Exit',self)
        self.IconosAccionSalir.setShortcut("Ctrl+Q")
        self.IconosAccionSalir.setStatusTip("Salir de la aplicación")
        self.IconosAccionSalir.setToolTip("Salir de la aplicación")

        self.BarraTareas= self.addToolBar("Salir")
        self.BarraTareas.addAction(self.IconosAccionCargar)
        self.BarraTareas.addAction(self.IconosAccionEstadistica)
        self.BarraTareas.addAction(self.IconosAccionSalir)

        '''DIMESIONES DEL RECUADRO PRINCIPAL'''
        self.BarraEstado=self.statusBar()
        self.BarraEstado.setToolTip("Indicador de estado del proceso")
        self.BarraEstado.showMessage("En ejecución") # Indicador en la parte inferior
        self.resize(900,500) # self.setGeometry(50,30,900,600) #Orden 1er: Posicion pantalla X, 2do: Posicion pantalla Y, 3er: Altura de la venta, 4to: Ancho de la ventana
        self.setWindowTitle("Detector de caracteres en matriculas vehiculares")#Le da un nombre
        self.setWindowIcon(QIcon("IconoVentan.jpg")) #Coloca el Icono en la parte Superior de la ventana

        '''INDICARO DE LA POSICION DEL MOUSE'''
        x=0
        y=0
        self.text= "X:{}, Y:{}".format(x,y)
        self.setMouseTracking(True)

        self.show()

    '''Evento encarga de pregutar nuevamente en la ventana principal si se desea cerrar '''
    def closeEvent(self,event):
        reply=QMessageBox.question(self,'Atencion',"Esta seguro que desea salir?",QMessageBox.Yes|QMessageBox.No)
        if reply==QMessageBox.Yes:
            self.ProDash.terminate()
            self.ProDash.join()
            event.accept()
        else:
            event.ignore()

    '''Metodo encargado de centrar la imagen'''
    def CentrarInterfaz(self):
        qr=self.frameGeometry
        cp=QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    '''Metodo para mostrar o esconder la barra de estado'''
    def toggleMenu (self,state):
         if state:
             self.BarraEstado.show()
             self.BarraEstado.showMessage("En ejecución") # Indicador en la parte inferior
         else:
             self.BarraEstado.hide()

    def mouseMoveEvent(self,e):
        x=e.x()
        y=e.y()

        text="X:{}, Y:{}".format(x,y)
        self.BarraEstado.showMessage(text)

    def CargarImagen (self):
        image = QFileDialog.getOpenFileName(None,'OpenFile','',"Image file(*.jpg)")
        self.imagePath = image[0]
        self.pixmap = QPixmap(self.imagePath)
        self.Texto2=QLabel(self)
        self.Texto2.move(25,55)
        self.Texto2.resize(self.square.size())
        self.Texto2.setScaledContents(True)
        self.Texto2.setPixmap(self.pixmap)
        self.Texto2.show()
        self.Texto3.setText(" ")

    def checkEvents(self):
        '''EVENTO DE BOTONES DE LA INTERFAZ'''
        self.Boton0.clicked.connect(self.CargarImagen)
        self.Boton1.clicked.connect(self.EvaluarPlaca)
        self.Boton2.clicked.connect(self.Start_Dash)
        self.Boton3.clicked.connect(self.close)

        '''EVENTOS DE LOS ICONOS DE LA BARRA DE TAREAS'''
        self.IconosAccionCargar.triggered.connect(self.CargarImagen)
        self.IconosAccionEstadistica.triggered.connect(self.Start_Dash)
        self.IconosAccionSalir.triggered.connect(self.close)

    def EvaluarPlaca(self):
        self.Test_plate=Model_plate_car.IdentificadorCaracter()
        self.Resultado,self.PorcentPrediction=self.Test_plate.Modelo(self.imagePath)
        self.Registro(self.PorcentPrediction)
        self.matricula=str("{} - {} - {} - {} - {} - {}".format(self.Resultado[0],self.Resultado[1],self.Resultado[2],self.Resultado[3],self.Resultado[4],self.Resultado[5]))
        self.Texto3.setText(self.matricula)
        self.Texto3.setFont(QFont('SansSerif',15))
        self.Texto3.resize(self.Prediccion.size())
        self.MatriculaFinal=QPixmap('image.jpg')
        self.Texto2.resize(self.square.size())
        self.Texto2.setScaledContents(True)
        self.Texto2.setPixmap(self.MatriculaFinal)
        self.Texto2.show()

    # def Estadisticas(self):
        # Sharedmemori=mp.queues()
        # self.dashGUI.DashMethod(str("{} - {} - {} - {} - {} - {}".format(self.Resultado[0],self.Resultado[1],self.Resultado[2],self.Resultado[3],self.Resultado[4],self.Resultado[5])))
        # self.dashGUI.LaunchWebBrowser(url)

    def Start_Dash(self):
        self.ProDash=mp.Process(target=self.DashMethod,)
        self.ProDash.start()


    def Registro(self,Datos):    #Registro de datos en excel
        self.Datos=list(map(list, zip(*Datos)))
        df=pd.DataFrame(self.Datos)# Create a una tiras de datos en formato de pandas.
        df.to_csv('Predicciones.csv', encoding='utf-8', index=False,header=False)

    def LaunchWebBrowser(self,url):
        webbrowser.open_new(url)
        self.app.run_server(debug=False,  processes=1000)

    def generate_table(self,dataframe, max_rows=36):
        return html.Table(
            # Header
            [html.Tr([html.Th("Carater #1"),html.Th("Carater #2"),html.Th("Carater #3"),html.Th("Carater #4"),html.Th("Carater #5"),html.Th("Carater #6")])] +

            # Body
            [html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))]
        )

    def DashMethod(self):

        df=pd.read_csv('Predicciones.csv',header=None,dtype=str)
        dft = pd.read_csv('Entrenamiento.csv', header=None, dtype=float)
        dft = np.array(dft)
        x = np.arange(0,100,1)
        self.app = dash.Dash()

        colors = {
            'background': '#111111',
            'text': '#7FDBFF'
        }

        self.app.layout = html.Div(children=[
            html.H1(children='ESTIMADOR DE MATRICULAS VEHICULARES',
            style={
            'textAlign': 'center',"font-family":"verdana"}),

            dcc.Graph(
                id='Gráfica de entrenamiento del modelo para la predicción',
                figure={
                    'data': [
                        {'x': x, 'y': dft[::][0], 'type': 'line', 'name': u'Train_Loss'},
                        {'x': x, 'y': dft[::][1], 'type': 'line', 'name': u'Val_Loss'},
                        {'x': x, 'y': dft[::][2], 'type': 'line', 'name': u'Train_Acc'},
                        {'x': x, 'y': dft[::][3], 'type': 'line', 'name': u'Val_Acc'}
                    ],
                    'layout': {
                        'title': 'Visualizacion del entrenamiento del modelo para la predición de caracteres'
                    }
                }
            )
        ,html.H1(children='Porcentaje de prediccion de cada caracter de la matricula vehicular {}'.format(self.matricula)),
        self.generate_table(df)],style={
        "font-family":"arial"})
        self.LaunchWebBrowser('http://127.0.0.1:8050/')


if __name__ =='__main__':
    app=QApplication(sys.argv)
    ex=VentanaPrincipal()
    sys.exit(app.exec_())
    self.ProDash.terminate()
    self.ProDash.join()
