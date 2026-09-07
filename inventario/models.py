from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Movimiento(models.Model):
    TIPO_CHOICES = [
        ('ENTRADA', 'Entrada (Reposición)'),
        ('SALIDA', 'Salida (Consumo / Venta)'),
        ('ALTA', 'Alta Inicial'),
        ('AJUSTE', 'Ajuste de Stock'),
    ]
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cantidad = models.IntegerField()
    motivo = models.CharField(max_length=200, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        prod_nombre = self.producto.nombre if self.producto else "Producto eliminado"
        return f"{self.tipo} - {prod_nombre} ({self.cantidad})"