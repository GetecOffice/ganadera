
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from Aplicacion.models import *
import time
from Usuarios.views import servicioActivo, agregarDatosTecnicos, editarDatosTecnicos
@login_required
def grupo_user(request):
    user = request.user
    if user.groups.exists():
        grupo = user.groups.first()
        grupos_user = grupo.name
        grupos = grupos_user
        return grupos
    
def FormularioGrupos(request):
    grupos = grupo_user(request)
    ultimo_id = Group.objects.order_by('-id').first()
    if ultimo_id:
        ultimo_folio = ultimo_id.id + 1
    else:
        ultimo_folio = 1
    ServiciosWeb = servicioActivo()
    return render(request, 'Grupos/form.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb,
    'ultimo_folio': ultimo_folio})
    
def agregarGrupos(request):
    id = request.POST['id']
    descripcion_v = request.POST['descripcion'].title()

    # tecnicos
    Tecnico_v = request.POST['tecnico'].title()
    NombreTabla_v = 'Grupo'
    IDFilaTabla_v = "Vacio"
    AreaRegistro_v = 'Configuración'
    IDFila_v = id

    existente = Group.objects.filter(name=descripcion_v).exists()
    if existente:
        errorCol = 'error'
        messages.error(request, f'El Grupo {descripcion_v} ya ha sido registrado antreriormente')
        columnas = {'ultimo_folio': id, 'errorCol':errorCol}
        return render(request, "Grupos/form.html", columnas)
    else:
        Group.objects.create( name = descripcion_v )
        agregarDatosTecnicos(request, Tecnico_v, NombreTabla_v, IDFilaTabla_v, AreaRegistro_v, IDFila_v)
        messages.success(request, f'El Grupo {descripcion_v} se ha registrado exitosamente')

    if request.method == 'POST':
        if 'salir' in request.POST:
            return redirect('configuracion:T_Grupos')
        elif 'agregar' in request.POST:
            return redirect('configuracion:F_Grupos')
    else:
        return redirect('configuracion:T_Grupos')
    
def TablaGrupos(request):
    grupos = grupo_user(request)
    ultimo_id = Group.objects.order_by('-id').first()
    if ultimo_id:
        ultimo_folio = ultimo_id.id + 1
    else:
        ultimo_folio = 1
    TGrupos = Group.objects.all()
    ServiciosWeb = servicioActivo()
    return render(request, 'Grupos/index.html',{'grupos': grupos,
    'ServiciosWeb': ServiciosWeb,'TGrupos': TGrupos, 'ultimo_folio':ultimo_folio})

def editarGrupos(request, ID):
    grupos = grupo_user(request)
    TEGrupos = Group.objects.get(id=ID)
    return render(request, "Grupos/edit.html",{'grupos': grupos,'TEGrupos': TEGrupos})

def actualizarGrupo(request):
    id = request.POST['id']
    descripcion_v = request.POST['descripcion'].title()

   # tecnicos
    TecnicoEditor_v = request.POST['tecnico'].title()
    NombreTabla_v = 'Grupo'
    IDFilaTabla_v = id

    nombre_existente = Group.objects.filter(name=descripcion_v).exclude(id=id).exists()
    if nombre_existente:
        messages.error(request, f'El Grupo "{descripcion_v}" ya ha sido registrado anteriormente.')
    else:
        grupo = Group.objects.get(id=id)
        grupo.name = descripcion_v
        grupo.save()
        editarDatosTecnicos(request, TecnicoEditor_v, NombreTabla_v, IDFilaTabla_v)
        messages.success(request, f'El Grupo "{descripcion_v}" se ha actualizado exitosamente.')
    return redirect('configuracion:T_Grupos')

def TablaPermisos(request):
    grupos = grupo_user(request)
    TPermisos = Permission.objects.exclude(name__icontains = 'Restringido')
    ServiciosWeb = servicioActivo()
    return render(request, 'Permisos/permisos.html',{'grupos': grupos,
    'ServiciosWeb': ServiciosWeb,'TPermisos': TPermisos})

