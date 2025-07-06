from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User
from Aplicacion.models import *
from datetime import datetime, timedelta, date
from django.contrib import messages
from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.utils import timezone
# ---------------------------------------------------CONSULTA PARA LAS TABLAS DE USUARIOS---------------------------------------------------}

@login_required
def grupo_user(request):
    user = request.user
    if user.groups.exists():
        grupo = user.groups.first()
        grupos_user = grupo.name
        grupos = grupos_user
        return grupos
    
def servicioActivo():
    ServiciosWeb = tblServiciosWeb.objects.get(ID=1)
    FechaDeHoy = date.today().strftime('%Y-%m-%d')
    FechaDeHoy = date.today()

    if ServiciosWeb.FechaVencimiento <= FechaDeHoy:
        fecha_vencimiento = datetime.combine(
            ServiciosWeb.FechaVencimiento, datetime.min.time())
        diferencia = FechaDeHoy - fecha_vencimiento.date()
        dias_pasados = diferencia.days
        print(dias_pasados)

        EstadoDePago = False
        save_servicio = tblServiciosWeb.objects.get(ID=1)
        save_servicio.EstadoPago = EstadoDePago
        save_servicio.save()

        if ServiciosWeb.EstadoPago == False and dias_pasados >= 5:
            Servicios = False
            save_servicio = tblServiciosWeb.objects.get(ID=1)
            save_servicio.Servicio = Servicios
            save_servicio.save()
    return ServiciosWeb

def estadoPago(request):
    TServicio = tblServiciosWeb.objects.all()
    ServiciosWeb = tblServiciosWeb.objects.get(ID=1)
    FechaDeHoy = date.today().strftime('%Y-%m-%d')
    FechaDeHoy = date.today()

    if ServiciosWeb.FechaVencimiento <= FechaDeHoy:
        fecha_vencimiento = datetime.combine(
            ServiciosWeb.FechaVencimiento, datetime.min.time())
        diferencia = FechaDeHoy - fecha_vencimiento.date()
        dias_pasados = diferencia.days
        EstadoDePago = False
        save_servicio = tblServiciosWeb.objects.get(ID=1)
        save_servicio.EstadoPago = EstadoDePago
        save_servicio.save()
        dias_restantes = 5-dias_pasados


        if ServiciosWeb.EstadoPago == False and dias_pasados >= 5:
            Servicios = False
            save_servicio = tblServiciosWeb.objects.get(ID=1)
            save_servicio.Servicio = Servicios
            save_servicio.save()
    else:
        fecha_vencimiento = datetime.combine(
            ServiciosWeb.FechaVencimiento, datetime.min.time())
        diferenciaVencer = fecha_vencimiento.date() - FechaDeHoy
        dias_faltantes = diferenciaVencer.days
        dias_restantes = dias_faltantes
    return render(request, 'Configuracion/pagos/index.html', {'ServiciosWeb': ServiciosWeb, 'dias_restantes': dias_restantes, 'TServicio': TServicio})


def registrarPago(request):
    id = 1
    save_pago = tblServiciosWeb.objects.get(ID=id)
    fechaVencimiento = save_pago.FechaVencimiento

    if 'aplazar' in request.POST:
        ServicioActivo = True
        PagoActivo = True
        fechaFinal = fechaVencimiento + relativedelta(months=1)
        messages.success(request, f'El pago se ha autorizado correctamente')
    elif 'cancelar'in request.POST:
        ServicioActivo = False
        PagoActivo = False
        fechaFinal = date.today().strftime('%Y-%m-%d')
        messages.error(request, f'El servicio se ha cancelado')

    # Obtener la fecha de vencimiento actual y agregar 30 días
    fechaActualizada = fechaFinal
    save_pago.Servicio = ServicioActivo 
    save_pago.EstadoPago = PagoActivo
    save_pago.FechaVencimiento = fechaActualizada
    save_pago.save()

    return redirect('Pagos')

def notificacion(request):
    id = 1
    if 'Activar' in request.POST:
        Notificacion = False
        activar = tblServiciosWeb.objects.get(ID=id)
        activar.Notificacion = Notificacion
        activar.save()
        messages.success(request, f'Se han activado las notificaciones')
        return redirect('Pagos')
    elif 'Desactivar' in request.POST:
        Notificacion = True
        activar = tblServiciosWeb.objects.get(ID=id)
        activar.Notificacion = Notificacion
        activar.save()
        messages.success(request, f'Se han desactivado las notificaciones')
        return redirect('Pagos')

