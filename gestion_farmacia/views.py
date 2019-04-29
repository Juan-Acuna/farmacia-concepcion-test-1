from django.core.mail import EmailMessage
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Usuario, Notificacion, OrdenDeCompra, Producto, SolicitudReserva,TicketSoporte, Sesion
import requests
import json     
#json.dumps() para convertir de python a json
#json.loads() para convertir de json a python


urlBase = 'http://sheemin.club/api/v1' #RESERVADO PARA LA URL DEL SERVIDOR
user = Usuario() #NO TOCAR
sesion = Sesion() #NO TOCAR
notificaciones = None #NO TOCAR
productos = None #NO TOCAR
localnot = []

def Inicio(request):
    novistas = False
    context = {'user':user,'sesion':sesion.activa,'novistas':novistas,'volver':{'url':'#','D':'none'}}
    return render(request,'main.html',context)

def Login(request):
    msg = ''
    dspl = 'none'
    if request.method == 'POST':
        obj = {'rut':request.POST['rut'],'password':request.POST['password']}
        headers = {'content-type': 'application/json'}
        url = '/usuario/autenticacion'
        r = requests.post(urlBase + url,data=json.dumps(obj),headers=headers)
        print(r.status_code)
        if r.status_code == 200:
            ujson = r.json()
            user.rut = request.POST['rut']
            user.password = request.POST['password']
            sesion.iniciar(user,ujson['token'],ujson['creacion'],ujson['expiracion'])
            return HttpResponseRedirect('/')
        elif r.status_code == 504:
            msg = 'El servidor tardó demasiado en responder.'
            dspl = 'inline-block'
        else:
            ujson = r.json()
            msg = ujson['message']
            dspl = 'inline-block'
    context = {'sesion':sesion.activa,'novistas':False,'msg':msg,'dspl':dspl,'volver':{'url':'/','D':'block'}}
    return render(request,'login.html',context)

def Recupera(request):
    template = 'recupera.html'
    msg = ''
    dspl ='none'
    if request.method == 'POST':
        obj = {'rut':request.POST['rut']}
        headers = {'content-type': 'application/json'}
        url = '' #FALTA URL RECUPERACION                    *************************************!
        r = requests.post(urlBase + url,data=json.dumps(obj),headers=headers)
        if r.status_code == 400 or r.status_code == 403:
            msg = 'El rut no esta registrado.'
            dspl = 'inline-block'
        else:
            template = 'recupera2.html'
    context = {'sesion':sesion.activa,'novistas':False,'msg':msg,'dspl':dspl,'volver':{'url':'/login/','D':'block'}}
    return render(request,template,context)

#REGISTRADO
def Logout(request):
    if not sesion.activa:
        return HttpResponseRedirect('/login')
    sesion.cerrar()
    #notificaciones = None
    return HttpResponseRedirect('/')

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

def Busqueda(request):
    novistas = False
    url = '/producto/'
    texto = ''
    filtros = []
    labs = None
    tipos = None
    productos = {}
    headers = {'content-type': 'application/json'}    
    if request.method == 'POST':
        if request.POST['pagina'] == 'main':
            if len(request.POST['busqueda']) > 0:
                obj = {'nombre':request.POST['busqueda']}
                r = requests.get(urlBase + url,headers=headers,data=json.dumps(obj))
            else:
                texto = 'No se realizó busqueda.'
                productos = None
                context = {'user':user,'sesion':sesion.activa,'novistas':novistas,'texto':texto,'productos':productos,'fil':filtros,'tipos':tipos,'labs':labs,'volver':{'url':'/','D':'block'}}
                return render(request,'busqueda.html',context)
        else:
            obj = {}
            if len(request.POST['busqueda']) > 0:
                obj['nombre'] = request.POST['busqueda']
            if len(request.POST['lab']) > 0:
                obj['laboratorio'] = request.POST['lab']
                filtros += 'Laboratorio: '+ request.POST['lab']
            #if len(request.POST['tipo']) > 0:
            #    filtros += 'Tipo: '+ request.POST['tipo']
            #    obj['laboratorio'] = request.POST['tipo']
            r = requests.get(urlBase + url,headers=headers,data=json.dumps(obj))
        print(r.status_code)
        if r.status_code == 200:
            rlab = requests.get(urlBase + '/laboratorio/',headers=headers)
            rt = requests.get(urlBase + '/tipoproducto/',headers=headers)
            labs = rlab.json()
            tipos = rt.json()
            productos = r.json()
            if len(productos) <=0:
                texto = 'No se encontraron coincidencias.'
                productos = {}
        elif r.status_code == 504 or r.status_code == 502:
            texto = 'El servidor tardó mucho en responder.'
        else:
            j = r.json()
            texto = j['message']
            #texto = 'Hubo un problema en el servidor.'
    else:
        texto = 'No se realizó busqueda.'
        productos = None
    context = {'user':user,'sesion':sesion.activa,'novistas':novistas,'texto':texto,'productos':productos,'fil':filtros,'tipos':tipos,'labs':labs,'volver':{'url':'/','D':'block'}}
    return render(request,'busqueda.html',context)