def TablaPermisosAsignaElimina(request):
    grupos = grupo_user(request)
    ServiciosWeb = servicioActivo()
    FGrupos = Group.objects.all()
    GrupoID = request.POST.get('grupo', '')
    if GrupoID is not None and GrupoID != '':
        Grupo_Select = Group.objects.get(id=GrupoID)
        grupoPost = [{'id': Grupo_Select.id, 'name': Grupo_Select.name}]
    else:
        grupoPost = [{'id': ''}]

    if GrupoID is not None and GrupoID != '':
        grupo = Group.objects.get(id=GrupoID)
        TPermisosAsignados = grupo.permissions.all()
        TPermisosLibres = Permission.objects.exclude(id__in=TPermisosAsignados.values_list('id', flat=True))
    else:
        TPermisosLibres = Permission.objects.all()
        TPermisosAsignados = Group.objects.all()

    asignar = request.POST.get('asignar', '')
    if asignar is not None and asignar != '':
        grupo = request.POST['grupo']
        permiso = request.POST['permiso']
        grupoPost = [{'id': Grupo_Select.id, 'name': Grupo_Select.name}]

        # # Obtener el grupo y el permiso
        # grupo = Group.objects.get(id=grupo)
        # permiso = Permission.objects.get(id=idpermiso)

        # # Agregar el permiso al grupo
        # grupo.permissions.add(permiso)

        grupo_id = request.POST['grupo']
        grupo = Group.objects.get(id=grupo_id)
        
        permisos_seleccionados = request.POST.getlist('permisos_seleccionados')
        for permiso_id in permisos_seleccionados:
            permiso = Permission.objects.get(id=permiso_id)
            grupo.permissions.add(permiso)
            
        messages.success(request, f'Permisos asignados exitosamente')

        return render(request, 'Permisos/index.html',{'grupos': grupos,
        'grupos': grupos, 'ServiciosWeb':ServiciosWeb, 
        'TPermisosLibres': TPermisosLibres, 'TPermisosAsignados':TPermisosAsignados,
        'FGrupos':FGrupos, 'grupoPost': grupoPost})
    
    liberar = request.POST.get('liberar', '')
    if liberar is not None and liberar != '':
        grupo = request.POST['grupo']
        permiso = request.POST['permiso']
        grupoPost = [{'id': Grupo_Select.id, 'name': Grupo_Select.name}]

        # # Obtener el grupo y el permiso
        # grupo = Group.objects.get(id=grupo)
        # permiso = Permission.objects.get(id=idpermiso)

        # # Agregar el permiso al grupo
        # grupo.permissions.remove(permiso)

        grupo_id = request.POST['grupo']
        grupo = Group.objects.get(id=grupo_id)
        
        permisos_seleccionados = request.POST.getlist('permisos_seleccionados')
        for permiso_id in permisos_seleccionados:
            permiso = Permission.objects.get(id=permiso_id)
            grupo.permissions.remove(permiso)
            
        messages.success(request, f'Permisos eliminados exitosamente')

        return render(request, 'Permisos/index.html',{'grupos': grupos,
        'grupos': grupos, 'ServiciosWeb':ServiciosWeb, 
        'TPermisosLibres': TPermisosLibres, 'TPermisosAsignados':TPermisosAsignados,
        'FGrupos':FGrupos, 'grupoPost': grupoPost})
    
    return render(request, 'Permisos/index.html',{'grupos': grupos, 'ServiciosWeb':ServiciosWeb, 
    'TPermisosLibres': TPermisosLibres, 'TPermisosAsignados':TPermisosAsignados, 'FGrupos':FGrupos, 'grupoPost': grupoPost})

def editarPermisos(request, ID):
    grupos = grupo_user(request)
    TEPermisos = Permission.objects.get(id=ID)
    return render(request, "Permisos/edit.html",{'grupos': grupos,'TEPermisos': TEPermisos })

def actualizarPermiso(request):
    id = request.POST['id']
    descripcion_v = request.POST['descripcion'].title()

    nombre_existente = Permission.objects.filter(name=descripcion_v).exclude(id=id).exists()
    if nombre_existente:
        messages.error(request, f'El permiso "{descripcion_v}" ya ha sido registrado anteriormente.')
    else:
        permiso = Permission.objects.get(id=id)
        permiso.name = descripcion_v
        permiso.save()
        messages.success(request, f'El Grupo "{descripcion_v}" se ha actualizado exitosamente.')
    return redirect('configuracion:T_Permisos')
    
    
    
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def TablaTiposDeRol(request):
    grupos = grupo_user(request)
    usuario = request.user
    grupos_usuario = usuario.groups.all()

    for grupo in grupos_usuario:
        TPermisos = grupo.permissions.all()
        

    ServiciosWeb = servicioActivo()
    return render(request, 'perfil/TiposRol.html',{'grupos': grupos,
    'ServiciosWeb': ServiciosWeb,'TPermisos': TPermisos})
