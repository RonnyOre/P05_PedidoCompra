import sys
from datetime import datetime
from Funciones04 import*
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
import urllib.request

sqlCond_Comp="SELECT Descrip_Condicion,Tipo_Cond_compra FROM TAB_COMP_011_Tipos_de_Condiciones_de_Compras"

sqlCond_Comp1="SELECT Descrip_Condicion,Tipo_Cond_compra FROM TAB_COMP_011_Tipos_de_Condiciones_de_Compras WHERE Tipo_Cond_compra<'06'"

sqlCond_Comp2="SELECT Descrip_Condicion,Tipo_Cond_compra FROM TAB_COMP_011_Tipos_de_Condiciones_de_Compras WHERE Tipo_Cond_compra>'05'"

sqlCond_Comp3="SELECT Descrip_Condicion,Tipo_Cond_compra FROM TAB_COMP_011_Tipos_de_Condiciones_de_Compras WHERE Tipo_Cond_compra='06'"

sqlMoneda="SELECT Cod_moneda,Descrip_moneda FROM TAB_SOC_008_Monedas"

class Condiciones_Posicion(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("ERP_PCOMP_007.ui",self)

        self.pbSalir.clicked.connect(self.Salir)
        self.pbGrabar.clicked.connect(self.Grabar)
        # self.tbwCond_Pos.currentCellChanged.connect(self.AgregarFila)
        # self.pbAgregar.clicked.connect(self.Tabla1)
        # self.pbAgregar_2.clicked.connect(self.Tabla2)

    def datosCabecera(self,codsoc,codusuario,nrocotiza,razonsocial,codprov,nropedido,descrip_tipo_pedido,nomsoc,orgcomp,estadopedido,item,precio,valor,moneda):

        global Cod_Soc,Nom_Soc,Cod_Usuario,Nro_Cotiza,Razon_Social,Cod_Prov,Nro_Pedido,Tipo_Pedido,Org_Compra,Fecha,Año,dicPlanta,Estado_Pedido,Item,Precio,Valor,Moneda

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
        Item=item
        Precio=precio
        Valor=valor
        Moneda=moneda

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
        cargarIcono(self.pbSalir, 'salir')
        cargarIcono(self.pbGrabar, 'grabar')

        global dicCond_Comp,Cond_Comp1,Cond_Comp2,Cond_Comp3,dicMoneda

        Cond_Comp = consultarSql(sqlCond_Comp)
        dicCond_Comp={}
        for dato in Cond_Comp:
            dicCond_Comp[dato[1]]=dato[0]

        Cond_Comp1 = consultarSql(sqlCond_Comp1)
        Cond_Comp2 = consultarSql(sqlCond_Comp2)
        Cond_Comp3 = consultarSql(sqlCond_Comp3)

        moneda=consultarSql(sqlMoneda)
        dicMoneda={}
        for m in moneda:
            dicMoneda[m[0]]=m[1]

        sqlCondPos='''SELECT b.Descrip_Condicion, a.Porcentaje, a.Cantidad, a.Valor_Condicion, c.Descrip_moneda FROM TAB_COMP_012_Condiciones_de_Pedido_de_Compras a LEFT JOIN TAB_COMP_011_Tipos_de_Condiciones_de_Compras b ON a.Tipo_Cond_compra=b.Tipo_Cond_compra LEFT JOIN TAB_SOC_008_Monedas c ON a.Moneda=c.Cod_moneda
        WHERE a.Cod_Soc='%s' AND a.Nro_Pedido='%s' AND a.Año_Pedido='%s' AND a.Clase_condicion='2' AND a.Item_Pedido='%s';'''%(Cod_Soc,Nro_Pedido,Año,Item)
        condPos(self,self.tbwCond_Pos,sqlCondPos,Cond_Comp,Cond_Comp1,Cond_Comp2,Cond_Comp3,dicCond_Comp,Precio,Valor,Moneda,Tipo_Pedido)

        self.Inicio()

    def Inicio(self):
        insertarDatos(self.cbCondicion,Cond_Comp1)
        self.cbCondicion.setCurrentIndex(-1)

        if Tipo_Pedido=='Importaciones':
            insertarDatos(self.cbCondicion_2,Cond_Comp2)
            self.cbCondicion_2.setCurrentIndex(-1)
        else:
            insertarDatos(self.cbCondicion_2,Cond_Comp3)
            self.cbCondicion_2.setCurrentIndex(-1)
    #
    # def AgregarFila(self, fila, columna):
    #     if (fila == self.tbwCond_Pos.currentRow()) and (columna == self.tbwCond_Pos.columnCount()-1):
    #         rowPosition = self.tbwCond_Pos.currentRow()+1
    #         reply = mensajeDialogo("pregunta", "Pregunta","¿Realmente desea insertar una fila?")
    #         if reply == 'Yes':
    #             self.tbwCond_Pos.insertRow(rowPosition)
    #
    #             cb = QComboBox(self.tbwCond_Pos)
    #             self.tbwCond_Pos.setCellWidget(rowPosition, 0, cb)
    #             if rowPosition<5:
    #                 insertarDatos(cb,Cond_Comp1)
    #                 cb.setCurrentIndex(-1)
    #                 font = QtGui.QFont()
    #                 font.setPointSize(12)
    #                 cb.setFont(font)
    #                 self.tbwCond_Pos.resizeColumnToContents(0)
    #                 cb.activated.connect(self.Condicion1)
    #             elif rowPosition>5:
    #                 if Tipo_Pedido=='Importaciones':
    #                     insertarDatos(cb,Cond_Comp2)
    #                     cb.setCurrentIndex(-1)
    #                     font = QtGui.QFont()
    #                     font.setPointSize(12)
    #                     cb.setFont(font)
    #                     self.tbwCond_Pos.resizeColumnToContents(0)
    #                     cb.activated.connect(self.Condicion2)
    #                 else:
    #                     insertarDatos(cb,Cond_Comp3)
    #                     cb.setCurrentIndex(-1)
    #                     font = QtGui.QFont()
    #                     font.setPointSize(12)
    #                     cb.setFont(font)
    #                     self.tbwCond_Pos.resizeColumnToContents(0)
    #                     cb.activated.connect(self.Condicion3)

    # def Condicion1(self):
    #     condicion=self.tbwCond_Pos.cellWidget(self.tbwCond_Pos.currentRow(),0).currentText()
    #     try:
    #         global total
    #         flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    #         if condicion=='Descuento 1':
    #             Monto=Valor.replace(",","")
    #             porcentaje=self.tbwCond_Pos.item(self.tbwCond_Pos.currentRow(),1).text()
    #             if porcentaje!="":
    #                 Porc_Adelanto=porcentaje.replace(",","")
    #                 n1 = float(Monto)
    #                 n2 = float(Porc_Adelanto)
    #                 res = eval("n1 * (n2 / 100)")
    #
    #                 info = QTableWidgetItem(porcentaje)
    #                 info.setFlags(flags)
    #                 info.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow(), 1, info)
    #
    #                 item1=QTableWidgetItem(formatearDecimal(str(res),'2'))
    #                 item1.setFlags(flags)
    #                 item1.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow(), 3, item1)
    #
    #                 item3=QTableWidgetItem(Moneda)
    #                 item3.setFlags(flags)
    #                 item3.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow(), 4, item3)
    #
    #                 total=float(Monto)-float(res)
    #                 item11=QTableWidgetItem(formatearDecimal(str(total),'2'))
    #                 item11.setFlags(flags)
    #                 brush = QtGui.QBrush(QtGui.QColor(255, 213, 79))
    #                 brush.setStyle(QtCore.Qt.SolidPattern)
    #                 item11.setBackground(brush)
    #                 item11.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow()+1, 3, item11)
    #
    #                 item33=QTableWidgetItem(Moneda)
    #                 item33.setFlags(flags)
    #                 brush = QtGui.QBrush(QtGui.QColor(255, 213, 79))
    #                 brush.setStyle(QtCore.Qt.SolidPattern)
    #                 item33.setBackground(brush)
    #                 item33.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow()+1, 4, item33)
    #
    #
    #         elif condicion=='Descuento 2':
    #             Monto=Valor.replace(",","")
    #             descuento1=self.tbwCond_Pos.item(1,3).text()
    #             descuento1=descuento1.replace(",","")
    #             porcentaje=self.tbwCond_Pos.item(self.tbwCond_Pos.currentRow(),1).text()
    #             if porcentaje!="":
    #                 Porc_Adelanto=porcentaje.replace(",","")
    #                 n1 = float(Monto)-float(descuento1)
    #                 n2 = float(Porc_Adelanto)
    #                 res = eval("n1 * (n2 / 100)")
    #
    #                 info = QTableWidgetItem(porcentaje)
    #                 info.setFlags(flags)
    #                 info.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow(), 1, info)
    #
    #                 item1=QTableWidgetItem(formatearDecimal(str(res),'2'))
    #                 item1.setFlags(flags)
    #                 item1.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow(), 3, item1)
    #
    #                 item3=QTableWidgetItem(Moneda)
    #                 item3.setFlags(flags)
    #                 item3.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow(), 4, item3)
    #
    #                 total=float(Monto)-(float(descuento1)+float(res))
    #                 item11=QTableWidgetItem(formatearDecimal(str(total),'2'))
    #                 item11.setFlags(flags)
    #                 brush = QtGui.QBrush(QtGui.QColor(255, 213, 79))
    #                 brush.setStyle(QtCore.Qt.SolidPattern)
    #                 item11.setBackground(brush)
    #                 item11.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow()+1, 3, item11)
    #
    #                 item33=QTableWidgetItem(Moneda)
    #                 item33.setFlags(flags)
    #                 brush = QtGui.QBrush(QtGui.QColor(255, 213, 79))
    #                 brush.setStyle(QtCore.Qt.SolidPattern)
    #                 item33.setBackground(brush)
    #                 item33.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow()+1, 4, item33)
    #
    #         elif condicion=='Descuento 3':
    #             Monto=Valor.replace(",","")
    #             descuento1=self.tbwCond_Pos.item(1,3).text()
    #             descuento1=descuento1.replace(",","")
    #             descuento2=self.tbwCond_Pos.item(2,3).text()
    #             descuento2=descuento2.replace(",","")
    #             porcentaje=self.tbwCond_Pos.item(self.tbwCond_Pos.currentRow(),1).text()
    #             if porcentaje!="":
    #                 Porc_Adelanto=porcentaje.replace(",","")
    #                 n1 = float(Monto)-(float(descuento1)+float(descuento2))
    #                 n2 = float(Porc_Adelanto)
    #                 res = eval("n1 * (n2 / 100)")
    #
    #                 info = QTableWidgetItem(porcentaje)
    #                 info.setFlags(flags)
    #                 info.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow(), 1, info)
    #
    #                 item1=QTableWidgetItem(formatearDecimal(str(res),'2'))
    #                 item1.setFlags(flags)
    #                 item1.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow(), 3, item1)
    #
    #                 item3=QTableWidgetItem(Moneda)
    #                 item3.setFlags(flags)
    #                 item3.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow(), 4, item3)
    #
    #                 total=float(Monto)-(float(descuento1)+float(descuento2)+float(res))
    #                 item11=QTableWidgetItem(formatearDecimal(str(total),'2'))
    #                 item11.setFlags(flags)
    #                 brush = QtGui.QBrush(QtGui.QColor(255, 213, 79))
    #                 brush.setStyle(QtCore.Qt.SolidPattern)
    #                 item11.setBackground(brush)
    #                 item11.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow()+1, 3, item11)
    #
    #                 item33=QTableWidgetItem(Moneda)
    #                 item33.setFlags(flags)
    #                 brush = QtGui.QBrush(QtGui.QColor(255, 213, 79))
    #                 brush.setStyle(QtCore.Qt.SolidPattern)
    #                 item33.setBackground(brush)
    #                 item33.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow()+1, 4, item33)
    #         else:
    #             transporte=self.tbwCond_Pos.item(self.tbwCond_Pos.currentRow(),2).text()
    #             flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    #             item1=QTableWidgetItem(formatearDecimal(str(transporte),'2'))
    #             item1.setFlags(flags)
    #             item1.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #             self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow(), 3, item1)
    #
    #             num = formatearDecimal(transporte,'2')
    #             info = QTableWidgetItem(num)
    #             info.setFlags(flags)
    #             info.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #             self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow(), 2, info)
    #
    #             item3=QTableWidgetItem(Moneda)
    #             item3.setFlags(flags)
    #             item3.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #             self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow(), 4, item3)
    #
    #             Total=float(total)+float(transporte)
    #             item11=QTableWidgetItem(formatearDecimal(str(Total),'2'))
    #             item11.setFlags(flags)
    #             brush = QtGui.QBrush(QtGui.QColor(255, 213, 79))
    #             brush.setStyle(QtCore.Qt.SolidPattern)
    #             item11.setBackground(brush)
    #             item11.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #             self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow()+1, 3, item11)
    #
    #             item33=QTableWidgetItem(Moneda)
    #             item33.setFlags(flags)
    #             brush = QtGui.QBrush(QtGui.QColor(255, 213, 79))
    #             brush.setStyle(QtCore.Qt.SolidPattern)
    #             item33.setBackground(brush)
    #             item33.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #             self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow()+1, 4, item33)
    #
    #     except Exception as e:
    #         mensajeDialogo("error", "Error", "Se necesita llenar los campos indicados")
    #         print(e)
    #
    # def Condicion2(self):
    #     condicion=self.tbwCond_Pos.cellWidget(self.tbwCond_Pos.currentRow(),0).currentText()
    #     flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    #     try:
    #         global total2
    #         if condicion=='IGV':
    #             Total=self.tbwCond_Pos.item(self.tbwCond_Pos.currentRow()-1,3).text()
    #             Total=Total.replace(",","")
    #             porcentaje=self.tbwCond_Pos.item(self.tbwCond_Pos.currentRow(),1).text()
    #             if porcentaje!="":
    #                 n1 = float(Total)
    #                 n2 = float(porcentaje)
    #                 res = eval("n1 * (n2 / 100)")
    #
    #                 info = QTableWidgetItem(porcentaje)
    #                 info.setFlags(flags)
    #                 info.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow(), 1, info)
    #
    #                 flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    #                 item1=QTableWidgetItem(formatearDecimal(str(res),'2'))
    #                 item1.setFlags(flags)
    #                 item1.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow(), 3, item1)
    #
    #                 item3=QTableWidgetItem(Moneda)
    #                 item3.setFlags(flags)
    #                 item3.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow(), 4, item3)
    #
    #                 total2=float(Total)+float(res)
    #                 flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    #                 item11=QTableWidgetItem(formatearDecimal(str(total2),'2'))
    #                 item11.setFlags(flags)
    #                 brush = QtGui.QBrush(QtGui.QColor(255, 213, 79))
    #                 brush.setStyle(QtCore.Qt.SolidPattern)
    #                 item11.setBackground(brush)
    #                 item11.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow()+1, 3, item11)
    #
    #                 item33=QTableWidgetItem(Moneda)
    #                 item33.setFlags(flags)
    #                 brush = QtGui.QBrush(QtGui.QColor(255, 213, 79))
    #                 brush.setStyle(QtCore.Qt.SolidPattern)
    #                 item33.setBackground(brush)
    #                 item33.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow()+1, 4, item33)
    #
    #         else:
    #             CIs=self.tbwCond_Pos.item(self.tbwCond_Pos.currentRow(),3).text()
    #             item1=QTableWidgetItem(formatearDecimal(str(CIs),'2'))
    #             item1.setFlags(flags)
    #             item1.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #             self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow(), 3, item1)
    #
    #             item3=QTableWidgetItem(Moneda)
    #             item3.setFlags(flags)
    #             item3.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #             self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow(), 4, item3)
    #
    #             total2=float(total2)+float(CIs)
    #             item11=QTableWidgetItem(formatearDecimal(str(total2),'2'))
    #             item11.setFlags(flags)
    #             brush = QtGui.QBrush(QtGui.QColor(255, 213, 79))
    #             brush.setStyle(QtCore.Qt.SolidPattern)
    #             item11.setBackground(brush)
    #             item11.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #             self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow()+1, 3, item11)
    #
    #             item33=QTableWidgetItem(Moneda)
    #             item33.setFlags(flags)
    #             brush = QtGui.QBrush(QtGui.QColor(255, 213, 79))
    #             brush.setStyle(QtCore.Qt.SolidPattern)
    #             item33.setBackground(brush)
    #             item33.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #             self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow()+1, 4, item33)
    #
    #     except Exception as e:
    #         mensajeDialogo("error", "Error", "Se necesita llenar los campos indicados")
    #         print(e)
    #
    # def Condicion3(self):
    #     condicion=self.tbwCond_Pos.cellWidget(self.tbwCond_Pos.currentRow(),0).currentText()
    #     flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    #     try:
    #         global total2
    #         if condicion=='IGV':
    #             Total=self.tbwCond_Pos.item(self.tbwCond_Pos.currentRow()-1,3).text()
    #             Total=Total.replace(",","")
    #             porcentaje=self.tbwCond_Pos.item(self.tbwCond_Pos.currentRow(),1).text()
    #             if porcentaje!="":
    #                 n1 = float(Total)
    #                 n2 = float(porcentaje)
    #                 res = eval("n1 * (n2 / 100)")
    #
    #                 info = QTableWidgetItem(porcentaje)
    #                 info.setFlags(flags)
    #                 info.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow(), 1, info)
    #
    #                 item1=QTableWidgetItem(formatearDecimal(str(res),'2'))
    #                 item1.setFlags(flags)
    #                 item1.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow(), 3, item1)
    #
    #                 item3=QTableWidgetItem(Moneda)
    #                 item3.setFlags(flags)
    #                 item3.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow(), 4, item3)
    #
    #                 total2=float(Total)+float(res)
    #                 item11=QTableWidgetItem(formatearDecimal(str(total2),'2'))
    #                 item11.setFlags(flags)
    #                 brush = QtGui.QBrush(QtGui.QColor(255, 213, 79))
    #                 brush.setStyle(QtCore.Qt.SolidPattern)
    #                 item11.setBackground(brush)
    #                 item11.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow()+1, 3, item11)
    #
    #                 item33=QTableWidgetItem(Moneda)
    #                 item33.setFlags(flags)
    #                 brush = QtGui.QBrush(QtGui.QColor(255, 213, 79))
    #                 brush.setStyle(QtCore.Qt.SolidPattern)
    #                 item33.setBackground(brush)
    #                 item33.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    #                 self.tbwCond_Pos.setItem(self.tbwCond_Pos.currentRow()+1, 4, item33)
    #
    #     except Exception as e:
    #         mensajeDialogo("error", "Error", "Se necesita llenar los campos indicados")
    #         print(e)

    def Grabar(self):
        Hora=datetime.now().strftime("%H:%M:%S.%f")
        d=self.tbwCond_Pos.rowCount()
        for i in range(d):
            try:
                tipcondcomp=self.tbwCond_Pos.cellWidget(i,0).currentText()
                for k,v in dicCond_Comp.items():
                    if v==tipcondcomp:
                        condcomp=k
                try:
                    porcentaje=self.tbwCond_Pos.item(i,1).text()
                except:
                    porcentaje=""
                try:
                    monto=self.tbwCond_Pos.item(i,2).text()
                except:
                    monto=""
                try:
                    valor=self.tbwCond_Pos.item(i,3).text()
                except:
                    valor=""
                try:
                    descripmoneda=self.tbwCond_Pos.item(i,4).text()
                    for k,v in dicMoneda.items():
                        if v==descripmoneda:
                            moneda=k
                except:
                    moneda=""

                sql='''INSERT INTO TAB_COMP_012_Condiciones_de_Pedido_de_Compras(Cod_Soc, Nro_Pedido, Año_Pedido, Clase_condicion, Tipo_Cond_compra, Item_Pedido, Porcentaje, Cantidad, Valor_Condicion, Moneda, Fecha_Reg, Hora_Reg, Usuario_Reg)
                VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')''' %(Cod_Soc,Nro_Pedido,Año,2,condcomp,Item,porcentaje,monto,valor,moneda,Fecha,Hora,Cod_Usuario)
                respuesta=ejecutarSql(sql)

            except Exception as e:
                continue
                print(e)

        if respuesta['respuesta']=='correcto':
            mensajeDialogo("informacion", "Información", "Las Condiciones de Posicion se han grabado correctamente")

        elif respuesta['respuesta']=='incorrecto':
            mensajeDialogo("error", "Error", "Ocurrio un problema, comuniquese con soporte")

    def Salir(self):
        self.close()

if __name__ == '__main__':
    app=QApplication(sys.argv)
    _main=Condiciones_Posicion()
    _main.showMaximized()
    app.exec_()
