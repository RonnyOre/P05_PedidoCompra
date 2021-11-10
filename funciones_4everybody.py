import mysql.connector

# BASE DE DATOS DE PRUEBA

# url = 'https://www.multiplay.com.pe/consultas/consulta-prueba.php' # BD para pruebas de desarrollo
# db = mysql.connector.connect(host="67.23.254.35",user="multipla_admin",passwd="multiplay123",database="multipla_pruebas")
# RUTA_WEB = '''https://www.multiplay.com.pe/pruebas'''
# FTP_HOST = "ftp.multiplay.com.pe"
# FTP_USER = "pruebas@multiplay.com.pe"
# FTP_PASS = "multiplay123"
# print('BASE DE DATOS DE PRUEBA..')

# BASE DE DATOS LIMPIA

url = 'https://www.multiplay.com.pe/consultas/consulta-erp-productivo.php' # BD para pruebas de integración
db = mysql.connector.connect(host="67.23.254.35",user="multipla_admin",passwd="multiplay123",database="multipla_erp_productivo")
RUTA_WEB = '''https://www.multiplay.com.pe/productivo'''
FTP_HOST = "ftp.multiplay.com.pe"
FTP_USER = 'productivo@multiplay.com.pe'
FTP_PASS = 'UGAGUXqiq5tA'
print('BASE DE DATOS DEL PRODUCTIVO..')

# BASE DE DATOS DE PRUEBA v2

# url = 'https://www.multiplay.com.pe/consultas/consulta-prueba-v2.php' # BD para datos reales
# db = mysql.connector.connect(host="67.23.254.35",user="multipla_admin",passwd="multiplay123",database="multipla_pruebas_v2")
