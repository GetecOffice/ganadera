from django.urls import path
from . import views
from Catalogo.consultasCatalogo import actualizar, agregar, editar, mostrar, formulario


urlpatterns = [
   path('', views.homeCatalogos, name='Inicio'),
   
   # Tablas
   path('Clientes/', mostrar.TablaClientes, name='T_Cliente'),
   path('Proveedores/', mostrar.TablaProveedores, name='T_Proveedor'),
   path('Operadores/', mostrar.TablaOperadores, name='T_Operador'),
   path('Materias_Primas/', mostrar.TablaMateriasPrimas, name='T_MateriaPrima'),
   path('Productos/', mostrar.TablaProductos, name='T_Producto'),
   path('Corrales/', mostrar.TablaCorrales, name='T_Corral'),
   path('Tipo_Animales/', mostrar.TablaTipoAnimales, name='T_TipoAnimal'),
   path('Contenedores_Materias_Primas/', mostrar.TablaContenedoresMateriasPrimas, name='T_ContenedorMP'),
   path('Contenedores_Productos/', mostrar.TablaContenedoresProductos, name='T_ContenedorProducto'),
   path('Tolvas/', mostrar.TablaTolva, name='T_Tolva'),
   
   # Formulario
   path('Formulario_Clientes/', formulario.FormualrioClientes, name='F_Cliente'),
   path('Formulario_Proveedores/', formulario.FormualrioProveedores, name='F_Proveedor'),
   path('Formulario_Operadores/', formulario.FormualrioOperadores, name='F_Operador'),
   path('Formulario_Materias_Primas/', formulario.FormualrioMateriasPrimas, name='F_MateriaPrima'),
   path('Formulario_Productos/', formulario.FormualrioProductos, name='F_Producto'),
   path('Formulario_Corrales/', formulario.FormualrioCorrales, name='F_Corral'),
   path('Formulario_Tipo_Animales/', formulario.FormualrioTipoAnimaless, name='F_TipoAnimal'),
   path('Formulario_Contenedores_Materias_Primas/', formulario.FormualrioContnendoresMateriasPrimas, name='F_ContenedorMP'),
   path('Formulario_Contenedores_Productos/', formulario.FormualrioContenedoresProductos, name='F_ContenedorProducto'),
   path('Formulario_Tolvas/', formulario.FormualrioTolva, name='F_Tolva'),   
   
   # Guardar
   path('Guardar_Clientes/', agregar.guardarCliente, name='G_Cliente'),
   path('Guardar_Proveedores/', agregar.guardarProveedor, name='G_Proveedor'),
   path('Guardar_Operadores/', agregar.guardarOperador, name='G_Operador'),
   path('Guardar_Materias_Primas/', agregar.guardarMateriasPrimas, name='G_MateriaPrima'),
   path('Guardar_Productos/', agregar.guardarProductos, name='G_Producto'),
   path('Guardar_Corrales/', agregar.guardarCorrales, name='G_Corral'),
   path('Guardar_Tipo_Animales/', agregar.guardarTipoAnimales, name='G_TipoAnimal'),
   path('Guardar_Contenedores_Materias_Primas/', agregar.guardarContenedoresMateriasPrimas, name='G_ContenedorMP'),
   path('Guardar_Contenedores_Productos/', agregar.guardarContenedoresProductos, name='G_ContenedorProducto'),
   path('Guardar_Tolvas/', agregar.guardarTolva, name='G_Tolva'),   

   #Editar
   path('Clientes/Editar/<ID>', editar.editarCliente, name='E_Cliente'),
   path('Proveedores/Editar/<ID>', editar.editarProveedor, name='E_Proveedor'),
   path('Operadores/Editar/<ID>', editar.editarOperador, name='E_Operador'),
   path('Materias_Primas/Editar/<ID>', editar.editarMateriaPrima, name='E_MateriaPrima'),
   path('Productos/Editar/<ID>', editar.editarProducto, name='E_Producto'),
   path('Corrales/Editar/<ID>', editar.editarCorral, name='E_Corral'),
   path('Tipo_Animales/Editar/<ID>', editar.editarTipoAnimal, name='E_TipoAnimal'),
   path('Contenedores_Materias_Primas/Editar/<ID>', editar.editarContenendorMP, name='E_ContenedorMP'),
   path('Contenedores_Productos/Editar/<ID>', editar.editarContnenedorProducto, name='E_ContenedorProducto'),
   path('Tolvas/Editar/<ID>', editar.editarTolva, name='E_Tolva'),   

   # Actualizar
   path('Actualizar_Clientes/', actualizar.actualizarCliente, name='A_Cliente'),
   path('Actualizar_Proveedores/', actualizar.actualizarProveedor, name='A_Proveedor'),
   path('Actualizar_Operadores/', actualizar.actualizarOperador, name='A_Operador'),
   path('Actualizar_Materias_Primas/', actualizar.actualizarMateriaPrima, name='A_MateriaPrima'),
   path('Actualizar_Productos/', actualizar.actualizarProductos, name='A_Producto'),
   path('Actualizar_Corrales/', actualizar.actualizarCorral, name='A_Corral'),
   path('Actualizar_Tipo_Animales/', actualizar.actualizarTipoAnimales, name='A_TipoAnimal'),
   path('Actualizar_Contenedores_Materias_Primas/', actualizar.actualizarContenedoresMP, name='A_ContenedorMP'),
   path('Actualizar_Contenedores_Productos/', actualizar.actualizarContenedoresProductos, name='A_ContenedorProducto'),
   path('Actualizar_Tolvas/', actualizar.actualizarTolva, name='A_Tolva'),   
]
