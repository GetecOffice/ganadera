from django.urls import path
from . import views
from Reporte.ConsultaReporte import reportes


urlpatterns = [
       # REPORTES
    # bascula
    path('Reporte_Movimientos_Entrada_Materia_Prima/', reportes.reporteMovEntradaMP, name='R_Entrada_Materia_Prima'),
    path('Reporte_Movimientos_Salida_Materia_Prima/', reportes.reporteMovSalidaMP, name='R_Salida_Materia_Prima'),
    
    # animales nuevos
    path('Reporte_Movimientos_Animales/', reportes.reporteAnimalesMovimientos, name='R_Movimientos_Animales'),
    # animales
    path('Reporte_Animales_Clientes/', reportes.reportePorClientes, name='R_Animales_Clientes'),
    path('Reporte_Animales_Clientes_Corrales/', reportes.reportePorClientesCorrales, name='R_Animales_Clientes_Corrales'),
    # servidos
    path('Reporte_Movimientos_Servidos/', reportes.reporteServidosMovimientos, name='R_Movimientos_Servidos'),
    path('Reporte_Servidos_Liquidacion/', reportes.reporteServidosLiquidacion, name='R_Servidos_Liquidacion'),
     path('Reporte_Servidos_Promedio_Diario/', reportes.reporteServidosPromedio, name='R_Servidos_Promedio'),
]
