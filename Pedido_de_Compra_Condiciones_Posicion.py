import sys
from datetime import datetime
from Funciones04 import*
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
import urllib.request

sqlCond_Comp="SELECT Descrip_Condicion,Tipo_Cond_compra FROM TAB_COMP_011_Tipos_de_Condiciones_de_Compras"

sqlCond_Comp1="SELECT Descrip_Condicion,Tipo_Cond_compra FROM TAB_COMP_011_Tipos_de_Condiciones_de_Compras WHERE Tipo_Cond_compra<'07'"

sqlMoneda="SELECT Cod_moneda,Descrip_moneda FROM TAB_SOC_008_Monedas"

flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

class Condiciones_Posicion(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("ERP_PCOMP_007.ui",self)

        self.pbSalir.clicked.connect(self.Salir)
        self.pbGrabar.clicked.connect(self.Grabar)
        self.cbCondicion.activated.connect(self.Condicion)
        self.pbAgregar.clicked.connect(self.Tabla)
        self.pbLimpiar.clicked.connect(self.Limpiar)

    def datosCabecera(self,data):

        global Data,Fecha,Año,dicCond_Comp,Cond_Comp,Cond_Comp1,dicMoneda

        Data=data

        Fecha=datetime.now().strftime("%Y-%m-%d")
        now = datetime.now()
        Año=str(now.year)

        self.leNro_Cotizacion.setText(Data[3])
        self.cbProveedor.addItem(Data[5])
        self.leRazon_Social.setText(Data[4])
        self.leEstado.setText(Data[9])
        fecha=formatearFecha(Fecha)
        self.leFecha_Pedido.setText(fecha)
        self.leNro_Pedido.setText(Data[6])
        self.leTipo_Pedido.setText(Data[7])
        self.leEmpresa.setText(Data[1])
        self.cbOrg_Compra.addItem(Data[8])

        cargarLogo(self.lbLogo_Mp,'multiplay')
        cargarLogo(self.lbLogo_Soc, Data[0])
        cargarIcono(self, 'erp')
        cargarIcono(self.pbSalir, 'salir')
        cargarIcono(self.pbGrabar, 'grabar')

        Cond_Comp = consultarSql(sqlCond_Comp)
        dicCond_Comp={}
        for dato in Cond_Comp:
            dicCond_Comp[dato[1]]=dato[0]

        Cond_Comp1 = consultarSql(sqlCond_Comp1)

        moneda=consultarSql(sqlMoneda)
        dicMoneda={}
        for m in moneda:
            dicMoneda[m[0]]=m[1]

        sqlCondPos='''SELECT b.Descrip_Condicion, a.Porcentaje, a.Cantidad, a.Valor_Condicion, c.Descrip_moneda
        FROM TAB_COMP_012_Condiciones_de_Pedido_de_Compras a
        LEFT JOIN TAB_COMP_011_Tipos_de_Condiciones_de_Compras b ON a.Tipo_Cond_compra=b.Tipo_Cond_compra
        LEFT JOIN TAB_SOC_008_Monedas c ON a.Moneda=c.Cod_moneda
        WHERE a.Cod_Soc='%s' AND a.Nro_Pedido='%s' AND a.Año_Pedido='%s' AND a.Clase_condicion='2' AND a.Tipo_Cond_compra<'06' AND a.Item_Pedido='%s';'''%(Data[0],Data[6],Año,Data[10])

        sqlCondPos_2='''SELECT b.Descrip_Condicion, a.Porcentaje, a.Cantidad, a.Valor_Condicion, c.Descrip_moneda
        FROM TAB_COMP_012_Condiciones_de_Pedido_de_Compras a
        LEFT JOIN TAB_COMP_011_Tipos_de_Condiciones_de_Compras b ON a.Tipo_Cond_compra=b.Tipo_Cond_compra
        LEFT JOIN TAB_SOC_008_Monedas c ON a.Moneda=c.Cod_moneda
        WHERE a.Cod_Soc='%s' AND a.Nro_Pedido='%s' AND a.Año_Pedido='%s' AND a.Clase_condicion='2' AND a.Tipo_Cond_compra>'05' AND a.Item_Pedido='%s';'''%(Data[0],Data[6],Año,Data[10])

        condPos(self,self.tbwCond_Pos,self.tbwCond_Pos_2,sqlCondPos,sqlCondPos_2)

        # self.Inicio()

    def Inicio(self):

        if Data[7]!='Importaciones':
            insertarDatos(self.cbCondicion,Cond_Comp1)
            self.cbCondicion.setCurrentIndex(-1)
        else:
            insertarDatos(self.cbCondicion,Cond_Comp)
            self.cbCondicion.setCurrentIndex(-1)

        Lista=['Precio','', Data[11], Data[12], Data[13]]
        col = 0
        for i in Lista:
            item=QTableWidgetItem(i)
            item.setFlags(flags)
            insertarFila(col,item,[2,3],[0],[1,4])
            if self.tbwCond_Pos.rowCount() <= 0:
                self.tbwCond_Pos.insertRow(self.tbwCond_Pos.rowCount())
            self.tbwCond_Pos.setItem(0, col, item)
            col += 1

        self.leVN_ID.setText(Data[12])

    def CalcularValores(self):
        try:
            Lista=[]
            for i in range(self.tbwCond_Pos.rowCount()):
                try:
                    Lista.append(self.tbwCond_Pos.item(i,3).text().replace(",",""))
                except Exception as e:
                    print(e)

            n=len(Lista)
            suma=0
            for i in Lista:
                suma += float(i)

            Calculo=float(Lista[0]) + float(Lista[n-1])
            Descuento = suma - (Calculo)

            ValorNeto_ID = Calculo - Descuento

            self.leVN_ID.setText(formatearDecimal(str(ValorNeto_ID), '2'))

            Lista2=[]
            for i in range(self.tbwCond_Pos_2.rowCount()):
                try:
                    Lista2.append(self.tbwCond_Pos_2.item(i,3).text().replace(",",""))
                except Exception as e:
                    print(e)

            suma2=0
            for i in Lista2:
                suma2 += float(i)

            ValorNeto_II = ValorNeto_ID + suma2

            self.leVN_II.setText(formatearDecimal(str(ValorNeto_II), '2'))

        except Exception as e:
            print(e)

    def Condicion(self):
        self.lePorcentaje.setReadOnly(False)
        self.leMonto.setReadOnly(False)
        Condicion=self.cbCondicion.currentText()

        if Condicion[:9]=='Descuento':
            listaCondicion=[]
            for i in range(self.tbwCond_Pos.rowCount()):
                try:
                    listaCondicion.append(self.tbwCond_Pos.item(i,0).text())
                except Exception as e:
                    print(e)
            if Condicion=='Descuento 2':
                if 'Descuento 1' not in listaCondicion:
                    mensajeDialogo("error", "Error", "Es necesario seguir el orden de descuentos")
                    self.cbCondicion.setCurrentIndex(-1)
            if Condicion=='Descuento 3':
                if 'Descuento 2' not in listaCondicion:
                    mensajeDialogo("error", "Error", "Es necesario seguir el orden de descuentos")
                    self.cbCondicion.setCurrentIndex(-1)
            self.leMonto.setReadOnly(True)
        if Condicion=='Transporte':
            self.lePorcentaje.setReadOnly(True)
        if Condicion=='IGV':
            self.leMonto.setReadOnly(True)
        if Condicion[:3]=='CI.':
            self.lePorcentaje.setReadOnly(True)

    def Tabla(self):
        try:
            listaCondicion=[]
            for i in range(self.tbwCond_Pos.rowCount()):
                try:
                    listaCondicion.append(self.tbwCond_Pos.item(i,0).text())

                except Exception as e:
                    print(e)

            for i in range(self.tbwCond_Pos_2.rowCount()):
                try:
                    listaCondicion.append(self.tbwCond_Pos_2.item(i,0).text())
                except Exception as e:
                    print(e)

            Condicion=self.cbCondicion.currentText()
            ValorNeto=self.leVN_ID.text().replace(",","")
            ValorNeto_2=self.leVN_II.text().replace(",","")

            if Condicion not in listaCondicion:

                fila = []
                fila.append(Condicion)

                porcentaje=formatearDecimal(self.lePorcentaje.text(), '2')
                Porcentaje=porcentaje.replace(",","")
                fila.append(porcentaje)

                monto=formatearDecimal(self.leMonto.text(), '2')
                Monto=monto.replace(",","")
                fila.append(monto)

                if Condicion[:9]=='Descuento':
                    ValorCondicion=float(ValorNeto)*(float(Porcentaje) / 100)
                    ValorNetoActual=float(ValorNeto)-ValorCondicion
                    fila.append(formatearDecimal(str(ValorCondicion),'2'))
                    fila.append(Data[13])
                    self.CargarData(self.tbwCond_Pos,self.leVN_ID,fila,ValorCondicion,ValorNetoActual)

                if Condicion=='Transporte':
                    ValorCondicion=float(Monto)
                    ValorNetoActual=float(ValorNeto)+ValorCondicion
                    fila.append(formatearDecimal(str(ValorCondicion),'2'))
                    fila.append(Data[13])
                    self.CargarData(self.tbwCond_Pos,self.leVN_ID,fila,ValorCondicion,ValorNetoActual)

                if Condicion=='IGV':
                    ValorCondicion=float(ValorNeto)*(float(Porcentaje) / 100)
                    ValorNetoActual=float(ValorNeto)+ValorCondicion
                    fila.append(formatearDecimal(str(ValorCondicion),'2'))
                    fila.append(Data[13])
                    self.CargarData(self.tbwCond_Pos_2,self.leVN_II,fila,ValorCondicion,ValorNetoActual)

                if Condicion[:3]=='CI.':
                    ValorCondicion=float(Monto)
                    ValorNetoActual=float(ValorNeto_2)+ValorCondicion
                    fila.append(formatearDecimal(str(ValorCondicion),'2'))
                    fila.append(Data[13])
                    self.CargarData(self.tbwCond_Pos_2,self.leVN_II,fila,ValorCondicion,ValorNetoActual)

            else:
                mensajeDialogo("error", "Error", "Esta Condición ya se encuentra registrada")

        except Exception as e:
            self.cbCondicion.setCurrentIndex(-1)
            self.lePorcentaje.clear()
            self.leMonto.clear()
            print(e)

    def CargarData(self,tw,lineEdit,fila,ValorCondicion,ValorNetoActual):
        try:
            row=tw.rowCount()
            col = 0
            for i in fila:
                item=QTableWidgetItem(i)
                item.setFlags(flags)
                insertarFila(col,item,[2,3],[0],[1,4])
                if tw.rowCount()<=row:
                    tw.insertRow(tw.rowCount())
                tw.setItem(row, col, item)
                col += 1

            lineEdit.setText(formatearDecimal(str(ValorNetoActual),'2'))

            self.cbCondicion.setCurrentIndex(-1)
            self.lePorcentaje.clear()
            self.leMonto.clear()

        except Exception as e:
            self.cbCondicion.setCurrentIndex(-1)
            self.lePorcentaje.clear()
            self.leMonto.clear()
            print(e)

    def Limpiar(self):
        reply = mensajeDialogo("pregunta", "Pregunta","¿Realmente desea limpiar las tablas? Se perderán todos los datos ingresados")
        if reply == 'Yes':
            # reply = mensajeDialogo("pregunta", "Pregunta","¿Está seguro?")
            # if reply == 'Yes':
            #     reply = mensajeDialogo("pregunta", "Pregunta","Que conste que le avise")
            #     if reply == 'Yes':
            self.tbwCond_Pos.clearContents()
            rows=self.tbwCond_Pos.rowCount()
            for r in range(rows):
                self.tbwCond_Pos.removeRow(1)
            self.tbwCond_Pos_2.clearContents()
            rows=self.tbwCond_Pos_2.rowCount()
            for r in range(rows):
                self.tbwCond_Pos_2.removeRow(0)

            Lista=['Precio','', Data[11], Data[12], Data[13]]
            col = 0
            for i in Lista:
                item=QTableWidgetItem(i)
                item.setFlags(flags)
                insertarFila(col,item,[2,3],[0],[1,4])
                if self.tbwCond_Pos.rowCount() <= 0:
                    self.tbwCond_Pos.insertRow(self.tbwCond_Pos.rowCount())
                self.tbwCond_Pos.setItem(0, col, item)
                col += 1

            self.leVN_ID.clear()
            self.leVN_ID.setText(Data[12])
            self.leVN_II.clear()


    def Grabar(self):
        Hora=datetime.now().strftime("%H:%M:%S.%f")

        Detalle=[]
        nrofilas=self.tbwCond_Pos.rowCount()
        for i in range(nrofilas):
            fila=[]
            fila.append(Data[0])
            fila.append(Data[6])
            fila.append(Año)
            fila.append(2)

            tipcondcomp=self.tbwCond_Pos.item(i,0).text()
            for k,v in dicCond_Comp.items():
                if v==tipcondcomp:
                    condcomp=k

            fila.append(condcomp)
            fila.append(Data[10])

            try:
                porcentaje=self.tbwCond_Pos.item(i,1).text().replace(",","")
            except:
                porcentaje=""

            fila.append(porcentaje)

            try:
                monto=self.tbwCond_Pos.item(i,2).text().replace(",","")
            except:
                monto=""

            fila.append(monto)

            try:
                valor=self.tbwCond_Pos.item(i,3).text().replace(",","")
            except:
                valor=""

            fila.append(valor)

            try:
                descripmoneda=self.tbwCond_Pos.item(i,4).text()
                for k,v in dicMoneda.items():
                    if v==descripmoneda:
                        moneda=k
            except:
                moneda=""

            fila.append(moneda)
            fila.append(Fecha)
            fila.append(Hora)
            fila.append(Data[2])
            Detalle.append(tuple(fila))

        nrofilas2=self.tbwCond_Pos_2.rowCount()
        for i in range(nrofilas2):
            fila2=[]
            fila2.append(Data[0])
            fila2.append(Data[6])
            fila2.append(Año)
            fila2.append(2)

            tipcondcomp=self.tbwCond_Pos_2.item(i,0).text()
            for k,v in dicCond_Comp.items():
                if v==tipcondcomp:
                    condcomp=k

            fila2.append(condcomp)
            fila2.append(Data[10])

            try:
                porcentaje=self.tbwCond_Pos_2.item(i,1).text().replace(",","")
            except:
                porcentaje=""

            fila2.append(porcentaje)

            try:
                monto=self.tbwCond_Pos_2.item(i,2).text().replace(",","")
            except:
                monto=""

            fila2.append(monto)

            try:
                valor=self.tbwCond_Pos_2.item(i,3).text().replace(",","")
            except:
                valor=""

            fila2.append(valor)

            try:
                descripmoneda=self.tbwCond_Pos_2.item(i,4).text()
                for k,v in dicMoneda.items():
                    if v==descripmoneda:
                        moneda=k
            except:
                moneda=""

            fila2.append(moneda)
            fila2.append(Fecha)
            fila2.append(Hora)
            fila2.append(Data[2])
            Detalle.append(tuple(fila2))

        sql='''INSERT INTO TAB_COMP_012_Condiciones_de_Pedido_de_Compras(Cod_Soc, Nro_Pedido, Año_Pedido, Clase_condicion, Tipo_Cond_compra, Item_Pedido, Porcentaje, Cantidad, Valor_Condicion, Moneda, Fecha_Reg, Hora_Reg, Usuario_Reg)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        respuesta=ejecutarSqlDB(sql,Detalle)

        if respuesta['respuesta']=='correcto':
            mensajeDialogo("informacion", "Información", "Las Condiciones de Posicion se han grabado correctamente")

        else:
            mensajeDialogo("error", "Error", "Ocurrio un problema, comuniquese con soporte")

    def Salir(self):
        self.close()

if __name__ == '__main__':
    app=QApplication(sys.argv)
    _main=Condiciones_Posicion()
    _main.showMaximized()
    app.exec_()
