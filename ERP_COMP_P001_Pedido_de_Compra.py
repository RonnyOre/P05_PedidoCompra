import sys
from datetime import datetime
from Funciones04 import*
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
import urllib.request
import pandas as pd
from pylab import *
from fpdf import FPDF
import tkinter as tk
from tkinter import filedialog
from Pedido_de_Compra_Datos_Importacion import Datos_Importacion
from Pedido_de_Compra_Condiciones_Cabecera import Condiciones_Cabecera
from Pedido_de_Compra_Interlocutor import Interlocutor
from Pedido_de_Compra_Depositos import Depositos
from Pedido_de_Compra_Condiciones_Posicion import Condiciones_Posicion


dicTip_Ped={'1':'Compra Nacional','2':'Importaciones','3':'Traslados entre Plantas','4':'Entrada Gratis'}
dicEstado={'1':'Proceso Emisión','2':'Enviado a Prov.','3':'Saldo Pendiente','4':'Recepcionada','9':'Eliminado'}

sqlMoneda="SELECT Cod_moneda,Descrip_moneda FROM TAB_SOC_008_Monedas"
sqlProv="SELECT a.Cod_prov, b.Nombre FROM TAB_PROV_001_Registro_de_Proveedores a LEFT JOIN TAB_SOC_009_Ubigeo b ON a.País=b.Cod_Pais WHERE b.Cod_Depart_Region='0' AND b.Cod_Provincia='0' AND b.Cod_Distrito='0' AND a.Estado_Prov='1'"

class TextoCabecera(QDialog):
    def __init__(self,Nro_Ped):
        QDialog.__init__(self)
        uic.loadUi('ERP_COMP_P001_Texto_Cabecera.ui',self)

        global NroDoc
        NroDoc=Nro_Ped

        self.pbGrabar.clicked.connect(self.Grabar)
        self.pbModificar.clicked.connect(self.Modificar)
        self.pbSalir.clicked.connect(self.Salir)

        cargarIcono(self, 'erp')
        cargarIcono(self.pbGrabar, 'grabar')
        cargarIcono(self.pbModificar,'modificar')
        cargarIcono(self.pbSalir,'salir')

        sqlTexCab="SELECT Texto FROM TAB_SOC_019_Texto_Proceso WHERE Cod_Soc='%s' AND Año='%s' AND Tipo_Proceso='3' AND Nro_Doc='%s' AND Item_Doc='0'"%(Cod_Soc,Año,NroDoc)
        TexCab=consultarSql(sqlTexCab)

        if TexCab!=[]:
            self.teDetalle.setPlainText(TexCab[0][0])
            self.teDetalle.setEnabled(False)
            self.pbGrabar.setEnabled(False)

        else:
            try:
                self.teDetalle.setPlainText(texto_cabecera)
                self.teDetalle.setEnabled(False)
                self.pbGrabar.setEnabled(False)

            except Exception as e:
                print(e)

    def Grabar(self):

        global texto_cabecera
        texto_cabecera = self.teDetalle.toPlainText()

        Hora=datetime.datetime.now().strftime("%H:%M:%S.%f")

        if NroDoc!="":

            sqlTexCab="SELECT Texto FROM TAB_SOC_019_Texto_Proceso WHERE Cod_Soc='%s' AND Año='%s' AND Tipo_Proceso='3' AND Nro_Doc='%s' AND Item_Doc='0'"%(Cod_Soc,Año,NroDoc)
            TexCab=convlist(sqlTexCab)

            if TexCab!=[]:
                sqlTextoCabecera="UPDATE TAB_SOC_019_Texto_Proceso SET Texto='%s',Fecha_Mod='%s',Hora_Mod='%s',Usuario_Mod='%s' WHERE Cod_Soc='%s' AND Año='%s' AND Tipo_Proceso='3' AND Nro_Doc='%s' AND Item_Doc='0'"%(texto_cabecera,Fecha,Hora,Cod_Usuario,Cod_Soc,Año,NroDoc)
                respuesta=ejecutarSql(sqlTextoCabecera)

                if respuesta['respuesta']=='correcto':
                    mensajeDialogo("informacion", "Información", "Texto de Cabecera Modificado")
                    del texto_cabecera
                    self.close()

                elif respuesta['respuesta']=='incorrecto':
                    mensajeDialogo("error", "Error", "El Texto de cabecera no se pudo modificar")
            else:
                sqlTextoCabecera='''INSERT INTO TAB_SOC_019_Texto_Proceso(Cod_Soc, Año, Tipo_Proceso, Nro_Doc, Item_Doc, Texto, Fecha_Reg, Hora_Reg, Usuario_Reg) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')''' %(Cod_Soc,Año,3,NroDoc,0,texto_cabecera,Fecha,Hora,Cod_Usuario)
                respuesta=ejecutarSql(sqlTextoCabecera)

                if respuesta['respuesta']=='correcto':
                    mensajeDialogo("informacion", "Información", "Texto de cabecera grabado correctamente")
                    del texto_cabecera
                    self.close()

                elif respuesta['respuesta']=='incorrecto':
                    mensajeDialogo("error", "Error", "El Texto de cabecera no se pudo grabar")

        else:
            mensajeDialogo("informacion", "Información", "Texto de cabecera grabado correctamente")
            self.close()

        self.teDetalle.setEnabled(False)
        self.pbGrabar.setEnabled(False)

    def Modificar(self):
        self.teDetalle.setEnabled(True)
        self.pbGrabar.setEnabled(True)

    def Salir(self):
        self.close()

