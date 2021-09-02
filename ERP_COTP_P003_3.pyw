### Programa: ERP_COTP_P003 Evaluar Oferta de Proveedores
### Título: Evaluar Ofertas Enviadas por los proveedores en ERP
### Descripción: Programa que permite evaluar las ofertas de los proveedores
### Versión: V1
### Tablas empleadas: TAB_SOLP_001, TAB_SOLP_002, TAB_SOC_005, TAB_SOC_010, TAB_SOC_018, TAB_SOC_019, TAB_COMP_001, TAB_COMP_002
### Programador: Sleiter S. Ramos Sanchez

import sys
import requests
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtGui import *
from funciones_05 import *
import urllib.request
import time
import pandas as pd
from pylab import *
from fpdf import FPDF
import tkinter as tk
from tkinter import filedialog
# from decimal import Decimal

# dict_garantia
dict_garantia = {'1':"Años", '2':"Meses", '3':"Días"}

sqlFormaPago = '''SELECT Forma_Pago, Descrip_Pago FROM `TAB_SOC_024: Forma de pago`'''
infoFormaPago = consultarSql(sqlFormaPago)
formaPago = []
for info in infoFormaPago:
    for elemento in info:
        formaPago.append(elemento)
# print(formaPago) # lista
dict_formaPago = {}
for index, item in enumerate(formaPago):
    if index % 2 == 0:
        dict_formaPago[item] = formaPago[index+1]
# print(dict_formaPago) # diccionario

sqlMedioEntrega = '''SELECT Forma_Envio, Descrip_Envio FROM `TAB_SOC_025: Forma de Envío`'''
infoMedioEntrega = consultarSql(sqlMedioEntrega)
medioEntrega = []
for info in infoMedioEntrega:
    for elemento in info:
        medioEntrega.append(elemento)
# print(medioEntrega) # lista
dict_medioEntrega = {}
for index, item in enumerate(medioEntrega):
    if index % 2 == 0:
        dict_medioEntrega[item] = medioEntrega[index+1]
# print(dict_medioEntrega) # diccionario

# global dict_materiales
sqlMateriales = '''SELECT Cod_Mat, CONCAT(Uni_Base, ",", Descrip_Mat) FROM TAB_MAT_001_Catalogo_Materiales'''
infoMat = consultarSql(sqlMateriales)
materiales = []
for info in infoMat:
    for elemento in info:
        materiales.append(elemento)
# print(materiales) # lista
dict_materiales = {}
for index, item in enumerate(materiales):
    if index % 2 == 0:
        dict_materiales[item] = materiales[index+1]
# print(dict_materiales) # diccionario

# global dict_cond_pago
sqlCondPago = '''SELECT Cond_Pago, Descrip_cond FROM `TAB_COM_003_Condiciones de Pago por Clientes`'''
infoCondPago = consultarSql(sqlCondPago)
cond_pago = []
for info in infoCondPago:
    for elemento in info:
        cond_pago.append(elemento)
# print(cond_pago) # lista
dict_cond_pago = {}
for index, item in enumerate(cond_pago):
    if index % 2 == 0:
        dict_cond_pago[item] = cond_pago[index+1]
# print(dict_cond_pago) # diccionario

# global dict_bancos
sqlBancos = '''SELECT Cod_Banco, Descrip_Banco FROM TAB_SOC_016_Tipo_de_Bancos'''
infoBancos = consultarSql(sqlBancos)
bancos = []
for info in infoBancos:
    for elemento in info:
        bancos.append(elemento)
# print(bancos) # lista
dict_bancos = {}
for index, item in enumerate(bancos):
    if index % 2 == 0:
        dict_bancos[item] = bancos[index+1]
# print(dict_bancos) # diccionario

# global dict_monedas
sqlMonedas = '''SELECT Cod_moneda, Descrip_moneda FROM TAB_SOC_008_Monedas'''
infoMonedas = consultarSql(sqlMonedas)
monedas = []
for info in infoMonedas:
    for elemento in info:
        monedas.append(elemento)
# print(monedas) # lista
dict_monedas = {}
for index, item in enumerate(monedas):
    if index % 2 == 0:
        dict_monedas[item] = monedas[index+1]
# print(dict_monedas) # diccionario

sqlSolp = '''SELECT CONCAT(Cod_Soc, Año, Nro_Cotiza), Nro_Solp FROM TAB_COMP_001_Cotización_Compra'''
infoNroSolp = consultarSql(sqlSolp)
dict_nroSolp = {}
for cot in infoNroSolp:
    dict_nroSolp[cot[0]] = cot[1]
# print(dict_nroSolp)

