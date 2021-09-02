import requests
import re
import time
import ftplib
from datetime import date, datetime, timedelta
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtGui import*
import urllib.request
import hashlib
url = 'https://www.multiplay.com.pe/consultas/consulta-prueba.php'


# import sys
# from PyQt5.QtWidgets import QApplication, QMessageBox
#
# app = QApplication(sys.argv)
# msg = QMessageBox()
# msg.setIcon(QMessageBox.Warning)
# msg.setText("Where is my icon?")
# msg.exec_()

def ejecutarSql(sql):
    datos = {'accion':'ejecutar','sql': sql}
    x = requests.post(url, data = datos)
    if x.text!="":
        respuesta=x.json()
        if respuesta!=[]:
            print(respuesta)
    else:
        print("respuesta vacía")

    return respuesta

def ejecutarSql2(sql):
    datos = {'accion':'ejecutar','sql': sql}
    x = requests.post(url, data = datos)
    if x.text!="":
        respuesta=x.json()
        if respuesta!=[]:
            print(respuesta)
            return respuesta
    else:
        print("respuesta vacía")
        return {'respuesta':'incorrecto'}

def consultarSql(sql):
    datos = {'accion':'leer','sql': sql}
    x = requests.post(url, data=datos)
    respuesta=x.json()
    myresult=[]
    if respuesta!=[]:
        for datos in respuesta:
            contenido=[]
            for k,dato in datos.items():
                contenido.append(dato)
            myresult.append(contenido)

    return myresult

def insertarFila(tw,Fila):
    item=QTreeWidgetItem(tw,Fila)
    item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
    tw.addTopLevelItem(item)

