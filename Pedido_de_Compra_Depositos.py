import sys
from datetime import datetime
from Funciones04 import*
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
import urllib.request

sqlCondPago="SELECT Descrip_cond,Cond_pago FROM `TAB_COM_003_Condiciones de Pago por Clientes`"

sqlMoneda="SELECT Descrip_moneda,Cod_moneda FROM TAB_SOC_008_Monedas"

sqlBanco="SELECT Descrip_Banco,Cod_Banco FROM TAB_SOC_016_Tipo_de_Bancos"

sqlPais="SELECT Nombre,Cod_Pais FROM TAB_SOC_009_Ubigeo WHERE Cod_Depart_Region='0' AND Cod_Provincia='0' AND Cod_Distrito='0'"

class Depositos(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("ERP_PCOMP_004.ui",self)

        self.pbSalir.clicked.connect(self.Salir)
        self.pbGrabar.clicked.connect(self.Grabar)
        self.tbwDeposito.currentCellChanged.connect(self.AgregarFila)
        self.lePorcentaje_Adelanto.editingFinished.connect(self.Porcentaje)

    def datosCabecera(self,codsoc,codusuario,nrocotiza,razonsocial,codprov,nropedido,descrip_tipo_pedido,nomsoc,orgcomp,estadopedido,montoaprobado):

        global Cod_Soc,Nom_Soc,Cod_Usuario,Nro_Cotiza,Razon_Social,Cod_Prov,Nro_Pedido,Tipo_Pedido,Org_Compra,Fecha,Año,dicPlanta,Estado_Pedido,Monto_Aprobado

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
        Monto_Aprobado=montoaprobado

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
        self.leMonto_Compra.setText(Monto_Aprobado)

        cargarLogo(self.lbLogo_Mp,'multiplay')
        cargarLogo(self.lbLogo_Soc, Cod_Soc)
        cargarIcono(self, 'erp')
        cargarIcono(self.pbSalir, 'salir')
        cargarIcono(self.pbGrabar, 'grabar')

        global dicpago, dicmoneda, dicbanco, dicpais

        condpago=consultarSql(sqlCondPago)
        dicpago={}
        for dato in condpago:
            dicpago[dato[1]]=dato[0]

        moneda=consultarSql(sqlMoneda)
        dicmoneda={}
        for dato in moneda:
            dicmoneda[dato[1]]=dato[0]

        banco=consultarSql(sqlBanco)
        dicbanco={}
        for dato in banco:
            dicbanco[dato[1]]=dato[0]

        pais=consultarSql(sqlPais)
        dicpais={}
        for dato in pais:
            dicpais[dato[1]]=dato[0]

        insertarDatos(self.cbMoneda,moneda)
        self.cbMoneda.setCurrentIndex(-1)

        insertarDatos(self.cbCondicion_Credito,condpago)
        self.cbCondicion_Credito.setCurrentIndex(-1)

        insertarDatos(self.cbBanco,banco)
        self.cbBanco.setCurrentIndex(-1)

        insertarDatos(self.cbPais,pais)
        self.cbPais.setCurrentIndex(-1)

        self.Inicio()

    def Inicio(self):

        sqlDep='''SELECT a.Monto_Compra, b.Descrip_moneda, c.Descrip_cond, a.Cuotas_Pagar, a.Cuota, a.Porc_Adelanto, a.Adelanto, d.Descrip_Banco, a.Nro_Cuenta, e.Nombre FROM TAB_COMP_014_Pedido_de_Compra_Crédito_Depósitos a LEFT JOIN TAB_SOC_008_Monedas b ON a.Moneda=b.Cod_moneda LEFT JOIN `TAB_COM_003_Condiciones de Pago por Clientes` c ON a.Condicion_Credito=c.Cond_pago LEFT JOIN TAB_SOC_016_Tipo_de_Bancos d ON a.Banco=d.Cod_Banco LEFT JOIN TAB_SOC_009_Ubigeo e ON a.Pais=e.Cod_Pais AND e.Cod_Depart_Region='0' AND e.Cod_Provincia='0' AND e.Cod_Distrito='0' WHERE Cod_Empresa='%s' AND Año_Pedido='%s' AND  Nro_Pedido='%s';'''%(Cod_Soc,Año,Nro_Pedido)
        Dep=convlist(sqlDep)

        if Dep!=[]:

            self.leMonto_Compra.setText(formatearDecimal(Dep[0],'3'))
            self.cbMoneda.setCurrentText(Dep[1])
            self.cbCondicion_Credito.setCurrentText(Dep[2])
            self.leCuotas.setText(Dep[3])
            self.leMonto.setText(formatearDecimal(Dep[4],'3'))
            self.lePorcentaje_Adelanto.setText(formatearDecimal(Dep[5],'2'))
            self.leAdelanto.setText(formatearDecimal(Dep[6],'3'))
            self.cbBanco.setCurrentText(Dep[7])
            self.leNro_Cuenta.setText(Dep[8])
            self.cbPais.setCurrentText(Dep[9])

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


        sqlDetDep="SELECT Nro_Cuota, Fecha_Deposito, Monto_Deposito FROM TAB_COMP_015_Pedido_de_Compra_Detalle_Depósitos WHERE Cod_Empresa='%s' AND Año_Pedido='%s' AND Nro_Pedido='%s'"%(Cod_Soc,Año,Nro_Pedido)
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
            sqlDep='''SELECT a.Monto_Compra, b.Descrip_moneda, c.Descrip_cond, a.Cuotas_Pagar, a.Cuota, a.Porc_Adelanto, a.Adelanto, d.Descrip_Banco, a.Nro_Cuenta, e.Nombre FROM TAB_COMP_014_Pedido_de_Compra_Crédito_Depósitos a LEFT JOIN TAB_SOC_008_Monedas b ON a.Moneda=b.Cod_moneda LEFT JOIN `TAB_COM_003_Condiciones de Pago por Clientes` c ON a.Condicion_Credito=c.Cond_pago LEFT JOIN TAB_SOC_016_Tipo_de_Bancos d ON a.Banco=d.Cod_Banco LEFT JOIN TAB_SOC_009_Ubigeo e ON a.Pais=e.Cod_Pais AND e.Cod_Depart_Region='0' AND e.Cod_Provincia='0' AND e.Cod_Distrito='0' WHERE Cod_Empresa='%s' AND Año_Pedido='%s' AND  Nro_Pedido='%s';'''%(Cod_Soc,Año,Nro_Pedido)
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
                VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')'''%(Cod_Soc,Año,Nro_Pedido,Monto_Compra,Cod_Moneda,Cod_Condicion,Cuotas_Pagar,Cuota,Porc_Adelanto,Adelanto,Cod_Banco,Nro_Cuenta,Cod_Pais,Fecha,Hora,Cod_Usuario)
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
                        VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')'''%(Cod_Soc,Año,Nro_Pedido,Nro_Cuota, Fecha_Deposito, Monto_Deposito,Fecha,Hora,Cod_Usuario)
                        respuesta=ejecutarSql(sqlDeposito)
                    except Exception as e:
                    	print(e)

                if respuesta['respuesta']=='correcto':
                    mensajeDialogo("informacion", "Información", "Registro guardado correctamente")

                    sqlDetDep="SELECT Nro_Cuota, Fecha_Deposito, Monto_Deposito FROM TAB_COMP_015_Pedido_de_Compra_Detalle_Depósitos WHERE Cod_Empresa='%s' AND Año_Pedido='%s' AND Nro_Pedido='%s'"%(Cod_Soc,Año,Nro_Pedido)
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
                VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')'''%(Cod_Soc,Año,Nro_Pedido,Nro_Cuota, Fecha_Deposito, Monto_Deposito,Fecha,Hora,Cod_Usuario)
                respuesta=ejecutarSql(sqlDeposito)

                if respuesta['respuesta']=='correcto':
                    mensajeDialogo("informacion", "Información", "El depósito se grabo correctamente")

                    sqlDetDep="SELECT Nro_Cuota, Fecha_Deposito, Monto_Deposito FROM TAB_COMP_015_Pedido_de_Compra_Detalle_Depósitos WHERE Cod_Empresa='%s' AND Año_Pedido='%s' AND Nro_Pedido='%s'"%(Cod_Soc,Año,Nro_Pedido)
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
