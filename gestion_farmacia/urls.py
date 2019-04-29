from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Inicio, name="inicio"),
    url(r'^login/$', views.Login),
    url(r'^logout/$', views.Logout),
    url(r'^perfil/$', views.Perfil),
    url(r'^notificaciones/$', views.Notificaciones),
    url(r'^notificaciones/(?P<pk>[0-9]+)/$', views.VerNotificacion),
    url(r'^resultados/$', views.Busqueda),
    url(r'^comprar/(?P<pk>[0-9]+)/$', views.Compra),
    #url(r'^reservar/(?P<pk>[0-9]+)/$', views.Reserva),
    url(r'^resultado-compra/$', views.Res_compra),
    url(r'^resultado-reserva/$', views.Res_reserva),
    url(r'^soporte/$', views.Soporte),
    url(r'^recuperar-contrasena/$', views.Recupera),
    url(r'^faq/$', views.Faq),
    
]