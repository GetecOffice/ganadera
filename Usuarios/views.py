from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User
from Aplicacion.models import *
from datetime import datetime, timedelta, date
from django.contrib import messages
from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
# Create your views here.
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
        return redirect('perfil')
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
            return render(request, "Configuracion/Tecnicos/Agregados.html", {'grupos': grupos, 'catalogosUL': catalogosUL, 'ServiciosWeb': ServiciosWeb,
            'procesosUL':procesosUL,'subtablaUL':subtablaUL,'tabla_v':tabla_v, 'usuario':usuario, 'contenidoTabla':contenidoTabla})
        else:
            tabla_v = "No se ha seleccionado ninguna tabla"
            return render(request, "Configuracion/Tecnicos/Agregados.html", {'grupos': grupos, 'catalogosUL': catalogosUL, 'ServiciosWeb': ServiciosWeb,
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
            return render(request, "Configuracion/Tecnicos/Editados.html", {'grupos': grupos,'catalogosUL': catalogosUL, 'ServiciosWeb': ServiciosWeb,
            'procesosUL':procesosUL, 'subtablaUL':subtablaUL,'tabla_v':tabla_v, 'usuario':usuario, 'contenidoTabla':contenidoTabla})
        else:
            tabla_v = "No se ha seleccionado ninguna tabla"
            return render(request, "Configuracion/Tecnicos/Editados.html", {'grupos': grupos, 'catalogosUL': catalogosUL, 'ServiciosWeb': ServiciosWeb,
            'procesosUL':procesosUL, 'subtablaUL':subtablaUL,'tabla_v':tabla_v, 'usuario':usuario})