def NoPago(request):
    ServiciosWeb = servicioActivo()
    return render(request, 'Configuracion/pagos/Nopago.html',{'ServiciosWeb': ServiciosWeb})

def usuarioBloqueado(request):
    ServiciosWeb = servicioActivo()
    return render(request, 'Configuracion/Bloqueados/index.html',{'ServiciosWeb': ServiciosWeb})

def TablaUsuarios(request):
    usuarios_con_grupo = []
    TUsuarios = User.objects.all()

    for usuario in TUsuarios:
        is_authenticated = usuario.is_authenticated
        grupos = usuario.groups.exclude(name='Bloqueado')
        usuarios_con_grupo.append(
            {'usuario': usuario, 'is_authenticated': is_authenticated, 'grupos': grupos})
    ServiciosWeb = servicioActivo()
    return render(request, 'Configuracion/Tecnicos/index.html', {'ServiciosWeb': ServiciosWeb,
    'usuarios_con_grupo': usuarios_con_grupo})


def edicionUsuario(request, id):
    TEUser = User.objects.get(id=id)
    grupos = TEUser.groups.all()
    grupos_restantes = Group.objects.exclude(user=TEUser)
    ServiciosWeb = servicioActivo()
    return render(request, "Tecnicos/edit.html", {'ServiciosWeb': ServiciosWeb, 'TEUser': TEUser, 'grupos': grupos, 'grupos_restantes': grupos_restantes})

def actualizarUsuario(request):
    id = request.POST['id']
    nombre = request.POST['nombre'].title().strip()
    apellido = request.POST['apellido'].title().strip()
    roles = request.POST['roles']
    email = request.POST['email']

    # En esta variable depéndera al template al que se redireccionara
    vista = request.POST['vista']
    
    email_existente = User.objects.exclude(
        id=id).filter(username=email).exists()
    if email_existente:
        messages.error(
            request, f'El email "{email}" ya ha sido registrado anteriormente.')
    else:
        if 'bloqueado' in request.POST:
            roles = 'Bloqueado'
            usuario = User.objects.get(id=id)
            default_group = Group.objects.get(name=roles)
            usuario.groups.clear()
            usuario.groups.add(default_group)
            usuario.save()
        else:
            usuario = User.objects.get(id=id)
            default_group = Group.objects.get(name=roles)
            usuario.groups.clear()
            usuario.groups.add(default_group)
            usuario.first_name = nombre
            usuario.last_name = apellido
            usuario.username = email
            usuario.save()
            messages.success(
                request, f'El usuario "{email}" se ha actualizado exitosamente.')
    if vista == '1':
        return redirect('Usuarios:perfil')
    elif vista == '2':
        return redirect('/#Usuarios')
    elif vista == '3':
        return redirect('/#Usuarios')
    return redirect('/#Usuarios')

def agregarTecnicos(request):
    grupos = grupo_user(request)
    ServiciosWeb = servicioActivo()
    if request.method == 'POST':
        usuario_v = request.POST.get('usuario')
        full_name = request.POST.get('full_name')

        usuario = User.objects.get(id=usuario_v)
        catalogosUL = tblTecnicos.objects.filter(Tecnico__icontains = full_name, AreaRegistro = 'Catalogos', Acciones = 'Agregado').values('NombreTabla').distinct().order_by('NombreTabla')
        procesosUL = tblTecnicos.objects.filter(Tecnico__icontains = full_name, AreaRegistro = 'Procesos', Acciones = 'Agregado').values('NombreTabla').distinct().order_by('NombreTabla')
        subtablaUL = tblTecnicos.objects.filter(Tecnico__icontains = full_name, AreaRegistro = 'Subtabla', Acciones = 'Agregado').values('NombreTabla').distinct().order_by('NombreTabla')
        
        if 'tabla' in request.POST:
            tabla_v = request.POST.get('tabla')
            contenidoTabla = tblTecnicos.objects.filter(Tecnico__icontains = full_name, NombreTabla = tabla_v, Acciones = 'Agregado') 
            return render(request, "Registros/Agregados.html", {'grupos': grupos, 'catalogosUL': catalogosUL, 'ServiciosWeb': ServiciosWeb,
            'procesosUL':procesosUL,'subtablaUL':subtablaUL,'tabla_v':tabla_v, 'usuario':usuario, 'contenidoTabla':contenidoTabla})
        else:
            tabla_v = "No se ha seleccionado ninguna tabla"
            return render(request, "Registros/Agregados.html", {'grupos': grupos, 'catalogosUL': catalogosUL, 'ServiciosWeb': ServiciosWeb,
            'procesosUL':procesosUL,'subtablaUL':subtablaUL,'tabla_v':tabla_v, 'usuario':usuario})

