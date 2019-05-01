from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from gestion_farmacia.models import Usuario, Notificacion, OrdenDeCompra, Producto, SolicitudReserva,TicketSoporte, Sesion
from base import getSesion,getURL,getUser
import requests
import json

urlBase = getURL() #NO TOCAR
user = getUser() #NO TOCAR
sesion = getSesion() #NO TOCAR
notificaciones = None #NO TOCAR
productos = None #NO TOCAR

#REGISTRADO
def Perfil(request):
    if not sesion.activa:
        return HttpResponseRedirect('/login')
    msg = ''
    dspl = 'none'
    novistas = False
    url = '/usuario/' + user.rut + '/'
    headers = {'content-type': 'application/json','Authorization':'Bearer '+sesion.token}
    if request.method == 'POST':
        if request.POST['cambio'] == 'email':
            if request.POST['password'] == user.password:
                contra = user.password
                correo = request.POST['email']
        else:
            if request.POST['new-pass'] == request.POST['new-pass2'] and request.POST['password'] == user.password:
                contra = request.POST['new-pass']
                correo = user.email
        obj = {'password':contra,'email':correo}
        r = requests.patch(urlBase + url,headers=headers,data=json.dumps(obj))
        if r.status_code == 200:
            ujson = r.json()
            user.rut = ujson['rut']
            user.email = ujson['email']
        else:
            msg = 'Hubo un problema al consultar al servidor.'
            dspl = 'inline-block'
    else:
        r = requests.get(urlBase + url,headers=headers)
        if r.status_code == 200:
            ujson = r.json()
            user.rut = ujson['rut']
            user.email = ujson['email']
            user.fecha_nac = ujson['fecha_nacimiento']
        elif r.status_code ==400:
            msg = 'Hubo un problema al consultar al servidor.'
            dspl = 'inline-block'
        elif r.status_code == 403:
            return HttpResponseRedirect('/login')
    context = {'user':user,'sesion':sesion.activa,'novistas':novistas,'dspl':dspl,'msg':msg,'volver':{'url':'/','D':'block'}} 
    return render(request,'perfil.html',context)

#REGISTRADO
def Notificaciones(request):
    if not sesion.activa:
        return HttpResponseRedirect('/login')
    novistas = False
    texto = ''
    notificaciones = {}
    url = '/notificacion/'
    headers = {'content-type': 'application/json','Authorization':'Bearer '+sesion.token}
    r = requests.get(urlBase + url,headers=headers)
    if r.status_code == 200:
        notificaciones = json.loads(r.json())
        for n in notificaciones:
            if n['esta_visto'] == False:
                novistas = True
        if not novistas:
            texto = 'No tienes notificaciones pendientes.'
    elif r.status_code == 400:
        texto = 'Hubo un problema al consultar al servidor.'
    elif r.status_code == 404:
        texto = 'No tienes notificaciones pendientes.'
    else:
        return HttpResponseRedirect('/login')
    context = {'user':user,'sesion':sesion.activa,'novistas':novistas, 'notificaciones':notificaciones,'texto':texto,'volver':{'url':'/','D':'block'}}
    return render(request,'notificaciones.html',context)

def VerNotificacion(request,pk):
    if not sesion.activa:
        return HttpResponseRedirect('/login')
    novistas = False
    notifi = None
    #for n in notificaciones:
    #    if n.id == pk:
    #        notifi = n
    url = '/notificacion/' + notifi.id
    headers = {'content-type': 'application/json','Authorization':'Bearer '+sesion.token}
    obj = {'esta_visto':True}
    r = requests.get(urlBase + url,headers=headers,data=json.dumps(obj))
    context = {'user':user,'sesion':sesion.activa,'novistas':novistas,'notificacion':notifi,'volver':{'url':'/notificaciones/','D':'block'}}
    return render(request,'notificaciones.html',context)
