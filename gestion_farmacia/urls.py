from django.conf.urls import url
from .views import Inicio,Login,Logout,Perfil,Notificaciones,VerNotificacion,Busqueda,Compra,Res_compra,Res_reserva,Soporte,Recupera,Faq
urlpatterns = [
    url(r'^$', Inicio, name="inicio"),
    url(r'^login/$', Login),
    url(r'^logout/$', Logout),
    url(r'^perfil/$', Perfil),
    url(r'^notificaciones/$', Notificaciones),
    url(r'^notificaciones/(?P<pk>[0-9]+)/$', VerNotificacion),
    url(r'^resultados/$', Busqueda),
    url(r'^comprar/(?P<pk>[0-9]+)/$', Compra),
    #url(r'^reservar/(?P<pk>[0-9]+)/$', Reserva),
    url(r'^resultado-compra/$', Res_compra),
    url(r'^resultado-reserva/$', Res_reserva),
    url(r'^soporte/$', Soporte),
    url(r'^recuperar-contrasena/$', Recupera),
    url(r'^faq/$', Faq),
    
]