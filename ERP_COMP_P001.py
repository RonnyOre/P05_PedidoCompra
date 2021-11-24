import sys
from datetime import datetime
from Funciones04 import *
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import urllib.request
import pandas as pd
from pylab import *
from fpdf import FPDF
import tkinter as tk
from tkinter import filedialog
from ERP_COMP_P001_Pedido_de_Compra import Pedido_de_Compra
from ERP_COTP_P003_3 import ERP_COTP_P003_3
from ERP_COMP_P001_Consulta_PC import Consulta_PC

# Estado_Solp={'1':'Activa','2':'-','3':'Para Aprobación','4':'Anulada','5':'Aprobada','6':'Proceso de invitación','7':'--','8':'Prov. Cotizó','9':'Concluido'}
dict_estado = {'1':"En Proceso", '2':"Proceso de Invitación", '3':"Invitado", '4':"Evaluar Ofertas",
'5':"Mail enviado", '6':"Prov. Cotizo", '7':"Prov. NO cotizo", '8':"Ganador", '9':"Concluido"}

sqlProv="SELECT Cod_prov, Razón_social FROM TAB_PROV_001_Registro_de_Proveedores"

class ERP_COMP_P001(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("ERP_PCOMP_005.ui",self)

        self.pbEmitir.clicked.connect(self.Pedido_Compra)
        self.pbCargar.clicked.connect(self.Cargar)
        self.pbPed_Comp.clicked.connect(self.Consulta_PedComp)
        self.pbNuevo.clicked.connect(self.Limpiar)
        self.pbCancelar_Cot.clicked.connect(self.Cancelar_Cot)
        self.pbImprimir.clicked.connect(self.Imprimir)
        self.pbSalir.clicked.connect(self.Salir)
        self.pbConsultar.clicked.connect(self.Consultar)
        self.deInicial.dateChanged.connect(self.Fecha_Inicial)
        self.deFinal.setDateTime(QtCore.QDateTime.currentDateTime())
        self.deFinal.dateChanged.connect(self.Fecha_Final)

        global Cod_Soc,Nom_Soc,Cod_Usuario,dicProv

        Cod_Soc='1000'
        Nom_Soc='MULTI PLAY TELECOMUNICACIONES S.A.C'
        # Nom_Soc='MULTICABLE PERU SOCIEDAD ANONIMA CERRADA'
        # Cod_Soc='2000'
        Cod_Usuario='2021100004'

    # def datosGenerales(self, codSoc, empresa, usuario):
    #
    #     global Cod_Soc, Nom_Soc, Cod_Usuario,dicProv
    #     Cod_Soc = codSoc
    #     Nom_Soc = empresa
    #     Cod_Usuario = usuario

        cargarLogo(self.lbLogo_Mp,'multiplay')
        cargarLogo(self.lbLogo_Soc, Cod_Soc)
        cargarIcono(self, 'erp')
        cargarIcono(self.pbSalir, 'salir')
        cargarIcono(self.pbImprimir, 'imprimir')
        cargarIcono(self.pbEmitir, 'registrar')
        cargarIcono(self.pbCancelar_Cot, 'darbaja')
        cargarIcono(self.pbConsultar, 'visualizar')
        cargarIcono(self.pbPed_Comp, 'buscar')
        cargarIcono(self.pbCargar, 'cargar')
        cargarIcono(self.pbNuevo, 'nuevo')

        self.leInicial.setReadOnly(True)
        self.leFinal.setReadOnly(True)

        Prov=consultarSql(sqlProv)
        dicProv={}
        for dato in Prov:
            dicProv[dato[0]]=dato[1]

    def Fecha_Inicial(self):
        Fec_Inicial=QDateToStrView(self.deInicial)
        self.leInicial.setText(Fec_Inicial)

    def Fecha_Final(self):
        Fec_Final=QDateToStrView(self.deFinal)
        self.leFinal.setText(Fec_Final)

    def Cargar(self):
        try:
            global Año
            self.tbwCot_Aprov_Ped_Comp.clearContents()
            rows=self.tbwCot_Aprov_Ped_Comp.rowCount()
            for r in range(rows):
                self.tbwCot_Aprov_Ped_Comp.removeRow(1)

            fecha1=self.leInicial.text()
            fecha2=self.leFinal.text()
            Fec_Inicial=formatearFecha(fecha1)
            Fec_Final=formatearFecha(fecha2)

            now = datetime.datetime.now()
            Año=str(now.year)

            if Fec_Inicial!='' and Fec_Final!='':
                sqlCotComp='''SELECT c.Nro_Cotiza, p.Razón_social, p.Nro_Telf, SUM(d.Cant_Asignada*d.Precio_Cotiza), c.Fecha_Evalua_Oferta, c.Nro_Solp, c.Fecha_Doc, u.Nom_usuario, e.Estado_Pedido
                FROM TAB_COMP_001_Cotización_Compra c
                LEFT JOIN TAB_COMP_002_Detalle_Cotización_de_Compra d ON c.Cod_Soc=d.Cod_Soc AND c.Año=d.Año AND c.Nro_Cotiza=d.Nro_Cotiza AND c.Cod_Prov=d.Cod_Prov
                LEFT JOIN TAB_PROV_001_Registro_de_Proveedores p ON c.Cod_Prov = p.Cod_prov
                LEFT JOIN TAB_SOC_005_Usuarios u ON c.Cod_Soc = u.Cod_Soc AND c.User_Finaliza_Oferta = u.Cod_usuario
                LEFT JOIN TAB_COMP_004_Pedido_Compra e ON c.Cod_Soc=e.Cod_Emp AND c.Cod_Prov=e.Cod_Prov AND c.Nro_Cotiza=e.Nro_Cotiza
                WHERE c.Cod_Soc='%s' AND c.Año='%s' AND c.Estado_Tipo='8' AND c.Fecha_Evalua_Oferta>='%s' AND c.Fecha_Evalua_Oferta<='%s'
                GROUP BY c.Nro_Cotiza, c.Cod_Prov
                ORDER BY c.Nro_Cotiza ASC, c.Fecha_Evalua_Oferta ASC, p.Razón_social ASC'''%(Cod_Soc,Año,Fec_Inicial,Fec_Final)

            elif Fec_Inicial!='' and Fec_Final=='':
               sqlCotComp='''SELECT c.Nro_Cotiza,p.Razón_social,p.Nro_Telf,SUM(d.Cant_Asignada*d.Precio_Cotiza),c.Fecha_Evalua_Oferta,c.Nro_Solp,c.Fecha_Doc,u.Nom_usuario,e.Estado_Pedido
               FROM TAB_COMP_001_Cotización_Compra c
               LEFT JOIN TAB_COMP_002_Detalle_Cotización_de_Compra d ON c.Cod_Soc=d.Cod_Soc AND c.Año=d.Año AND c.Nro_Cotiza=d.Nro_Cotiza AND c.Cod_Prov=d.Cod_Prov
               LEFT JOIN TAB_PROV_001_Registro_de_Proveedores p ON c.Cod_Prov = p.Cod_prov
               LEFT JOIN TAB_SOC_005_Usuarios u ON  c.Cod_Soc = u.Cod_Soc AND c.User_Finaliza_Oferta = u.Cod_usuario
               LEFT JOIN TAB_COMP_004_Pedido_Compra e ON c.Cod_Soc=e.Cod_Emp AND c.Cod_Prov=e.Cod_Prov AND c.Nro_Cotiza=e.Nro_Cotiza
               WHERE c.Cod_Soc='%s' AND c.Año='%s' AND c.Estado_Tipo='8' AND c.Fecha_Evalua_Oferta>='%s'
               GROUP BY c.Nro_Cotiza, c.Cod_Prov
               ORDER BY c.Nro_Cotiza ASC, c.Fecha_Evalua_Oferta ASC, p.Razón_social ASC'''%(Cod_Soc,Año,Fec_Inicial)

            elif Fec_Inicial=='' and Fec_Final=='':
               sqlCotComp='''SELECT c.Nro_Cotiza,p.Razón_social,p.Nro_Telf,SUM(d.Cant_Asignada*d.Precio_Cotiza),c.Fecha_Evalua_Oferta,c.Nro_Solp,c.Fecha_Doc,u.Nom_usuario,e.Estado_Pedido
               FROM TAB_COMP_001_Cotización_Compra c
               LEFT JOIN TAB_COMP_002_Detalle_Cotización_de_Compra d ON c.Cod_Soc=d.Cod_Soc AND c.Año=d.Año AND c.Nro_Cotiza=d.Nro_Cotiza AND c.Cod_Prov=d.Cod_Prov
               LEFT JOIN TAB_PROV_001_Registro_de_Proveedores p ON c.Cod_Prov = p.Cod_prov
               LEFT JOIN TAB_SOC_005_Usuarios u ON  c.Cod_Soc = u.Cod_Soc AND c.User_Finaliza_Oferta = u.Cod_usuario
               LEFT JOIN TAB_COMP_004_Pedido_Compra e ON c.Cod_Soc=e.Cod_Emp AND c.Cod_Prov=e.Cod_Prov AND c.Nro_Cotiza=e.Nro_Cotiza
               WHERE c.Cod_Soc='%s' AND c.Año='%s' AND c.Estado_Tipo='8'
               GROUP BY c.Nro_Cotiza, c.Cod_Prov
               ORDER BY c.Nro_Cotiza ASC, c.Fecha_Evalua_Oferta ASC, p.Razón_social ASC'''%(Cod_Soc,Año)

            CargarCotApro(self,self.tbwCot_Aprov_Ped_Comp,sqlCotComp)

        except Exception as e:
            mensajeDialogo("error", "Error", "No se pudieron cargar los datos")
            self.leInicial.clear()
            self.leFinal.clear()
            print(e)

    def Limpiar(self):

        self.leInicial.clear()
        self.leFinal.clear()

    def Pedido_Compra(self):
        try:
            data=[]
            data.append(Cod_Soc) # Código de Sociedad - data[0]
            data.append(Nom_Soc) # Nombre de Sociedad - data[1]
            data.append(Cod_Usuario) # Código de Usuario - data[2]
            data.append(self.tbwCot_Aprov_Ped_Comp.item(self.tbwCot_Aprov_Ped_Comp.currentRow(),0).text()) # Número de Cotización - data[3]
            data.append(self.tbwCot_Aprov_Ped_Comp.item(self.tbwCot_Aprov_Ped_Comp.currentRow(),1).text()) # Razón Social - data[4]
            Razon_Social=self.tbwCot_Aprov_Ped_Comp.item(self.tbwCot_Aprov_Ped_Comp.currentRow(),1).text()
            for k,v in dicProv.items():
                if Razon_Social==v:
                    Cod_Prov=k
            data.append(Cod_Prov) # Código de Proveedor - data[5]
            data.append(self.tbwCot_Aprov_Ped_Comp.item(self.tbwCot_Aprov_Ped_Comp.currentRow(),3).text()) # Monto Aprobado - data[6]
            data.append(self.tbwCot_Aprov_Ped_Comp.item(self.tbwCot_Aprov_Ped_Comp.currentRow(),6).text()) # Fecha de Requerimiento - data[7]
            data.append("") # Número de Pedido - data[8]

            self.pc=Pedido_de_Compra()
            self.pc.datosCabecera(data)
            self.pc.pbGrabar.clicked.connect(self.Cargar)
            self.pc.showMaximized()

        except Exception as e:
            mensajeDialogo("informacion", "Información", "Es necesario que seleccione una fila, verifique")
            print(e)

    def Consulta_PedComp(self):
        try:
            self.cpc=Consulta_PC()
            self.cpc.datosCabecera(Cod_Soc,Nom_Soc,Cod_Usuario)
            self.cpc.showMaximized()
        except Exception as e:
            mensajeDialogo("error", "Error", "Algo paso, verifique")
            print(e)

    def Cancelar_Cot(self):
        try:
            Fecha=datetime.datetime.now().strftime("%Y-%m-%d")
            Hora=datetime.datetime.now().strftime("%H:%M:%S.%f")
            Nro_Cotiza=self.tbwCot_Aprov_Ped_Comp.item(self.tbwCot_Aprov_Ped_Comp.currentRow(),0).text()
            Razon_Social=self.tbwCot_Aprov_Ped_Comp.item(self.tbwCot_Aprov_Ped_Comp.currentRow(),1).text()
            for k,v in dicProv.items():
                if Razon_Social==v:
                    Cod_Prov=k
            Estado=self.tbwCot_Aprov_Ped_Comp.item(self.tbwCot_Aprov_Ped_Comp.currentRow(),8).text()
            if Estado=="Ganador":
                reply = mensajeDialogo("pregunta", "Pregunta","Realmente desea dar de baja a la cotización")
                if reply == 'Yes':
                    sql="UPDATE TAB_COMP_001_Cotización_Compra SET Estado_Tipo='%s',Fecha_Mod='%s',Hora_Mod='%s',Usuario_Mod='%s' WHERE Cod_Soc='%s' AND Año='%s' AND Nro_Cotiza='%s' AND Cod_Prov='%s' ;" % (9,Fecha,Hora,Cod_Usuario,Cod_Soc,Año,Nro_Cotiza,Cod_Prov)
                    respuesta=ejecutarSql(sql)
                    if respuesta['respuesta']=='correcto':
                        mensajeDialogo("informacion", "Información", "La cotización " + Nro_Cotiza + " fue cancelada")
                    elif respuesta['respuesta']=='incorrecto':
                        mensajeDialogo("error", "Error", "Ocurrio un problema, comuniquese con soporte")

                    self.Cargar()

        except Exception as e:
            mensajeDialogo("error", "Error", "No se selecciono ninguna Cotización, verifique")
            print(e)

    def Consultar(self):
        try:
            self.co = ERP_COTP_P003_3(self)
            row = self.tbwCot_Aprov_Ped_Comp.currentRow()
            col = self.tbwCot_Aprov_Ped_Comp.columnCount()
            data = []
            for i in range(col):
                try:
                    item = self.tbwCot_Aprov_Ped_Comp.item(row, i).text()
                except:
                    item = ""
                data.append(item)
                i+=1
            nro_cotiza = data[0]
            fecha_doc = ''
            prov = data[1]
            num_req=data[5]
            fec_req=data[6]
            estatus='Concluido'
            fecha_entrega=''

            self.co.mostrarInfo(Cod_Soc, Año, nro_cotiza, prov, num_req, fec_req, estatus, fecha_entrega,Cod_Usuario)
            self.co.showMaximized()

        except Exception as e:
            mensajeDialogo("error", "Error", "No se selecciono ninguna Cotización, verifique")
            print(e)

    def Imprimir(self):
        try:
            Fecha=datetime.datetime.now().strftime("%Y-%m-%d")
            Hora=datetime.datetime.now().strftime("%H:%M:%S")

            list_nro_cotizacion = []
            list_proveedor = []
            list_telefono = []
            list_monto_aprobado = []
            list_fecha_aprobado = []
            list_nro_requerimiento = []
            list_fecha_requerimiento = []
            list_responsable = []
            list_emitido = []

            for i in range(self.tbwCot_Aprov_Ped_Comp.rowCount()):
                try:
                    list_nro_cotizacion.append(self.tbwCot_Aprov_Ped_Comp.item(i,0).text())
                except:
                    list_nro_cotizacion.append("")
                try:
                    list_proveedor.append(self.tbwCot_Aprov_Ped_Comp.item(i,1).text())
                except:
                    list_proveedor.append("")
                try:
                    list_telefono.append(self.tbwCot_Aprov_Ped_Comp.item(i,2).text())
                except:
                    list_telefono.append("")
                try:
                    list_monto_aprobado.append(self.tbwCot_Aprov_Ped_Comp.item(i,3).text())
                except:
                    list_monto_aprobado.append("")
                try:
                    list_fecha_aprobado.append(self.tbwCot_Aprov_Ped_Comp.item(i,4).text())
                except:
                    list_fecha_aprobado.append("")
                try:
                    list_nro_requerimiento.append(self.tbwCot_Aprov_Ped_Comp.item(i,5).text())
                except:
                    list_nro_requerimiento.append("")
                try:
                    list_fecha_requerimiento.append(self.tbwCot_Aprov_Ped_Comp.item(i,6).text())
                except:
                    list_fecha_requerimiento.append("")
                try:
                    list_responsable.append(self.tbwCot_Aprov_Ped_Comp.item(i,7).text())
                except:
                    list_responsable.append("")
                try:
                    list_emitido.append(self.tbwCot_Aprov_Ped_Comp.item(i,8).text())
                except:
                    list_emitido.append("")

            print("LISTA 1: ",list_nro_cotizacion)
            print("LISTA 2: ",list_proveedor)
            print("LISTA 3: ",list_telefono)
            print("LISTA 4: ",list_monto_aprobado)
            print("LISTA 5: ",list_fecha_aprobado)
            print("LISTA 6: ",list_nro_requerimiento)
            print("LISTA 7: ",list_fecha_requerimiento)
            print("LISTA 8: ",list_responsable)
            print("LISTA 9: ",list_emitido)

            df = pd.DataFrame()
            df['1'] = list_nro_cotizacion
            df['2'] = list_proveedor
            df['3'] = list_telefono
            df['4'] = list_monto_aprobado
            df['5'] = list_fecha_aprobado
            df['6'] = list_nro_requerimiento
            df['7'] = list_fecha_requerimiento
            df['8'] = list_responsable
            df['9'] = list_emitido

            title = 'COTIZACIONES APROBADAS PARA EMITIR PEDIDO DE COMPRA'

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
            pdf.ln(40)
            # pdf.cell(-40)
            # pdf.cell(5)
            # pdf.set_fill_color(255,0,120)
            pdf.set_fill_color(255, 213, 79)
            pdf.cell(20, 10, 'Nro. Cot.', 1, 0, 'C', 1)
            pdf.cell(86, 10, 'Proveedor', 1, 0, 'C', 1)
            pdf.cell(17, 10, 'Teléfono', 1, 0, 'C', 1)
            pdf.cell(20, 10, 'Monto Apr.', 1, 0, 'C', 1)
            pdf.cell(20, 10, 'Fecha Apr.', 1, 0, 'C', 1)
            pdf.cell(15, 10, 'Nro. Req.', 1, 0, 'C', 1)
            pdf.cell(20, 10, 'Fecha Req.', 1, 0, 'C', 1)
            pdf.cell(65, 10, 'Responsable', 1, 0, 'C', 1)
            pdf.cell(14, 10, 'Estado', 1, 2, 'C', 1)
            # pdf.cell(-90)
            pdf.cell(-263)
            pdf.set_font('arial', '', 8)
            for i in range(0, len(df)):
                pdf.cell(20, 8, '%s' % (df['1'].iloc[i]), 1, 0, 'C')
                pdf.cell(86, 8, '%s' % (df['2'].iloc[i]), 1, 0, 'C')
                pdf.cell(17, 8, '%s' % (df['3'].iloc[i]), 1, 0, 'C')
                pdf.cell(20, 8, '%s' % (df['4'].iloc[i]), 1, 0, 'C')
                pdf.cell(20, 8, '%s' % (df['5'].iloc[i]), 1, 0, 'C')
                pdf.cell(15, 8, '%s' % (df['6'].iloc[i]), 1, 0, 'C')
                pdf.cell(20, 8, '%s' % (df['7'].iloc[i]), 1, 0, 'C')
                pdf.cell(65, 8, '%s' % (df['8'].iloc[i]), 1, 0, 'C')
                pdf.cell(14, 8, '%s' % (df['9'].iloc[i]), 1, 2, 'C')
                pdf.cell(-263)

            root = tk.Tk()
            root.withdraw()

            ruta_Carpeta=crearCarpeta("COTIZACIONES APROBADAS")
            ruta_Pdf=ruta_Carpeta+'Cotizaciones Aprobadas_' + Fecha.replace("-","") + Hora.replace(":","") + '.pdf'
            print(ruta_Pdf)
            if ruta_Pdf !="":
                pdf.output(ruta_Pdf, 'F')
                reply = mensajeDialogo("pregunta", "Pregunta","Reporte PDF Generado con éxito, ¿Desea abrir el archivo?")
                if reply == 'Yes':
                    abrirArchivo(ruta_Pdf)

        except Exception as e:
            mensajeDialogo("error", "Error", "Reporte Fallido")
            print(e)

    def Salir(self):
        self.close()

if __name__ == '__main__':
    app=QApplication(sys.argv)
    _main=ERP_COMP_P001()
    _main.showMaximized()
    app.exec_()
