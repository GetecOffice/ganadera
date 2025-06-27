from django.urls import path
from . import views

from Subtabla.consultasSubtabla import actualizar, agregar, editar, mostrar, formulario

urlpatterns = [
    path('SubTabla_Estatus/', mostrar.TablaEstatus, name='T_Estatus'),
    path('SubTabla_Tipo_Material/', mostrar.TablaTipoMaterial, name='T_Tipo_Material'),
    path('SubTabla_Tipo_Movimiento/', mostrar.TablaTipoMovimiento, name='T_Tipo_Movimiento'),
    path('SubTabla_Tipo_Presentacion/', mostrar.TablaTipoPresentacion, name='T_Tipo_Presentacion'),
    path('SubTabla_Unidad_Medida/', mostrar.TablaUnidadMedida, name='T_Unidad_Medida'),
    path('Base_de_datos/', mostrar.TablaConfiguracion, name='Base_de_datos'),
    
    # FORMULARIO SUBTABLAS
    path('Formulario_Estatus/', formulario.formularioEstatus, name='F_Estatus'),
    path('Formulario_Tipo_Material/', formulario.formularioTipoMaterial, name='F_Tipo_Material'),
    path('Formulario_Tipo_Movimiento/', formulario.formularioTipoMovimiento, name='F_Tipo_Movimiento'),
    path('Formulario_Tipo_Presentacion/', formulario.formularioTipoPresentacion, name='F_Tipo_Presentacion'),
    path('Formulario_Unidad_Medida/', formulario.formularioUnidadMedida, name='F_Unidad_Medida'),
    
    # FORMULARIO SUBTABLA
    path('Guardar_Estatus/', agregar.guardarEstatus, name="G_Estatus"),
    path('Guardar_Tipo_Movimiento/', agregar.guardarTipoMovimiento, name="G_TipoMovimiento"),
    path('Guardar_Tipo_Material/', agregar.guardarTipoMaterial, name="G_Tipo_Material"),
    path('Guardar_Tipo_Presentacion/', agregar.guardarTipoPresentacion, name="G_Tipo_Presentacion"),
    path('Guardar_Unidades/', agregar.guardarUnidadMedida, name="G_Unidad_Medida"),    

    # SUBTABLA EDITAR
    path('SubTabla_Estatus/Editar/<ID>', editar.editarEstatus, name="E_Estatus"),
    path('SubTabla_Tipo_Movimiento/Editar/<ID>', editar.editarTipoMovimiento, name="E_Tipo_Movimiento"),
    path('SubTabla_Tipo_Material/Editar/<ID>', editar.editarTipoMaterial, name="E_Tipo_Material"),
    path('SubTabla_Tipo_Presentacion/Editar/<ID>', editar.editarTipoPresentacion, name="E_Tipo_Presentacion"),
    path('SubTabla_Unidad_Medida/Editar/<ID>', editar.editarUnidadMedida, name="E_Unidad_Medida"),   

    # ACTUALIZAR SUBTABLA
    path('ActualizarEstatus/', actualizar.actualizarEstatus, name="A_Estatus"),
    path('ActualizarTipoMovimiento/', actualizar.actualizarTipoMovmimiento, name="A_Tipo_Movimiento"),
    path('ActualizarTipoMaterial/', actualizar.actualizarTipoMaterial, name="A_Tipo_Material"),
    path('ActualizarTipoPresentacion/', actualizar.actualizarTipoPresentacion, name="A_Tipo_Presentacion"),
    path('ActualizarUnidad/', actualizar.actualizarUnidadMedida, name="A_Unidad_Medida"),     
]