def editadoTecnicos(request):
    grupos = grupo_user(request)
    ServiciosWeb = servicioActivo()
    
    if request.method == 'POST':
        usuario_v = request.POST.get('usuario')
        full_name = request.POST.get('full_name')

        usuario = User.objects.get(id=usuario_v)
        catalogosUL = tblTecnicos.objects.filter(Tecnico__icontains = full_name, AreaRegistro = 'Catalogos', AccionesEditado = 'Editado').values('NombreTabla').distinct().order_by('NombreTabla')
        procesosUL = tblTecnicos.objects.filter(Tecnico__icontains = full_name, AreaRegistro = 'Procesos', AccionesEditado = 'Editado').values('NombreTabla').distinct().order_by('NombreTabla')
        subtablaUL = tblTecnicos.objects.filter(Tecnico__icontains = full_name, AreaRegistro = 'Subtabla', AccionesEditado = 'Editado').values('NombreTabla').distinct().order_by('NombreTabla')

        if 'tabla' in request.POST:
            tabla_v = request.POST.get('tabla')
            contenidoTabla = tblTecnicos.objects.filter(Tecnico__icontains = full_name, NombreTabla = tabla_v, AccionesEditado = 'Editado') 
            return render(request, "Registros/Editados.html", {'grupos': grupos,'catalogosUL': catalogosUL, 'ServiciosWeb': ServiciosWeb,
            'procesosUL':procesosUL, 'subtablaUL':subtablaUL,'tabla_v':tabla_v, 'usuario':usuario, 'contenidoTabla':contenidoTabla})
        else:
            tabla_v = "No se ha seleccionado ninguna tabla"
            return render(request, "Registros/Editados.html", {'grupos': grupos, 'catalogosUL': catalogosUL, 'ServiciosWeb': ServiciosWeb,
            'procesosUL':procesosUL, 'subtablaUL':subtablaUL,'tabla_v':tabla_v, 'usuario':usuario})

