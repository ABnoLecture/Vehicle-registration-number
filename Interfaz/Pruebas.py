#!/usr/bin/python3
# -*- coding: utf-8 -*-

#Interfaz con PyQt5
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import random

class VentanaPrincipal(QMainWindow):
    def __init__ (self):
        super().__init__()#Se define como super clase
        self.initUI()# Se Crea un metodo encargado de lanzar GUI

    '''Definicion y ubicacion de elementos en la ventana principal del programa'''
    def initUI(self):

        '''Creacion de boton de muestas'''
        Boton=QPushButton("Mostrar Ventana",self)
        Boton.clicked.connect(self.PresionasteBoton)
        Boton.setToolTip("Esto es un <b>QtPushButton</b> Widget Boton") # El <b> ### </b> Sirve para poner en negrita
        Boton.resize(Boton.sizeHint()) #Ajusta el tamano del boton al texto que tiene en el interior
        Boton.move(50,150)

        '''Creacion de boton para salir del programa'''
        Salir=QPushButton("Cerrar",self)
        Salir.clicked.connect(QApplication.instance().quit)
        Salir.setToolTip("Boton para <b>Cerrar</b> el programa")
        Salir.resize(Salir.sizeHint())
        Salir.move(820,570)

        ''' Mensaje de ayuda en la pantalla'''
        QToolTip.setFont(QFont('SansSerif', 10)) #Mensaje de ayuda que aparece en pantalla cuando se deja  el mouse sobre la ventan
        self.setToolTip("Esto es un <b>Mensaje de ayuda</b> si se deja el mouse quieto")

        '''Diseno de la ventana Principal'''
        BarraMenu=self.menuBar()
        FileMenu =BarraMenu.addMenu("Archivo")

        Menu=QMenu("Cargar",self) # Crea un subMenu
        MenuAccion=QAction("Matriculas vehiculares",self) #Crea una accion
        Menu.addAction(MenuAccion) #Agrega la accion al subMenu

        self.Edito=QTextEdit(self)
        self.Edito.move(500,250)
        self.Edito.resize(200,200)

        '''Texto en pantalla'''
        self.Texto1=QLabel('Editor de texto',self)
        self.Texto1.move(500,220)

        IconosAccionSalir=QAction(QIcon("logout.png"),'Exit',self)
        IconosAccionSalir.setShortcut("Ctrl+Q")
        IconosAccionSalir.setStatusTip("Salir de la aplicación")
        IconosAccionSalir.setToolTip("Salir de la aplicación")
        IconosAccionSalir.triggered.connect(self.close)

        Checklist=QAction("Barra de estado",self, checkable=True)
        Checklist.setStatusTip("Barra visible o invisible")
        Checklist.setToolTip("Activa o desactiva la barra de estado")
        Checklist.setChecked(True)
        Checklist.triggered.connect(self.toggleMenu)

        BarraTareas= self.addToolBar("Salir")
        BarraTareas.addAction(IconosAccionSalir)

        FileMenu.addMenu(Menu) #Agrega el subMenu a la barra de principal
        FileMenu.addAction(Checklist)
        FileMenu.addAction(QAction("Salir",self))

        self.BarraEstado=self.statusBar()
        self.BarraEstado.setToolTip("Indicador de estado del proceso")
        self.BarraEstado.showMessage("En ejecución") # Indicador en la parte inferior
        self.resize(900,600) # self.setGeometry(50,30,900,600) #Orden 1er: Posicion pantalla X, 2do: Posicion pantalla Y, 3er: Altura de la venta, 4to: Ancho de la ventana
        self.setWindowTitle("Detector de caracteres en matriculas vehiculares")#Le da un nombre
        self.setWindowIcon(QIcon("IconoVentan.jpg")) #Coloca el Icono en la parte Superior de la ventana


        '''Indicador de la posicion del mouse en la pantall'''
        grid=QGridLayout()
        x=0
        y=0

        self.text= "X:{}, Y:{}".format(x,y)
        self.label=QLabel(self.text,self)
        self.label.move(0,560)
        # self.BarraEstado.setStatusTip(self.text)
        grid.addWidget(self.label, 0,0, Qt.AlignCenter)
        self.setMouseTracking(True)

        self.setLayout(grid)

        self.show()

    '''Evento encarga de pregutar nuevamente en la ventana principal si se desea cerrar '''
    def closeEvent(self,event):
        reply=QMessageBox.question(self,'Atencion',"Esta seguro que desea salir?",QMessageBox.Yes|QMessageBox.No)
        if reply==QMessageBox.Yes:
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

    @pyqtSlot()
    def PresionasteBoton(self):
        self.Mensaje=QMessageBox.information(self, 'PyQt5 Mensaje', "Te gusta PyQt5?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if self.Mensaje == QMessageBox.Yes:
            self.BarraEstado.setStatusTip("Te gusta PyQt5")
        else:
            self.BarraEstado.setStatusTip("No te gusta PyQt5")

    def mouseMoveEvent(self,e):
        x=e.x()
        y=e.y()

        text="X:{}, Y:{}".format(x,y)
        self.label.setText(text)

if __name__ =='__main__':
    app=QApplication(sys.argv)
    ex=VentanaPrincipal()
    sys.exit(app.exec_())
