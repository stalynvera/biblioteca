from django.db import models

class libros(models.model):
    codigo = models.CharField(primary_key=True, max_length=10, unique=10)
    titulo = models.CharField(max_length=100)
    libro = models.CharField(max_length=100)
    autor = models.CharField(max_length=50)
    genero = models.CharField(max_length=50)
    fecha_publicacion = models.DateTimeField()

    def __str__(self):
        return self.libro
    
class usuario(models.Model):
    cedula = models.CharField(primary_key=True, max_length=10, unique= True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    celular = models.CharField(max_length=10)
     
    def __str__(self):
        return self.nombre + " " + self.apellido
    
class prestamo (models.Model):
    codigof = models.ForeignKey(libros, on_delete= models.CASCADE)
    cedulaf = models.ForeignKey(usuario, on_delete= models.CASCADE)
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion = models.DateTimeField(null= True, blank=True)
    def __str__(self):
        return str(self.codigof.titulo) + " - " + str(self.cedulaf.nombre)

