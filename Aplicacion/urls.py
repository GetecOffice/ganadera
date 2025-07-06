from django.urls import path
from . import views

from Aplicacion.CRUD import Correo, cliente, CopiaDeSeguridad, CopiaAMysql

# from .views import PDFView formularioCatalogos
from django.contrib.auth.views import LoginView, LogoutView
from .views import CustomLoginView
# La F = Formulario
# La T =  Tabla
# La G = Guardar Formulario


urlpatterns = [
     #  Presentacion
     path('', views.menuInfo, name='Menu_Presentacion'),
    
    # USUARIOS LOGIN, REGISTER O LOGOUT
    path('Logout/', LogoutView.as_view(template_name='Acceso/logout.html'), name='Logout'),
    path('Login/', CustomLoginView.as_view(), name='Login'),
    path('Register/', views.Register, name='Register'),
    
    path('Copia_de_seguridad/', CopiaDeSeguridad.copiaDeSeguridad, name='Copia'),
    path('Descargar_copia_de_seguridad/',
         CopiaDeSeguridad.descargar_backup, name='Descargar-SQLite3'),
    path('Importar_SQLite3_A_Mysql/',
         CopiaAMysql.import_data, name='SQLite3-A-Mysql'),    
    # Vistas para el cliente
    path('Agregar_Servidos_Cliente/', cliente.formulario, name='FP-Cliente'),
    path('Ver_Servidos_Cliente/', cliente.servidos, name='FP-Servidos-Cliente'),
    path('Guardar_Servidos_Cliente/', cliente.guardarSolicitudServidoCliente, name='GS-Cliente'),
    path('Resultados_Cliente/', cliente.cliente, name='Cliente'),
     path('Correo/', Correo.index, name="correos"),
]
