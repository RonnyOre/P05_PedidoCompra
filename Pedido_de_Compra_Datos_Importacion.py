import sys
from datetime import datetime
from Funciones04 import*
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from Pedido_de_Compra_Datos_Importacion_Continuacion import Continuacion
import urllib.request

sqlProvAdu="SELECT Razón_social,Cod_prov FROM TAB_PROV_001_Registro_de_Proveedores WHERE Tip_Prov='5'"
sqlPais="SELECT Nombre, Cod_Pais FROM TAB_SOC_009_Ubigeo WHERE Cod_Depart_Region='0' AND Cod_Provincia='0' AND Cod_Distrito='0'"
sqlMoneda="SELECT Descrip_moneda,Cod_moneda FROM TAB_SOC_008_Monedas"

# sqlProvTra="SELECT Razón_social,Cod_prov FROM TAB_PROV_001_Registro_de_Proveedores WHERE Tip_Prov='4'"
# ProvTra=consultarSql(sqlProvTra)
# dicProvTra={}
# for t in ProvTra:
#     dicProvTra[t[1]]=t[0]

class TextoEnvio(QDialog):
    def __init__(self,Nro_Ped):
        QDialog.__init__(self)
        uic.loadUi('ERP_COMP_P001_Texto_Envio.ui',self)

        global NroDoc
        NroDoc=Nro_Ped

        self.pbGrabar.clicked.connect(self.Grabar)
        self.pbModificar.clicked.connect(self.Modificar)
        self.pbSalir.clicked.connect(self.Salir)

        cargarIcono(self, 'erp')
        cargarIcono(self.pbGrabar, 'grabar')
        cargarIcono(self.pbModificar,'modificar')
        cargarIcono(self.pbSalir,'salir')

        sqlTexEnv="SELECT Text_Envio  FROM TAB_COMP_006_Datos_de_Importacion WHERE Cod_Empresa='%s' AND Nro_Pedido='%s';"%(Cod_Soc,NroDoc)
        TexEnv=convlist(sqlTexEnv)

        if TexEnv!=[]:
            if len(TexEnv[0])!=0:
                self.teDetalle.setPlainText(TexEnv[0])
                self.teDetalle.setEnabled(False)
                self.pbGrabar.setEnabled(False)

        else:
            try:
                self.teDetalle.setPlainText(texto_envio)
                self.teDetalle.setEnabled(False)
                self.pbGrabar.setEnabled(False)
            except Exception as e:
            	print(e)

    def Grabar(self):
        global texto_envio
        texto_envio = self.teDetalle.toPlainText()

        Hora=datetime.now().strftime("%H:%M:%S.%f")

        sqlTexEnv="SELECT Text_Envio FROM TAB_COMP_006_Datos_de_Importacion WHERE Cod_Empresa='%s' AND Nro_Pedido='%s';"%(Cod_Soc,NroDoc)
        TexEnv=convlist(sqlTexEnv)

        if TexEnv!=[]:
            sqlTextoEnvio="UPDATE TAB_COMP_006_Datos_de_Importacion SET Text_Envio='%s',Fecha_Mod='%s',Hora_Mod='%s',Usuario_Mod='%s' WHERE Cod_Empresa='%s' AND Nro_Pedido='%s';"%(texto_envio,Fecha,Hora,Cod_Usuario,Cod_Soc,NroDoc)
            respuesta=ejecutarSql(sqlTextoEnvio)

            if len(TexEnv[0])!=0:

                if respuesta['respuesta']=='correcto':
                    mensajeDialogo("informacion", "Información", "Texto de Envio Modificado")
                    del texto_envio
                    self.close()

                elif respuesta['respuesta']=='incorrecto':
                    mensajeDialogo("error", "Error", "El Texto de Envio no se pudo modificar")
            else:

                if respuesta['respuesta']=='correcto':
                    mensajeDialogo("informacion", "Información", "Texto de Envio grabado correctamente")
                    del texto_envio
                    self.close()

                elif respuesta['respuesta']=='incorrecto':
                    mensajeDialogo("error", "Error", "El Texto de Envio no se pudo grabar")

        else:
            mensajeDialogo("informacion", "Información", "Texto de Envio grabado correctamente")
            self.close()

        self.teDetalle.setEnabled(False)
        self.pbGrabar.setEnabled(False)

    def Modificar(self):
        self.teDetalle.setEnabled(True)
        self.pbGrabar.setEnabled(True)

    def Salir(self):
        self.close()

