import sys
from datetime import datetime
from Funciones04 import*
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
import urllib.request

class Condiciones_Cabecera(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("ERP_PCOMP_008.ui",self)

        self.pbSalir.clicked.connect(self.Salir)
        # self.pbGrabar.clicked.connect(self.Grabar)

    def datosCabecera(self,codsoc,codusuario,nrocotiza,razonsocial,codprov,nropedido,descrip_tipo_pedido,nomsoc,orgcomp,estadopedido):

        global Cod_Soc,Nom_Soc,Cod_Usuario,Nro_Cotiza,Razon_Social,Cod_Prov,Nro_Pedido,Tipo_Pedido,Org_Compra,Fecha,Año,dicPlanta,Estado_Pedido

        Cod_Soc=codsoc
        Cod_Usuario=codusuario
        Nro_Cotiza=nrocotiza
        Razon_Social=razonsocial
        Cod_Prov=codprov
        Nro_Pedido=nropedido
        Tipo_Pedido=descrip_tipo_pedido
        Org_Compra=orgcomp
        Nom_Soc=nomsoc
        Estado_Pedido=estadopedido

        Fecha=datetime.now().strftime("%Y-%m-%d")
        now = datetime.now()
        Año=str(now.year)

        self.leNro_Cotizacion.setText(Nro_Cotiza)
        self.cbProveedor.addItem(Cod_Prov)
        self.leRazon_Social.setText(Razon_Social)
        self.leEstado.setText(Estado_Pedido)
        fecha=formatearFecha(Fecha)
        self.leFecha_Pedido.setText(fecha)
        self.leNro_Pedido.setText(Nro_Pedido)
        self.leTipo_Pedido.setText(Tipo_Pedido)
        self.leEmpresa.setText(Nom_Soc)
        self.cbOrg_Compra.addItem(Org_Compra)

        cargarLogo(self.lbLogo_Mp,'multiplay')
        cargarLogo(self.lbLogo_Soc, Cod_Soc)
        cargarIcono(self, 'erp')
        # cargarIcono(self.pbSalir, 'salir')
        # cargarIcono(self.pbImprimir, 'imprimir')
        # cargarIcono(self.pbCancelar_Cot, 'darbaja')
        # cargarIcono(self.pbConsultar, 'visualizar')
        # cargarIcono(self.pbPed_Comp, 'registrar')


        

    #     cb0 = QComboBox(self.tbwCond_Cab)
    #     self.tbwCond_Cab.setCellWidget(0, 0, cb0)
    #     insertarDatos(cb0,Cond_Comp1)
    #     cb0.setCurrentIndex(0)
    #     font = QtGui.QFont()
    #     font.setPointSize(12)
    #     cb0.setFont(font)
    #     self.tbwCond_Cab.resizeColumnToContents(0)
    #
    #     flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    #     item1=QTableWidgetItem(Precio)
    #     item1.setFlags(flags)
    #     item1.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #     self.tbwCond_Cab.setItem(0, 2, item1)
    #
    #     item2=QTableWidgetItem(Valor)
    #     item2.setFlags(flags)
    #     item2.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #     self.tbwCond_Cab.setItem(0, 3, item2)
    #
    #     item3=QTableWidgetItem(Moneda)
    #     item3.setFlags(flags)
    #     item3.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #     self.tbwCond_Cab.setItem(0, 4, item3)
    #
    #     item22=QTableWidgetItem(Valor)
    #     item22.setFlags(flags)
    #     brush = QtGui.QBrush(QtGui.QColor(255, 213, 79))
    #     brush.setStyle(QtCore.Qt.SolidPattern)
    #     item22.setBackground(brush)
    #     item22.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #     self.tbwCond_Cab.setItem(1, 3, item22)
    #
    #     item33=QTableWidgetItem(Moneda)
    #     item33.setFlags(flags)
    #     brush = QtGui.QBrush(QtGui.QColor(255, 213, 79))
    #     brush.setStyle(QtCore.Qt.SolidPattern)
    #     item33.setBackground(brush)
    #     item33.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #     self.tbwCond_Cab.setItem(1, 4, item33)
    #
    #     # cb0.activated.connect(self.Condicion1)
    #
    #     cb1 = QComboBox(self.tbwCond_Cab)
    #     self.tbwCond_Cab.setCellWidget(2, 0, cb1)
    #     if Tipo_Pedido=='Importaciones':
    #         insertarDatos(cb1,Cond_Comp2)
    #         cb1.setCurrentIndex(-1)
    #         font = QtGui.QFont()
    #         font.setPointSize(12)
    #         cb1.setFont(font)
    #         self.tbwCond_Cab.resizeColumnToContents(0)
    #         cb1.activated.connect(self.Condicion2)
    #     else:
    #         insertarDatos(cb1,Cond_Comp3)
    #         cb1.setCurrentIndex(-1)
    #         font = QtGui.QFont()
    #         font.setPointSize(12)
    #         cb1.setFont(font)
    #         self.tbwCond_Cab.resizeColumnToContents(0)
    #         cb1.activated.connect(self.Condicion3)
    #
    # def Centrar(self, item):
    #     try:
    #         row = item.row()
    #         col = item.column()
    #         if col == 1:
    #             num = self.tbwCond_Cab.item(row, col).text()
    #             info = QTableWidgetItem(num)
    #             info.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #             num = self.tbwCond_Cab.setItem(row, col, info)
    #     except:
    #         ""
    #
    # def AgregarFila(self, fila, columna, filaAnterior, columnaAnterior):
    #     # print("Fila: ", fila, "Columna: ", columna, "Fila Anterior: ", filaAnterior, "Columna Anterior: ", columnaAnterior)
    #     if (fila == self.tbwCond_Cab.currentRow()) and (columna == self.tbwCond_Cab.columnCount()-1):
    #         rowPosition = self.tbwCond_Cab.currentRow()+1
    #         reply = QMessageBox.question(self,'Insertar fila',"¿Realmente desea insertar una fila?",QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    #         if reply == QMessageBox.Yes:
    #             self.tbwCond_Cab.insertRow(rowPosition)
    #
    #
    #             cb = QComboBox(self.tbwCond_Cab)
    #             self.tbwCond_Cab.setCellWidget(rowPosition, 0, cb)
    #             if rowPosition<5:
    #                 insertarDatos(cb,Cond_Comp1)
    #                 cb.setCurrentIndex(-1)
    #                 font = QtGui.QFont()
    #                 font.setPointSize(12)
    #                 cb.setFont(font)
    #                 self.tbwCond_Cab.resizeColumnToContents(0)
    #                 cb.activated.connect(self.Condicion1)
    #             elif rowPosition>5:
    #                 if Tipo_Pedido=='Importaciones':
    #                     insertarDatos(cb,Cond_Comp2)
    #                     cb.setCurrentIndex(-1)
    #                     font = QtGui.QFont()
    #                     font.setPointSize(12)
    #                     cb.setFont(font)
    #                     self.tbwCond_Cab.resizeColumnToContents(0)
    #                     cb.activated.connect(self.Condicion2)
    #                 else:
    #                     insertarDatos(cb,Cond_Comp3)
    #                     cb.setCurrentIndex(-1)
    #                     font = QtGui.QFont()
    #                     font.setPointSize(12)
    #                     cb.setFont(font)
    #                     self.tbwCond_Cab.resizeColumnToContents(0)
    #                     cb.activated.connect(self.Condicion3)
    #
    # def Condicion1(self):
    #     condicion=self.tbwCond_Cab.cellWidget(self.tbwCond_Cab.currentRow(),0).currentText()
    #     try:
    #         global total
    #         if condicion=='Descuento 1':
    #             Monto=Valor.replace(",","")
    #             porcentaje=self.tbwCond_Cab.item(self.tbwCond_Cab.currentRow(),1).text()
    #             if porcentaje!="":
    #                 Porc_Adelanto=porcentaje.replace(",","")
    #                 n1 = float(Monto)
    #                 n2 = float(Porc_Adelanto)
    #                 res = eval("n1 * (n2 / 100)")
    #
    #                 flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    #                 item=QTableWidgetItem(formatearDecimal(str(res),'2'))
    #                 item.setFlags(flags)
    #                 item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Cab.setItem(self.tbwCond_Cab.currentRow(), 3, item)
    #
    #                 item3=QTableWidgetItem(Moneda)
    #                 item3.setFlags(flags)
    #                 item3.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Cab.setItem(self.tbwCond_Cab.currentRow(), 4, item3)
    #
    #                 total=float(Monto)-float(res)
    #                 flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    #                 item11=QTableWidgetItem(formatearDecimal(str(total),'2'))
    #                 item11.setFlags(flags)
    #                 brush = QtGui.QBrush(QtGui.QColor(255, 213, 79))
    #                 brush.setStyle(QtCore.Qt.SolidPattern)
    #                 item11.setBackground(brush)
    #                 item11.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Cab.setItem(self.tbwCond_Cab.currentRow()+1, 3, item11)
    #
    #                 item33=QTableWidgetItem(Moneda)
    #                 item33.setFlags(flags)
    #                 brush = QtGui.QBrush(QtGui.QColor(255, 213, 79))
    #                 brush.setStyle(QtCore.Qt.SolidPattern)
    #                 item33.setBackground(brush)
    #                 item33.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Cab.setItem(self.tbwCond_Cab.currentRow()+1, 4, item33)
    #
    #
    #         elif condicion=='Descuento 2':
    #             Monto=Valor.replace(",","")
    #             descuento1=self.tbwCond_Cab.item(1,3).text()
    #             descuento1=descuento1.replace(",","")
    #             porcentaje=self.tbwCond_Cab.item(self.tbwCond_Cab.currentRow(),1).text()
    #             if porcentaje!="":
    #                 Porc_Adelanto=porcentaje.replace(",","")
    #                 n1 = float(Monto)-float(descuento1)
    #                 n2 = float(Porc_Adelanto)
    #                 res = eval("n1 * (n2 / 100)")
    #
    #                 flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    #                 item=QTableWidgetItem(formatearDecimal(str(res),'2'))
    #                 item.setFlags(flags)
    #                 item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Cab.setItem(self.tbwCond_Cab.currentRow(), 3, item)
    #
    #                 item3=QTableWidgetItem(Moneda)
    #                 item3.setFlags(flags)
    #                 item3.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Cab.setItem(self.tbwCond_Cab.currentRow(), 4, item3)
    #
    #                 total=float(Monto)-(float(descuento1)+float(res))
    #                 flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    #                 item11=QTableWidgetItem(formatearDecimal(str(total),'2'))
    #                 item11.setFlags(flags)
    #                 brush = QtGui.QBrush(QtGui.QColor(255, 213, 79))
    #                 brush.setStyle(QtCore.Qt.SolidPattern)
    #                 item11.setBackground(brush)
    #                 item11.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Cab.setItem(self.tbwCond_Cab.currentRow()+1, 3, item11)
    #
    #                 item33=QTableWidgetItem(Moneda)
    #                 item33.setFlags(flags)
    #                 brush = QtGui.QBrush(QtGui.QColor(255, 213, 79))
    #                 brush.setStyle(QtCore.Qt.SolidPattern)
    #                 item33.setBackground(brush)
    #                 item33.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Cab.setItem(self.tbwCond_Cab.currentRow()+1, 4, item33)
    #
    #         elif condicion=='Descuento 3':
    #             Monto=Valor.replace(",","")
    #             descuento1=self.tbwCond_Cab.item(1,3).text()
    #             descuento1=descuento1.replace(",","")
    #             descuento2=self.tbwCond_Cab.item(2,3).text()
    #             descuento2=descuento2.replace(",","")
    #             porcentaje=self.tbwCond_Cab.item(self.tbwCond_Cab.currentRow(),1).text()
    #             if porcentaje!="":
    #                 Porc_Adelanto=porcentaje.replace(",","")
    #                 n1 = float(Monto)-(float(descuento1)+float(descuento2))
    #                 n2 = float(Porc_Adelanto)
    #                 res = eval("n1 * (n2 / 100)")
    #
    #                 flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    #                 item=QTableWidgetItem(formatearDecimal(str(res),'2'))
    #                 item.setFlags(flags)
    #                 item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Cab.setItem(self.tbwCond_Cab.currentRow(), 3, item)
    #
    #                 item3=QTableWidgetItem(Moneda)
    #                 item3.setFlags(flags)
    #                 item3.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Cab.setItem(self.tbwCond_Cab.currentRow(), 4, item3)
    #
    #                 total=float(Monto)-(float(descuento1)+float(descuento2)+float(res))
    #                 flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    #                 item11=QTableWidgetItem(formatearDecimal(str(total),'2'))
    #                 item11.setFlags(flags)
    #                 brush = QtGui.QBrush(QtGui.QColor(255, 213, 79))
    #                 brush.setStyle(QtCore.Qt.SolidPattern)
    #                 item11.setBackground(brush)
    #                 item11.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Cab.setItem(self.tbwCond_Cab.currentRow()+1, 3, item11)
    #
    #                 item33=QTableWidgetItem(Moneda)
    #                 item33.setFlags(flags)
    #                 brush = QtGui.QBrush(QtGui.QColor(255, 213, 79))
    #                 brush.setStyle(QtCore.Qt.SolidPattern)
    #                 item33.setBackground(brush)
    #                 item33.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Cab.setItem(self.tbwCond_Cab.currentRow()+1, 4, item33)
    #         else:
    #             transporte=self.tbwCond_Cab.item(self.tbwCond_Cab.currentRow(),2).text()
    #             flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    #             item=QTableWidgetItem(formatearDecimal(str(transporte),'2'))
    #             item.setFlags(flags)
    #             item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #             self.tbwCond_Cab.setItem(self.tbwCond_Cab.currentRow(), 3, item)
    #
    #             num_format = formatearDecimal(transporte,'2')
    #             info = QTableWidgetItem(num_format)
    #             info.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #             self.tbwCond_Cab.setItem(self.tbwCond_Cab.currentRow(), 2, info)
    #
    #             item3=QTableWidgetItem(Moneda)
    #             item3.setFlags(flags)
    #             item3.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #             self.tbwCond_Cab.setItem(self.tbwCond_Cab.currentRow(), 4, item3)
    #
    #             Total=float(total)+float(transporte)
    #             flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    #             item11=QTableWidgetItem(formatearDecimal(str(Total),'2'))
    #             item11.setFlags(flags)
    #             brush = QtGui.QBrush(QtGui.QColor(255, 213, 79))
    #             brush.setStyle(QtCore.Qt.SolidPattern)
    #             item11.setBackground(brush)
    #             item11.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #             self.tbwCond_Cab.setItem(self.tbwCond_Cab.currentRow()+1, 3, item11)
    #
    #             item33=QTableWidgetItem(Moneda)
    #             item33.setFlags(flags)
    #             brush = QtGui.QBrush(QtGui.QColor(255, 213, 79))
    #             brush.setStyle(QtCore.Qt.SolidPattern)
    #             item33.setBackground(brush)
    #             item33.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #             self.tbwCond_Cab.setItem(self.tbwCond_Cab.currentRow()+1, 4, item33)
    #     except:
    #         QMessageBox.critical(self, "Error", "Se necesita llenar los campos indicados", QMessageBox.Ok)
    #
    # def Condicion2(self):
    #     condicion=self.tbwCond_Cab.cellWidget(self.tbwCond_Cab.currentRow(),0).currentText()
    #     try:
    #         global total2
    #         if condicion=='IGV':
    #             Total=self.tbwCond_Cab.item(self.tbwCond_Cab.currentRow()-1,3).text()
    #             Total=Total.replace(",","")
    #             porcentaje=self.tbwCond_Cab.item(self.tbwCond_Cab.currentRow(),1).text()
    #             if porcentaje!="":
    #                 n1 = float(Total)
    #                 n2 = float(porcentaje)
    #                 res = eval("n1 * (n2 / 100)")
    #
    #                 flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    #                 item=QTableWidgetItem(formatearDecimal(str(res),'2'))
    #                 item.setFlags(flags)
    #                 item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Cab.setItem(self.tbwCond_Cab.currentRow(), 3, item)
    #
    #                 item3=QTableWidgetItem(Moneda)
    #                 item3.setFlags(flags)
    #                 item3.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Cab.setItem(self.tbwCond_Cab.currentRow(), 4, item3)
    #
    #                 total2=float(Total)+float(res)
    #                 flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    #                 item11=QTableWidgetItem(formatearDecimal(str(total2),'2'))
    #                 item11.setFlags(flags)
    #                 brush = QtGui.QBrush(QtGui.QColor(255, 213, 79))
    #                 brush.setStyle(QtCore.Qt.SolidPattern)
    #                 item11.setBackground(brush)
    #                 item11.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Cab.setItem(self.tbwCond_Cab.currentRow()+1, 3, item11)
    #
    #                 item33=QTableWidgetItem(Moneda)
    #                 item33.setFlags(flags)
    #                 brush = QtGui.QBrush(QtGui.QColor(255, 213, 79))
    #                 brush.setStyle(QtCore.Qt.SolidPattern)
    #                 item33.setBackground(brush)
    #                 item33.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Cab.setItem(self.tbwCond_Cab.currentRow()+1, 4, item33)
    #         else:
    #             CIs=self.tbwCond_Cab.item(self.tbwCond_Cab.currentRow(),3).text()
    #             flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    #             item=QTableWidgetItem(formatearDecimal(str(CIs),'2'))
    #             item.setFlags(flags)
    #             item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #             self.tbwCond_Cab.setItem(self.tbwCond_Cab.currentRow(), 3, item)
    #
    #             item3=QTableWidgetItem(Moneda)
    #             item3.setFlags(flags)
    #             item3.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #             self.tbwCond_Cab.setItem(self.tbwCond_Cab.currentRow(), 4, item3)
    #
    #             total2=float(total2)+float(CIs)
    #             flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    #             item11=QTableWidgetItem(formatearDecimal(str(total2),'2'))
    #             item11.setFlags(flags)
    #             brush = QtGui.QBrush(QtGui.QColor(255, 213, 79))
    #             brush.setStyle(QtCore.Qt.SolidPattern)
    #             item11.setBackground(brush)
    #             item11.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #             self.tbwCond_Cab.setItem(self.tbwCond_Cab.currentRow()+1, 3, item11)
    #
    #             item33=QTableWidgetItem(Moneda)
    #             item33.setFlags(flags)
    #             brush = QtGui.QBrush(QtGui.QColor(255, 213, 79))
    #             brush.setStyle(QtCore.Qt.SolidPattern)
    #             item33.setBackground(brush)
    #             item33.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #             self.tbwCond_Cab.setItem(self.tbwCond_Cab.currentRow()+1, 4, item33)
    #
    #     except:
    #         QMessageBox.critical(self, "Error", "Se necesita llenar los campos indicados", QMessageBox.Ok)
    #
    # def Condicion3(self):
    #     condicion=self.tbwCond_Cab.cellWidget(self.tbwCond_Cab.currentRow(),0).currentText()
    #     try:
    #         global total2
    #         if condicion=='IGV':
    #             Total=self.tbwCond_Cab.item(self.tbwCond_Cab.currentRow()-1,3).text()
    #             Total=Total.replace(",","")
    #             porcentaje=self.tbwCond_Cab.item(self.tbwCond_Cab.currentRow(),1).text()
    #             if porcentaje!="":
    #                 n1 = float(Total)
    #                 n2 = float(porcentaje)
    #                 res = eval("n1 * (n2 / 100)")
    #
    #                 flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    #                 item=QTableWidgetItem(formatearDecimal(str(res),'2'))
    #                 item.setFlags(flags)
    #                 item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Cab.setItem(self.tbwCond_Cab.currentRow(), 3, item)
    #
    #                 item3=QTableWidgetItem(Moneda)
    #                 item3.setFlags(flags)
    #                 item3.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Cab.setItem(self.tbwCond_Cab.currentRow(), 4, item3)
    #
    #                 total2=float(Total)+float(res)
    #                 flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    #                 item11=QTableWidgetItem(formatearDecimal(str(total2),'2'))
    #                 item11.setFlags(flags)
    #                 brush = QtGui.QBrush(QtGui.QColor(255, 213, 79))
    #                 brush.setStyle(QtCore.Qt.SolidPattern)
    #                 item11.setBackground(brush)
    #                 item11.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Cab.setItem(self.tbwCond_Cab.currentRow()+1, 3, item11)
    #
    #                 item33=QTableWidgetItem(Moneda)
    #                 item33.setFlags(flags)
    #                 brush = QtGui.QBrush(QtGui.QColor(255, 213, 79))
    #                 brush.setStyle(QtCore.Qt.SolidPattern)
    #                 item33.setBackground(brush)
    #                 item33.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Cab.setItem(self.tbwCond_Cab.currentRow()+1, 4, item33)
    #
    #     except:
    #         QMessageBox.critical(self, "Error", "Se necesita llenar los campos indicados", QMessageBox.Ok)


    def Salir(self):
        self.close()

if __name__ == '__main__':
    app=QApplication(sys.argv)
    _main=Condiciones_Cabecera()
    _main.showMaximized()
    app.exec_()
