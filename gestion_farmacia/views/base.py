from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from gestion_farmacia.models import Usuario, Notificacion, OrdenDeCompra, Producto, SolicitudReserva,TicketSoporte, Sesion
import requests
import json     
#json.dumps() para convertir de python a json
#json.loads() para convertir de json a python

urlBase = 'http://localhost:80/api/v1' #RESERVADO PARA LA URL DEL SERVIDOR
user = Usuario() #NO TOCAR
sesion = Sesion() #NO TOCAR

def getURL():
    return urlBase

def getUser():
    return user

def getSesion():
    return sesion

def Inicio(request):
    novistas = False
    context = {'user':user,'sesion':sesion.activa,'novistas':novistas,'volver':{'url':'#','D':'none'}}
    return render(request,'base/main.html',context)

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
    return render(request,'base/login.html',context)

def Recupera(request):
    template = 'base/recupera.html'
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
            template = 'base/recupera2.html'
    context = {'sesion':sesion.activa,'novistas':False,'msg':msg,'dspl':dspl,'volver':{'url':'/login/','D':'block'}}
    return render(request,template,context)

#REGISTRADO
def Logout(request):
    if not sesion.activa:
        return HttpResponseRedirect('/login')
    sesion.cerrar()
    #notificaciones = None
    return HttpResponseRedirect('/')

def Soporte(request):
    novistas = False
    context = {'user':user,'novistas':novistas,'sesion':sesion.activa,'volver':{'url':'/','D':'block'}}
    if request.method == 'POST':
        return render(request,'base/soporte2.html',context)    
    return render(request,'base/soporte.html',context)

def Faq(request):
    novistas = False
    context = {'user':user,'novistas':novistas,'sesion':sesion.activa,'volver':{'url':'/','D':'block'}}
    return render(request,'base/faq.html',context)
