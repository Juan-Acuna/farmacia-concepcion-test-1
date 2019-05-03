from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from gestion_farmacia.models import Usuario, Notificacion, OrdenDeCompra, Producto, SolicitudReserva,TicketSoporte, Sesion
from .base import getSesion,getURL,getUser
import requests
import json

urlBase = getURL() #NO TOCAR
user = getUser() #NO TOCAR
sesion = getSesion() #NO TOCAR
notificaciones = None #NO TOCAR
productos = None #NO TOCAR

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
                return render(request,'compra/busqueda.html',context)
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
    return render(request,'compra/busqueda.html',context)

def Compra(request,pk):
    novistas = False
    res = None
    labs = None
    headers = {'content-type': 'application/json'}
    if request.method == 'POST':
        headers['Authorization'] = 'Bearer '+sesion.token
        url = '/reserva/'
        if not sesion.activa:
                return HttpResponseRedirect('/login')
        if request.POST['boton'] == 'C':
            res = True
        else:
            res = False  
        o = [{'cantidad':int(request.POST['cantidad']),'producto':int(pk)}]
        obj = {'usuario':user.rut,'reservas':o}
        r = requests.post(urlBase + url,headers=headers,data=json.dumps(obj))
        if r.status_code == 200 or r.status_code == 201:
            j = r.json()
            n = None
            if res:
                costo = int(request.POST['cantidad']) * int(request.POST['precio'])
                return HttpResponseRedirect('/webpay.tbk.token=A324dF_3L6hSDs3.53sNJdKS4&https=2=A=1A2www.webpay.transbakn.com=A2pago=A2.G6HJ8FG3gjfFjh4g854J7G=NOT_NULL&92s3=X2a1WA_33TH&PAGO_INNECESARIAMENTE_NECESARIO=DAfdsaFD8f.2Byeja&W2s=26d5.fX2wWw&XV1D3O5=HD&KCio1d59Sa=A_8dF&MeN5ajEs-5UBl1mIn4l35.DONDE=I-nE3D-U&G=H7D.L&5L=GD666/'+ str(costo) +'/')
                #return HttpResponseRedirect('/resultado-compra/')
            else:
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
    return render(request,'compra/producto.html',context)

def webpay(request,costo):
    if not sesion.activa:
        return HttpResponse('<h1 style="font-size:3em;">Forbiden</h1>'
        +'<p>La transaccion no existe o no tienes permiso para acceder a ella.</p><a class="link-def"href="/">volver a la página principal</a>')
    context = {'monto':costo}
    return render(request,'webpay/webpay-index.html',context)

def Res_compra(request):
    context = {'res':True,'user':user,'sesion':sesion.activa}
    return render(request,'compra/res_compra.html',context)

def Res_reserva(request):
    context = {'res':False,'user':user,'sesion':sesion.activa}
    return render(request,'compra/res_compra.html',context)
