from django.conf.urls import url
from .views.base import Inicio,Login,Logout,Soporte,Recupera,Faq
from .views.usuario import Perfil,Notificaciones,VerNotificacion
from .views.compra import Busqueda,Compra,Res_compra,Res_reserva,webpay
urlpatterns = [
    url(r'^$', Inicio, name="inicio"),
    url(r'^login/$', Login),
    url(r'^logout/$', Logout),
    url(r'^perfil/$', Perfil),
    url(r'^notificaciones/$', Notificaciones),
    url(r'^notificaciones/(?P<pk>[0-9]+)/$', VerNotificacion),
    url(r'^resultados/$', Busqueda),
    url(r'^comprar/(?P<pk>[0-9]+)/$', Compra),
    url(r'^webpay.tbk.token=A324dF_3L6hSDs3.53sNJdKS4&https=2=A=1A2www.webpay.transbakn.com=A2pago=A2.G6HJ8FG3gjfFjh4g854J7G=NOT_NULL&92s3=X2a1WA_33TH&PAGO_INNECESARIAMENTE_NECESARIO=DAfdsaFD8f.2Byeja&W2s=26d5.fX2wWw&XV1D3O5=HD&KCio1d59Sa=A_8dF&MeN5ajEs-5UBl1mIn4l35.DONDE=I-nE3D-U&G=H7D.L&5L=GD666/([0-9]+)/$', webpay),
    url(r'^resultado-compra/$', Res_compra),
    url(r'^resultado-reserva/$', Res_reserva),
    url(r'^soporte/$', Soporte),
    url(r'^recuperar-contrasena/$', Recupera),
    url(r'^faq/$', Faq),
    
]