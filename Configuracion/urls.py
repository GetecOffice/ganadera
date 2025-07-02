from django.urls import path
from . import views



urlpatterns = [
       # GRUPOS
    path('Formulario_Grupos/', views.FormularioGrupos, name='F_Grupos'),
    path('Guardar_Grupos/', views.agregarGrupos, name="G_Grupos"),
    path('Datos_Grupos/', views.TablaGrupos, name='T_Grupos'),
    path('Datos_Grupos/Editar/<ID>', views.editarGrupos, name='E_Grupos'),
    path('Actualizar_Grupo/', views.actualizarGrupo, name='A_Grupos'),
    path('Permisos/Editar/<ID>', views.editarPermisos, name='E_Permisos'),
    path('Permisos/', views.TablaPermisos, name='T_Permisos'),
    path('Actualizar_Permiso/', views.actualizarPermiso, name='A_Permisos'),
    path('Movimiento_Permisos/', views.TablaPermisosAsignaElimina, name='T_PermisoAsignadosEliminados'),
    
    path('Tipos_De_Rol/', views.TablaTiposDeRol, name='T_Tipo_Rol'),
    
]
