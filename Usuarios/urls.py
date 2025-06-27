from django.urls import path
from . import views



urlpatterns = [
    # PAGOS
    path('Estado-Pago/', views.estadoPago, name='Pagos'),
    path('No-Hay-Servicio/', views.NoPago, name='NoPago'),
    path('SeAgregoElPago/', views.registrarPago),
    path('Notificaciones/', views.notificacion),
    
    # EDITAR USUARIOS
    path('EdicionUsuario/<id>', views.edicionUsuario, name="E_Usuario"),

    # ACTUALIZAR USUARIOS
    path('ActualizarUsuario/', views.actualizarUsuario, name="A_Usuario"),
    
    # USUARIOS
    # path('Perfil/', views.perfil, name='perfil'),
    path('Usuarios/', views.TablaUsuarios, name='TUsuarios'),
    path('Agregar-Tecnicos/', views.agregarTecnicos, name='Agregar-tecnicos'),
    path('Editar-Tecnicos/', views.editadoTecnicos, name='Editar-tecnicos'),
    path('Usuario-Bloqueado/', views.usuarioBloqueado, name='Bloqueado'),    
]