class TextoPosicion(QDialog):
    def __init__(self,Nro_Ped,item_pos):
        QDialog.__init__(self)
        uic.loadUi('ERP_COMP_P001_Texto_Posicion.ui',self)

        global NroDoc,ItemDoc

        NroDoc=Nro_Ped
        ItemDoc=item_pos

        self.pbGrabar.clicked.connect(self.Grabar)
        self.pbModificar.clicked.connect(self.Modificar)
        self.pbSalir.clicked.connect(self.Salir)

        cargarIcono(self.pbGrabar,'grabar')
        cargarIcono(self.pbModificar,'modificar')
        cargarIcono(self.pbSalir,'salir')

        sqlText="SELECT Texto FROM TAB_SOC_019_Texto_Proceso WHERE Cod_Soc='%s'AND Año='%s' AND Tipo_Proceso='3' AND Nro_Doc='%s' AND Item_Doc='%s'"%(Cod_Soc,Año,NroDoc,ItemDoc)
        text= consultarSql(sqlText)

        if text!=[]:
            self.teDetalle.setText(text[0][0])
            self.teDetalle.setEnabled(False)
            self.pbGrabar.setEnabled(False)
        else:
            try:
                texto_item = dict_textoPosicion[ItemDoc]
                self.teDetalle.setPlainText(texto_item)
                self.teDetalle.setEnabled(False)
                self.pbGrabar.setEnabled(False)

            except Exception as e:
                print(e)


    def Grabar(self):

        texto_pos=self.teDetalle.toPlainText()
        k = ItemDoc
        v = texto_pos
        # print(texto_pos)
        dict_temp = {}
        dict_temp.setdefault(k,v)
        dict_textoPosicion.update(dict_temp)

        Hora=datetime.datetime.now().strftime("%H:%M:%S.%f")

        if NroDoc!="":

            sqlText="SELECT Texto FROM TAB_SOC_019_Texto_Proceso WHERE Cod_Soc='%s'AND Año='%s' AND Tipo_Proceso='3' AND Nro_Doc='%s' AND Item_Doc='%s'"%(Cod_Soc,Año,NroDoc,ItemDoc)
            text= consultarSql(sqlText)

            if text!=[]:
                sqlTextoPos="UPDATE TAB_SOC_019_Texto_Proceso SET Texto='%s',Fecha_Mod='%s',Hora_Mod='%s',Usuario_Mod='%s' WHERE Cod_Soc='%s' AND Año='%s' AND Tipo_Proceso='3' AND Nro_Doc='%s' AND Item_Doc='%s' "%(texto_pos,Fecha,Hora,Cod_Usuario,Cod_Soc,Año,NroDoc,ItemDoc)
                respuesta=ejecutarSql(sqlTextoPos)

                if respuesta['respuesta']=='correcto':
                    mensajeDialogo("informacion", "Información", "Texto de posición modificado con éxito")
                    dict_textoPosicion.clear()
                    self.close()

                elif respuesta['respuesta']=='incorrecto':
                    mensajeDialogo("error", "Error", "El Texto de posición no se pudo modificar")

            else:
                sqlTextoPos = '''INSERT INTO TAB_SOC_019_Texto_Proceso (Cod_Soc, Año, Tipo_Proceso, Nro_Doc, Item_Doc, Texto, Fecha_Reg, Hora_Reg, Usuario_Reg)
                VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s') ''' % (Cod_Soc, Año, 3, NroDoc, ItemDoc, texto_pos, Fecha, Hora, Cod_Usuario)
                respuesta = ejecutarSql(sqlTextoPos)

                if respuesta['respuesta']=='correcto':
                    mensajeDialogo("informacion", "Información", "Texto de posición grabado con éxito")
                    dict_textoPosicion.clear()
                    self.close()

                elif respuesta['respuesta']=='incorrecto':
                    mensajeDialogo("error", "Error", "El Texto de posición no se pudo grabar")
        else:
            mensajeDialogo("informacion", "Información", "Texto de posición grabado correctamente")
            self.close()

        self.teDetalle.setEnabled(False)
        self.pbGrabar.setEnabled(False)

    def Modificar(self):
        self.teDetalle.setEnabled(True)
        self.pbGrabar.setEnabled(True)

    def Salir(self):
        self.close()

