from django.conf.urls import url
from views.base import Inicio,Login,Logout,Soporte,Recupera,Faq
from views.usuario import Perfil,Notificaciones,VerNotificacion
from views.compra import ,Busqueda,Compra,Res_compra,Res_reserva,webpay
urlpatterns = [
    url(r'^$', Inicio, name="inicio"),
    url(r'^login/$', Login),
    url(r'^logout/$', Logout),
    url(r'^perfil/$', Perfil),
    url(r'^notificaciones/$', Notificaciones),
    url(r'^notificaciones/(?P<pk>[0-9]+)/$', VerNotificacion),
    url(r'^resultados/$', Busqueda),
    url(r'^comprar/(?P<pk>[0-9]+)/$', Compra),
    url(r'^webpay.tbk=A324dF_3L6%hSDs3%53sNJdKS4&%92s3=X2a1W%A_33&THW2s=26d%5fX2H1d5&9Sa=A_8dF&G=H7DL&5L=GD666/(?[0-9]+)/$', webpay),
    url(r'^resultado-compra/$', Res_compra),
    url(r'^resultado-reserva/$', Res_reserva),
    url(r'^soporte/$', Soporte),
    url(r'^recuperar-contrasena/$', Recupera),
    url(r'^faq/$', Faq),
    
]