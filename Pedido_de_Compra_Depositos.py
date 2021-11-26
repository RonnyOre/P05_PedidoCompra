import sys
from datetime import datetime
from Funciones04 import*
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
import urllib.request

sqlFormaPago="SELECT Descrip_Pago, Forma_Pago FROM `TAB_SOC_024: Forma de pago`"

class Depositos(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("ERP_PCOMP_004.ui",self)

        self.pbSalir.clicked.connect(self.Salir)
        self.pbGrabar.clicked.connect(self.Grabar)
        self.tbwDeposito.currentCellChanged.connect(self.AgregarFila)
        self.lePorcentaje_Adelanto.editingFinished.connect(self.Porcentaje)

        self.leTipo_Pedido.setReadOnly(True)
        self.leNro_Pedido.setReadOnly(True)
        self.leEstado.setReadOnly(True)
        self.leFecha_Pedido.setReadOnly(True)
        self.leNro_Cotizacion.setReadOnly(True)
        self.leProveedor.setReadOnly(True)
        self.leRazon_Social.setReadOnly(True)
        self.leEmpresa.setReadOnly(True)
        self.leOrg_Compra.setReadOnly(True)

    def datosCabecera(self,data):

        global Data,Fecha,Año
        Data=data

        Fecha=datetime.now().strftime("%Y-%m-%d")
        now = datetime.now()
        Año=str(now.year)

        self.leNro_Cotizacion.setText(Data[3])
        self.leProveedor.setText(Data[5])
        self.leRazon_Social.setText(Data[4])
        self.leEstado.setText(Data[9])
        self.leFecha_Pedido.setText(formatearFecha(Fecha))
        self.leNro_Pedido.setText(Data[6])
        self.leTipo_Pedido.setText(Data[7])
        self.leEmpresa.setText(Data[1])
        self.leOrg_Compra.setText(Data[8])
        self.leMonto_Compra.setText(Data[10])

        cargarLogo(self.lbLogo_Mp,'multiplay')
        cargarLogo(self.lbLogo_Soc, Data[0])
        cargarIcono(self, 'erp')
        cargarIcono(self.pbSalir, 'salir')
        cargarIcono(self.pbGrabar, 'grabar')

        global dicpago, dicmoneda, dicbanco, dicpais

        condpago=consultarSql(sqlCondPago)
        dicpago={}
        for dato in condpago:
            dicpago[dato[1]]=dato[0]

        insertarDatos(self.cbCondicion_Credito,condpago)
        self.cbCondicion_Credito.setCurrentIndex(-1)

        self.Inicio()

    def Inicio(self):

        sqlBanco='''SELECT f.Descrip_Pago, c.Descrip_Banco, d.Nombre, e.Descrip_moneda, a.Cuenta_Banco
        FROM TAB_COMP_004_Pedido_Compra a
		LEFT JOIN TAB_PROV_007_Bancos_y_cuentas_del_Proveedor b ON b.Cod_Prov=a.Cod_Prov AND b.Nro_Correlativo=a.Banco_deposito
        LEFT JOIN TAB_SOC_016_Tipo_de_Bancos c ON c.Cod_Banco=b.Entidad_Bancaria
        LEFT JOIN TAB_SOC_009_Ubigeo_NuevaVersion d ON d.Cod_Pais=b.Pais AND d.Cod_Depart_Region='00' AND d.Cod_Provincia='00' AND d.Cod_Distrito='00'
        LEFT JOIN TAB_SOC_008_Monedas e ON e.Cod_moneda=b.Moneda
        LEFT JOIN `TAB_SOC_024: Forma de pago` f ON f.Forma_Pago=a.Forma_Pago
        WHERE a.Cod_Emp='%s' AND a.Nro_Pedido='%s' AND a.Año_Pedido='%s';'''%(Data[0],Data[6],Año)
        Banco=convlist(sqlBanco)

        self.cbBanco.addItem(Banco[0])
        self.cbBanco.setCurrentIndex(0)
        self.cbPais.addItem(Banco[1])
        self.cbPais.setCurrentIndex(0)
        self.cbMoneda.addItem(Banco[2])
        self.cbMoneda.setCurrentIndex(0)
        self.leNro_Cuenta.setText(Banco[3])

        # sqlDep='''SELECT a.Monto_Compra, b.Descrip_moneda, c.Descrip_cond, a.Cuotas_Pagar, a.Cuota, a.Porc_Adelanto, a.Adelanto, d.Descrip_Banco, a.Nro_Cuenta, e.Nombre
        # FROM TAB_COMP_014_Pedido_de_Compra_Crédito_Depósitos a
        # LEFT JOIN TAB_SOC_008_Monedas b ON a.Moneda=b.Cod_moneda
        # LEFT JOIN `TAB_COM_003_Condiciones de Pago por Clientes` c ON a.Condicion_Credito=c.Cond_pago
        # LEFT JOIN TAB_SOC_016_Tipo_de_Bancos d ON a.Banco=d.Cod_Banco
        # LEFT JOIN TAB_SOC_009_Ubigeo_NuevaVersion e ON a.Pais=e.Cod_Pais AND e.Cod_Depart_Region='00' AND e.Cod_Provincia='00' AND e.Cod_Distrito='00'
        # WHERE Cod_Empresa='%s' AND Año_Pedido='%s' AND  Nro_Pedido='%s';'''%(Data[0],Año,Data[6])
        # Dep=convlist(sqlDep)
        #
        # if Dep!=[]:
        #
        #     self.leMonto_Compra.setText(formatearDecimal(Dep[0],'3'))
        #     self.cbMoneda.setCurrentText(Dep[1])
        #     self.cbCondicion_Credito.setCurrentText(Dep[2])
        #     self.leCuotas.setText(Dep[3])
        #     self.leMonto.setText(formatearDecimal(Dep[4],'3'))
        #     self.lePorcentaje_Adelanto.setText(formatearDecimal(Dep[5],'2'))
        #     self.leAdelanto.setText(formatearDecimal(Dep[6],'3'))
        #     self.cbBanco.setCurrentText(Dep[7])
        #     self.leNro_Cuenta.setText(Dep[8])
        #     self.cbPais.setCurrentText(Dep[9])
        #
        #     self.leMonto_Compra.setReadOnly(True)
        #     self.cbMoneda.setEnabled(False)
        #     self.cbCondicion_Credito.setEnabled(False)
        #     self.leCuotas.setReadOnly(True)
        #     self.leMonto.setReadOnly(True)
        #     self.lePorcentaje_Adelanto.setReadOnly(True)
        #     self.leAdelanto.setReadOnly(True)
        #     self.cbBanco.setEnabled(False)
        #     self.leNro_Cuenta.setReadOnly(True)
        #     self.cbPais.setEnabled(False)
        #
        # sqlDetDep='''SELECT Nro_Cuota, Fecha_Deposito, Monto_Deposito
        # FROM TAB_COMP_015_Pedido_de_Compra_Detalle_Depósitos
        # WHERE Cod_Empresa='%s' AND Año_Pedido='%s' AND Nro_Pedido='%s','''%(Data[0],Año,Data[6])
        # DetDep=consultarSql(sqlDetDep)
        #
        # if DetDep!=[]:
        #     self.tbwDeposito.clearContents()
        #     rows=self.tbwDeposito.rowCount()
        #     for r in range(rows):
        #         self.tbwDeposito.removeRow(1)
        #     flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        #     row=0
        #     for fila in DetDep:
        #         fila[1]=formatearFecha(fila[1])
        #         fila[2]=formatearDecimal(fila[2],'3')
        #         col=0
        #         for i in fila:
        #             item=QTableWidgetItem(i)
        #             item.setFlags(flags)
        #             item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        #             if self.tbwDeposito.rowCount()<=row:
        #                 self.tbwDeposito.insertRow(self.tbwDeposito.rowCount())
        #             self.tbwDeposito.setItem(row, col, item)
        #             col += 1
        #         row+=1

    def Porcentaje(self):
        montocompra=self.leMonto_Compra.text()
        Monto_Compra=montocompra.replace(",","")
        porcadelanto=self.lePorcentaje_Adelanto.text()
        if porcadelanto!="":
            Porc_Adelanto=porcadelanto.replace(",","")
            n1 = float(Monto_Compra)
            n2 = float(Porc_Adelanto)
            res = eval("n1 * (n2 / 100)")
            self.leAdelanto.setText(formatearDecimal(str(res),'3'))

    def AgregarFila(self,fila,columna):
        if fila==self.tbwDeposito.rowCount()-1:
            rowPosition = self.tbwDeposito.rowCount()
            self.tbwDeposito.insertRow(rowPosition)

    def Grabar(self):
        try:
            sqlDep='''SELECT a.Monto_Compra, b.Descrip_moneda, c.Descrip_cond, a.Cuotas_Pagar, a.Cuota, a.Porc_Adelanto, a.Adelanto, d.Descrip_Banco, a.Nro_Cuenta, e.Nombre
            FROM TAB_COMP_014_Pedido_de_Compra_Crédito_Depósitos a
            LEFT JOIN TAB_SOC_008_Monedas b ON a.Moneda=b.Cod_moneda
            LEFT JOIN `TAB_COM_003_Condiciones de Pago por Clientes` c ON a.Condicion_Credito=c.Cond_pago
            LEFT JOIN TAB_SOC_016_Tipo_de_Bancos d ON a.Banco=d.Cod_Banco
            LEFT JOIN TAB_SOC_009_Ubigeo_NuevaVersion e ON a.Pais=e.Cod_Pais AND e.Cod_Depart_Region='00' AND e.Cod_Provincia='00' AND e.Cod_Distrito='00'
            WHERE Cod_Empresa='%s' AND Año_Pedido='%s' AND  Nro_Pedido='%s';'''%(Data[0],Año,Data[6])
            Dep=convlist(sqlDep)

            # Fecha=datetime.now().strftime("%Y-%m-%d")
            Hora=datetime.now().strftime("%H:%M:%S.%f")

            if Dep==[]:

                montocompra=self.leMonto_Compra.text()
                Monto_Compra=montocompra.replace(",","")

                Descrip_moneda=self.cbMoneda.currentText()
                for k,v in dicmoneda.items():
                    if v==Descrip_moneda:
                        Cod_Moneda=k

                Descrip_Condicion_Credito=self.cbCondicion_Credito.currentText()
                for k,v in dicpago.items():
                    if v==Descrip_Condicion_Credito:
                        Cod_Condicion=k

                cuotaspagar=self.leCuotas.text()
                Cuotas_Pagar=cuotaspagar.replace(",","")

                cuota=self.leMonto.text()
                Cuota=cuota.replace(",","")

                porcadelanto=self.lePorcentaje_Adelanto.text()
                Porc_Adelanto=porcadelanto.replace(",","")

                adelanto=self.leAdelanto.text()
                Adelanto=adelanto.replace(",","")

                Descrip_Banco=self.cbBanco.currentText()
                for k,v in dicbanco.items():
                    if v==Descrip_Banco:
                        Cod_Banco=k

                Nro_Cuenta=self.leNro_Cuenta.text()

                Descrip_Pais=self.cbPais.currentText()
                for k,v in dicpais.items():
                    if v==Descrip_Pais:
                        Cod_Pais=k

                sql='''INSERT INTO TAB_COMP_014_Pedido_de_Compra_Crédito_Depósitos(Cod_Empresa,Año_Pedido,Nro_Pedido,Monto_Compra,Moneda,Condicion_Credito,Cuotas_Pagar,Cuota,Porc_Adelanto,Adelanto,Banco,Nro_Cuenta,Pais,Fecha_Reg,Hora_Reg,Usuario_Reg)
                VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')'''%(Data[0],Año,Data[6],Monto_Compra,Cod_Moneda,Cod_Condicion,Cuotas_Pagar,Cuota,Porc_Adelanto,Adelanto,Cod_Banco,Nro_Cuenta,Cod_Pais,Fecha,Hora,Data[2])
                respuesta=ejecutarSql(sql)

                d=self.tbwDeposito.rowCount()-1
                for row in range(d):
                    try:
                        Nro_Cuota=self.tbwDeposito.item(row,0).text()

                        fechadeposito=self.tbwDeposito.item(row,1).text()
                        Fecha_Deposito=formatearFecha(fechadeposito)

                        montodeposito=self.tbwDeposito.item(row,2).text()
                        Monto_Deposito=montodeposito.replace(",","")


                        sqlDeposito='''INSERT INTO TAB_COMP_015_Pedido_de_Compra_Detalle_Depósitos(Cod_Empresa, Año_Pedido, Nro_Pedido, Nro_Cuota, Fecha_Deposito, Monto_Deposito, Fecha_Reg, Hora_Reg, Usuario_Reg)
                        VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')'''%(Data[0],Año,Data[6],Nro_Cuota, Fecha_Deposito, Monto_Deposito,Fecha,Hora,Data[2])
                        respuesta=ejecutarSql(sqlDeposito)
                    except Exception as e:
                    	print(e)

                if respuesta['respuesta']=='correcto':
                    mensajeDialogo("informacion", "Información", "Registro guardado correctamente")

                    sqlDetDep="SELECT Nro_Cuota, Fecha_Deposito, Monto_Deposito FROM TAB_COMP_015_Pedido_de_Compra_Detalle_Depósitos WHERE Cod_Empresa='%s' AND Año_Pedido='%s' AND Nro_Pedido='%s'"%(Data[0],Año,Data[6])
                    DetDep=consultarSql(sqlDetDep)

                    if DetDep!=[]:
                        self.tbwDeposito.clearContents()
                        rows=self.tbwDeposito.rowCount()
                        for r in range(rows):
                            self.tbwDeposito.removeRow(1)
                        flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                        row=0
                        for fila in DetDep:
                            fila[1]=formatearFecha(fila[1])
                            fila[2]=formatearDecimal(fila[2],'3')
                            col=0
                            for i in fila:
                                item=QTableWidgetItem(i)
                                item.setFlags(flags)
                                item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
                                if self.tbwDeposito.rowCount()<=row:
                                    self.tbwDeposito.insertRow(self.tbwDeposito.rowCount())
                                self.tbwDeposito.setItem(row, col, item)
                                col += 1
                            row+=1

                    self.leMonto_Compra.setReadOnly(True)
                    self.cbMoneda.setEnabled(False)
                    self.cbCondicion_Credito.setEnabled(False)
                    self.leCuotas.setReadOnly(True)
                    self.leMonto.setReadOnly(True)
                    self.lePorcentaje_Adelanto.setReadOnly(True)
                    self.leAdelanto.setReadOnly(True)
                    self.cbBanco.setEnabled(False)
                    self.leNro_Cuenta.setReadOnly(True)
                    self.cbPais.setEnabled(False)

                elif respuesta['respuesta']=='incorrecto':
                    mensajeDialogo("error", "Error", "Ingrese Datos Válido")

            else:
                data=[]
                d=self.tbwDeposito.columnCount()
                for n in range(d):
                    try:
                        m=self.tbwDeposito.item(self.tbwDeposito.currentRow(),n).text()
                        data.append(m)
                    except Exception as e:
                        mensajeDialogo("informacion", "Información", "Llene todos los campos")
                        print(e)

                Nro_Cuota=data[0]

                fechadeposito=data[1]
                Fecha_Deposito=formatearFecha(fechadeposito)

                montodeposito=data[2]
                Monto_Deposito=montodeposito.replace(",","")

                sqlDeposito='''INSERT INTO TAB_COMP_015_Pedido_de_Compra_Detalle_Depósitos(Cod_Empresa, Año_Pedido, Nro_Pedido, Nro_Cuota, Fecha_Deposito, Monto_Deposito, Fecha_Reg, Hora_Reg, Usuario_Reg)
                VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')'''%(Data[0],Año,Data[6],Nro_Cuota, Fecha_Deposito, Monto_Deposito,Fecha,Hora,Data[2])
                respuesta=ejecutarSql(sqlDeposito)

                if respuesta['respuesta']=='correcto':
                    mensajeDialogo("informacion", "Información", "El depósito se grabo correctamente")

                    sqlDetDep="SELECT Nro_Cuota, Fecha_Deposito, Monto_Deposito FROM TAB_COMP_015_Pedido_de_Compra_Detalle_Depósitos WHERE Cod_Empresa='%s' AND Año_Pedido='%s' AND Nro_Pedido='%s'"%(Data[0],Año,Data[6])
                    DetDep=consultarSql(sqlDetDep)

                    if DetDep!=[]:
                        self.tbwDeposito.clearContents()
                        rows=self.tbwDeposito.rowCount()
                        for r in range(rows):
                            self.tbwDeposito.removeRow(1)
                        flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                        row=0
                        for fila in DetDep:
                            fila[1]=formatearFecha(fila[1])
                            fila[2]=formatearDecimal(fila[2],'3')
                            col=0
                            for i in fila:
                                item=QTableWidgetItem(i)
                                item.setFlags(flags)
                                item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
                                if self.tbwDeposito.rowCount()<=row:
                                    self.tbwDeposito.insertRow(self.tbwDeposito.rowCount())
                                self.tbwDeposito.setItem(row, col, item)
                                col += 1
                            row+=1

                elif respuesta['respuesta']=='incorrecto':
                    mensajeDialogo("error", "Error", "Ingrese Datos Válido")

        except Exception as e:
            mensajeDialogo("error", "Error", "Algo salio mal, comuniquese con soporte")
            print(e)

    def Salir(self):
        self.close()

if __name__ == '__main__':
    app=QApplication(sys.argv)
    _main=Depositos()
    _main.showMaximized()
    app.exec_()