class Pedido_de_Compra(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("ERP_PCOMP_001.ui",self)

        # self.pbImprimir.setEnabled(False)
        self.pbEnviar.setEnabled(False)

        global dicMoneda,dicPaisProv
        moneda=consultarSql(sqlMoneda)
        dicMoneda={}
        for m in moneda:
            dicMoneda[m[0]]=m[1]

        PaisProv=consultarSql(sqlProv)
        dicPaisProv={}
        for p in PaisProv:
            dicPaisProv[p[0]]=p[1]

        self.pbDat_Import.clicked.connect(self.Dat_Imp)
        self.pbCon_Cab.clicked.connect(self.Cond_Cab)
        self.pbInterlocutor.clicked.connect(self.Inter)
        self.pbText_Cab.clicked.connect(self.TextoCabecera)
        self.pbDepositos.clicked.connect(self.Depos)
        self.pbCon_Pos.clicked.connect(self.Cond_Pos)
        self.pbSalir.clicked.connect(self.Salir)
        self.pbImprimir.clicked.connect(self.Imprimir)
        self.pbEnviar.clicked.connect(self.Enviar)
        self.pbGrabar.clicked.connect(self.Grabar)

        self.pbDat_Import.setEnabled(False)
        self.pbCon_Cab.setEnabled(False)
        self.pbInterlocutor.setEnabled(False)
        # self.pbText_Cab.setEnabled(False)
        self.pbDepositos.setEnabled(False)
        self.pbCon_Pos.setEnabled(False)

        self.leEmpresa.setEnabled(False)
        self.cbNro_Cotizacion.setEnabled(False)
        self.cbProveedor.setEnabled(False)
        self.leRazon_Social.setEnabled(False)
        self.leFecha_Pedido.setEnabled(False)
        self.leNro_Pedido.setEnabled(False)
        self.leEstado.setEnabled(False)

        global dict_textoPosicion
        dict_textoPosicion = {}

    def datosCabecera(self,codsoc,nomsoc,codusuario,nrocotiza,razonsocial,codprov,montoaprobado,fecha_req):

        global Cod_Soc,Nom_Soc,Cod_Usuario,Nro_Cotiza,Razon_Social,Cod_Prov,Monto_Aprobado,Fecha_Req,Fecha,Año

        Cod_Soc=codsoc
        Cod_Usuario=codusuario
        Nom_Soc=nomsoc
        Nro_Cotiza=nrocotiza
        Razon_Social=razonsocial
        Cod_Prov=codprov
        Monto_Aprobado=montoaprobado
        Fecha_Req=fecha_req

        Fecha=datetime.datetime.now().strftime("%Y-%m-%d")
        now = datetime.datetime.now()
        Año=str(now.year)

        cargarLogo(self.lbLogo_Mp,'multiplay')
        cargarLogo(self.lbLogo_Soc, Cod_Soc)
        cargarIcono(self, 'erp')
        cargarIcono(self.pbGrabar, 'grabar')
        cargarIcono(self.pbImprimir, 'imprimir')
        cargarIcono(self.pbEnviar, 'enviar')
        cargarIcono(self.pbBaja, 'darbaja')
        cargarIcono(self.pbSalir, 'salir')
        cargarIcono(self.pbInterlocutor, 'usuario')
        cargarIcono(self.pbText_Cab, 'compra')
        # cargarIcono(self.pbText_Pos, 'compra')
        cargarIcono(self.pbDepositos, 'depositar')
        cargarIcono(self.pbDat_Import, 'importar')
        cargarIcono(self.pbCon_Cab, 'condicion')
        cargarIcono(self.pbCon_Pos, 'condicion')

        self.Inicio()

    def Inicio(self):

        global dicPlanta

        sqlOrgComp="SELECT Nomb_Comp,Cod_Org_Comp FROM TAB_SOC_004_Org_Compra WHERE Cod_Soc='%s'"%(Cod_Soc)
        OrgComp=consultarSql(sqlOrgComp)

        sqlCabPed='''SELECT a.Nro_Pedido, a.Año_Pedido, a.Tipo_Pedido, a.Fecha_Doc_Pedido, a.Nro_Solp, a.Estado_Pedido, b.Descrip_moneda
        FROM TAB_COMP_004_Pedido_Compra a
        LEFT JOIN TAB_SOC_008_Monedas b ON a.Moneda=b.Cod_moneda
        WHERE a.Cod_Emp='%s'AND a.Año_Pedido='%s' AND a.Nro_Pedido='%s';'''%(Cod_Soc,Año,Nro_Cotiza)
        CabPed=convlist(sqlCabPed)

        insertarDatos(self.cbOrg_Compra, OrgComp)

        self.leEmpresa.setText(Nom_Soc)
        self.cbNro_Cotizacion.addItem(Nro_Cotiza)
        self.cbProveedor.addItem(Cod_Prov)
        self.leRazon_Social.setText(Razon_Social)

        sqlCodPlanta="SELECT Cod_Planta,Nomb_Planta FROM TAB_SOC_002_Planta WHERE Cod_Soc='%s'"%(Cod_Soc)
        planta=consultarSql(sqlCodPlanta)
        dicPlanta={}
        for p in planta:
            dicPlanta[p[0]]=p[1]

        if CabPed!=[]:

            for k,v in dicTip_Ped.items():
                if CabPed[2]==k:
                    TipoPedido=v
            self.cbTipo_Pedido.addItem(TipoPedido)
            self.cbTipo_Pedido.setEnabled(False)

            self.leNro_Pedido.setText(CabPed[0])

            for k,v in dicEstado.items():
                if CabPed[5]==k:
                    EstadoPedido=v
            self.leEstado.setText(EstadoPedido)

            fecha=formatearFecha(CabPed[3])
            self.leFecha_Pedido.setText(fecha)

            self.cbOrg_Compra.setCurrentIndex(0)
            self.cbOrg_Compra.setEnabled(False)

            if TipoPedido=='Importaciones':
                self.pbDat_Import.setEnabled(True)

            self.pbCon_Cab.setEnabled(True)
            self.pbInterlocutor.setEnabled(True)
            # self.pbText_Cab.setEnabled(True)
            self.pbDepositos.setEnabled(True)
            self.pbCon_Pos.setEnabled(True)
            self.pbGrabar.setEnabled(False)

            sqlTabla ='''SELECT a.Cod_Mat, a.Descrp_Mat, a.Unid_Pedido, a.Cant_Pedido, a.Precio_Pedido,(a.Cant_Pedido*a.Precio_Pedido),b.Descrip_moneda, c.Nomb_Planta, d.Nomb_Alm, a.Lote_Mat
            FROM TAB_COMP_005_Detalle_Pedido_de_Compra a
            LEFT JOIN TAB_SOC_008_Monedas b ON a.Moneda=b.Cod_moneda
            LEFT JOIN TAB_SOC_002_Planta c ON a.Cod_Empresa=c.Cod_soc AND a.Cod_Planta=c.Cod_Planta
            LEFT JOIN TAB_SOC_003_Almacén d ON a.Cod_Empresa=d.Cod_Soc AND a.Cod_Planta=d.Cod_Planta AND a.Cod_Almacen=d.Cod_Alm
            WHERE a.Cod_Empresa='%s' AND a.Nro_Pedido='%s' AND a.Año_Pedido='%s';'''%(Cod_Soc,CabPed[0], Año)
            CargarPedComp(self,self.tbwPed_Comp,sqlTabla,Cod_Soc,Año,CabPed[0])

        else:
            self.cbOrg_Compra.setCurrentIndex(0)

            for v in dicTip_Ped.values():
                self.cbTipo_Pedido.addItem(v)

            if dicPaisProv[Cod_Prov]=='PERU':
                self.cbTipo_Pedido.setCurrentIndex(0)
            elif dicPaisProv[Cod_Prov]!='PERU':
                self.cbTipo_Pedido.setCurrentIndex(1)

            fecha=formatearFecha(Fecha)
            self.leFecha_Pedido.setText(fecha)

            sqlTabla = '''SELECT d.Cod_Mat, c.Descrip_Idioma, d.Unid_Cot, d.Cant_Asignada, d.Precio_Cotiza, (d.Cant_Asignada*d.Precio_Cotiza),m.Descrip_moneda, p.Nomb_Planta,n.Nomb_Alm
            FROM TAB_COMP_002_Detalle_Cotización_de_Compra d
            LEFT JOIN TAB_COMP_001_Cotización_Compra a ON d.Cod_Soc=a.Cod_Soc AND d.Año=a.Año AND d.Nro_Cotiza = a.Nro_Cotiza AND d.Cod_Prov=a.Cod_Prov
            LEFT JOIN TAB_MAT_011_Descripcion_Idiomas c ON d.Cod_Mat= c.Cod_Mat AND d.Cod_Idioma=c.Cod_Idioma
            LEFT JOIN TAB_SOLP_002_Detalle_Solicitud_Pedido s ON d.Año=s.Año AND d.Item_SOLP = s.Item_Solp AND d.Cod_Soc=s.Cod_Soc AND d.Cod_Mat=s.Cod_Mat AND s.Nro_Solp=a.Nro_Solp
            LEFT JOIN TAB_SOC_008_Monedas m ON s.Moneda=m.Cod_moneda
            LEFT JOIN TAB_SOC_002_Planta p ON s.Cod_Soc=p.Cod_soc AND s.Centro=p.Cod_Planta
            LEFT JOIN TAB_SOC_003_Almacén n ON s.Cod_Soc=n.Cod_Soc AND s.Centro=n.Cod_Planta AND s.Almacen=n.Cod_Alm
            WHERE d.Cod_Soc='%s' AND d.Año='%s' AND d.Nro_Cotiza='%s' AND d.Cod_Prov='%s' AND d.Estado_Item='8' AND a.Estado_Tipo='8';''' %(Cod_Soc, Año, Nro_Cotiza, Cod_Prov)
            CargarPedComp(self,self.tbwPed_Comp,sqlTabla,Cod_Soc,Año,"")

    def Grabar(self):
        global texto_cabecera

        try:
            descrip_tipo_pedido=self.cbTipo_Pedido.currentText()
            for k,v in dicTip_Ped.items():
                if descrip_tipo_pedido==v:
                    Tipo_pedido=k

            sqlNroSolp="SELECT a.Nro_Solp FROM TAB_COMP_002_Detalle_Cotización_de_Compra d LEFT JOIN TAB_COMP_001_Cotización_Compra a ON (d.Cod_Soc=a.Cod_Soc AND d.Año=a.Año AND d.Nro_Cotiza = a.Nro_Cotiza AND d.Cod_Prov=a.Cod_Prov) WHERE d.Cod_Soc='%s' AND d.Año='%s' AND d.Nro_Cotiza='%s' AND d.Cod_Prov='%s' AND d.Estado_Item='8' AND a.Estado_Tipo='8'"%(Cod_Soc, Año, Nro_Cotiza, Cod_Prov)
            NroSolp=convlist(sqlNroSolp)

            Hora=datetime.datetime.now().strftime("%H:%M:%S.%f")

            if len(Tipo_pedido)!=0:

                sqlCodProv="SELECT Cod_Actual FROM TAB_SOC_018_Rango_de_Números_de_Documentos_de_procesos WHERE Cod_Soc='%s'AND Tipo_Rango ='03'AND Año_Rango='%s'"%(Cod_Soc,Año)
                Cod_Actual=convlist(sqlCodProv)
                self.leNro_Pedido.setText(Cod_Actual[0])
                Nro_Pedido=self.leNro_Pedido.text()
                Estado_Pedido='1'
                self.leEstado.setText('Proceso Emisión')

                sqlDatosCab='''SELECT Moneda, Monto_Desc, Descuento, Forma_Pago, Cuotas_Credito, Monto_deposito, Fecha_deposito, Banco_deposito, Cuenta_Banco, Tiempo_Garantia, Forma_Garantia,Forma_Envio,FValidez_oferta
                FROM TAB_COMP_001_Cotización_Compra
                WHERE Cod_Soc='%s' AND Año='%s' AND Cod_Prov='%s' AND Nro_Cotiza='%s';'''%(Cod_Soc, Año, Cod_Prov, Nro_Cotiza)
                DatosCab=convlist(sqlDatosCab)

                moneda=DatosCab[0]
                montodesc=DatosCab[1]
                descuento=DatosCab[2]
                formapago=DatosCab[3]
                cuotascredito=DatosCab[4]
                montodeposito=DatosCab[5]
                fechadeposito=DatosCab[6]
                bancodeposito=DatosCab[7]
                cuentabanco=DatosCab[8]
                tiempogarantia=DatosCab[9]
                formagarantia=DatosCab[10]

                sqlCabecera_PedComp='''INSERT INTO TAB_COMP_004_Pedido_Compra(Cod_Emp, Nro_Pedido, Año_Pedido, Tipo_Pedido, Cod_Prov, Nro_Cotiza, Fecha_Doc_Pedido, Nro_Solp, Estado_Pedido, Moneda, Monto_Desc, Descuento, Forma_Pago, Cuotas_Credito, Monto_deposito, Fecha_deposito, Banco_deposito, Cuenta_Banco, Tiempo_garantia, Forma_Garantia, Fecha_Reg, Hora_Reg, Usuario_Reg)
                VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')''' %(Cod_Soc,Nro_Pedido,Año,Tipo_pedido,Cod_Prov,Nro_Cotiza,Fecha,NroSolp[0],Estado_Pedido,moneda,montodesc,descuento,formapago,cuotascredito,montodeposito,fechadeposito,bancodeposito,cuentabanco,tiempogarantia,formagarantia,Fecha,Hora,Cod_Usuario)
                respuesta=ejecutarSql(sqlCabecera_PedComp)

                self.pbCon_Cab.setEnabled(True)
                self.pbInterlocutor.setEnabled(True)
                self.pbDepositos.setEnabled(True)
                self.pbCon_Pos.setEnabled(True)
                self.pbGrabar.setEnabled(False)
                self.cbTipo_Pedido.setEnabled(False)
                self.cbOrg_Compra.setEnabled(False)

                if descrip_tipo_pedido=='Importaciones':
                    self.pbDat_Import.setEnabled(True)

                try:
                    # Texto Cabecera para la Nota de Ingreso
                    if texto_cabecera != None:
                        sqlTextoCabecera='''INSERT INTO TAB_SOC_019_Texto_Proceso(Cod_Soc, Año, Tipo_Proceso, Nro_Doc, Item_Doc, Texto, Fecha_Reg, Hora_Reg, Usuario_Reg) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')''' %(Cod_Soc,Año,3,Nro_Pedido,0,texto_cabecera,Fecha,Hora,Cod_Usuario)
                        info=ejecutarSql(sqlTextoCabecera)
                except Exception as e:
                    print(e)

                sqlItemCotiza = '''SELECT d.Item_Cotiza FROM TAB_COMP_002_Detalle_Cotización_de_Compra d LEFT JOIN TAB_COMP_001_Cotización_Compra a ON (d.Cod_Soc=a.Cod_Soc AND d.Año=a.Año AND d.Nro_Cotiza = a.Nro_Cotiza AND d.Cod_Prov=a.Cod_Prov)
                WHERE d.Cod_Soc='%s' AND d.Año='%s' AND d.Nro_Cotiza='%s' AND d.Cod_Prov='%s' AND d.Estado_Item='8' AND a.Estado_Tipo='8';''' % (Cod_Soc, Año, Nro_Cotiza, Cod_Prov)
                ItemCotiza=convlist(sqlItemCotiza)

                d=self.tbwPed_Comp.rowCount()
                for row in range(d):

                    #Detalles de solicitud de pedido
                    Item_Cotiza=ItemCotiza[row]
                    Item=self.tbwPed_Comp.item(row,0).text()
                    Cod_Mat=self.tbwPed_Comp.item(row,1).text()
                    Descripcion=self.tbwPed_Comp.item(row,2).text()
                    Unidad=self.tbwPed_Comp.item(row,3).text()
                    Cantidad=self.tbwPed_Comp.item(row,4).text().replace(",","")
                    Precio=self.tbwPed_Comp.item(row,5).text().replace(",","")
                    Valor=self.tbwPed_Comp.item(row,6).text().replace(",","")

                    NombreM=self.tbwPed_Comp.item(row,7).text()
                    for k,v in dicMoneda.items():
                        if NombreM==v:
                            Moneda=k

                    NombreCentro=self.tbwPed_Comp.item(row,8).text()
                    for k,v in dicPlanta.items():
                        if NombreCentro==v:
                            Centro=k

                    sqlComp="SELECT Nomb_Alm,Cod_Alm FROM TAB_SOC_003_Almacén WHERE Cod_Soc='%s' AND Cod_Planta='%s'" %(Cod_Soc,Centro)
                    alm=consultarSql(sqlComp)

                    diccAlmacen={}
                    for a in alm:
                        diccAlmacen[a[1]]=a[0]

                    NombreAlmacen=self.tbwPed_Comp.item(row,9).text()
                    for k,v in diccAlmacen.items():
                        if NombreAlmacen==v:
                            Almacen=k
                    try:
                        Lote=self.tbwPed_Comp.item(row,10).text()
                    except:
                        Lote=''

                    Good_Recep='1'

                    ## Texto posición
                    try:
                        textoposicion = dict_textoPosicion[Item]
                        sqlTextoPos = '''INSERT INTO TAB_SOC_019_Texto_Proceso (Cod_Soc, Año, Tipo_Proceso, Nro_Doc, Item_Doc, Texto, Fecha_Reg, Hora_Reg, Usuario_Reg)
                        VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s') ''' % (Cod_Soc, Año, 3, Nro_Pedido, Item, textoposicion, Fecha, Hora, Cod_Usuario)
                        infoTexto = ejecutarSql(sqlTextoPos)
                        actualizarboton2(self,self.tbwPed_Comp,Cod_Soc,Año,Nro_Pedido,Item,row)
                    except Exception as e:
                        print(e)

                    sqlDetalle='''INSERT INTO TAB_COMP_005_Detalle_Pedido_de_Compra(Cod_Empresa, Nro_Pedido, Año_Pedido, Item_Pedido, Cod_Mat, Descrp_Mat, Unid_Pedido, Nro_Cotiza,Item_Cotiza, Nro_Solp, Cant_Pedido, Precio_Pedido, Moneda, Cod_Planta, Cod_Almacen, Lote_Mat, Good_Recep, Estado_Pedido, Fecha_Reg, Hora_Reg, Usuario_Reg)
                    VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')''' %(Cod_Soc,Nro_Pedido,Año,Item,Cod_Mat,Descripcion,Unidad,Nro_Cotiza,Item_Cotiza, NroSolp[0],Cantidad,Precio,Moneda,Centro,Almacen,Lote,Good_Recep,Estado_Pedido,Fecha,Hora,Cod_Usuario)
                    respuesta=ejecutarSql(sqlDetalle)

                    sqlSelect="SELECT Stock_Transito_Compra,Cod_Mat FROM TAB_MAT_002_Stock_Almacen WHERE Cod_Soc='%s' AND Cod_Planta='%s' AND Cod_Alm='%s' AND Cod_Mat='%s';"%(Cod_Soc,Centro,Almacen,Cod_Mat)
                    select=convlist(sqlSelect)
                    print(select)
                    if select!=[]:
                        if select[0]=='0.000':
                            sqlUpdate="UPDATE TAB_MAT_002_Stock_Almacen SET Stock_Transito_Compra='%s',Fecha_Mod='%s',Hora_Mod='%s',Usuario_Mod='%s' WHERE Cod_Soc='%s' AND Cod_Planta='%s' AND Cod_Alm='%s' AND Cod_Mat='%s';"%(Cantidad,Fecha,Hora,Cod_Usuario,Cod_Soc,Centro,Almacen,Cod_Mat)
                        else:
                            NuevoStock=float(select[0])+float(Cantidad)
                            sqlUpdate="UPDATE TAB_MAT_002_Stock_Almacen SET Stock_Transito_Compra='%s',Fecha_Mod='%s',Hora_Mod='%s',Usuario_Mod='%s' WHERE Cod_Soc='%s' AND Cod_Planta='%s' AND Cod_Alm='%s' AND Cod_Mat='%s';"%(NuevoStock,Fecha,Hora,Cod_Usuario,Cod_Soc,Centro,Almacen,Cod_Mat)
                        ejecutarSql(sqlUpdate)
                    else:
                        sqlInsert="INSERT INTO TAB_MAT_002_Stock_Almacen(Cod_Soc, Cod_Planta, Cod_Alm, Cod_Mat, Stock_Transito_Compra,Fecha_Reg, Hora_Reg, Usuario_Reg) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%(Cod_Soc,Centro,Almacen,Cod_Mat,Cantidad,Fecha,Hora,Cod_Usuario)
                        ejecutarSql(sqlInsert)

                if respuesta['respuesta']=='correcto':
                    self.pbImprimir.setEnabled(True)
                    mensajeDialogo("informacion", "Información", "El pedido de Compra se ha grabado correctamente")
                    Cod_Actual[0]=int(Cod_Actual[0])
                    Cod_Actual=str(Cod_Actual[0]+1)

                    sqlCodActual="UPDATE TAB_SOC_018_Rango_de_Números_de_Documentos_de_procesos SET Cod_Actual='%s' WHERE Cod_Soc='%s' AND Tipo_Rango ='03' AND Año_Rango='%s'" %(Cod_Actual,Cod_Soc,Año)
                    ejecutarSql(sqlCodActual)
                    self.limpiar()

                elif respuesta['respuesta']=='incorrecto':
                    mensajeDialogo("error", "Error", "Ocurrio un problema, comuniquese con soporte")


            else:
                mensajeDialogo("error", "Error", "Faltan llenar datos")

        except Exception as e:
            mensajeDialogo("error", "Error", "Faltan llenar todos los datos")
            print(e)

    def limpiar(self):
        global texto_cabecera, dict_textoPosicion
        texto_cabecera = None
        del texto_cabecera
        dict_textoPosicion = {}

    def Imprimir(self):
        global ruta_Pdf

        sqlDatosCab='''SELECT b.Descrip_moneda, a.Monto_Desc, a.Descuento, e.Descrip_Pago, a.Cuotas_Credito, a.Monto_deposito, a.Fecha_deposito, c.Descrip_Banco, a.Cuenta_Banco, a.Tiempo_Garantia, a.Forma_Garantia,d.Descrip_Envio, a.FValidez_oferta
        FROM TAB_COMP_001_Cotización_Compra a
        LEFT JOIN TAB_SOC_008_Monedas b ON a.Moneda=b.Cod_moneda
        LEFT JOIN TAB_SOC_016_Tipo_de_Bancos c ON a.Banco_deposito=c.Cod_Banco
        LEFT JOIN `TAB_SOC_025: Forma de Envío` d ON a.Forma_Envio=d.Forma_Envio
        LEFT JOIN `TAB_SOC_024: Forma de pago` e ON a.Forma_Pago=e.Forma_Pago
        WHERE a.Cod_Soc='%s' AND a.Año='%s' AND a.Cod_Prov='%s' AND a.Nro_Cotiza='%s';'''%(Cod_Soc, Año, Cod_Prov, Nro_Cotiza)
        DatosCab=convlist(sqlDatosCab)

        sqlFecha_Entrega='''SELECT MAX(Fecha_Ent_Prov)
        FROM TAB_COMP_002_Detalle_Cotización_de_Compra
        WHERE Cod_Soc='%s' AND Año='%s' AND Cod_Prov='%s' AND Nro_Cotiza='%s';'''%(Cod_Soc, Año, Cod_Prov, Nro_Cotiza)
        FechaEntrega=convlist(sqlFecha_Entrega)

        Nro_Pedido=self.leNro_Pedido.text()

        sqlTexCab="SELECT Texto FROM TAB_SOC_019_Texto_Proceso WHERE Cod_Soc='%s' AND Año='%s' AND Tipo_Proceso='3' AND Nro_Doc='%s' AND Item_Doc='0'"%(Cod_Soc,Año,Nro_Pedido)
        TexCab=convlist(sqlTexCab)

        try:
            list_item = []
            list_descripcion = []
            list_unid = []
            list_cantidad = []
            list_precio = []
            list_total = []
            list_moneda = []


            for i in range(self.tbwPed_Comp.rowCount()):
                try:
                    list_item.append(self.tbwPed_Comp.item(i,0).text())
                except:
                    list_item.append("")
                try:
                    list_descripcion.append(self.tbwPed_Comp.item(i,2).text())
                except:
                    list_descripcion.append("")
                try:
                    list_unid.append(self.tbwPed_Comp.item(i,3).text())
                except:
                    list_unid.append("")
                try:
                    list_cantidad.append(self.tbwPed_Comp.item(i,4).text())
                except:
                    list_cantidad.append("")
                try:
                    list_precio.append(self.tbwPed_Comp.item(i,5).text())
                except:
                    list_precio.append("")
                try:
                    list_total.append(self.tbwPed_Comp.item(i,6).text())
                except:
                    list_total.append("")

            print("LISTA 1: ",list_item)
            print("LISTA 2: ",list_descripcion)
            print("LISTA 3: ",list_unid)
            print("LISTA 4: ",list_cantidad)
            print("LISTA 5: ",list_precio)
            print("LISTA 6: ",list_total)

            df = pd.DataFrame()
            df['1'] = list_item
            df['2'] = list_descripcion
            df['3'] = list_unid
            df['4'] = list_cantidad
            df['5'] = list_precio
            df['6'] = list_total

            title = 'PEDIDO DE COMPRA NRO. : ' + Nro_Pedido

            class PDF(FPDF):
                def header(self):
                    self.image('Logos/LogoMp_st.png', 20, 10, 55)
                    self.image('Logos/Logo'+ Cod_Soc +'.png', 222, 10, 55)
                    self.set_font('Arial', 'B', 13)
                    ## Posición del título en el centro
                    w = self.get_string_width(title) + 6
                    self.set_xy((297 - w) / 2, 20)
                    self.set_text_color(0, 0, 0)
                    self.cell(w, 9, title, 0, 1, 'C')
                    ## espacio vertical
                    self.ln(5)
                    ## espacio horizontal
                    self.cell(10)
                    ## Texto Encabezado
                    self.set_font('Arial', 'B', 10)
                    self.set_text_color(0, 0, 0)
                    ## Primera Fila Encabezado
                    self.cell(40, 8, "Ref. Cotización : ", 0, 0,'L')
                    self.cell(30, 8, Nro_Cotiza, 0, 0,'C')
                    self.cell(30)
                    self.cell(30, 8, "Fecha Req. : ", 0, 0,'L')
                    self.cell(30, 8, formatearFecha(Fecha_Req), 0, 0,'C')
                    self.cell(30)
                    self.cell(30, 8, "Fecha Entrega : ", 0, 0,'L')
                    self.cell(37, 8, formatearFecha(FechaEntrega[0]), 0, 2,'C')
                    ## Segunda Fila Encabezado
                    self.cell(-220)
                    self.cell(40, 8, "Proveedor : ", 0, 0,'L')
                    self.cell(130, 8, Razon_Social, 0, 0,'L')
                    self.cell(20)
                    self.cell(30, 8, "Validez Oferta : ", 0, 0,'L')
                    self.cell(37, 8, formatearFecha(DatosCab[12]), 0, 2,'C')
                    ## Tercera Fila Encabezado
                    self.cell(-220)
                    self.cell(40, 8, "Forma Pago : ", 0, 0,'L')
                    self.cell(30, 8, DatosCab[3], 0, 0,'C')
                    self.cell(30)
                    self.cell(30, 8, "Cuotas : ", 0, 0,'L')
                    self.cell(30, 8, DatosCab[4], 0, 0,'C')
                    self.cell(30)
                    self.cell(30, 8, "Monto Depósito : ", 0, 0,'L')
                    self.cell(37, 8, formatearDecimal(Monto_Aprobado,'2'), 0, 2,'C')
                    ## Cuarta Fila Encabezado
                    self.cell(-220)
                    self.cell(40, 8, "Forma de Envío : ", 0, 0,'L')
                    self.cell(30, 8, DatosCab[11], 0, 0,'C')
                    self.cell(30)
                    self.cell(30, 8, "Moneda : ", 0, 0,'L')
                    self.cell(30, 8, DatosCab[0], 0, 0,'C')
                    self.cell(30)
                    self.cell(30, 8, "Garantía : ", 0, 0,'L')
                    self.cell(37, 8, DatosCab[9]+' '+DatosCab[10], 0, 2,'C')
                    ## Quinta Fila Encabezado
                    self.cell(-220)
                    self.cell(40, 8, "Banco : ", 0, 0,'L')
                    self.cell(30, 8, DatosCab[7], 0, 0,'L')
                    self.cell(30)
                    self.cell(30, 8, "Cuenta : ", 0, 0,'L')
                    self.cell(30, 8, DatosCab[8], 0, 0,'C')
                    self.cell(30)
                    ## espacio vertical
                    self.ln(10)

                def footer(self):
                    ## Position at 1.5 cm from bottom
                    self.set_y(-15)
                    self.set_font('Arial', 'I', 8)
                    self.set_text_color(128)
                    ## Número de Página
                    self.cell(0, 10, 'Página ' + str(self.page_no()), 0, 0, 'C')

            # pdf = PDF('P', 'mm', (210, 297))
            pdf = PDF('L')
            pdf.add_page()
            pdf.set_xy(0,0)
            pdf.set_font('arial', 'B', 9)
            # pdf.set_auto_page_break(True, 0.5)
            # pdf.cell(75, 10, " ", 0, 2, 'C')
            pdf.ln(80)
            pdf.set_fill_color(255, 213, 79)
            pdf.cell(10, 10, 'Item', 1, 0, 'C', 1)
            pdf.cell(187, 10, 'Material', 1, 0, 'C', 1)
            pdf.cell(10, 10, 'UB', 1, 0, 'C', 1)
            pdf.cell(20, 10, 'Cantidad', 1, 0, 'C', 1)
            pdf.cell(25, 10, 'Precio', 1, 0, 'C', 1)
            pdf.cell(25, 10, 'Total', 1, 2, 'C', 1)
            pdf.cell(-252)
            pdf.set_font('arial', '', 9)
            for i in range(0, len(df)):
                pdf.cell(10, 8, '%s' % (df['1'].iloc[i]), 1, 0, 'C')
                pdf.cell(187, 8, '%s' % (df['2'].iloc[i]), 1, 0, 'C')
                pdf.cell(10, 8, '%s' % (df['3'].iloc[i]), 1, 0, 'C')
                pdf.cell(20, 8, '%s' % (df['4'].iloc[i]), 1, 0, 'C')
                pdf.cell(25, 8, '%s' % (df['5'].iloc[i]), 1, 0, 'C')
                pdf.cell(25, 8, '%s' % (df['6'].iloc[i]), 1, 2, 'C')

                pdf.cell(-252)

            # pdf.ln(60)
            pdf.ln(10)
            if TexCab==[]:
                pdf.ln(50)
            else:
                pdf.set_font('Arial', 'B', 9)
                pdf.cell(27, 8, "Observaciones: ", 0, 0,'L')
                pdf.set_font('Arial', '', 9)
                # pdf.cell(25, 8, "", 0, 0,'L')
                pdf.cell(250, 8, TexCab[0], 0, 2,'L')
                pdf.ln(35)
            pdf.set_font('Arial', 'B', 9)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(277, 5, '----------------------------------------------', 0, 2, 'C') # los guiones ocupan los 50mm
            pdf.cell(277, 5, 'Firma', 0, 2, 'C')
            pdf.cell(277, 5, 'Jefe de Ventas', 0, 0, 'C')
            root = tk.Tk()
            root.withdraw()

            ruta_Carpeta=crearCarpeta("PEDIDOS DE COMPRA")
            ruta_Pdf=ruta_Carpeta+'Pedido de Compra ' + Nro_Pedido + '.pdf'
            print(ruta_Pdf)
            if ruta_Pdf !="":
                pdf.output(ruta_Pdf, 'F')
                self.pbEnviar.setEnabled(True)
                reply = mensajeDialogo("pregunta", "Pregunta","Reporte PDF Generado con éxito, ¿Desea abrir el archivo?")
                if reply == 'Yes':
                    abrirArchivo(ruta_Pdf)

        except Exception as e:
            mensajeDialogo("error", "Error", "Reporte Fallido")
            print(e)

    def Enviar(self):
        try:
            Hora=datetime.datetime.now().strftime("%H:%M:%S.%f")
            Nro_Pedido=self.leNro_Pedido.text()
            Estado_pedido='2'

            sql="SELECT Correo_Inter FROM TAB_COMP_013_Pedido_de_Compra_Interlocutor WHERE Cod_Empresa='%s' AND Año_Pedido='%s' AND Nro_Pedido='%s';"%(Cod_Soc,Año,Nro_Pedido)
            correo=convlist(sql)
            sqlUsuario="SELECT Correo FROM TAB_SOC_005_Usuarios WHERE Cod_Soc='%s' AND Cod_usuario='%s';"%(Cod_Soc,Cod_Usuario)
            mailUsuario=convlist(sqlUsuario)
            if correo != []:
                EnviarCorreo(correo[0],ruta_Pdf,"Pedido de Compra","Atte. Multiplay")
                EnviarCorreo(mailUsuario[0],ruta_Pdf,"Pedido de Compra","Atte. Multiplay")
                sqlCab="UPDATE TAB_COMP_004_Pedido_Compra SET Estado_Pedido='%s', Fecha_Mod='%s',Hora_Mod='%s',Usuario_Mod='%s' WHERE Cod_Emp='%s' AND Año_Pedido='%s' AND Nro_Pedido='%s';"%(Estado_pedido,Fecha,Hora,Cod_Usuario,Cod_Soc,Año,Nro_Pedido)
                ejecutarSql(sqlCab)
                sqlDet="UPDATE TAB_COMP_005_Detalle_Pedido_de_Compra SET Estado_Pedido='%s',Fecha_Mod='%s',Hora_Mod='%s',Usuario_Mod='%s' WHERE Cod_Empresa='%s' AND Año_Pedido='%s' AND Nro_Pedido='%s';"%(Estado_pedido,Fecha,Hora,Cod_Usuario,Cod_Soc,Año,Nro_Pedido)
                ejecutarSql(sqlDet)
                self.leEstado.setText('Enviado a Prov.')
                mensajeDialogo("informacion", "Información", "El Documento fue enviado con éxito")
            else:
                mensajeDialogo("error", "Error", "No se pudo enviar el correo")
        except Exception as e:
            mensajeDialogo("error", "Error", "No se pudo enviar el correo")
            print(e)

    def Dat_Imp(self):
        Descrip_Tipo_Pedido=self.cbTipo_Pedido.currentText()
        Nro_Pedido=self.leNro_Pedido.text()
        Estado_Pedido=self.leEstado.text()
        orgcomp=self.cbOrg_Compra.currentText()
        self.di=Datos_Importacion()
        self.di.datosCabecera(Cod_Soc,Cod_Usuario,Nro_Cotiza,Razon_Social,Cod_Prov,Nro_Pedido,Descrip_Tipo_Pedido,Nom_Soc,orgcomp,Estado_Pedido)
        self.di.showMaximized()

    def Cond_Cab(self):
        Descrip_Tipo_Pedido=self.cbTipo_Pedido.currentText()
        Nro_Pedido=self.leNro_Pedido.text()
        Estado_Pedido=self.leEstado.text()
        orgcomp=self.cbOrg_Compra.currentText()
        self.cc=Condiciones_Cabecera()
        self.cc.datosCabecera(Cod_Soc,Cod_Usuario,Nro_Cotiza,Razon_Social,Cod_Prov,Nro_Pedido,Descrip_Tipo_Pedido,Nom_Soc,orgcomp,Estado_Pedido)
        self.cc.showMaximized()

    def Inter(self):
        Descrip_Tipo_Pedido=self.cbTipo_Pedido.currentText()
        Nro_Pedido=self.leNro_Pedido.text()
        Estado_Pedido=self.leEstado.text()
        orgcomp=self.cbOrg_Compra.currentText()
        self.int=Interlocutor()
        self.int.datosCabecera(Cod_Soc,Cod_Usuario,Nro_Cotiza,Razon_Social,Cod_Prov,Nro_Pedido,Descrip_Tipo_Pedido,Nom_Soc,orgcomp,Estado_Pedido)
        self.int.showMaximized()

    def Depos(self):
        Descrip_Tipo_Pedido=self.cbTipo_Pedido.currentText()
        Nro_Pedido=self.leNro_Pedido.text()
        Estado_Pedido=self.leEstado.text()
        orgcomp=self.cbOrg_Compra.currentText()
        self.de=Depositos()
        self.de.datosCabecera(Cod_Soc,Cod_Usuario,Nro_Cotiza,Razon_Social,Cod_Prov,Nro_Pedido,Descrip_Tipo_Pedido,Nom_Soc,orgcomp,Estado_Pedido,Monto_Aprobado)
        self.de.showMaximized()

    def Cond_Pos(self):
        try:
            Item=self.tbwPed_Comp.item(self.tbwPed_Comp.currentRow(),0).text()
            Precio=self.tbwPed_Comp.item(self.tbwPed_Comp.currentRow(),5).text()
            Valor=self.tbwPed_Comp.item(self.tbwPed_Comp.currentRow(),6).text()
            Moneda=self.tbwPed_Comp.item(self.tbwPed_Comp.currentRow(),7).text()
            Descrip_Tipo_Pedido=self.cbTipo_Pedido.currentText()
            Nro_Pedido=self.leNro_Pedido.text()
            Estado_Pedido=self.leEstado.text()
            orgcomp=self.cbOrg_Compra.currentText()
            self.cp=Condiciones_Posicion()
            self.cp.datosCabecera(Cod_Soc,Cod_Usuario,Nro_Cotiza,Razon_Social,Cod_Prov,Nro_Pedido,Descrip_Tipo_Pedido,Nom_Soc,orgcomp,Estado_Pedido,Item,Precio,Valor,Moneda)
            self.cp.showMaximized()
        except Exception as e:
            mensajeDialogo("error", "Error", "No se selecciono ninguna posición, verifique")
            print(e)

    def TextoCabecera(self):
        try:
            Nro_Ped=self.leNro_Pedido.text()
            TextoCabecera(Nro_Ped).exec_()
        except Exception as e:
            mensajeDialogo("error", "Error", "Ocurrio un error, comuniquese con soporte")
            print(e)


    def TextoPosicion(self):
        try:
            fila=self.tbwPed_Comp.currentRow()
            Nro_Ped=self.leNro_Pedido.text()
            item_pos=self.tbwPed_Comp.item(fila,0).text()
            TextoPosicion(Nro_Ped,item_pos).exec_()
            actualizarboton2(self,self.tbwPed_Comp,Cod_Soc,Año,Nro_Ped,item_pos,fila)
        except Exception as e:
            mensajeDialogo("error", "Error", "Complete los Campos")
            print(e)

    def Salir(self):
        self.close()

if __name__ == '__main__':
    app=QApplication(sys.argv)
    _main=Pedido_de_Compra()
    _main.showMaximized()
    app.exec_()
