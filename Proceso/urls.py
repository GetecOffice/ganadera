from django.urls import path
from . import views
from Proceso.consultarProcesos import actualizar, agregar, editar, mostrar, formulario, presentacion, DescargaPDF


urlpatterns = [
    path('', views.homeProcesos, name='Inicio'),
   
    #  Presentacion
    path('Servidos_presentacion/', presentacion.presentacionServidos, name='Servidos_Presentacion'),
    path('Bascula_presentacion/', presentacion.presentacionBascula, name='Bascula_Presentacion'),
    path('Invenario_presentacion/', presentacion.presentacionInventario, name='Inventario_Presentacion'),
    
   # Tablas
    path('Entrada_Materia_Prima/', mostrar.TablaEntradaMateriasPrimas, name='T_Ent_Materia_Prima'),
    path('Salida_Materia_Prima/', mostrar.TablaSalidaMateriasPrimas, name='T_Sal_Materia_Prima'),
    path('Entrada_Producto/', mostrar.TablaEntradaProductos, name='T_Ent_Productos'),
    path('Salida_Producto/', mostrar.TablaSalidaProductos, name='T_Sal_Productos'),
    path('Movimientos_Animales/', mostrar.TablaMovimientoAnimales, name='T_MovAnimales'),
    path('Movimientos_Animales/Agregar/<ID>', mostrar.AgregarMovimientoAnimales, name='A_MovAnimales'),
    path('Movimientos_Animales/Detalle/<str:ID>', mostrar.detalleAnimales, name='D_MovAnimales'),
    path('Detalles_Animales/', mostrar.TablaDetallesAnimales, name='T_DetallesAnimales'),
    path('Historial/', mostrar.TablaHistorialAsignacionCorral, name='T_Historial'),
    path('Inventario_Materia_Prima/', mostrar.TablaInventarioMateriaPrima, name="T_InventarioMP"),
    path('Inventario_Productos/', mostrar.TablaInventarioProducto, name="T_InventarioProductos"),

    # DATOS DEL AREA DE SERVIDOS
    path('Solicitud_Servidos/', mostrar.TablaSolicitudServido, name='T_Solicitud_Servidos'),
    path('Corrales_Servidos/', mostrar.TablaServidoCorral, name='T_Corrales_Servidos'),
    path('Consolidacion_Servido/', mostrar.TablaConsolidacionServido, name='T_Consolidacion'),
    path('Consolidacion_Servido/Filtro/Tolva/<str:ID>/<int:Estatus>/<int:Producto>/', mostrar.TablaTolvaServido),
    path('Consolidacion_Servido_Filtro/', mostrar.TablaFiltroServido, name='FT_Consolidacion'),
    path('Tolva_Servido/', mostrar.TablaTolva, name='T_Tolva_Servido'),
    path('Tolva_Servido_Se_Sirve/', mostrar.TablaTolvaServidoCorral, name='T_Se_Sirve'),
    path('Servidos_Manuales/', mostrar.TablaServidoAnimales, name='T_Servidos'),

    # DATOS DE LOS DATOS DE LA TOLVA
    path('Cargamento_Tolva/', mostrar.TablaCargamentoTolva, name='T_Cargamento_Tolva'),
    
    # DETALLES DE OPERADORES
    path('Operador_Entrada_Productos/', mostrar.TablaOperadoresEntradaProductos, name="T_Operador_Entrada_Producto"),
    path('Operador_Salida_Productos/', mostrar.TablaOperadoresSalidaProductos, name="T_Operador_Salida_Producto"),
    path('Operador_Entrada_Materias_Primas/', mostrar.TablaOperadoresEntradaMateriasPrimas, name="T_Operador_Entrada_MP"),
    path('Operador_Salida_Materias_Primas/', mostrar.TablaOperadoresSalidasMateriasPrimas, name="T_Operador_Salida_MP"),

    # ASIGNACION CORRALES
    path('Asignacion_Corrales/', mostrar.asignacionCorral, name='T_Asignacion'),

    # TRAER CORRALES EN TIEMPO REAL
    path('obtener_corrales/<int:id>/', mostrar.obtener_corrales),
    path('obtener_clientes/<int:id>/', mostrar.obtener_clientes),
    path('obtener_corrales_clientes/<int:id>/', mostrar.obtener_corrales_animales_clientes),
   
    # FORMULARIO DE PROCESOS
    path('Formulario_Entrada_Materia_Prima/',formulario.FormularioEntradaMateriasPrimas, name='F_Ent_Materia_Prima'),
    path('Formulario_Salida_Materia_Prima/',formulario.FormularioSalidaMateriasPrimas, name='F_Sal_Materia_Prima'),
    path('Formulario_Entrada_Producto/',formulario.FormularioEntradaProductos, name='F_Ent_Productos'),
    path('Formulario_Salida_Producto/',formulario.FormularioSalidaProductos, name='F_Sal_Productos'),
    path('Formulario_Movimientos_Animales/',formulario.FormularioMovimientoAnimales, name='F_MovAnimales'),
    path('Formulario_Detalles_Animales/',formulario.FormularioDetallesAnimales, name='F_DetallesAnimales'),
    path('Formulario_Solicitud_Servido/',formulario.FormularioSolicitudServido, name='F_Solicitud_Servidos'),
    path('Formulario_Servidos_Manuales/',formulario.FormularioServidoAnimales, name='F_Servidos'),
    path('Formulario_Inventario_Materia_Prima/',formulario.FormularioInventarioMateriaPrima, name="F_InventarioMP"),
    path('Formulario_Inventario_Productos/',formulario.FormularioInventarioProducto, name="F_InventarioProductos"),

    # FORMULARIO DE OPERADORES
    path('Operador_Entrada_Productos/Agregar/<str:ID>',formulario.FormularioOperadoresEntradaProductos, name="A_Operaror_Entrada_Producto"),
    path('Operador_Salida_Productos/Agregar/<str:ID>',formulario.FormularioOperadoresSalidaProductos, name="A_Operaror_Salida_Producto"),
    path('Operador_Entrada_Materias_Primas/Agregar/<str:ID>',formulario.FormularioOperadorEntradaMateriaPrima, name="A_Operaror_Entrada_Materia"),
    path('Operador_Salida_Materias_Primas/Agregar/<str:ID>',formulario.FormularioOperadorSalidaMateriaPrima, name="A_Operaror_Salida_Materia"),
   
    # FORMULARIO PROCESOS
    path('Guardar_Entrada_Materia_Prima/', agregar.guardarEntradaMateriaPrima, name="G_Entrada_Materia_Prima"),
    path('Guardar_Salidas_Materias_Primas/', agregar.guardarSalidasMateriaPrima, name="G_Salida_Materia_Prima"),
    path('Guardar_Entradas_Productos/', agregar.guardarEntradaBasculas, name="G_Entrada_Productos"),
    path('Guardar_Salidas_Productos/', agregar.guardarSalidaBasculas, name="G_Salida_Producto"),
    path('Guardar_Movimiento_De_Amimales/', agregar.guardarMovimientos, name="G_Mov_De_Animales"),
    path('Guardar_Movimiento_Animales/', agregar.guardarMovimientoAniamles, name="G_Mov_Animales"),
    path('Guardar_Solicitud_Servidos/', agregar.guardarSolicitudServido, name="G_Solicitud_Servidos"),
    path('Guardar_Servidos_Manual/', agregar.guardarServidosManuales),
    path('Guardar_Inventario_Materia_Prima/', agregar.guardarInventarioMateriaPrima),
    path('Guardar_Inventario_Productos/', agregar.guardarInventarioProductos),
      # Servidos Materia prima
     path('Salidas_De_Servidos/', agregar.salidaMPServidos, name="ServidosSalidas"),


    # EDITAR PROCESOS
    path('Entrada_Materia_Prima/Editar/<ID>', editar.editarEntradaMateriaPrima),
    path('Salida_Materia_Prima/Editar/<ID>', editar.editarSalidaMateriaPrima),
    path('Entrada_Producto/Editar/<ID>', editar.editarEntradaProductos),
    path('Salida_Producto/Editar/<ID>', editar.editarSalidaProductos),
    path('Movimientos_Animales/Editar/<ID>', editar.editarMovimientosAnimales),
    path('Movimientos_Animales/Detalle/Editar/<ID>', editar.editarCantidadMovimientosAnimales),
    path('Solicitud_Servidos/Editar/<ID>', editar.editarSolicitudServidos),
    path('Dato_Servidos_Manuales/Editar/<ID>', editar.editarServidosManuales),
    path('Dato_Inventario_Materia_Prima/Editar/<ID>', editar.editarInventarioInicialMateriaPrima),
    path('Dato_Inventario_Productos/Editar/<ID>', editar.editarInventarioInicialProducto),

    # EDITAR  DE OPERADORES
    path('Operador_Entrada_Productos/Editar/<str:ID>', editar.editarOperadorEntradaProducto, name="E_Operaror_Entrada_Producto"),
    path('Operador_Salida_Productos/Editar/<str:ID>', editar.editarOperadoresSalidaProductos, name="E_Operaror_Salida_Producto"),
    path('Operador_Entrada_Materias_Primas/Editar/<str:ID>', editar.editarOperadorEntradaMateriaPrima, name="E_Operaror_Entrada_Materia"),
    path('Operador_Salida_Materias_Primas/Editar/<str:ID>', editar.editarOperadorSalidaMateriaPrima, name="E_Operaror_Salida_Materia"),

    # ACTUALIZAR PROCESOS
    path('ActualizarServidorManual/', actualizar.actualizarServidosManual, name="A_Solicitud_Servidos"),
    path('ActualizarServidorManualCantidad/', actualizar.actualizarCantidadServidosManual, name="Cantidad_servidos_manuales"),
    path('ActualizarEntradaMateriasPrimas/',actualizar.actualizarEntradaMateriaPrima, name="A_Entrada_Materia_Prima"),
    path('ActualizarSalidaMateriasPrimas/',actualizar.actualizarSalidaMateriaPrima, name="A_Salida_Materia_Prima"),
    path('ActualizarEntradaProductos/',actualizar.actualizarEntradaProductos, name="A_Entrada_Productos"),
    path('ActualizarSalidaProductos/',actualizar.actualizarSalidaProductos, name="A_Salida_Productos"),
    path('ActualizarCantidadMovimientosAnimales/',actualizar.actualizarCantidadAnimales, name="A_Cantidad_Animal"),
    path('ActualizarMovimientosAnimales/',actualizar.actualizarMovimientosAniamales, name="A_Movimiento_Animal"),
    path('ActualizarInventatioInicialMateriaPrima/',actualizar.actualizarInventatioInicialMateriaPrima),
    path('ActualizarInventatioInicialProducto/',actualizar.actualizarInventatioInicialProducto),
    path('ActualizarServidosATolva/', actualizar.actualizarServidosATolva, name="A_Servidos_Tolva"),

    # ACTUALIZAR OPRADORES PROCESOS
    path('ActualizarOperadoresEntradaProducto/', actualizar.actualizarOperadoresEntradaProducto, name="A_Operador_Entrada_Producto"),
    path('ActualizarOperadoresSalidaProducto/', actualizar.actualizarOperadoresSalidaProducto, name="A_Operador_Salida_Producto"),
    path('ActualizarOperadoresEntradaMateriaPrima/', actualizar.actualizarOperadoresEntradaMateriasPrimas, name="A_Operador_Entrada_MP"),
    path('ActualizarOperadoresSalidaMateriaPrima/', actualizar.actualizarOperadoresSalidaMateriasPrimas, name="A_Operador_Salida_MP"),
    path('ActualizarCancelarServidosVehiculos/', actualizar.actualizarCancelarTolva, name="A_Pedido_Tolva"),
    ]
