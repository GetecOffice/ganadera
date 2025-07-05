from django.urls import path
from . import views



urlpatterns = [
   
    # EDITAR USUARIOS
    path('EdicionUsuario/<id>', views.edicionUsuario, name="E_Usuario"),

    # ACTUALIZAR USUARIOS
    path('ActualizarUsuario/', views.actualizarUsuario, name="A_Usuario"),
    
    # USUARIOS
    path('Perfil/', views.perfil, name='perfil'),
    path('Usuarios/', views.TablaUsuarios, name='TUsuarios'),
    path('Agregar_Tecnicos/', views.agregarTecnicos, name='Agregar_tecnicos'),
    path('Editar_Tecnicos/', views.editadoTecnicos, name='Editar_tecnicos'),
    path('Usuario-Bloqueado/', views.usuarioBloqueado, name='Bloqueado'),    
]