def insertarFila2(tw,Fila,Columnas):
    item=QTreeWidgetItem(tw, Fila)
    item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
    if Columnas!=[]:
        for i in Columnas:
            item.setTextAlignment(i,QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            tw.insertTopLevelItems(0,[item])

def insertarDatos(cb, Datos):
    cb.clear()
    for dato in Datos:
        cb.addItem(dato[0])

def QDateToDate(Qdate):
    a1=int(str(Qdate.date().year()))
    m1=int(str(Qdate.date().month()))
    d1=int(str(Qdate.date().day()))
    fecha=date(a1,m1,d1)
    return fecha

def QDateToStr(Qdate):
    a1=str(Qdate.date().year())
    m1=str(Qdate.date().month())
    d1=str(Qdate.date().day())
    if len(m1) == 1:
        m1 = '0'+m1
    if len(d1) == 1:
        d1 = '0'+d1
    strFecha="%s-%s-%s" % (a1,m1,d1)
    return strFecha

def QDateToStrView(Qdate):
    a1=str(Qdate.date().year())
    m1=str(Qdate.date().month())
    d1=str(Qdate.date().day())
    if len(m1) == 1:
        m1 = '0'+m1
    if len(d1) == 1:
        d1 = '0'+d1
    strFecha="%s-%s-%s" % (d1,m1,a1)
    return strFecha

def StrToQDate(FechaString):
    if FechaString == "None" or FechaString == None or FechaString == "":
        return QtCore.QDate.fromString("2000-01-01", "yyyy-MM-dd")
    else:
        return QtCore.QDate.fromString(FechaString, "yyyy-%s-%s" % ("M"*len(FechaString.split("-")[1]), "d"*len(FechaString.split("-")[2])))

def StrToDate(FechaString):
    if FechaString == "None" or FechaString == None or FechaString == "":
        return date(2000,1,1)
    else:
        return date(int(FechaString.split("-")[0]), int(FechaString.split("-")[1]),int(FechaString.split("-")[2]))

def formatearFecha(fecha):
    if fecha=="":
        return ""
    fecha=fecha.split("/")
    fecha.reverse()
    return "-".join(fecha)

def formatearFecha2(fecha):
    if fecha=="":
        return ""
    fecha=fecha.split("-")
    fecha.reverse()
    return "-".join(fecha)

def leerFecha(de):
    Fecha=de.date()
    year=str(Fecha.year())
    month="0"*(2-len(str(Fecha.month()))) + str(Fecha.month())
    day="0"*(2-len(str(Fecha.day()))) + str(Fecha.day())
    return "%s-%s-%s" % (year, month, day)

def mostrarFecha(fecha):
    if fecha=="":
        return ""
    fecha=fecha.split("-")
    fecha.reverse()
    return "/".join(fecha)

def llenarCombobox(sql, cb):
    resultado=consultarSql(sql)
    for fila in resultado:
        if fila[0]=="":
            continue
        cb.addItem(fila[0])
    cb.clearEditText()

def buscarTabla(tw, texto, columnas):
    palabras=re.sub(' +', ' ', texto).split(" ")
    patrones=[]
    for palabra in palabras:
        patrones.append(re.compile(palabra.upper()))
    if texto=="":
        for i in range(0,tw.topLevelItemCount()):
            tw.topLevelItem(i).setHidden(False)
    else:
        for i in range(0,tw.topLevelItemCount()):
            busqueda=True
            for j in columnas:
                subBusqueda=False
                for patron in patrones:
                    subBusqueda=subBusqueda or (patron.search(tw.topLevelItem(i).text(j).upper()) is None)
                busqueda=busqueda and subBusqueda
            if busqueda:
                tw.topLevelItem(i).setHidden(True)
            else:
                tw.topLevelItem(i).setHidden(False)

def formatearDecimal(str, nro):
    try:
        decimal = float(str)
        decimalRound = round(decimal,int(nro))
        cantDecimales = "{:,." + nro + "f}"
        decimalStr = cantDecimales.format(decimalRound)
        return decimalStr
    except:
        ""

def subirArchivoFTP(ruta, sub, mismoNombre):
    FTP_HOST = "ftp.multiplay.com.pe"
    FTP_USER = "pruebas@multiplay.com.pe"
    FTP_PASS = "multiplay123"
    ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
    ftp.encoding = "utf-8"
    ftp.cwd(sub)
    if mismoNombre:
        nuevoNombre=ruta.split('/')[-1]
    else:
        extension=ruta.split('/')[-1].split('.')[-1]
        fecha="".join("".join("".join(str(datetime.today()).split(".")[0].split("-")).split(":")).split(" "))
        nuevoNombre=fecha + "." + extension
    with open(ruta, "rb") as file:
        ftp.storbinary(f"STOR {nuevoNombre}", file)
        ftp.quit()
        return nuevoNombre

def empaquetarImagenCarpeta(ruta):
    data = open(ruta,'rb').read()
    imagen = QImage()
    imagen.loadFromData(data)
    return imagen

def empaquetarImagenWeb(ruta):
    data = urllib.request.urlopen(ruta).read()
    imagen = QImage()
    imagen.loadFromData(data)
    return imagen

def cargarLogoWeb(lb, codSoc):
    try:
        if codSoc == 'multiplay':
            codSoc = 'Mp_st'
        urlLogo = '''https://www.multiplay.com.pe/pruebas/logos/Logo'''+ codSoc +'.png'
        logoSoc = QPixmap(empaquetarImagenWeb(urlLogo))
        ratio = QtCore.Qt.KeepAspectRatio
        logoSoc = logoSoc.scaled(250, 35, ratio)
        lb.setPixmap(logoSoc)
    except:
        ""

def cargarLogo(lb, codSoc):
    try:
        if codSoc == 'multiplay':
            codSoc = 'Mp_st'
        folderLogo = '''Logos/Logo'''+ codSoc +'.png'
        logoSoc = QPixmap(folderLogo)
        ratio = QtCore.Qt.KeepAspectRatio
        logoSoc = logoSoc.scaled(250, 35, ratio)
        lb.setPixmap(logoSoc)
    except:
        ""

def cargarIconoWeb(obj, tipoIcono):
    try:
        iconos = {'guardar': "diskette", 'grabar': "diskette", 'editar': "edit", 'modificar': "edit", 'salir': "logout", 'añadir': "add", 'registrar': "clipboard", 'imprimir': "printer", 'pdf': "pdf", 'imagen': "imagen",
        'documentos': "documents", 'verificar': "verify", 'darbaja': "x-button", 'buscar': "loupe", 'visualizar': "visualizar", 'finalizar': "finalizar", 'usuario': "user", 'texto': "articulo" , 'material': "router",
        'cargar': "sand-clock", 'copiar': "copy", 'erp': "organization"}
        icono = iconos[tipoIcono]
        urlIcono = '''https://www.multiplay.com.pe/pruebas/iconos/'''+ icono +'.png'
        icon = QPixmap(empaquetarImagenWeb(urlIcono))
        if tipoIcono != 'erp':
            obj.setIcon(QIcon(icon))
        else:
            obj.setWindowIcon(QIcon(icon))
    except:
        ""

def cargarIcono(obj, tipoIcono):
    try:
        iconos = {
        'añadir': "add",
        'texto': "articulo" ,
        'comprar': "bolsa-de-la-compra" ,
        'copiar': "copy",
        'registrar': "clipboard",
        'contabilidad': "contabilidad",
        'guardar': "diskette",
        'grabar': "diskette",
        'documentos': "documents",
        'editar': "edit",
        'modificar': "edit",
        'finalizar': "finalizar",
        'nuevo': "file",
        'equivalencias': "justa",
        'imagen': "imagen",
        'idiomas': "languages",
        'salir': "logout",
        'buscar': "loupe",
        'informacion': "mas-informacion",
        'erp': "organization",
        'paquetes': "paquetes",
        'pdf': "pdf",
        'imprimir': "printer",
        'material': "router",
        'cargar': "sand-clock",
        'componentes': "soporte-tecnico",
        'tecnico': "tecnico",
        'usuario': "user",
        'ventas': "ventas",
        'verificar': "verify",
        'visualizar': "visualizar",
        'almacen': "warehouse",
        'darbaja': "x-button"}
        icono = iconos[tipoIcono]
        folderIcono = '''IconosLocales/'''+ icono +'.png'
        icon = QPixmap(folderIcono)
        if tipoIcono != 'erp':
            obj.setIcon(QIcon(icon))
        else:
            obj.setWindowIcon(QIcon(icon))
    except:
        ""