#REGISTRADO
def Compra(request,pk):
    novistas = False
    res = None
    headers = {'content-type': 'application/json'}
    if request.method == 'POST':
        if request.POST['boton'] == 'C':
            headers['Authorization'] = 'Bearer '+sesion.token
            if not sesion.activa:
                return HttpResponseRedirect('/login')
            #Compra
            res = True
            url = '/compra/'
            obj = {'usuario':user.rut,'cantidad':request.POST['cantidad'],'producto':pk}
        else:
            if not sesion.activa:
                return HttpResponseRedirect('/login')
            #Reserva
            headers['Authorization'] = 'Bearer '+sesion.token
            res = False
            url = '/reserva/'
            obj = {'usuario':user.rut,'reservas':[request.POST['cantidad'],pk]}
        r = requests.post(urlBase + url,headers=headers,data=json.dumps(obj))
        if r.status_code == 200:
            j = r.json()
            if res:
                #primero medio de pago (simulado)
                n = Notificacion()
                n.ausnto = 'Compra realizada'
                n.mensaje = 'Se ha realizado una compra en su cuenta.\n Detalles: ID Producto: '+ j['producto'] +', Cantidad: '+j['cantidad']
                n.usuario = user.rut
                localnot += n
                return HttpResponseRedirect('/resultado-compra/')
            else:
                n = Notificacion()
                n.ausnto = 'Reserva realizada'
                n.mensaje = 'Se ha realizado una reserva en su cuenta.\n Detalles: ID Producto: '+ j['producto']
                n.usuario = user.rut
                localnot += n
                return HttpResponseRedirect('/resultado-reserva/')
        elif r.status_code == 403:
            return HttpResponseRedirect('/login')
        else:
            texto = 'Hubo un problema al consultar al servidor.'
    else:
        rlab = requests.get(urlBase + '/laboratorio/',headers=headers)
        labs = rlab.json()
        url = '/producto/'+pk
        pr = requests.get(urlBase + url,headers=headers)
        producto = pr.json()
    context = {'user':user,'novistas':novistas,'sesion':sesion.activa,'labs':labs,'producto':producto,'volver':{'url':'#','D':'none'}}
    return render(request,'producto.html',context)

def Res_compra(request):
    context = {'res':True}
    return render(request,'res_compra.html',context)

def Res_reserva(request):
    context = {'res':False}
    return render(request,'res_compra.html',context)

#REGISTRADO
#def Reserva(request,pk):
#    novistas = False
#    headers = {'content-type': 'application/json','Authorization':'Bearer '+sesion.token}
#    url = '/reserva/'
#    obj = {'usuario':user.rut,'producto':pk}
#    r = requests.post(urlBase + url,headers=headers,data=json.dumps(obj))
#    if r.status_code == 200:
#        j = r.json()
#            n = Notificacion()
#            n.ausnto = 'Reserva realizada'
#            n.mensaje = 'Se ha realizado una reserva en su cuenta.\n Detalles: ID Producto: '+ j['producto']
#            n.usuario = user.rut
#            localnot += n
#            return HttpResponseRedirect('/resultado-reserva/')
#        elif r.status_code == 403:
#            return HttpResponseRedirect('/login')
#        else:
#            texto = 'Hubo un problema al consultar al servidor.'
#    context = {'user':user,'novistas':novistas,'sesion':sesion.activa,'volver':{'url':'#','D':'none'}}
#    return render(request,'reserva.html',context)

def Soporte(request):
    novistas = False
    context = {'user':user,'novistas':novistas,'sesion':sesion.activa,'volver':{'url':'/','D':'block'}}
    if request.method == 'POST':
        return render(request,'soporte2.html',context)    
    return render(request,'soporte.html',context)

def Faq(request):
    novistas = False
    context = {'user':user,'novistas':novistas,'sesion':sesion.activa,'volver':{'url':'/','D':'block'}}
    return render(request,'faq.html',context)