import sys
from datetime import datetime
from Funciones04 import *
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import urllib.request
import pandas as pd
from pylab import *
from fpdf import FPDF
import tkinter as tk
from tkinter import filedialog
from ERP_COMP_P001_Pedido_de_Compra import Pedido_de_Compra
from ERP_COTP_P003_3 import ERP_COTP_P003_3

# dict_estado = {'1':"En Proceso", '2':"Proceso de Invitación", '3':"Invitado", '4':"Evaluar Ofertas",
# '5':"Mail enviado", '6':"Prov. Cotizo", '7':"Prov. NO cotizo", '8':"Ganador", '9':"Concluido"}
dicTipPed={'1':'Compra Nacional','2':'Importaciones','3':'Traslados entre Plantas','4':'Entrada Gratis'}
dicEstado={'1':'Proceso Emisión','2':'Enviado a Prov.','3':'Saldo Pendiente','4':'Recepcionada','9':'Eliminado'}

sqlProv="SELECT Cod_prov, Razón_social FROM TAB_PROV_001_Registro_de_Proveedores"

sqlMate="SELECT Cod_Mat FROM TAB_MAT_001_Catalogo_Materiales"

sqlFamilias = "SELECT Familia, Descrip FROM TAB_MAT_009_Sub_Familias WHERE Sub_Fam='00';"

sqlSubFamilias = "SELECT CONCAT(Familia, Sub_Fam), Descrip FROM TAB_MAT_009_Sub_Familias WHERE Sub_Fam!='00';"

sqlCatMat="SELECT Cod_Mat,Descrip_Mat,Uni_Base FROM TAB_MAT_001_Catalogo_Materiales"

