import sys
from datetime import datetime
from Funciones04 import*
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
import urllib.request

sqlTipo_Inter="SELECT Descrip_inter,Cod_tipo_inter FROM TAB_SOC_014_Tipo_de_Interlocutor"

class Interlocutor(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("ERP_PCOMP_006.ui",self)

        global TipoInter, dicTipoInter

        self.pbGrabar.clicked.connect(self.Grabar)
        self.pbRetornar.clicked.connect(self.Retornar)

        TipoInter = consultarSql(sqlTipo_Inter)
        dicTipoInter={}
        for dato in TipoInter:
            dicTipoInter[dato[1]]=dato[0]

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
        cargarIcono(self.pbRetornar, 'salir')
        cargarIcono(self.pbGrabar, 'grabar')

        sqlInter="SELECT b.Descrip_inter,a.Nombre_Inter,a.Correo_Inter,a.DNI_Inter,a.Anexo,a.Telef_Fijo,a.Telef_Inter,a.Estado_Inter FROM TAB_COMP_013_Pedido_de_Compra_Interlocutor a LEFT JOIN TAB_SOC_014_Tipo_de_Interlocutor b ON a.Tipo_Inter=b.Cod_tipo_inter WHERE a.Cod_Empresa='%s'AND a.Año_Pedido='%s'AND a.Nro_Pedido='%s'" %(Cod_Soc,Año,Nro_Pedido)
        datos=consultarSql(sqlInter)

        if datos!=[]:
            cargarInter(self.tbwInter_Ped_Comp,sqlInter)
            self.pbGrabar.setEnabled(False)
        else:
            sqlInter="SELECT b.Descrip_inter,a.Nombre_Inter,a.Correo_Inter,a.DNI_Inter,a.Anexo,a.Telef_Fijo,a.Telef_Inter,a.Estado_Inter FROM TAB_PROV_002_Registro_de_Interlocutores_del_Proveedor a LEFT JOIN TAB_SOC_014_Tipo_de_Interlocutor b ON a.Tipo_Inter_Prov=b.Cod_tipo_inter WHERE a.Cod_Prov='%s'AND a.Estado_Inter='1'" %(Cod_Prov)
            cargarInter(self.tbwInter_Ped_Comp,sqlInter)

    def Grabar(self):
        try:
            Descrip_inter=self.tbwInter_Ped_Comp.item(self.tbwInter_Ped_Comp.currentRow(), 0).text()
            for k,v in dicTipoInter.items():
                if Descrip_inter==v:
                    Tipo_Inter=k

            data=[]
            d=self.tbwInter_Ped_Comp.columnCount()-1
            for n in range(d):
                if n!=0:
                    if self.tbwInter_Ped_Comp.item(self.tbwInter_Ped_Comp.currentRow(),n)==None:
                        m=""
                    else:
                        m=self.tbwInter_Ped_Comp.item(self.tbwInter_Ped_Comp.currentRow(),n).text()
                    data.append(m)

            Nombre_Inter=data[0]
            Correo_Inter=data[1]
            DNI_Inter=data[2]
            Anexo=data[3]
            Telf_Fijo=data[4]
            Telf_Inter=data[5]
            Estado_Inter=1

            Hora=datetime.now().strftime("%H:%M:%S.%f")

            sql ="INSERT INTO TAB_COMP_013_Pedido_de_Compra_Interlocutor (Cod_Empresa,Año_Pedido,Nro_Pedido,Tipo_Inter,Nombre_Inter,Correo_Inter,DNI_Inter,Anexo,Telef_Fijo,Telef_Inter,Estado_Inter,Usuario_Reg,Fecha_Reg,Hora_Reg) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (Cod_Soc,Año,Nro_Pedido,Tipo_Inter,Nombre_Inter,Correo_Inter,DNI_Inter,Anexo,Telf_Fijo,Telf_Inter,Estado_Inter,Cod_Usuario,Fecha,Hora)
            respuesta=ejecutarSql(sql)

            if respuesta['respuesta']=='correcto':
                mensajeDialogo("informacion", "Información", "Registro guardado")
                self.pbGrabar.setEnabled(False)

            elif respuesta['respuesta']=='incorrecto':
                mensajeDialogo("error", "Error", "Ingrese Datos Válido")

            sqlInter="SELECT b.Descrip_inter,a.Nombre_Inter,a.Correo_Inter,a.DNI_Inter,a.Anexo,a.Telef_Fijo,a.Telef_Inter,a.Estado_Inter FROM TAB_COMP_013_Pedido_de_Compra_Interlocutor a LEFT JOIN TAB_SOC_014_Tipo_de_Interlocutor b ON a.Tipo_Inter=b.Cod_tipo_inter WHERE a.Cod_Empresa='%s'AND a.Año_Pedido='%s'AND a.Nro_Pedido='%s';" %(Cod_Soc,Año,Nro_Pedido)
            cargarInter(self.tbwInter_Ped_Comp,sqlInter)

        except Exception as e:
            mensajeDialogo("error", "Error", "Faltan datos, verifique")
            print(e)

    def Retornar(self):
        self.close()

if __name__ == '__main__':
    app=QApplication(sys.argv)
    _main=Interlocutor()
    _main.showMaximized()
    app.exec_()