class Texto_Cabecera(QDialog):
    def __init__(self, cod_soc, nro_cotizacion):
        QDialog.__init__(self)
        uic.loadUi("ERP_TextoCabecera.ui",self)
        self.pbSalir.clicked.connect(self.close)
        self.llenarTexto(cod_soc, nro_cotizacion)

    def llenarTexto(self, cod_soc, nro_cotizacion):
        # try:
        nro_solp = dict_nroSolp[cod_soc+año+nro_cotizacion]
        sql = '''SELECT Texto FROM TAB_SOC_019_Texto_Proceso
        WHERE Cod_Soc='%s' AND Tipo_Proceso='1' AND Nro_Doc='%s' AND Item_Doc='0';''' %(cod_soc, nro_solp)
        infoTexto = consultarSql(sql)
        self.txtedTexto_Cabecera.setPlainText(infoTexto[0][0])
        # except:
        #    self.txtedTexto_Cabecera.setPlainText("")

class ERP_COTP_P003_3(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        uic.loadUi("ERP_PCOTP_004_2.ui",self)
        header_view = self.tbwDatos_Cot_Prov.horizontalHeader()
        header_view.setSectionResizeMode(QHeaderView.ResizeToContents)
        # item1 = QTableWidgetItem('red')
        # item1.setBackground(QBrush(QColor(255, 0, 0)))
        # self.tbwDatos_Cot_Prov.setHorizontalHeaderItem(0,item1)
        self.pbListar.clicked.connect(self.listar)
        self.pbGrabar.clicked.connect(self.grabar2)
        self.pbTexto_Cabecera.clicked.connect(self.textoCabecera)
        self.pbAsignarBP_Todo.clicked.connect(self.asignarBP_Todo)
        self.pbSalir.clicked.connect(self.close)

        cargarLogo(self.lbLogo_Mp, 'multiplay')
        cargarIcono(self.pbGrabar, 'guardar')
        cargarIcono(self.pbListar, 'imprimir')
        cargarIcono(self.pbAsignarBP_Todo, 'verificar')
        cargarIcono(self.pbTexto_Cabecera, 'texto')
        cargarIcono(self.pbSalir, 'salir')
        cargarIcono(self, 'erp')

    def asignarBP_Todo(self):
        nro_filas = self.tbwDatos_Cot_Prov.rowCount()
        for i in range(nro_filas):
            self.tbwDatos_Cot_Prov.cellWidget(i, 14).setChecked(True)

    def mostrarInfo(self, Cod_Soc, Año, nro_cotiza, prov, num_req, fec_req, estatus, fecha_entrega, codUsuario_login):
        cargarLogo(self.lbLogo_Soc, Cod_Soc)
        global cod_soc, año, nro_cotizacion, nro_req, fecha_req, fecha_ent_prov, Cod_Usuario_Login
        cod_soc = Cod_Soc
        año = Año
        nro_cotizacion = nro_cotiza
        nro_req = num_req
        fecha_req = fec_req
        fecha_ent_prov = fecha_entrega
        Cod_Usuario_Login = codUsuario_login
        ## debe consultar el estado_evalua
        if estatus != "Prov. Cotizo":
            self.pbGrabar.setEnabled(False)
            self.pbAsignarBP_Todo.setEnabled(False)
        else:
            self.pbGrabar.setEnabled(True)
            self.pbAsignarBP_Todo.setEnabled(True)
        self.leNro_Cot.setText(nro_cotiza)
        self.leRaz_Soc.setText(prov)
        flags = QtCore.Qt.ItemFlags()
        flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        sql = '''SELECT Cod_prov, Nro_Telf, Representante FROM TAB_PROV_001_Registro_de_Proveedores WHERE Razón_social='%s';''' % (prov)
        info = consultarSql(sql)
        if info != []:
            # print(info)
            global cod_prov
            cod_prov = info[0][0]
            self.leCod_Prov.setText(info[0][0])
            self.leNro_Telf.setText(info[0][1])
            self.leRep.setText(info[0][2])
            if estatus == "Prov. Cotizo": ### Estado 6
                sqlDatos = '''SELECT Item_Cotiza, Cod_Mat, Cant_Req, Unid_Cot, Cant_Notificada, Precio_Cotiza, Cant_Notificada*Precio_Cotiza, Cant_Notificada*Precio_Cotiza*Descuento/100, ((Cant_Notificada*Precio_Cotiza)*(1-Descuento/100))*(IGV/100), ((Cant_Notificada*Precio_Cotiza)*(1-Descuento/100))*(1+IGV/100), Fecha_Ent_Prov, Estado_Item, Item_SOLP
                FROM TAB_COMP_002_Detalle_Cotización_de_Compra WHERE Cod_Soc='%s' AND Año='%s' AND Nro_Cotiza='%s' AND Cod_Prov='%s' AND (Estado_Item='6' OR Estado_Item='8' OR Estado_Item='9');''' % (Cod_Soc, Año, nro_cotiza, cod_prov)
            if estatus == "Concluido": ### Estado 8 (Ganador) o 9 (Concluido)
                sqlDatos = '''SELECT Item_Cotiza, Cod_Mat, Cant_Req, Unid_Cot, Cant_Notificada, Precio_Cotiza, Cant_Notificada*Precio_Cotiza, Cant_Notificada*Precio_Cotiza*Descuento/100, ((Cant_Notificada*Precio_Cotiza)*(1-Descuento/100))*(IGV/100), ((Cant_Notificada*Precio_Cotiza)*(1-Descuento/100))*(1+IGV/100), Fecha_Ent_Prov, Estado_Item, Item_SOLP
                FROM TAB_COMP_002_Detalle_Cotización_de_Compra WHERE Cod_Soc='%s' AND Año='%s' AND Nro_Cotiza='%s' AND Cod_Prov='%s' AND (Estado_Item='6' OR Estado_Item='8' OR Estado_Item='9');''' % (Cod_Soc, Año, nro_cotiza, cod_prov)

            try:
                infoDatos = consultarSql(sqlDatos)
                if infoDatos != []:
                    print(infoDatos)
                    row = 0
                    for tup in infoDatos:
                        col = 0
                        rowPosition = self.tbwDatos_Cot_Prov.rowCount()
                        self.tbwDatos_Cot_Prov.insertRow(rowPosition)
                        chk = QCheckBox(self.tbwDatos_Cot_Prov)
                        self.tbwDatos_Cot_Prov.setCellWidget(row, 14, chk)
                        chk.stateChanged.connect(self.textBP)
                        for item in tup:
                            if col == 0: ## item cotiza
                                info = QTableWidgetItem(item)
                                info.setFlags(flags)
                                info.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                                info.setBackground(QtGui.QColor(200, 210, 230))
                                self.tbwDatos_Cot_Prov.setItem(row, col, info)
                            elif col == 1: #<> ## codigo material
                                info = QTableWidgetItem(item)
                                info.setFlags(flags)
                                info.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                                info.setBackground(QtGui.QColor(200, 210, 230))
                                self.tbwDatos_Cot_Prov.setItem(row, col, info)
                                try:
                                    item_concat = dict_materiales[item]
                                    uni_base = item_concat[0:item_concat.find(",")]
                                    descrip_mat = item_concat[item_concat.find(",")+1:]
                                except:
                                    uni_base = ""
                                    descrip_mat = ""
                                info2 = QTableWidgetItem(uni_base)
                                info2.setFlags(flags)
                                info2.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                                info2.setBackground(QtGui.QColor(200, 210, 230))
                                self.tbwDatos_Cot_Prov.setItem(row, col+3, info2)
                                info3 = QTableWidgetItem(descrip_mat)
                                info3.setFlags(flags)
                                info3.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                                info3.setBackground(QtGui.QColor(200, 210, 230))
                                self.tbwDatos_Cot_Prov.setItem(row, col+1, info3)
                            elif col == 2: ## cantidad requerida
                                item = formatearDecimal(item,'3')
                                info = QTableWidgetItem(item)
                                info.setFlags(flags)
                                info.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                                info.setBackground(QtGui.QColor(200, 210, 230))
                                self.tbwDatos_Cot_Prov.setItem(row, col+1, info)
                            elif col == 3: ## unidad cotiza
                                info = QTableWidgetItem(item)
                                info.setFlags(flags)
                                info.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                                self.tbwDatos_Cot_Prov.setItem(row, col+2, info)
                            elif col == 4: ## cantidad notificada
                                item = formatearDecimal(item,'3')
                                info = QTableWidgetItem(item)
                                info.setFlags(flags)
                                info.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                                self.tbwDatos_Cot_Prov.setItem(row, col+2, info)
                            elif col <= 9:
                                item = formatearDecimal(item,'2')
                                info = QTableWidgetItem(item)
                                info.setFlags(flags)
                                info.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                                self.tbwDatos_Cot_Prov.setItem(row, col+2, info)
                            elif col == 10:
                                info = QTableWidgetItem(formatearFecha2(item))
                                info.setFlags(flags)
                                info.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                                self.tbwDatos_Cot_Prov.setItem(row, col+2, info)
                            elif col == 11: ## estado de evaluación
                                estado_item = item
                                if estatus != "Prov. Cotizo":
                                    if estado_item == '8': ## Ganador
                                        self.tbwDatos_Cot_Prov.cellWidget(row, 14).setChecked(True)
                                        self.tbwDatos_Cot_Prov.cellWidget(row, 14).setText("BP")
                                        self.tbwDatos_Cot_Prov.cellWidget(row, 14).setEnabled(False)
                                        print("Ganador")
                                    elif estado_item == '9': ## Concluido
                                        self.tbwDatos_Cot_Prov.cellWidget(row, 14).setChecked(False)
                                        self.tbwDatos_Cot_Prov.cellWidget(row, 14).setEnabled(False)
                                        print("Concluido")
                                    else:
                                        self.tbwDatos_Cot_Prov.cellWidget(row, 14).setEnabled(True)
                                else:
                                    if estado_item == '8': ## Ganador
                                        self.tbwDatos_Cot_Prov.cellWidget(row, 14).setChecked(True)
                                        self.tbwDatos_Cot_Prov.cellWidget(row, 14).setText("BP")
                                    elif estado_item == '9': ## Concluido
                                        self.tbwDatos_Cot_Prov.cellWidget(row, 14).setChecked(False)
                                    # else:
                                    #     self.tbwDatos_Cot_Prov.cellWidget(row, 14).setEnabled(True)

                            elif col == 12: ## texto proceso
                                try:
                                    nro_solp = dict_nroSolp[cod_soc+año+nro_cotizacion]
                                    sql = '''SELECT Texto FROM TAB_SOC_019_Texto_Proceso
                                    WHERE Cod_Soc='%s' AND Tipo_Proceso='1' AND Nro_Doc='%s' AND Item_Doc='%s';''' %(cod_soc, nro_cotizacion, item)
                                    infoTxt = consultarSql(sql)
                                    if infoTxt != []:
                                        texto = "XXXX"
                                    else:
                                        texto = "---"
                                    info = QTableWidgetItem(texto)
                                    info.setFlags(flags)
                                    info.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                                    self.tbwDatos_Cot_Prov.setItem(row, col+1, info)
                                except:
                                    texto = "NONE"
                                    info = QTableWidgetItem(texto)
                                    info.setFlags(flags)
                                    info.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                                    self.tbwDatos_Cot_Prov.setItem(row, col+1, info)
                            col += 1
                        row += 1

    # suma acumulada en tabla
                    total = []
                    descuentos = []
                    columna_total_cot = 8
                    columna_desc = 9
                    nro_fila = self.tbwDatos_Cot_Prov.rowCount()
                    for i in range(nro_fila):
                        try:
                            total_parcial = self.tbwDatos_Cot_Prov.item(i,columna_total_cot).text()
                            desc = self.tbwDatos_Cot_Prov.item(i,columna_desc).text()
                            total.append(total_parcial.replace(",",""))
                            descuentos.append(desc.replace(",",""))
                        except:
                            print("")
                    # print(total)
                    monto_total = 0
                    for i in total:
                        monto_total = float(monto_total) + float(i)
                    self.leMonto_Total.setText(formatearDecimal(str(monto_total),'2'))
                    monto_descuentos = 0
                    for i in descuentos:
                        monto_descuentos = float(monto_descuentos) + float(i)
                    self.leDescuento.setText("- " + formatearDecimal(str(monto_descuentos),'2'))
                    transporte = 100.000
                    self.leTransporte.setText(formatearDecimal(str(transporte),'2'))
                    igv = (float(0.18) * (monto_total - monto_descuentos + transporte))
                    self.leIGV.setText(formatearDecimal(igv,'2'))
                    total_general = monto_total - monto_descuentos + igv + transporte
                    self.leTotal_General.setText(formatearDecimal(str(total_general),'2'))
                else:
                    print("Lista Vacía1")
            except:
                QMessageBox.critical(self, "Error", "No se encontraron Cotizaciones Registradas", QMessageBox.Ok)

            sqlDatos2 = '''SELECT FValidez_oferta, Forma_Pago, Cuotas_Credito, Monto_deposito, Banco_deposito, Cuenta_Banco, Tiempo_Garantia, Forma_Garantia, Moneda, Forma_Envio
            FROM TAB_COMP_001_Cotización_Compra WHERE Cod_Soc='%s' AND Año='%s' AND Nro_Cotiza='%s' AND Cod_Prov='%s';''' % (Cod_Soc, Año, nro_cotiza, cod_prov)
            # para unid_mat y descrip_mat diccionario con el cod_mat
            # para
            infoDatos2 = consultarSql(sqlDatos2)
            if infoDatos2 != []:
                print(infoDatos2)
                self.leValidez_Cot.setText(formatearFecha2(infoDatos2[0][0]))
                self.cbForma_Pago.setEditText(infoDatos2[0][1])
                try:
                    desc_forma_pago = dict_formaPago[infoDatos2[0][1]]
                except:
                    desc_forma_pago = ""
                self.leForma_Pago.setText(desc_forma_pago)
                self.cbCuotas.setEditText(infoDatos2[0][2])
                self.leMonto_Deposito.setText(formatearDecimal(infoDatos2[0][3],'2'))
                self.cbBanco.setEditText(infoDatos2[0][4])
                try:
                    desc_banco = dict_bancos[infoDatos2[0][4]]
                except:
                    desc_banco = ""
                self.leBanco.setText(desc_banco)
                self.leCuenta_Banco.setText(infoDatos2[0][5])
                self.cbTiempo_Garantia.setEditText(infoDatos2[0][6])
                # try:
                #     tiempo_garantia = dict_garantia[infoDatos2[0][7]]
                # except:
                #     tiempo_garantia = ""
                self.leTiempo_Garantia.setText(infoDatos2[0][7])
                try:
                    moneda = dict_monedas[infoDatos2[0][8]]
                except:
                    moneda = ""
                self.leMoneda.setText(moneda)
                try:
                    forma_envio = dict_medioEntrega[infoDatos2[0][9]]
                except:
                    forma_envio = ""
                self.leForma_Envio.setText(forma_envio)
            else:
                print("Lista Vacía2")
        else:
            QMessageBox.critical(self, "Error", " No se encontraron datos registrados", QMessageBox.Ok)

    def textBP(self):
        filas = range(self.tbwDatos_Cot_Prov.rowCount())
        for j in filas :
            if self.tbwDatos_Cot_Prov.cellWidget(j,14).isChecked():
                # tbw.cellWidget(j, 14).setFont(font_data)
                self.tbwDatos_Cot_Prov.cellWidget(j, 14).setText("BP")
            else:
                self.tbwDatos_Cot_Prov.cellWidget(j, 14).setText("")


    def listar(self):
        try:
            list_item = []
            list_descripcion = []
            list_cant_cot = []
            list_unid = []
            list_precio_cot = []
            list_descuento = []
            list_total_parcial = []
            list_bp = []

            for i in range(self.tbwDatos_Cot_Prov.rowCount()):
                try:
                    list_item.append(self.tbwDatos_Cot_Prov.item(i,0).text())
                except:
                    list_item.append("BLANCO")
                try:
                    list_descripcion.append(self.tbwDatos_Cot_Prov.item(i,2).text())
                except:
                    list_descripcion.append("BLANCO")
                try:
                    list_cant_cot.append(self.tbwDatos_Cot_Prov.item(i,6).text())
                except:
                    list_cant_cot.append("BLANCO")
                try:
                    list_unid.append(self.tbwDatos_Cot_Prov.item(i,4).text())
                except:
                    list_unid.append("BLANCO")
                try:
                    list_precio_cot.append(self.tbwDatos_Cot_Prov.item(i,7).text())
                except:
                    list_precio_cot.append("BLANCO")
                try:
                    list_descuento.append(self.tbwDatos_Cot_Prov.item(i,9).text())
                except:
                    list_descuento.append("BLANCO")
                try:
                    list_total_parcial.append(self.tbwDatos_Cot_Prov.item(i,11).text())
                except:
                    list_total_parcial.append("BLANCO")
                try:
                    list_bp.append(self.tbwDatos_Cot_Prov.cellWidget(i,14).text())
                except:
                    list_bp.append("BLANCO")

            nro_cot = self.leNro_Cot.text()
            # cod_prov = self.leCod_Prov.text()
            raz_soc = self.leRaz_Soc.text()
            # nro_telf = self.leNro_Telf.text()
            interloc = self.leRep.text()

            fecha_validez = self.leValidez_Cot.text()
            forma_pago = self.leForma_Pago.text()
            cuotas = self.cbCuotas.currentText()
            monto_deposito = self.leMonto_Deposito.text()
            moneda = self.leMoneda.text()
            tiempo_garantia = self.cbTiempo_Garantia.currentText()
            forma_garantia = self.leTiempo_Garantia.text()
            banco = self.leBanco.text()
            cuenta_banco = self.leCuenta_Banco.text()
            forma_envio = self.leForma_Envio.text()

            monto_total = self.leMonto_Total.text()
            descuento = self.leDescuento.text()
            transporte = self.leTransporte.text()
            igv = self.leIGV.text()
            total_general = self.leTotal_General.text()
            moneda = self.leMoneda.text()

            print("LISTA 1: ",list_item)
            print("LISTA 2: ",list_descripcion)
            print("LISTA 3: ",list_cant_cot)
            print("LISTA 4: ",list_unid)
            print("LISTA 5: ",list_precio_cot)
            print("LISTA 6: ",list_descuento)
            print("LISTA 7: ",list_total_parcial)
            print("LISTA 8: ",list_bp)

            list_precioxcant = []
            for i in range(len(list_cant_cot)):
                p = list_precio_cot[i].replace(",","")
                q = list_cant_cot[i].replace(",","")
                precio_x_cant = float(p) * float(q)
                list_precioxcant.append(formatearDecimal(str(precio_x_cant),'3'))
                i += 1

            df = pd.DataFrame()
            df['1'] = list_item
            df['2'] = list_descripcion
            df['3'] = list_cant_cot
            df['4'] = list_unid
            df['5'] = list_precio_cot
            df['6'] = list_descuento
            df['7'] = list_total_parcial
            df['8'] = list_precioxcant
            df['9'] = list_bp

            title = 'NRO. COTIZACIÓN : ' + nro_cot

            class PDF(FPDF):
                def header(self):
                    self.image('Logos/LogoMp_st.png', 20, 10, 55)
                    self.image('Logos/LogoMc.png', 222, 10, 55)
                    self.set_font('Arial', 'B', 13)
                    ## Posición del título en el centro
                    w = self.get_string_width(title) + 6
                    self.set_xy((297 - w) / 2, 20)
                    self.set_text_color(220, 50, 50)
                    self.cell(w, 9, title, 0, 1, 'C')
                    ## espacio vertical
                    self.ln(5)
                    ## espacio horizontal
                    self.cell(10)
                    ## Texto Encabezado
                    self.set_font('Arial', 'B', 10)
                    self.set_text_color(0, 0, 0)
                    ## Primera Fila Encabezado
                    self.cell(40, 8, "Ref. Requerimiento : ", 0, 0,'L')
                    self.cell(30, 8, nro_req, 0, 0,'C')
                    self.cell(30)
                    self.cell(30, 8, "Fecha Req. : ", 0, 0,'L')
                    self.cell(30, 8, fecha_req, 0, 0,'C')
                    self.cell(30)
                    self.cell(30, 8, "Fecha Entrega : ", 0, 0,'L')
                    self.cell(37, 8, fecha_ent_prov, 0, 2,'C')
                    ## Segunda Fila Encabezado
                    self.cell(-220)
                    self.cell(40, 8, "Proveedor : ", 0, 0,'L')
                    self.cell(130, 8, raz_soc, 0, 0,'L')
                    self.cell(20)
                    self.cell(30, 8, "Validez Oferta : ", 0, 0,'L')
                    self.cell(37, 8, fecha_validez, 0, 2,'C')
                    ## Tercera Fila Encabezado
                    self.cell(-220)
                    self.cell(40, 8, "Forma Pago : ", 0, 0,'L')
                    self.cell(30, 8, forma_pago, 0, 0,'C')
                    self.cell(30)
                    self.cell(30, 8, "Cuotas : ", 0, 0,'L')
                    self.cell(30, 8, cuotas, 0, 0,'C')
                    self.cell(30)
                    self.cell(30, 8, "Monto Depósito : ", 0, 0,'L')
                    self.cell(37, 8, monto_deposito, 0, 2,'C')
                    ## Cuarta Fila Encabezado
                    self.cell(-220)
                    self.cell(40, 8, "Forma de Envío : ", 0, 0,'L')
                    self.cell(30, 8, forma_envio, 0, 0,'C')
                    self.cell(30)
                    self.cell(30, 8, "Moneda : ", 0, 0,'L')
                    self.cell(30, 8, moneda, 0, 0,'C')
                    self.cell(30)
                    self.cell(30, 8, "Garantía : ", 0, 0,'L')
                    self.cell(37, 8, tiempo_garantia+' '+forma_garantia, 0, 2,'C')
                    ## Quinta Fila Encabezado
                    self.cell(-220)
                    self.cell(40, 8, "Banco : ", 0, 0,'L')
                    self.cell(30, 8, banco, 0, 0,'L')
                    self.cell(30)
                    self.cell(30, 8, "Cuenta : ", 0, 0,'L')
                    self.cell(30, 8, cuenta_banco, 0, 0,'C')
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
            # pdf.cell(-40)
            # pdf.cell(5)
            # pdf.set_fill_color(255,0,120)
            pdf.set_fill_color(255, 213, 79)
            pdf.cell(10, 10, 'Item', 1, 0, 'C', 1)
            pdf.cell(127, 10, 'Material', 1, 0, 'C', 1)
            pdf.cell(10, 10, 'UB', 1, 0, 'C', 1)
            # pdf.cell(147, 10, 'Proveedores Invitados', 1, 0, 'C')
            pdf.cell(20, 10, 'Cantidad', 1, 0, 'C', 1)
            pdf.cell(25, 10, 'Precio', 1, 0, 'C', 1)
            pdf.cell(25, 10, 'Total', 1, 0, 'C', 1)
            pdf.cell(25, 10, 'Descuento', 1, 0, 'C', 1)
            pdf.cell(25, 10, 'Total-Desct.', 1, 0, 'C', 1)
            pdf.cell(10, 10, 'BP', 1, 2, 'C', 1)
            # pdf.cell(-90)
            pdf.cell(-267)
            pdf.set_font('arial', '', 9)
            for i in range(0, len(df)):
                pdf.cell(10, 8, '%s' % (df['1'].iloc[i]), 1, 0, 'C')
                pdf.cell(127, 8, '%s' % (df['2'].iloc[i]), 1, 0, 'C')
                pdf.cell(10, 8, '%s' % (df['4'].iloc[i]), 1, 0, 'C')
                # pdf.cell(147, 8, '%s' % (df['3'].iloc[i]), 1, 0, 'C')
                pdf.cell(20, 8, '%s' % (df['3'].iloc[i]), 1, 0, 'C')
                pdf.cell(25, 8, '%s' % (df['5'].iloc[i]), 1, 0, 'C')
                pdf.cell(25, 8, '%s' % (df['8'].iloc[i]), 1, 0, 'C')
                pdf.cell(25, 8, '%s' % (df['6'].iloc[i]), 1, 0, 'C')
                pdf.cell(25, 8, '%s' % (df['7'].iloc[i]), 1, 0, 'C')
                pdf.cell(10, 8, '%s' % (df['9'].iloc[i]), 1, 2, 'C')
                pdf.cell(-267)
                # pdf.cell(-90)
            pdf.ln(10)
            pdf.cell(177)
            pdf.set_font('arial', 'B', 9)
            pdf.cell(30, 8, "Monto Total", 1, 0,'L', 1)
            pdf.set_font('arial', '', 9)
            pdf.cell(30, 8, monto_total, 1, 2,'R')
            pdf.cell(-30)
            pdf.set_font('arial', 'B', 9)
            pdf.cell(30, 8, "Descuento", 1, 0,'L', 1)
            pdf.set_font('arial', '', 9)
            pdf.cell(30, 8, descuento, 1, 2,'R')
            pdf.cell(-30)
            pdf.set_font('arial', 'B', 9)
            pdf.cell(30, 8, "Transporte", 1, 0,'L', 1)
            pdf.set_font('arial', '', 9)
            pdf.cell(30, 8, transporte, 1, 2,'R')
            pdf.cell(-30)
            pdf.set_font('arial', 'B', 9)
            pdf.cell(30, 8, "IGV", 1, 0,'L', 1)
            pdf.set_font('arial', '', 9)
            pdf.cell(30, 8, igv, 1, 2,'R')
            pdf.cell(-30)
            pdf.set_font('arial', 'B', 9)
            pdf.cell(30, 8, "Total General", 1, 0,'L', 1)
            pdf.set_font('arial', '', 9)
            pdf.cell(30, 8, total_general, 1, 0,'R')
            pdf.cell(35, 8, moneda, 1, 2,'C')
            # pdf.image('barchart.png', x = None, y = None, w = 0, h = 0, type = '', link = '')
            root = tk.Tk()
            root.withdraw()
            ruta = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=(("Documento PDF", "*.pdf"),))
            if ruta != "":
                pdf.output(ruta, 'F')
                QMessageBox.information(self, "Reporte", "Reporte PDF Generado con éxito", QMessageBox.Ok)
        except:
            QMessageBox.critical(self, "Reporte", "Reporte Fallido", QMessageBox.Ok)

    def grabar2(self):
        fecha_mod = time.strftime("%Y-%m-%d")
        fecha_evalua = fecha_mod
        hora_mod = datetime.datetime.now().strftime('%H:%M:%S.%f')
        # try:
        for i in range(self.tbwDatos_Cot_Prov.rowCount()):
            item_cot = self.tbwDatos_Cot_Prov.item(i,0).text()
            if self.tbwDatos_Cot_Prov.cellWidget(i,14).isChecked():
                ## de la cantidad cotizada, columna 6
                cant_req = self.tbwDatos_Cot_Prov.item(i,3).text()
                cant_notif = self.tbwDatos_Cot_Prov.item(i,6).text()
                if float(cant_req.replace(",","")) > float(cant_notif.replace(",","")):
                    cant_asignada = self.tbwDatos_Cot_Prov.item(i,6).text().replace(",","")
                else:
                    cant_asignada = self.tbwDatos_Cot_Prov.item(i,3).text().replace(",","")
                estado_item = '8' # Ganador
                estado_evalua = '1' # Buena Pro asignada
            else:
                cant_asignada = ""
                estado_item = '9' # Concluido
                estado_evalua = '2' # Rechazado
            # list_estados.append(estado)
            sql = '''UPDATE TAB_COMP_002_Detalle_Cotización_de_Compra
            SET Estado_Evalua='%s', Estado_Item='%s', Cant_Asignada='%s', Fecha_Evalua='%s', User_Valida_Ofert='%s', Fecha_Mod='%s', Hora_Mod='%s', Usuario_Mod='%s'
            WHERE Cod_Soc='%s' AND Año='%s' AND Nro_Cotiza='%s' AND Cod_Prov='%s' AND Item_Cotiza='%s';''' % (estado_evalua, estado_item, cant_asignada, fecha_evalua, Cod_Usuario_Login, fecha_mod, hora_mod, Cod_Usuario_Login, cod_soc, año, nro_cotizacion, cod_prov, item_cot)
            respuesta = ejecutarSql(sql)
            # print("AQUI! ------ ", cant_asignada)
            # if respuesta["respuesta"] == "correcto":
            #     print("ACTUALIZADO CON ÉXITO")
        QMessageBox.information(self, "Actualizar", "Información actualizada con éxito", QMessageBox.Ok)

        ### Actualización a Estado Ganador en Cabecera
        # if '8' in list_estados:
        #     estado = '8' ## Ganador
        # else:
        #     estado = '6' ## Prov. Cotizó
        # sql = '''UPDATE TAB_COMP_001_Cotización_Compra
        # SET Estado_Tipo='%s', Fecha_Mod='%s', Hora_Mod='%s', Usuario_Mod='%s'
        # WHERE Cod_Soc='%s' AND Año='%s' AND Nro_Cotiza='%s' AND Cod_Prov='%s';''' % (estado, fecha_mod, hora_mod, Cod_Usuario_Login, cod_soc, año, nro_cotizacion, cod_prov)

        # except:
        #     QMessageBox.critical(self, "Error", "No se pudo guardar toda la Información", QMessageBox.Ok)

    def grabar(self):
        item_estado = []
        for i in range(self.tbwDatos_Cot_Prov.rowCount()):
            if self.tbwDatos_Cot_Prov.cellWidget(i,14).isChecked():
                estado = '8' # Ganador
            else:
                estado = '9' # Concluido
            item_estado.append(estado)
        fecha_mod = time.strftime("%Y-%m-%d")
        hora_mod = datetime.now().strftime('%H:%M:%S.%f')

        if not '9' in item_estado:
            estado = '9' # Concluido
            sql = '''UPDATE TAB_COMP_001_Cotización_Compra
            SET Estado_Tipo='%s', Fecha_Mod='%s', Hora_Mod='%s', Usuario_Mod='%s'
            WHERE Cod_Soc='%s' AND Año='%s' AND Nro_Cotiza='%s';''' % (estado, fecha_mod, hora_mod, Cod_Usuario_Login, cod_soc, año, nro_cotizacion)
            respuesta = ejecutarSql2(sql)
            sql2 = '''UPDATE TAB_COMP_002_Detalle_Cotización_de_Compra
            SET Estado_Evalua='%s', Fecha_Mod='%s', Hora_Mod='%s', Usuario_Mod='%s'
            WHERE Cod_Soc='%s' AND Año='%s' AND Nro_Cotiza='%s';''' % (estado, fecha_mod, hora_mod, Cod_Usuario_Login, cod_soc, año, nro_cotizacion)
            respuesta2 = ejecutarSql2(sql2)
            try:
                for i in range(self.tbwDatos_Cot_Prov.rowCount()):
                    item = self.tbwDatos_Cot_Prov.item(i,0).text()
                    estado = '8' # Ganador
                    sql3 = '''UPDATE TAB_COMP_002_Detalle_Cotización_de_Compra
                    SET Estado_Evalua='%s', Fecha_Mod='%s', Hora_Mod='%s', Usuario_Mod='%s'
                    WHERE Cod_Soc='%s' AND Año='%s' AND Nro_Cotiza='%s' AND Cod_Prov='%s' AND Item_Cotiza='%s';''' % (estado, fecha_mod, hora_mod, Cod_Usuario_Login, cod_soc, año, nro_cotizacion, cod_prov, item)
                    respuesta3 = ejecutarSql2(sql3)
                    # if respuesta["respuesta"] == "correcto":
                    #     print("ACTUALIZADO CON ÉXITO")
                    i += 1
                print(item_estado)
                QMessageBox.information(self, "Actualizar", "Información actualizada con éxito", QMessageBox.Ok)
                self.pbGrabar.setEnabled(False)
            except:
                QMessageBox.critical(self, "Error", "No se pudo guardar la Información", QMessageBox.Ok)
        else:
            try:
                for i in range(self.tbwDatos_Cot_Prov.rowCount()):
                    item = self.tbwDatos_Cot_Prov.item(i,0).text()
                    if self.tbwDatos_Cot_Prov.cellWidget(i,14).isChecked():
                        estado = '8' # Ganador
                    else:
                        estado = '9' # Concluido
                    sql = '''UPDATE TAB_COMP_002_Detalle_Cotización_de_Compra
                    SET Estado_Evalua='%s', Fecha_Mod='%s', Hora_Mod='%s', Usuario_Mod='%s'
                    WHERE Cod_Soc='%s' AND Año='%s' AND Nro_Cotiza='%s' AND Cod_Prov='%s' AND Item_Cotiza='%s';''' % (estado, fecha_mod, hora_mod, Cod_Usuario_Login, cod_soc, año, nro_cotizacion, cod_prov, item)
                    respuesta = ejecutarSql(sql)
                    # if respuesta["respuesta"] == "correcto":
                    #     print("ACTUALIZADO CON ÉXITO")
                    i += 1
                print(item_estado)
                QMessageBox.information(self, "Actualizar", "Información actualizada con éxito", QMessageBox.Ok)
            except:
                QMessageBox.critical(self, "Error", "No se pudo guardar la Información", QMessageBox.Ok)

    def textoCabecera(self):
        Texto_Cabecera(cod_soc, nro_cotizacion).exec_()

if __name__ == "__main__":
    app=QApplication(sys.argv)
    _main=ERP_COTP_P003_3()
    _main.show()
    app.exec_()
