import sys
from datetime import datetime
from Funciones04 import*
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
import urllib.request

class Continuacion(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("ERP_PCOMP_010.ui",self)

        self.pbGrabar.clicked.connect(self.Grabar)
        self.pbSalir.clicked.connect(self.Salir)
        self.deFecha_Desaduanaje.dateChanged.connect(self.Fecha_Desaduanaje)
        self.deFecha_Ingreso_Alm_Aduana.dateChanged.connect(self.Fecha_Ingreso_Alm_Aduana)
        self.deFecha_Salida_Alm_Aduana.dateChanged.connect(self.Fecha_Salida_Alm_Aduana)
        self.deFecha_Alm_Propio.dateChanged.connect(self.Fecha_Alm_Propio)

        self.leFecha_Desaduanaje.setReadOnly(True)
        self.leFecha_Ingreso_Alm_Aduana.setReadOnly(True)
        self.leFecha_Salida_Alm_Aduana.setReadOnly(True)
        self.leFecha_Alm_Propio.setReadOnly(True)

        self.validarHora()

    def datosCabecera(self,codsoc,nomsoc,codusuario,nropedido):

        global Cod_Soc,Nom_Soc,Cod_Usuario,Nro_Pedido

        Cod_Soc=codsoc
        Nom_Soc=nomsoc
        Cod_Usuario=codusuario
        Nro_Pedido=nropedido

        cargarLogo(self.lbLogo_Mp,'multiplay')
        cargarLogo(self.lbLogo_Soc, Cod_Soc)
        cargarIcono(self, 'erp')
        cargarIcono(self.pbSalir, 'salir')
        cargarIcono(self.pbGrabar, 'grabar')

        sqlDatImp="SELECT  Fecha_Aduana, Fecha_Ingreso_Alm_Aduana, Fecha_Salida_Alm_Aduana, Fecha_Alm, Hora_Alm, Empresa_Transp, Name_Chofer, Placa_Transp, Cant_Comercial, Cant_Bultos, Unidad_bulto, Peso_Neto_Kg, Peso_bruto, Cant_Fisica, Sub_partida, FOB_Moneda_$, Flete_$, Seguro_$, Ajuste_Valor_$, Valor_Aduana_$ FROM TAB_COMP_006_Datos_de_Importacion WHERE Cod_Empresa='%s' AND Nro_Pedido='%s'"%(Cod_Soc,Nro_Pedido)
        DatImp=convlist(sqlDatImp)
        if DatImp!=[]:
            self.leFecha_Desaduanaje.setText(formatearFecha(DatImp[0]))
            self.leFecha_Ingreso_Alm_Aduana.setText(formatearFecha(DatImp[1]))
            self.leFecha_Salida_Alm_Aduana.setText(formatearFecha(DatImp[2]))
            self.leFecha_Alm_Propio.setText(formatearFecha(DatImp[3]))
            self.leHora.setText(DatImp[4])
            self.leEmpresa_Transporte.setText(DatImp[5])
            self.leNombre_Chofer.setText(DatImp[6])
            self.lePlaca.setText(DatImp[7])
            self.leCant_Comercial.setText(formatearDecimal(DatImp[8],'2'))
            self.leCant_Bultos.setText(DatImp[9])
            self.leUnid_Bulto.setText(DatImp[10])
            self.leCant_Fisica.setText(formatearDecimal(DatImp[11],'3'))
            self.lePeso_Neto.setText(formatearDecimal(DatImp[12],'3'))
            self.lePeso_Bruto.setText(formatearDecimal(DatImp[13],'3'))
            self.leNro_SubPartida.setText(DatImp[14])
            self.leValor_FOB.setText(formatearDecimal(DatImp[15],'3'))
            self.leFlete.setText(formatearDecimal(DatImp[16],'3'))
            self.leSeguro.setText(formatearDecimal(DatImp[17],'3'))
            self.leAjuste_Valor.setText(formatearDecimal(DatImp[18],'3'))
            self.leValor_Aduana.setText(formatearDecimal(DatImp[19],'3'))

            self.leHora.setReadOnly(True)
            self.leEmpresa_Transporte.setReadOnly(True)
            self.leNombre_Chofer.setReadOnly(True)
            self.lePlaca.setReadOnly(True)
            self.leCant_Comercial.setReadOnly(True)
            self.leCant_Bultos.setReadOnly(True)
            self.leUnid_Bulto.setReadOnly(True)
            self.leCant_Fisica.setReadOnly(True)
            self.lePeso_Neto.setReadOnly(True)
            self.lePeso_Bruto.setReadOnly(True)
            self.leNro_SubPartida.setReadOnly(True)
            self.leValor_FOB.setReadOnly(True)
            self.leFlete.setReadOnly(True)
            self.leSeguro.setReadOnly(True)
            self.leAjuste_Valor.setReadOnly(True)
            self.leValor_Aduana.setReadOnly(True)

            self.pbGrabar.setEnabled(False)

    def validarHora(self):
        # reg_ex = QRegExp("^(?:0?[1-9]|1[0-2]):[0-5][0-9]\s?(?:[AaPp](\.?)[Mm]\1)?$") ## Formato 12 horas
        reg_ex = QRegExp("^(?:0?[0-9]|1[0-9]|2[0-3]):[0-5][0-9]\s?$") ## Formato 24 horas
        input_validator = QRegExpValidator(reg_ex, self.leHora)
        self.leHora.setValidator(input_validator)

    def Fecha_Desaduanaje(self):
        Fec_Final=QDateToStrView(self.deFecha_Desaduanaje)
        self.leFecha_Desaduanaje.setText(Fec_Final)

    def Fecha_Ingreso_Alm_Aduana(self):
        Fec_Final=QDateToStrView(self.deFecha_Ingreso_Alm_Aduana)
        self.leFecha_Ingreso_Alm_Aduana.setText(Fec_Final)

    def Fecha_Salida_Alm_Aduana(self):
        Fec_Final=QDateToStrView(self.deFecha_Salida_Alm_Aduana)
        self.leFecha_Salida_Alm_Aduana.setText(Fec_Final)

    def Fecha_Alm_Propio(self):
        Fec_Final=QDateToStrView(self.deFecha_Alm_Propio)
        self.leFecha_Alm_Propio.setText(Fec_Final)

    def Grabar(self):

        Fecha_Desaduanaje=formatearFecha(self.leFecha_Desaduanaje.text())
        Fecha_Alm_Propio=formatearFecha(self.leFecha_Alm_Propio.text())
        Fecha_Ingreso_Alm_Aduana=formatearFecha(self.leFecha_Ingreso_Alm_Aduana.text())
        Fecha_Salida_Alm_Aduana=formatearFecha(self.leFecha_Salida_Alm_Aduana.text())
        Hora_Alm=self.leHora.text()
        Empresa_Transporte=self.leEmpresa_Transporte.text()
        Nombre_Chofer=self.leNombre_Chofer.text()
        Placa=self.lePlaca.text()
        Cant_Comercial=self.leCant_Comercial.text()
        Cant_Bultos=self.leCant_Bultos.text()
        Unid_Bulto=self.leUnid_Bulto.text()
        Cant_Fisica=self.leCant_Fisica.text()
        Peso_Neto=self.lePeso_Neto.text()
        Peso_Bruto=self.lePeso_Bruto.text()
        Nro_SubPartida=self.leNro_SubPartida.text()
        Valor_FOB=self.leValor_FOB.text()
        Flete=self.leFlete.text()
        Seguro=self.leSeguro.text()
        Ajuste_Valor=self.leAjuste_Valor.text()
        Valor_Aduana=self.leValor_Aduana.text()

        Fecha=datetime.now().strftime("%Y-%m-%d")
        Hora=datetime.now().strftime("%H:%M:%S.%f")

        # sql='''UPDATE TAB_COMP_006_Datos_de_Importacion SET Cant_Comercial='%s', Cant_Bultos='%s', Unidad_bulto='%s', Peso_Neto_Kg='%s', Peso_bruto='%s', Cant_Fisica='%s', Sub_partida='%s', FOB_Moneda_$='%s', Flete_$='%s', Seguro_$='%s', Ajuste_Valor_$='%s', Valor_Aduana_$='%s', Fecha_Reg='%s', Hora_Reg='%s', Usuario_Reg='%s'
        # WHERE Cod_Empresa='%s' AND Nro_Pedido='%s';'''%(Fecha_Desaduanaje,Fecha_Alm_Propio,Hora,Placa,Nombre_Chofer,Empresa_Transporte,Cant_Comercial,Cant_Bultos,Unid_Bulto,Peso_Neto,Peso_Bruto,Cant_Fisica,Nro_SubPartida,Valor_FOB,Flete,Seguro,Ajuste_Valor,Valor_Aduana,Fecha,Hora,Cod_Usuario,Cod_Soc,Nro_Pedido)
        # respuesta=ejecutarSql(sql)

        sql='''INSERT INTO TAB_COMP_006_Datos_de_Importacion(Cod_Empresa,Nro_Pedido,Fecha_Aduana,Fecha_Ingreso_Alm_Aduana,Fecha_Salida_Alm_Aduana,Fecha_Alm,Hora_Alm,Empresa_Transp,Name_Chofer,Placa_Transp,Cant_Comercial,Cant_Bultos,Unidad_bulto,Peso_Neto_Kg,Peso_bruto,Cant_Fisica,Sub_partida,FOB_Moneda_$,Flete_$,Seguro_$,Ajuste_Valor_$,Valor_Aduana_$,Fecha_Reg,Hora_Reg,Usuario_Reg) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')'''%(Cod_Soc,Nro_Pedido,Fecha_Desaduanaje,Fecha_Ingreso_Alm_Aduana,Fecha_Salida_Alm_Aduana,Fecha_Alm_Propio,Hora_Alm,Empresa_Transporte,Nombre_Chofer,Placa,Cant_Comercial,Cant_Bultos,Unid_Bulto,Peso_Neto,Peso_Bruto,Cant_Fisica,Nro_SubPartida,Valor_FOB,Flete,Seguro,Ajuste_Valor,Valor_Aduana,Fecha,Hora,Cod_Usuario)
        respuesta=ejecutarSql(sql)

        if respuesta['respuesta']=='correcto':
            mensajeDialogo("informacion", "Información", "Datos de importación grabados correctamente")
            self.pbGrabar.setEnabled(False)

            self.deFecha_Desaduanaje.setReadOnly(True)
            self.deFecha_Ingreso_Alm_Aduana.setReadOnly(True)
            self.deFecha_Salida_Alm_Aduana.setReadOnly(True)
            self.deFecha_Alm_Propio.setReadOnly(True)
            self.leHora.setReadOnly(True)
            self.leEmpresa_Transporte.setReadOnly(True)
            self.leNombre_Chofer.setReadOnly(True)
            self.lePlaca.setReadOnly(True)
            self.leCant_Comercial.setReadOnly(True)
            self.leCant_Bultos.setReadOnly(True)
            self.leUnid_Bulto.setReadOnly(True)
            self.leCant_Fisica.setReadOnly(True)
            self.lePeso_Neto.setReadOnly(True)
            self.lePeso_Bruto.setReadOnly(True)
            self.leNro_SubPartida.setReadOnly(True)
            self.leValor_FOB.setReadOnly(True)
            self.leFlete.setReadOnly(True)
            self.leSeguro.setReadOnly(True)
            self.leAjuste_Valor.setReadOnly(True)
            self.leValor_Aduana.setReadOnly(True)

        elif respuesta['respuesta']=='incorrecto':
            mensajeDialogo("error", "Error", "Ocurrio un problema, comuniquese con soporte")

    def Salir(self):
        self.close()

if __name__ == '__main__':
    app=QApplication(sys.argv)
    _main=Datos_Importacion()
    _main.showMaximized()
    app.exec_()