class Datos_Importacion(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("ERP_PCOMP_009.ui",self)

        global dicProvAdu,dicPais,dicMoneda

        self.pbSalir.clicked.connect(self.Salir)
        self.pbContinuar.clicked.connect(self.Continuar)
        self.pbTexto_Envio.clicked.connect(self.TextoEnvio)
        self.deFecha_Solicitud.dateChanged.connect(self.Fecha_Solicitud)
        self.deFecha_Inicio.dateChanged.connect(self.Fecha_Inicio)
        self.deFecha_Embarque.dateChanged.connect(self.Fecha_Embarque)
        self.deFecha_Puerto_Callao.dateChanged.connect(self.Fecha_Puerto_Callao)

        ProvAdu=consultarSql(sqlProvAdu)
        dicProvAdu={}
        for a in ProvAdu:
            dicProvAdu[a[1]]=a[0]

        Pais=consultarSql(sqlPais)
        dicPais={}
        for p in Pais:
            dicPais[p[1]]=p[0]

        Moneda=consultarSql(sqlMoneda)
        dicMoneda={}
        for m in Moneda:
            dicMoneda[m[1]]=m[0]

        insertarDatos(self.cbAgente_Aduanas,ProvAdu)
        self.cbAgente_Aduanas.setCurrentIndex(-1)
        insertarDatos(self.cbMoneda,Moneda)
        self.cbMoneda.setCurrentIndex(-1)
        insertarDatos(self.cbPais_Origen,Pais)
        self.cbPais_Origen.setCurrentIndex(-1)

        self.leFecha_Solicitud.setReadOnly(True)
        self.leFecha_Inicio.setReadOnly(True)
        self.leFecha_Embarque.setReadOnly(True)
        self.leFecha_Puerto_Callao.setReadOnly(True)

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
        cargarIcono(self.pbSalir, 'salir')
        cargarIcono(self.pbContinuar, 'continuar')
        cargarIcono(self.pbTexto_Envio, 'envio')

        # sqlDatImp="SELECT  a.Agente_Aduana, a.Nro_Servicio, a.Fecha_Solicitud, a.Declaración_Aduana, a.Fecha_Inicio_Tramite, b.Nombre, c.Descrip_moneda, a.Via_embarque, a.Puerto_Emb, a.Fecha_Embarque, a.Nro_Embarque, a.Incoterms1, a.Incoterms2, a.Contenedor, a.Fecha_Callao, a.Nro_manifiesto, a.RUC_Declarante, a.Porc_Deposito, a.Tiempo_Envio FROM TAB_COMP_006_Datos_de_Importacion a LEFT JOIN TAB_SOC_009_Ubigeo b ON b.Cod_Pais=a.País_Origen AND b.Cod_Depart_Region='0' AND b.Cod_Provincia='0' AND b.Cod_Distrito='0' LEFT JOIN TAB_SOC_008_Monedas c ON c.Cod_moneda=a.Moneda WHERE a.Cod_Empresa='%s' AND a.Nro_Pedido='%s'"%(Cod_Soc,Nro_Pedido)
        # DatImp=convlist(sqlDatImp)

        sqlDatImp="SELECT  d.Razón_social, a.Nro_Servicio, a.Fecha_Solicitud, a.Declaración_Aduana, a.Fecha_Inicio_Tramite, b.Nombre, c.Descrip_moneda, a.Via_embarque, a.Puerto_Emb, a.Fecha_Embarque, a.Nro_Embarque, a.Incoterms1, a.Incoterms2, a.Contenedor, a.Fecha_Callao, a.Nro_manifiesto, a.RUC_Declarante, a.Porc_Deposito, a.Tiempo_Envio FROM TAB_COMP_006_Datos_de_Importacion a LEFT JOIN TAB_SOC_009_Ubigeo b ON b.Cod_Pais=a.País_Origen AND b.Cod_Depart_Region='0' AND b.Cod_Provincia='0' AND b.Cod_Distrito='0' LEFT JOIN TAB_SOC_008_Monedas c ON c.Cod_moneda=a.Moneda LEFT JOIN TAB_PROV_001_Registro_de_Proveedores d ON a.Agente_Aduana=d.Cod_prov AND d.Tip_Prov='5' WHERE a.Cod_Empresa='%s' AND a.Nro_Pedido='%s'"%(Cod_Soc,Nro_Pedido)
        DatImp=convlist(sqlDatImp)

        if DatImp!=[]:
            self.cbAgente_Aduanas.setCurrentText(DatImp[0])
            self.leNro_Servicio.setText(DatImp[1])
            self.leFecha_Solicitud.setText(formatearFecha(DatImp[2]))
            self.leNro_Doc_Aduanas.setText(DatImp[3])
            self.leFecha_Inicio.setText(formatearFecha(DatImp[4]))
            self.cbPais_Origen.setCurrentText(DatImp[5])
            self.cbMoneda.setCurrentText(DatImp[6])
            self.leVia_Embarque.setText(DatImp[7])
            self.lePuerto_Embarque.setText(DatImp[8])
            self.leFecha_Embarque.setText(formatearFecha(DatImp[9]))
            self.leNro_Embarque.setText(DatImp[10])
            self.leIncoterms_1.setText(DatImp[11])
            self.leIncoterms_2.setText(DatImp[12])
            self.leContenedor.setText(DatImp[13])
            self.leFecha_Puerto_Callao.setText(formatearFecha(DatImp[14]))
            self.leNro_Manifiesto.setText(DatImp[15])
            self.leRUC_Declarante.setText(DatImp[16])
            self.lePorc_Deposito.setText(formatearDecimal(DatImp[17],'3'))
            self.leTiempo_Envio.setText(DatImp[18])

            self.cbAgente_Aduanas.setEnabled(False)
            self.leNro_Servicio.setReadOnly(True)
            self.leNro_Doc_Aduanas.setReadOnly(True)
            self.cbPais_Origen.setEnabled(False)
            self.cbMoneda.setEnabled(False)
            self.leVia_Embarque.setReadOnly(True)
            self.lePuerto_Embarque.setReadOnly(True)
            self.leNro_Embarque.setReadOnly(True)
            self.leIncoterms_1.setReadOnly(True)
            self.leIncoterms_2.setReadOnly(True)
            self.leContenedor.setReadOnly(True)
            self.leNro_Manifiesto.setReadOnly(True)
            self.leRUC_Declarante.setReadOnly(True)
            self.lePorc_Deposito.setReadOnly(True)
            self.leTiempo_Envio.setReadOnly(True)

    def Fecha_Solicitud(self):
        Fec_Final=QDateToStrView(self.deFecha_Solicitud)
        self.leFecha_Solicitud.setText(Fec_Final)

    def Fecha_Inicio(self):
        Fec_Final=QDateToStrView(self.deFecha_Inicio)
        self.leFecha_Inicio.setText(Fec_Final)

    def Fecha_Embarque(self):
        Fec_Final=QDateToStrView(self.deFecha_Embarque)
        self.leFecha_Embarque.setText(Fec_Final)

    def Fecha_Puerto_Callao(self):
        Fec_Final=QDateToStrView(self.deFecha_Puerto_Callao)
        self.leFecha_Puerto_Callao.setText(Fec_Final)

    def Grabar2(self):

        global texto_envio
        Fecha=datetime.now().strftime("%Y-%m-%d")
        Hora=datetime.now().strftime("%H:%M:%S.%f")
        agenteaduana=self.cbAgente_Aduanas.currentText()
        for k,v in dicProvAdu.items():
            if v==agenteaduana:
                Agente_Aduana=k

        Nro_Servicio=self.leNro_Servicio.text()

        fechasolicitud=self.leFecha_Solicitud.text()
        Fecha_Solicitud=formatearFecha(fechasolicitud)

        Nro_Doc_Aduanas=self.leNro_Doc_Aduanas.text()

        fechainicio=self.leFecha_Inicio.text()
        Fecha_Inicio=formatearFecha(fechainicio)

        paisorigen=self.cbPais_Origen.currentText()
        for k,v in dicPais.items():
            if v==paisorigen:
                Pais_Origen=k

        moneda=self.cbMoneda.currentText()
        for k,v in dicMoneda.items():
            if v==moneda:
                Moneda=k

        Via_Embarque=self.leVia_Embarque.text()
        Puerto_Embarque=self.lePuerto_Embarque.text()

        fechaembarque=self.leFecha_Embarque.text()
        Fecha_Embarque=formatearFecha(fechaembarque)

        Nro_Embarque=self.leNro_Embarque.text()
        Incoterms_1=self.leIncoterms_1.text()
        Incoterms_2=self.leIncoterms_2.text()
        Contenedor=self.leContenedor.text()

        fechapuertocallao=self.leFecha_Puerto_Callao.text()
        Fecha_Puerto_Callao=formatearFecha(fechapuertocallao)

        Nro_Manifiesto=self.leNro_Manifiesto.text()
        RUC_Declarante=self.leRUC_Declarante.text()
        Porc_Deposito=self.lePorc_Deposito.text()
        Tiempo_Envio=self.leTiempo_Envio.text()

        try:
            if texto_envio!=None:
                sql='''UPDATE TAB_COMP_006_Datos_de_Importacion SET Agente_Aduana='%s',Nro_Servicio='%s',Fecha_Solicitud='%s',Declaración_Aduana='%s',Fecha_Inicio_Tramite='%s',País_Origen='%s',Moneda='%s',Via_embarque='%s',Puerto_Emb='%s',Fecha_Embarque='%s',Nro_Embarque='%s',Incoterms1='%s',Incoterms2='%s',Contenedor='%s',Fecha_Callao='%s',Nro_manifiesto='%s',RUC_Declarante='%s',Porc_Deposito='%s',Tiempo_Envio='%s',Text_Envio='%s' WHERE Cod_Empresa='%s' AND Nro_Pedido='%s';'''%(Agente_Aduana,Nro_Servicio,Fecha_Solicitud,Nro_Doc_Aduanas,Fecha_Inicio,Pais_Origen,Moneda,Via_Embarque,Puerto_Embarque,Fecha_Embarque,Nro_Embarque,Incoterms_1,Incoterms_2,Contenedor,Fecha_Puerto_Callao,Nro_Manifiesto,RUC_Declarante,Porc_Deposito,Tiempo_Envio,texto_envio,Cod_Soc,Nro_Pedido)
                respuesta=ejecutarSql(sql)
                del texto_envio
        except Exception as e:
            sql='''UPDATE TAB_COMP_006_Datos_de_Importacion SET Agente_Aduana='%s',Nro_Servicio='%s',Fecha_Solicitud='%s',Declaración_Aduana='%s',Fecha_Inicio_Tramite='%s',País_Origen='%s',Moneda='%s',Via_embarque='%s',Puerto_Emb='%s',Fecha_Embarque='%s',Nro_Embarque='%s',Incoterms1='%s',Incoterms2='%s',Contenedor='%s',Fecha_Callao='%s',Nro_manifiesto='%s',RUC_Declarante='%s',Porc_Deposito='%s',Tiempo_Envio='%s' WHERE Cod_Empresa='%s' AND Nro_Pedido='%s';'''%(Agente_Aduana,Nro_Servicio,Fecha_Solicitud,Nro_Doc_Aduanas,Fecha_Inicio,Pais_Origen,Moneda,Via_Embarque,Puerto_Embarque,Fecha_Embarque,Nro_Embarque,Incoterms_1,Incoterms_2,Contenedor,Fecha_Puerto_Callao,Nro_Manifiesto,RUC_Declarante,Porc_Deposito,Tiempo_Envio,Cod_Soc,Nro_Pedido)
            respuesta=ejecutarSql(sql)
            print(e)


        # sql='''INSERT INTO TAB_COMP_006_Datos_de_Importacion(Cod_Empresa,Nro_Pedido,Agente_Aduana,Nro_Servicio,Fecha_Solicitud,Declaración_Aduana,Fecha_Inicio_Tramite,País_Origen,Moneda,Via_embarque,Puerto_Emb,Fecha_Embarque,Nro_Embarque,Incoterms1,Incoterms2,Contenedor,Fecha_Callao,Nro_manifiesto,RUC_Declarante,Porc_Deposito,Tiempo_Envio)
        # VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')'''%(Cod_Soc,Nro_Pedido,Agente_Aduana,Nro_Servicio,Fecha_Solicitud,Nro_Doc_Aduanas,Fecha_Inicio,Pais_Origen,Moneda,Via_Embarque,Puerto_Embarque,Fecha_Embarque,Nro_Embarque,Incoterms_1,Incoterms_2,Contenedor,Fecha_Puerto_Callao,Nro_Manifiesto,RUC_Declarante,Porc_Deposito,Tiempo_Envio)
        # respuesta=ejecutarSql(sql)

        if respuesta['respuesta']=='correcto':
            # mensajeDialogo("informacion", "Información", "Registro guardado")
            self.cbAgente_Aduanas.setEnabled(False)
            self.leNro_Servicio.setReadOnly(True)
            self.deFecha_Solicitud.setReadOnly(True)
            self.leNro_Doc_Aduanas.setReadOnly(True)
            self.deFecha_Inicio.setReadOnly(True)
            self.cbPais_Origen.setEnabled(False)
            self.cbMoneda.setEnabled(False)
            self.leVia_Embarque.setReadOnly(True)
            self.lePuerto_Embarque.setReadOnly(True)
            self.deFecha_Embarque.setReadOnly(True)
            self.leNro_Embarque.setReadOnly(True)
            self.leIncoterms_1.setReadOnly(True)
            self.leIncoterms_2.setReadOnly(True)
            self.leContenedor.setReadOnly(True)
            self.deFecha_Puerto_Callao.setReadOnly(True)
            self.leNro_Manifiesto.setReadOnly(True)
            self.leRUC_Declarante.setReadOnly(True)
            self.lePorc_Deposito.setReadOnly(True)
            self.leTiempo_Envio.setReadOnly(True)

        elif respuesta['respuesta']=='incorrecto':
            print("")
            # mensajeDialogo("error", "Error", "Ingrese Datos Válido")

    def Continuar(self):
        self.co=Continuacion()
        self.co.datosCabecera(Cod_Soc,Nom_Soc,Cod_Usuario,Nro_Pedido)
        self.co.pbGrabar.clicked.connect(self.Grabar2)
        self.co.showMaximized()

    def TextoEnvio(self):
        try:
            Nro_Pedido=self.leNro_Pedido.text()
            TextoEnvio(Nro_Pedido).exec_()
        except Exception as e:
            mensajeDialogo("error", "Error", "Ocurrio un error, contacte a soporte")
            print(e)

    def Salir(self):
        reply = mensajeDialogo("pregunta", "Pregunta","Recuerde grabar la información. ¿Realmente desea salir?")
        if reply == 'Yes':
            self.close()

if __name__ == '__main__':
    app=QApplication(sys.argv)
    _main=Datos_Importacion()
    _main.showMaximized()
    app.exec_()
