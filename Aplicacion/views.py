from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.models import Group
from django.db.models import Count, Sum, Q
from collections import defaultdict
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from Usuarios.views import servicioActivo
# LLAMAR ARCHIVOS LOCALES
from .forms import *
from .models import *
import json
import time

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< FUNCION REGISTRO DE USUARIOS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class CustomLoginView(LoginView):
    template_name = 'Acceso/login.html'
    def form_invalid(self, form):
        messages.error(self.request, 'Usuario o contraseña incorrectos.')
        return super().form_invalid(form)

# ------------------------------------------------------------REGISTRO-------------------------------------------------------------
def Register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_bound:  # Verifica si el formulario está enlazado
            form.full_clean()
            data = form.cleaned_data
            # Realiza tus propias validaciones aquí
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            print(first_name)
            print(last_name)

            # Ejemplo de validaciones personalizadas
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Error: El nombre de usuario "{username}" ya está en uso.')
            elif password1 != password2:
                messages.error(request, 'Error: Las contraseñas no coinciden.')
            elif len(password1) < 8:
                messages.error(request, 'Error: La contraseña debe tener al menos 8 caracteres.')
            else:
                # Si todas las validaciones pasan, guarda el usuario
                user = User.objects.create_user(username=username, password=password1, last_name=last_name, first_name=first_name)
                ultimo_usuario = User.objects.latest('id')
                default_group = Group.objects.get(name='Usuario')
                ultimo_usuario.groups.add(default_group)
                
                messages.success(request, f'El Usuario con el nombre de usuario "{username}" ha sido creado')
                return redirect('Login')

            # Si llega aquí, es porque hubo algún error
            return render(request, 'Acceso/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()

    context = {'form': form}
    return render(request, 'Acceso/register.html', context)
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def menuInfo(request):
    ContClientes = tblClientes.objects.count()
    ContProveedores = tblProveedores.objects.count()
    ContOperadores = tblOperadores.objects.count()
    ContMateriaPrima = tblMateriaPrima.objects.count()
    ContProductos = tblProductos.objects.count()
    ContCorrales = tblCorrales.objects.count()
    ContTipoAnimales = tblAnimalesTipo.objects.count()
    ContContMatPrima = tblContenedoresMateriaPrima.objects.count()
    ContContProductos = tblContenedoresProductos.objects.count()
    ContTolva = tblTolva.objects.count()
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< corrales liberador y ocupados >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    corralesLiberados = tblCorrales.objects.filter(IDCliente_id = 1).count()
    corralesAsignados = tblCorrales.objects.exclude(IDCliente_id = 1).count()
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Grafica de cantidad de corrales por clientes >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    corrales = (tblCorrales.objects.values('IDCliente__Nombre').annotate(total=Count('ID')).filter(total__gt=5).exclude(IDCliente=1).order_by('-total'))

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Tolvas cargadas >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    tolvas = tblTolva.objects.values('ID', 'Capacidad', 'Alias').exclude(ID = 1)
    servido_por_tolva = (tblServido.objects.filter(IDEstatus_id=8).values('IDTolva').annotate(total=Sum('CantidadSolicitada')).exclude(IDTolva = 1))
    servido_dict = {item['IDTolva']: item['total'] for item in servido_por_tolva}
    datos_tolvas = []
    for tolva in tolvas:
        id_tolva = tolva['ID']
        capacidad = tolva['Capacidad']
        alias = tolva['Alias']
        cantidad = servido_dict.get(id_tolva, 0)
        porcentaje = round((cantidad / capacidad) * 100, 2) if capacidad > 0 else 0
        datos_tolvas.append({
            'alias': alias,
            'capacidad': capacidad,
            'cantidad': cantidad,
            'porcentaje': porcentaje
        })
 

    labels = [c['IDCliente__Nombre'] for c in corrales]
    data = [c['total'] for c in corrales]

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Conteo de animales >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Traer todos los tipos de animales
    animales_tipo = tblAnimalesTipo.objects.all()

    # Traer todos los detalles de movimientos
    detalle_mov = tblDetalleMovAnimales.objects.values('IDFolio', 'IDAnimales', 'Cantidad')

    # Traer todos los movimientos con su tipo
    movimientos = tblMovimientoAnimales.objects.values('Folio', 'IDMovimiento')

    # Convertir movimientos a un diccionario para fácil acceso
    mov_dict = {m['Folio']: m['IDMovimiento'] for m in movimientos}

    # Calcular conteo por tipo
    conteo_animales = defaultdict(int)

    for d in detalle_mov:
        folio = d['IDFolio']
        tipo = mov_dict.get(folio)
        cantidad = d['Cantidad']
        animal_id = d['IDAnimales']
        if tipo == 1:  # Entrada
            conteo_animales[animal_id] += cantidad
        elif tipo == 2:  # Salida
            conteo_animales[animal_id] -= cantidad

    # Crear lista de resultados con nombre
    resultado_final = []
    for animal in animales_tipo:
        resultado_final.append({
            'nombre': animal.Descripcion,
            'cantidad': conteo_animales.get(animal.ID, 0)
        })
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Conteo de servidos >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    PServidosRegistros = tblServido.objects.all()
    registros = PServidosRegistros.count()
    
    PServidosPendientes = tblServido.objects.filter(Q(IDEstatus_id = 3) | Q(IDEstatus_id=9)).all()
    pendientes = PServidosPendientes.count()

    PServidosManual = tblServido.objects.filter(IDEstatus_id = 7).all()
    manuales = PServidosManual.count()

    PServidosConsolidacion = tblServido.objects.filter(IDEstatus_id= 8).all()
    tolva = PServidosConsolidacion.count()
    
    PServidosConsolidacion = tblServido.objects.filter(Q(IDEstatus_id =  10) | Q(IDEstatus_id = 11)).all()
    servidos = PServidosConsolidacion.count()    
    
    # USUARIOS
    usuarios_con_grupo = []
    TUsuarios = User.objects.all().exclude(username="admin@gmail.com")

    for usuario in TUsuarios:
        is_authenticated = usuario.is_authenticated
        grupos = usuario.groups.exclude(name='Bloqueado')
        usuarios_con_grupo.append({'usuario': usuario, 'is_authenticated': is_authenticated, 'grupos': grupos})
    
    ServiciosWeb = servicioActivo()

    
    # CONFIGURACION
    TConfiguracion = tblConfiguracion.objects.all()
    print(TConfiguracion)
    return render(request, 'Menu/index.html', { 'ContClientes': ContClientes, 'ContProveedores': ContProveedores, 'ContOperadores': ContOperadores, 
    'ContMateriaPrima': ContMateriaPrima, 'ContProductos': ContProductos, 'ContCorrales': ContCorrales, 'ContTipoAnimales': ContTipoAnimales, 
    'ContContMatPrima': ContContMatPrima, 'ContContProductos': ContContProductos, 'ContTolva': ContTolva, 'data': json.dumps(data), 'labels': json.dumps(labels), 
    'datos_tolvas':datos_tolvas, 'corralesLiberados': corralesLiberados, 'corralesAsignados':corralesAsignados, 'resultado_animales': resultado_final,
    'manuales':manuales, 'registros':registros, 'pendientes':pendientes, 'servidos':servidos, 'tolva':tolva, 'usuarios_con_grupo': usuarios_con_grupo  ,
    'ServiciosWeb': ServiciosWeb, 'TConfiguracion':TConfiguracion
    })
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