class BuscarMaterial(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("ERP_ALM_P029_Buscar.ui",self)

        self.twMaterial.itemDoubleClicked.connect(self.Codigo_Material)
        self.lePalabra.textChanged.connect(self.buscar)

        cargarIcono(self, 'erp')

        sqlMat="SELECT Cod_Mat, Descrip_Mat, Uni_Base, Fam_Mat, Sub_Fam_Mat FROM TAB_MAT_001_Catalogo_Materiales"
        info=consultarSql(sqlMat)

        self.twMaterial.clear()
        for fila in info:

            if (fila[3]+fila[4]) in dict_subfamilia:
                fila[4]=dict_subfamilia[fila[3]+fila[4]]
            if fila[3] in dict_familia:
                fila[3]=dict_familia[fila[3]]

            item=QTreeWidgetItem(self.twMaterial,fila)
            for i in range(len(fila)):
                self.twMaterial.resizeColumnToContents(i)
            self.twMaterial.addTopLevelItem(item)

    def buscar(self):
        buscarTabla(self.twMaterial, self.lePalabra.text(), [0,1,3,4])

    def Codigo_Material(self,item):
        global Codigo_Material,Descripcion,Unidad
        Codigo_Material=item.text(0)
        Descripcion=item.text(1)
        Unidad=item.text(2)
        self.close()

class Consulta_PC(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("ERP_PCOMP_003.ui",self)

        global infoMate, dict_familia, dict_subfamilia, dict, Año

        self.pbVerPedido.clicked.connect(self.Pedido_Compra)
        # self.tbwPedido_Compra.cellDoubleClicked.connect(self.Pedido_Compra)
        self.pbCargar.clicked.connect(self.Cargar)
        self.pbBuscar.clicked.connect(self.buscarMaterial)
        self.pbLimpiar.clicked.connect(self.Limpiar)
        self.pbSalir.clicked.connect(self.Salir)
        self.pbConsultar.clicked.connect(self.Consultar)
        self.deInicial.dateChanged.connect(self.Fecha_Inicial)
        self.deFinal.setDateTime(QtCore.QDateTime.currentDateTime())
        self.deFinal.dateChanged.connect(self.Fecha_Final)
        self.lePalabra.textChanged.connect(self.palabraClave)
        self.leMaterial.textChanged.connect(self.codigoMaterial)
        self.leInicial.textChanged.connect(self.FechaInicial)
        self.leFinal.textChanged.connect(self.FechaFinal)

        infoMate=convlist(sqlMate)

        infoFam = consultarSql(sqlFamilias)
        dict_familia = {}
        for info in infoFam:
            dict_familia[info[0]]=info[1]

        infoSubFam = consultarSql(sqlSubFamilias)
        dict_subfamilia = {}
        for i in infoSubFam:
            dict_subfamilia[i[0]]=i[1]

        catmat=consultarSql(sqlCatMat)
        dict={}
        for dato in catmat:
            codigo="|".join(dato[1:])
            if codigo not in dict:
                dict[dato[0]]=codigo

        now = datetime.datetime.now()
        Año=str(now.year)

    def datosCabecera(self, codSoc, empresa, usuario):

        global Cod_Soc, Nom_Soc, Cod_Usuario,dicProv
        Cod_Soc = codSoc
        Nom_Soc = empresa
        Cod_Usuario = usuario

        cargarLogo(self.lbLogo_Mp,'multiplay')
        cargarLogo(self.lbLogo_Soc, Cod_Soc)
        cargarIcono(self, 'erp')
        cargarIcono(self.pbSalir, 'salir')
        cargarIcono(self.pbVerPedido, 'visualizar')
        cargarIcono(self.pbConsultar, 'visualizar')
        cargarIcono(self.pbBuscar, 'buscar')
        cargarIcono(self.pbCargar, 'cargar')
        cargarIcono(self.pbLimpiar, 'nuevo')

        self.leInicial.setReadOnly(True)
        self.leFinal.setReadOnly(True)

        Prov=consultarSql(sqlProv)
        dicProv={}
        for dato in Prov:
            dicProv[dato[0]]=dato[1]

        self.Cargar()

    def Cargar(self):
        try:
            sqlCotComp="SELECT a.Nro_Pedido, a.Nro_Cotiza, a.Nro_Solp, a.Tipo_Pedido, b.Razón_social, a.Fecha_Doc_Pedido, a.Estado_Pedido, GROUP_CONCAT(' ', c.Cod_Mat) FROM TAB_COMP_004_Pedido_Compra a LEFT JOIN TAB_PROV_001_Registro_de_Proveedores b ON a.Cod_Prov=b.Cod_prov LEFT JOIN TAB_COMP_005_Detalle_Pedido_de_Compra c ON a.Cod_Emp=c.Cod_Empresa AND a.Año_Pedido=c.Año_Pedido AND a.Nro_Pedido=c.Nro_Pedido WHERE a.Cod_Emp='%s' AND a.Año_Pedido='%s' GROUP BY a.Nro_Pedido ORDER BY a.Fecha_Doc_Pedido ASC" %(Cod_Soc,Año)

            CargarPC(self,self.tbwPedido_Compra,sqlCotComp,dicTipPed,dicEstado)

        except Exception as e:
            mensajeDialogo("error", "Error", "No se pudieron cargar los datos")
            print(e)

    def palabraClave(self):
        buscarTablaPC(self,self.tbwPedido_Compra)

    def FechaInicial(self):
        buscarTablaPC(self,self.tbwPedido_Compra)

    def FechaFinal(self):
        buscarTablaPC(self,self.tbwPedido_Compra)

    def buscarMaterial(self):
        global Codigo_Material,Descripcion
        Codigo_Material=None
        Descripcion=None
        del Codigo_Material,Descripcion

        BuscarMaterial().exec_()
        try:
            if Codigo_Material in infoMate:
                self.leMaterial.setText(Codigo_Material)
                self.leDescripcion.setText(Descripcion)
                self.leUnidad.setText(Unidad)

            else:
                mensajeDialogo("error", "Error", "Código de Material no existe")
        except Exception as e:
            print(e)

    def codigoMaterial(self):
        try:
            Cod_Material=self.leMaterial.text()
            if len(Cod_Material) !=0:
                buscarTablaPC(self,self.tbwPedido_Compra)
                if Cod_Material in infoMate:
                    for k,v in dict.items():
                        if Cod_Material==k:
                            Descripcion=v[0:v.find('|')]
                            self.leDescripcion.setText(Descripcion)
                            Unidad=v[v.find('|')+1:]
                            self.leUnidad.setText(Unidad)
                else:
                    self.leDescripcion.clear()
                    self.leUnidad.clear()
            else:
                self.leDescripcion.clear()
                self.leUnidad.clear()

        except Exception as e:
            print(e)

    def Fecha_Inicial(self):
        Fec_Inicial=QDateToStrView(self.deInicial)
        self.leInicial.setText(Fec_Inicial)

    def Fecha_Final(self):
        Fec_Final=QDateToStrView(self.deFinal)
        self.leFinal.setText(Fec_Final)

    def Limpiar(self):
        self.leMaterial.clear()
        self.leDescripcion.clear()
        self.leUnidad.clear()
        self.lePalabra.clear()
        self.leInicial.clear()
        self.leFinal.clear()

    def Pedido_Compra(self):
        try:
            Nro_Pedido=self.tbwPedido_Compra.item(self.tbwPedido_Compra.currentRow(),0).text()
            Nro_Cotiza=self.tbwPedido_Compra.item(self.tbwPedido_Compra.currentRow(),1).text()
            Razon_Social=self.tbwPedido_Compra.item(self.tbwPedido_Compra.currentRow(),4).text()
            for k,v in dicProv.items():
                if Razon_Social==v:
                    Cod_Prov=k

            sql='''SELECT SUM(d.Cant_Asignada*d.Precio_Cotiza),c.Nro_Solp,c.Fecha_Doc FROM TAB_COMP_001_Cotización_Compra c LEFT JOIN TAB_COMP_002_Detalle_Cotización_de_Compra d ON c.Cod_Soc=d.Cod_Soc AND c.Año=d.Año AND c.Nro_Cotiza=d.Nro_Cotiza AND c.Cod_Prov=d.Cod_Prov LEFT JOIN TAB_PROV_001_Registro_de_Proveedores p ON c.Cod_Prov = p.Cod_prov LEFT JOIN TAB_COMP_004_Pedido_Compra e ON c.Cod_Soc=e.Cod_Emp AND c.Cod_Prov=e.Cod_Prov AND c.Nro_Cotiza=e.Nro_Cotiza WHERE c.Cod_Soc='%s' AND c.Año='%s' AND e.Nro_Pedido='%s' GROUP BY c.Nro_Cotiza, c.Cod_Prov ORDER BY c.Fecha_Evalua_Oferta ASC;'''%(Cod_Soc, Año, Nro_Pedido)
            dato=convlist(sql)
            Monto_Aprobado=dato[0]

            self.pc=Pedido_de_Compra()
            self.pc.datosCabecera(Cod_Soc,Nom_Soc,Cod_Usuario,Nro_Cotiza,Razon_Social,Cod_Prov,Monto_Aprobado)
            self.pc.showMaximized()

        except Exception as e:
            mensajeDialogo("error", "Error", "No se selecciono ninguna Cotización, verifique")
            print(e)

    def Consultar(self):
        try:
            self.co = ERP_COTP_P003_3(self)
            row = self.tbwPedido_Compra.currentRow()
            col = self.tbwPedido_Compra.columnCount()
            data = []
            for i in range(col):
                try:
                    item = self.tbwPedido_Compra.item(row, i).text()
                except:
                    item = ""
                data.append(item)
                i+=1

            sql='''SELECT SUM(d.Cant_Asignada*d.Precio_Cotiza),c.Nro_Solp,c.Fecha_Doc FROM TAB_COMP_001_Cotización_Compra c LEFT JOIN TAB_COMP_002_Detalle_Cotización_de_Compra d ON c.Cod_Soc=d.Cod_Soc AND c.Año=d.Año AND c.Nro_Cotiza=d.Nro_Cotiza AND c.Cod_Prov=d.Cod_Prov LEFT JOIN TAB_PROV_001_Registro_de_Proveedores p ON c.Cod_Prov = p.Cod_prov LEFT JOIN TAB_COMP_004_Pedido_Compra e ON c.Cod_Soc=e.Cod_Emp AND c.Cod_Prov=e.Cod_Prov AND c.Nro_Cotiza=e.Nro_Cotiza WHERE c.Cod_Soc='%s' AND c.Año='%s' AND e.Nro_Pedido='%s' GROUP BY c.Nro_Cotiza, c.Cod_Prov ORDER BY c.Fecha_Evalua_Oferta ASC;'''%(Cod_Soc, Año, data[0])
            dato=convlist(sql)

            nro_cotiza = data[1]
            fecha_doc = dato[2]
            prov = data[4]
            num_req=dato[1]
            fec_req=''
            estatus='Concluido'
            fecha_entrega=''

            self.co.mostrarInfo(Cod_Soc, Año, nro_cotiza, prov, num_req, fec_req, estatus, fecha_entrega,Cod_Usuario)
            self.co.showMaximized()

        except Exception as e:
            mensajeDialogo("error", "Error", "No se selecciono ninguna Cotización, verifique")
            print(e)

    def Salir(self):
        self.close()

if __name__ == '__main__':
    app=QApplication(sys.argv)
    _main=Consulta_PC()
    _main.showMaximized()
    app.exec_()
