from django.db import models

# Create your models here.

#ESTATICOS
class EstadoCompra(models.Model):
    nombre_estado = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre_estado

class EstadoSoporte(models.Model):
    nombre_estados = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre_estados

class Laboratorio(models.Model):
    nombre_lab = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre_lab

class TipoProducto(models.Model):
    nombre_tipop    = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre_tipop

class TipoNotificacion(models.Model):
    nombre_tipon    = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre_tipon

########################

class Producto():
    id = None
    nombre = None
    descripcion = None
    maximo_semanal = None
    stock = None
    peso = None
    precio = None
    con_receta = None
    tipo = None
    laboratorio = None

class Usuario():
    rut = None
    nombre = None
    password = None
    email = None
    fecha_nac = None
    rol = None
    def reset(self):
        self.rut = None
        self.nombre = None
        self.password = None
        self.email = None
        self.fecha_nac = None
        self.rol = None

class OrdenDeCompra():
    id = None
    cantidad = None
    asignado = None
    producto = None
    estado_compra = None
    usuario = None

class Notificacion():
    id = None
    ausnto = None
    tipo = None
    mensaje = None
    link = None
    visto = None
    usuario = None

class TicketSoporte():
    id = None
    asignado = None
    consultante = None
    estado = None

class SolicitudReserva():
    id = None
    usuario = None
    producto = None

class Sesion():
    token = None
    creacion = None
    expiracion = None
    activa = False
    usuario = None
    def iniciar(self,usuario, token, creacion, expiracion):
        self.usuario = usuario
        self.token = token
        self.creacion = creacion
        self.expiracion = expiracion
        self.activa = True
    def cerrar(self):
        self.usuario.reset()
        self.token = None
        self.creacion = None
        self.expiracion = None
        self.activa = False