def perfil(request):
    grupos = grupo_user(request)
    user = request.user 
    full_name = user.first_name + " " + user.last_name
    FTecnicosTablaCatalogos = tblTecnicos.objects.filter(Tecnico__icontains = full_name, AreaRegistro = 'Catalogos').values('NombreTabla').distinct().order_by('NombreTabla')
    FTecnicosTablaProcesos = tblTecnicos.objects.filter(Tecnico__icontains = full_name, AreaRegistro = 'Procesos').values('NombreTabla').distinct().order_by('NombreTabla')
    FTecnicosTablaSubTablas = tblTecnicos.objects.filter(Tecnico__icontains = full_name, AreaRegistro = 'Subtabla').values('NombreTabla').distinct().order_by('NombreTabla')
    ServiciosWeb = servicioActivo()
    
    if request.method == 'POST':
        TablaCatalogos = request.POST.get('tabla1')
        TablaProcesos = request.POST.get('tabla2')
        TablaSubtabla = request.POST.get('tabla3')

        if 'tabla1' in request.POST:
            TablaProcesos = "Buscar..."
            TablaSubtabla = "Buscar..."
            TablaSel = "Catálogos - " + TablaCatalogos
            TTecnicos = tblTecnicos.objects.filter(Tecnico__icontains=full_name, NombreTabla = TablaCatalogos)
            return render(request, 'Perfil/index.html', {'grupos': grupos, 'TTecnicos':TTecnicos, 'ServiciosWeb': ServiciosWeb,
            'FTecnicosTablaCatalogos':FTecnicosTablaCatalogos, 'FTecnicosTablaProcesos':FTecnicosTablaProcesos, 'FTecnicosTablaSubTablas':FTecnicosTablaSubTablas,
            'TablaCatalogos':TablaCatalogos, 'TablaProcesos':TablaProcesos, 'TablaSubtabla':TablaSubtabla,
            'tablaseleccionada':TablaSel
            })
        if 'tabla2' in request.POST:
            TablaCatalogos = "Buscar..."
            TablaSubtabla = "Buscar..."
            TablaSel = "Procesos - " + TablaProcesos
            TTecnicos = tblTecnicos.objects.filter(Tecnico__icontains=full_name, NombreTabla = TablaProcesos)
            return render(request, 'Perfil/index.html', {'grupos': grupos, 'TTecnicos':TTecnicos, 'ServiciosWeb': ServiciosWeb,
            'FTecnicosTablaCatalogos':FTecnicosTablaCatalogos, 'FTecnicosTablaProcesos':FTecnicosTablaProcesos,'FTecnicosTablaSubTablas':FTecnicosTablaSubTablas,
            'TablaCatalogos':TablaCatalogos, 'TablaProcesos':TablaProcesos, 'TablaSubtabla':TablaSubtabla,
            'tablaseleccionada':TablaSel
             })
        if 'tabla3' in request.POST:
            TablaCatalogos = "Buscar..."
            TablaProcesos = "Buscar..."
            TablaSel = "Subtablas - " + TablaSubtabla
            TTecnicos = tblTecnicos.objects.filter(Tecnico__icontains=full_name, NombreTabla = TablaSubtabla)
            return render(request, 'Perfil/index.html', {'grupos': grupos, 'TTecnicos':TTecnicos, 'ServiciosWeb': ServiciosWeb,
            'FTecnicosTablaCatalogos':FTecnicosTablaCatalogos, 'FTecnicosTablaProcesos':FTecnicosTablaProcesos, 'FTecnicosTablaSubTablas':FTecnicosTablaSubTablas,
            'TablaCatalogos':TablaCatalogos, 'TablaProcesos':TablaProcesos, 'TablaSubtabla':TablaSubtabla,
            'tablaseleccionada':TablaSel
            })
    else:
        TablaCatalogos = "Buscar..."
        TablaProcesos = "Buscar..."
        TablaSubtabla = "Buscar..."
        TTecnicos = tblTecnicos.objects.filter(Tecnico='').all
        return render(request, 'Perfil/index.html', {'grupos': grupos, 'TTecnicos':TTecnicos, 'ServiciosWeb': ServiciosWeb,
        'FTecnicosTablaCatalogos':FTecnicosTablaCatalogos, 'FTecnicosTablaProcesos':FTecnicosTablaProcesos, 'FTecnicosTablaSubTablas':FTecnicosTablaSubTablas,
        'TablaCatalogos':TablaCatalogos, 'TablaProcesos':TablaProcesos, 'TablaSubtabla':TablaSubtabla,
        'tablaseleccionada':TablaCatalogos,'tablaseleccionada':TablaProcesos,'tablaseleccionada':TablaSubtabla
        })
                
def agregarDatosTecnicos(request, Tecnico_v, NombreTabla_v, IDFilaTabla_v, AreaRegistro_v, IDFila_v):
    try:
        Acciones_v = 'Agregado'
        Fecha_v  = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')
        
        tblTecnicos.objects.create(
            Tecnico = Tecnico_v, NombreTabla = NombreTabla_v, IDFilaTabla = IDFilaTabla_v, 
            Acciones = Acciones_v, Fecha = Fecha_v, AreaRegistro = AreaRegistro_v, IDFila = IDFila_v
        )
    except Exception as e:
        print("Error ", e)
        
def editarDatosTecnicos(request, TecnicoEditor_v, NombreTabla_v, IDFilaTabla_v):
    try:
        Acciones_v = 'Editado'
        FechaEditor_v   = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')
        
        tecnicos_editor = tblTecnicos.objects.get(IDFila=IDFilaTabla_v, NombreTabla=NombreTabla_v)
        tecnicos_editor.TecnicoEditor = TecnicoEditor_v
        tecnicos_editor.FechaActualizado = FechaEditor_v
        tecnicos_editor.AccionesEditado = Acciones_v
        tecnicos_editor.save()
    except Exception as e:
        print("Error ", e)
                      